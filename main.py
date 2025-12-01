"""Main entry point and application wrapper for the Florida Retirement Resources
Multi-Agent System.

This module wires together:
- Coordinator agent (routes between Medicare / Medicaid / Local Resources)
- Session service
- Runner

It exposes:
- `RetirementResourcesApp` for programmatic use (see `example_usage.py`)
- A CLI entry point when run as `python main.py`
"""

import os
import asyncio
from typing import Optional

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents import create_coordinator_agent

# ============================================================================
# CONFIGURATION
# ============================================================================

# Configure API Key (falls back to placeholder if not set)
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"  # Use API directly, not Vertex AI

# Application/session defaults
# NOTE: ADK derives an "implied" app name from the root agent package path.
# For our coordinator agent (defined under the `agents` package), this must be
# "agents" to avoid app-name mismatch warnings.
APP_NAME = "agents"
# Use the same model you originally had working before the refactor so that
# quota/plan behavior matches your previous setup.
DEFAULT_MODEL = "gemini-2.5-flash-lite"
DEFAULT_USER_ID = "user_001"
DEFAULT_SESSION_ID = "retirement_session_001"


def _warn_if_missing_api_key() -> None:
    """Print a helpful warning if the API key is not configured."""
    if os.environ.get("GOOGLE_API_KEY") == "YOUR_GOOGLE_API_KEY":
        print("⚠️ WARNING: Please set your GOOGLE_API_KEY!")
        print("Get your key from: https://aistudio.google.com/app/apikey")
        print("Then run: export GOOGLE_API_KEY='your-actual-key'\n")


def _ensure_api_key() -> None:
    """Fail fast if the API key is missing."""
    if os.environ.get("GOOGLE_API_KEY") == "YOUR_GOOGLE_API_KEY":
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Get a key from "
            "https://aistudio.google.com/app/apikey and then run:\n"
            "  export GOOGLE_API_KEY='your-actual-key'\n"
        )


# ============================================================================
# APPLICATION WRAPPER
# ============================================================================


class RetirementResourcesApp:
    """High-level application wrapper around the multi-agent system.

    This is the main entry point for programmatic use. It:
    - Creates a coordinator agent (which talks to specialist agents)
    - Manages an in-memory session
    - Provides simple `chat` / `chat_async` methods
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        app_name: str = APP_NAME,
        user_id: str = DEFAULT_USER_ID,
        session_id: Optional[str] = None,
    ) -> None:
        _ensure_api_key()

        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id or DEFAULT_SESSION_ID

        # Core ADK components
        self.session_service = InMemorySessionService()
        self.agent = create_coordinator_agent(model=model)
        self.runner = Runner(
            agent=self.agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )
        self._session_created = False

    async def _create_session(self) -> None:
        """Create an ADK session once per app instance."""
        if self._session_created:
            return
        await self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id,
        )
        self._session_created = True

    async def chat_async(self, query: str) -> str:
        """Send a query to the coordinator agent and return the final response."""
        # Lazily ensure the session exists in whatever event loop we're in
        await self._create_session()
        content = types.Content(role="user", parts=[types.Part(text=query)])
        final_response_text = "Agent did not produce a final response."

        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=self.session_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response_text = (
                        f"Agent escalated: {event.error_message or 'No specific message.'}"
                    )
                break

        return final_response_text

    def chat(self, query: str) -> str:
        """Synchronous convenience wrapper around `chat_async`."""
        return asyncio.run(self.chat_async(query))


# ============================================================================
# CLI ENTRY POINT
# ============================================================================


async def main() -> None:
    """Main function to run the retirement resources system interactively."""
    _warn_if_missing_api_key()

    # Fail fast if we truly cannot proceed
    try:
        _ensure_api_key()
    except RuntimeError as exc:
        print(f"\n❌ Cannot proceed without a valid GOOGLE_API_KEY\n{exc}")
        return

    print("🏖️ Florida Retirement Resources - Multi-Agent System")
    print("=" * 70)
    print("Initializing system...\n")

    # Initialize application (coordinator + specialist agents)
    app = RetirementResourcesApp(model=DEFAULT_MODEL)
    print(f"✅ Coordinator agent '{app.agent.name}' initialized with tools")
    print(f"✅ Session: {app.app_name}/{app.user_id}/{app.session_id}\n")

    print("=" * 70)
    print("WELCOME TO FLORIDA RETIREMENT RESOURCES")
    print("=" * 70)
    print("I'm here to help you navigate Medicare, Medicaid, and local services.")
    print("Type 'quit' to exit at any time.\n")

    first_message = True

    while True:
        try:
            if first_message:
                user_input = input("What brings you here today? ").strip()
                first_message = False
            else:
                user_input = input("\nYou: ").strip()

            if user_input.lower() in ["quit", "exit", "bye", "q"]:
                print("\n👋 Thank you for using Florida Retirement Resources. Take care!")
                break

            if not user_input:
                continue

            print(f"\n{'=' * 70}")
            print(f"You: {user_input}")
            print(f"{'=' * 70}")

            response = await app.chat_async(user_input)
            print(f"\nAgent:\n{response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Take care.")
            break
        except Exception as exc:  # pragma: no cover - defensive logging
            print(f"\n❌ Error: {exc}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:  # pragma: no cover - top-level guard
        print(f"\n❌ Fatal error: {exc}")