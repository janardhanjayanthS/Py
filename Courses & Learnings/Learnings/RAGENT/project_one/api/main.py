import socketio
import uvicorn
from fastapi import FastAPI
from ragent.voice_gateway import CreateVoiceGateway

app = FastAPI()
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")


# Same callback as Flask!
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    response = f"You said: {transcript}"
    await TTS(response)
    return {"contextId": session_id}


# Create gateway - just pass socketio!
gateway = CreateVoiceGateway.create(
    framework_adapter=...,
    on_transcript=...,
    tools=...,
    function_map=...,
    config_overrides=...,
    callback_timeout=...,
    # socketio_instance=sio,  # Auto-detected as async ✅
    # on_transcript=on_transcript,
    # config_overrides={"voice": "alloy"},
)

# Mount and run
app.mount("/", socketio.ASGIApp(sio))
uvicorn.run(app, host="0.0.0.0", port=5000)
