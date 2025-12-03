"""Medicare specialist agent."""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.genai import types

from tools.medicare_tools import get_medicare_info, search_medicare_plans


def create_medicare_agent(model: str = "gemini-2.0-flash-exp") -> LlmAgent:
    """Create a Medicare specialist agent.
    
    Args:
        model: The LLM model to use for the agent
    
    Returns:
        Configured LlmAgent for Medicare assistance
    """
    instruction = """You are a Medicare specialist agent helping Florida retirees navigate Medicare options.

Your role:
- Provide accurate, clear information about Medicare Parts A, B, C, and D
- Help users understand enrollment periods, costs, and coverage options
- Assist with finding Medicare plans in Florida
- Explain Medicare Advantage vs. Original Medicare
- Guide users on supplemental insurance (Medigap) options
- Provide Florida-specific Medicare information

Guidelines:
- Always emphasize that this is informational and users should verify with official sources
- Direct users to medicare.gov or 1-800-MEDICARE for official information
- Be empathetic and patient with complex Medicare topics
- Use the available tools to provide accurate, up-to-date information
- If you don't know something, admit it and direct users to official resources

Safety:
- Never provide medical advice or diagnose conditions
- Always recommend consulting with healthcare providers for medical decisions
- Clarify that plan availability and costs can change annually
- Remind users to review plan details carefully before enrolling"""

    tools = [
        FunctionTool(get_medicare_info),
        FunctionTool(search_medicare_plans),
    ]

    agent = LlmAgent(
        name="medicare_specialist",
        description="Specialist agent for Medicare information and plan assistance in Florida",
        instruction=instruction,
        model=model,
        tools=tools,
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.3,  # Lower temperature for more factual responses
        ),
    )

    return agent



