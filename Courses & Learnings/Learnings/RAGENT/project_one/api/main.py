"""
Complete FastAPI + ragent Voice Gateway Implementation

This example shows how to integrate ragent's voice gateway with FastAPI
for real-time voice processing using OpenAI's Realtime API.
"""

import os

import uvicorn
from adapters import FastAPIAdapter
from ragent.voice_gateway import CreateVoiceGateway

# =============================================================================
# STEP 1: Create your transcript callback
# =============================================================================
# This function is called by ragent whenever OpenAI transcribes user speech.
# You receive:
#   - session_id: Unique identifier for this voice session
#   - transcript: The text of what the user said
#   - chat_payload: Dict with conversation context (message_log, contextId, etc.)
#   - event_emitter: For sending custom events to the frontend
#   - TTS: Function to speak text back to user (calls OpenAI TTS)


async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    """
    Handle transcribed speech from the user.

    This is where YOUR business logic goes:
    - Call an LLM to generate a response
    - Query a database
    - Run an AI agent
    - etc.
    """
    print(f"[{session_id}] User said: {transcript}")

    # Example: Echo back what the user said
    # In a real app, you'd call your AI/LLM here
    response = f"You said: {transcript}"

    # Use TTS to speak the response (sends to OpenAI Realtime API)
    await TTS(response)

    # Optionally emit custom events to frontend
    event_emitter.emit(
        "custom_event", {"message": "Processing complete", "session_id": session_id}
    )

    # Return context updates (optional)
    # - contextId: Session identifier for your backend
    # - message_log: Conversation history to maintain context
    return {
        "contextId": session_id,
        "message_log": chat_payload.get("metadata", {}).get("message_log", []),
    }


# =============================================================================
# STEP 2: Create the FastAPI adapter
# =============================================================================
# The adapter bridges FastAPI + Socket.IO with ragent's framework-agnostic gateway

adapter = FastAPIAdapter(
    cors_allowed_origins="*",  # Allow all origins (configure for production)
    async_mode="asgi",  # Required for FastAPI
)


# =============================================================================
# STEP 3: Create the Voice Gateway
# =============================================================================
# This sets up:
#   - WebSocket connection to OpenAI Realtime API
#   - Socket.IO events for browser communication
#   - Audio streaming pipeline
#   - Session management

gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,  # Your callback from Step 1
    config_overrides={  # Optional: customize voice settings
        "voice": "alloy",  # OpenAI voice: alloy, echo, fable, onyx, nova, shimmer
        "model": "gpt-4o-realtime-preview",
    },
)


# =============================================================================
# STEP 4: Get the ASGI app for uvicorn
# =============================================================================
# The adapter combines FastAPI + Socket.IO into one ASGI application

app = adapter.get_asgi_app()


# =============================================================================
# Run the server
# =============================================================================
if __name__ == "__main__":
    # Make sure OPENAI_API_KEY is set!
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")

    print("Starting Voice Gateway on http://0.0.0.0:5000")
    print("Socket.IO endpoint: ws://localhost:5000/socket.io/")
    uvicorn.run(app, host="0.0.0.0", port=5000)
