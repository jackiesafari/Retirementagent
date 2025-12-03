"""FastAPI server exposing the RetirementResourcesApp over HTTP.

Run with:

    uvicorn api_server_fixed:app --reload --port 8000

Then point the Expo frontend to http://localhost:8000/chat
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import RetirementResourcesApp


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# Create a single, long-lived instance of the retirement assistant
retirement_app = RetirementResourcesApp()


app = FastAPI(title="Retirement Resources Assistant API")

# Allow local development from the Expo web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Send a message to the retirement assistant and return the reply.

    The frontend sends a single user message; we keep the conversation
    context on the backend via the RetirementResourcesApp session.
    """

    reply = await retirement_app.chat_async(request.message)
    return ChatResponse(reply=reply)


