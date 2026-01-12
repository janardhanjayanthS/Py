"""
Complete FastAPI + ragent Voice Gateway Implementation

This example shows how to integrate ragent's voice gateway with FastAPI
for real-time voice processing using OpenAI's Realtime API.
"""

import asyncio
import inspect
import os
from src.core.main import mainloop

# =============================================================================
# CRITICAL: Patch ragent's async handling BEFORE importing ragent
# =============================================================================
# This fixes the "Task was destroyed but it is pending" warnings by ensuring
# async emit calls from background threads use the main event loop properly.

_main_loop = None  # Will be set when server starts


def _patched_safe_emit(emit_func, *args, **kwargs):
    """
    Patched version of ragent's safe_emit that properly handles
    cross-thread async emit by using the main event loop.
    """
    global _main_loop
    result = emit_func(*args, **kwargs)

    if inspect.iscoroutine(result):
        try:
            # Try to get running loop in current thread
            loop = asyncio.get_running_loop()
            task = loop.create_task(result)
            if not hasattr(loop, "_ragent_tasks"):
                loop._ragent_tasks = set()
            loop._ragent_tasks.add(task)
            task.add_done_callback(loop._ragent_tasks.discard)
        except RuntimeError:
            # No loop in this thread - use main loop via threadsafe call
            if _main_loop and _main_loop.is_running():
                future = asyncio.run_coroutine_threadsafe(result, _main_loop)
                try:
                    future.result(timeout=10.0)  # Wait for emit to complete
                except Exception:
                    pass
            else:
                # Last resort fallback
                try:
                    asyncio.run(result)
                except Exception:
                    pass
    return None


# Apply patch BEFORE importing ragent
import ragent.voice_gateway.utils.async_helpers as async_helpers

async_helpers.safe_emit = _patched_safe_emit

# NOW import ragent (uses patched safe_emit)
import uvicorn
from ragent.voice_gateway import CreateVoiceGateway

from .adapters import FastAPIAdapter


# =============================================================================
# STEP 1: Create your transcript callback
# =============================================================================
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    """
    Handle transcribed speech from the user.
    """
    try:
        print(f"[{session_id}] User said: {transcript}")

        # Example: Echo back what the user said
        response = f"You said: {transcript}"
        print("-" * 50)
        print(f"RESPONSE: {response}")
        print("-" * 50)

        # Use TTS to speak the response
        ai_response = mainloop(human_message=transcript)
        TTS(ai_response)

        return {
            "contextId": session_id,
            "message_log": chat_payload.get("metadata", {}).get("message_log", []),
        }
    except Exception as e:
        print(f"[{session_id}] ERROR: {e}")
        TTS(f"Sorry, error: {str(e)}")
        return {"contextId": session_id}


# =============================================================================
# STEP 2: Create the FastAPI adapter
# =============================================================================
adapter = FastAPIAdapter(
    cors_allowed_origins="*",
    async_mode="asgi",
)


# =============================================================================
# STEP 3: Create the Voice Gateway
# =============================================================================
gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,
    config_overrides={
        "voice": "alloy",
        "model": "gpt-4o-realtime-preview",
    },
)


# =============================================================================
# STEP 4: Get the ASGI app
# =============================================================================
app = adapter.get_asgi_app()


# =============================================================================
# Run the server
# =============================================================================
if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set!")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")

    print("Starting Voice Gateway on http://0.0.0.0:5000")
    print("Socket.IO endpoint: ws://localhost:5000/socket.io/")

    async def run_server():
        global _main_loop
        _main_loop = asyncio.get_running_loop()

        # Set main loop on socket handler for cross-thread emit
        websocket_handler = adapter.get_websocket_handler()
        if hasattr(websocket_handler, "set_main_loop"):
            websocket_handler.set_main_loop(_main_loop)

        config = uvicorn.Config(app, host="0.0.0.0", port=5000)
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(run_server())
