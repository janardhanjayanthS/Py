# Step-by-Step ragent Integration Guide

Use this checklist to integrate `ragent.voice_gateway` into any backend while reusing the same wrapper + event flow.

## 1. Import what ragent needs
```python
from ragent.voice_gateway import RealtimeConfig, CreateVoiceGateway
from ragent.voice_gateway.config.config import ConfigService
```
- `RealtimeConfig` exposes default realtime parameters and converts them into a serializable dict via `RealtimeConfig.to_dict()`.
- `CreateVoiceGateway` spins up the HTTP/WebSocket server and binds your callback into ragent’s streaming loop.
- `ConfigService` merges env vars with the overrides and ensures every required key (API tokens, host, CORS) is present.

### Additional ragent imports used elsewhere
Adapters pull extra interfaces/utilities from ragent so the gateway can stay framework-agnostic:

```python
from ragent.voice_gateway.interfaces import WebApp, WebFrameworkAdapter, WebSocketHandler
from ragent.voice_gateway.infrastructure import UniversalSocketIOHandler
```
- `WebApp`, `WebFrameworkAdapter`, `WebSocketHandler`: contracts implemented by the Flask/FastAPI adapters so `CreateVoiceGateway` can drive any framework the same way.@backend/apis/realtime_patient/adapters/flask_adapter.py#1-145 @backend/apis/realtime_patient/adapters/fastapi_adapter.py#1-134
- `UniversalSocketIOHandler`: helper supplied by ragent to normalize Flask-SocketIO and python-socketio behavior (sync vs async) before forwarding events back to the gateway.

#### Adapter reference snippet
```python
from ragent.voice_gateway.interfaces import (
    WebApp,
    WebFrameworkAdapter,
    WebSocketHandler,
)
from ragent.voice_gateway.infrastructure import UniversalSocketIOHandler


class YourWebApp(WebApp):
    def __init__(self, framework_app):
        self._app = framework_app

    def add_route(self, rule: str, endpoint: str, view_func, **options):
        self._app.add_url_rule(rule, endpoint=endpoint, view_func=view_func, **options)

    def route(self, rule: str, **options):
        return self._app.route(rule, **options)

    def get_wsgi_app(self):
        return self._app


class YourSocketHandler(WebSocketHandler):
    def __init__(self, socketio_instance):
        self._handler = UniversalSocketIOHandler(socketio_instance)

    def on(self, event: str, handler=None):
        return self._handler.on(event, handler)

    def emit(self, event: str, data=None, **kwargs):
        self._handler.emit(event, data, **kwargs)


class YourAdapter(WebFrameworkAdapter):
    def __init__(self, **config):
        framework_app = build_framework_app(**config)
        socketio_instance = build_socket_handler(framework_app, **config)
        self._web_app = YourWebApp(framework_app)
        self._websocket_handler = YourSocketHandler(socketio_instance)

    def get_app_instance(self) -> WebApp:
        return self._web_app

    def get_websocket_handler(self) -> WebSocketHandler:
        return self._websocket_handler
```
This mirrors both the Flask and FastAPI adapters: wrap your framework primitives inside ragent’s interfaces, then pass the adapter into `CreateVoiceGateway.create()`.

## 2. Collect configuration overrides
```python
config_overrides = RealtimeConfig.to_dict()
config_service = ConfigService(config_overrides=config_overrides)
server_config = config_service.get_server_config()
```
Purpose: share realtime defaults with ragent while still letting environment variables drive secrets. `server_config` feeds whichever HTTP framework adapter you choose.

## 3. Instantiate your framework adapter
Example for Flask/Socket.IO:
```python
flask_adapter = FlaskAdapter(
    secret_key=server_config["secret_key"],
    cors_allowed_origins=server_config["cors_allowed_origins"],
    async_mode=server_config["async_mode"],
    template_folder=template_dir,
)
```
Any adapter only needs to expose `emit`, `on_event`, and `on_error`. Swap in a FastAPI adapter (or your own) as long as it implements the same surface.

## 4. Build the transcript callback in the wrapper
`create_patient_agent_callback()` returns the function ragent will call whenever it finishes transcribing audio. The callback signature is:
```python
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    ...
```
How it operates inside the wrapper:
1. Keeps `session_id` inside `active_sessions` so disconnects can halt downstream work immediately.
2. Copies `chat_payload`, injects the latest `transcript` into `parts[0]["text"]`, and adds the persona key required by the patient agent stack.
3. Bootstraps the agent dependency container, runs the patient workflow coordinator, and extracts the text response plus updated context metadata.
4. Emits results back to the client through ragent using `_safe_emit` (see next section).

Because the callback already understands ragent’s arguments, you can reuse it in any project by swapping out the agent-specific processing block.

#### Callback reference snippet
```python executes domain logic. example: wrapping of agent logic 
async def create_domain_callback():
    active_sessions: set[str] = set()

    def on_session_start(session_id: str):
        active_sessions.add(session_id)

    def on_session_end(session_id: str):
        active_sessions.discard(session_id)

    async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
        if session_id not in active_sessions:
            on_session_start(session_id)

        payload = chat_payload.copy()
        payload.setdefault("parts", [{}])
        payload["parts"][0]["text"] = transcript

        response_text, context_update = await run_domain_logic(payload)

        _safe_emit(event_emitter, "ai_response", {
            "response": response_text,
            "session_id": session_id,
        })
        _safe_emit(event_emitter, "domain_response", {
            "context_update": context_update,
            "session_id": session_id,
        })

        return context_update

    on_transcript.on_session_start = on_session_start
    on_transcript.on_session_end = on_session_end
    return on_transcript
```
Drop in your own `run_domain_logic` implementation (LLM orchestrator, DB calls, etc.) and reuse `_safe_emit` for every outbound event.

## 5. Use `_safe_emit` for all outbound events
```python
def _safe_emit(event_emitter, event_name, payload):
    if not event_emitter or not hasattr(event_emitter, "emit"):
        return False
    try:
        event_emitter.emit(event_name, payload)
        return True
    except Exception:
        logger.error("Failed to emit event", event_name=event_name)
        return False
```
- Keeps the wrapper resilient when the WebSocket disappears mid-turn.
- Called for `"ai_response"` and `"patient_agent_response"`, ensuring both human-readable and structured payloads reach the frontend through ragent’s emitter.

## 6. Create the voice gateway
```python
on_transcript = asyncio.run(create_patient_agent_callback())
self._gateway = CreateVoiceGateway.create(
    framework_adapter=flask_adapter,
    on_transcript=on_transcript,
    config_overrides=config_overrides,
)
```
Arguments explained:
- `framework_adapter`: bridges ragent to your HTTP/WebSocket stack.
- `on_transcript`: async function described above; ragent will await it after every transcription result.
- `config_overrides`: dictionary produced from `RealtimeConfig` so the gateway knows which voice/model/turn-detection settings to use without hardcoding them inside the wrapper.

## 7. Hook session-ending events (optional but recommended)
After `CreateVoiceGateway` returns you can grab the framework’s Socket.IO handler (for Flask) or equivalent in other adapters and route events like `disconnect`, `session_end`, or `stop_audio` to `on_transcript.on_session_end(session_id)`. This keeps internal state in sync with what ragent sees and prevents stale sessions from emitting further audio.

## Quick reuse recipe
1. Import the ragent classes listed above.
2. Produce `config_overrides = RealtimeConfig.to_dict()` and hand them to `ConfigService`.
3. Instantiate a framework adapter using the validated server config.
4. Reuse (or adapt) `create_patient_agent_callback()` + `_safe_emit` to handle your domain logic.
5. Call `CreateVoiceGateway.create(adapter, on_transcript, config_overrides)`.
6. Optionally attach session-ending events to the callback helpers for graceful cleanup.

## Drop-in template for new projects
Use the following snippet as a starting point anywhere you want to embed ragent. Swap `YourAdapter` and `your_callback_factory` with project-specific implementations.

```python
import asyncio
from ragent.voice_gateway import RealtimeConfig, CreateVoiceGateway
from ragent.voice_gateway.config.config import ConfigService

from your_project.adapters import YourAdapter  # implements WebFrameworkAdapter
from your_project.services import your_callback_factory


def bootstrap_voice_gateway():
    # 1) Gather realtime defaults + validate env
    config_overrides = RealtimeConfig.to_dict()
    config_service = ConfigService(config_overrides=config_overrides)
    server_config = config_service.get_server_config()

    # 2) Instantiate your framework adapter with validated server settings
    adapter = YourAdapter(**server_config)

    # 3) Build the ragent-compatible callback once
    on_transcript = asyncio.run(your_callback_factory())

    # 4) Create the gateway Exactly once per process
    gateway = CreateVoiceGateway.create(
        framework_adapter=adapter,
        on_transcript=on_transcript,
        config_overrides=config_overrides,
    )

    return gateway
```

This mirrors the realtime patient setup: gather overrides, validate config, instantiate an adapter, produce an `on_transcript` callable, then hand all three objects to `CreateVoiceGateway.create()`. Reusing the structure ensures any project can plug into ragent with minimal code changes.