# ragent Voice Gateway Integration Guide

Complete guide to integrate `ragent.voice_gateway` with FastAPI, Flask, and Django for real-time voice processing with OpenAI's Realtime API.

## 📋 Overview

`ragent.voice_gateway` provides:
- **WebSocket connection** to OpenAI Realtime API
- **Audio streaming** (microphone input → TTS output)
- **Session management** 
- **Framework-agnostic** adapter pattern

## 🏗️ Architecture

```
Browser (WebSocket) → Your Framework → ragent Adapter → ragent Gateway → OpenAI Realtime API
```

## 🔧 Core Components

### Required Imports
```python
from ragent.voice_gateway import RealtimeConfig, CreateVoiceGateway
from ragent.voice_gateway.config.config import ConfigService
from ragent.voice_gateway.interfaces import WebApp, WebFrameworkAdapter, WebSocketHandler
from ragent.voice_gateway.infrastructure import UniversalSocketIOHandler
```

**Component Roles:**
- `RealtimeConfig`: Default voice/model settings → serializable dict
- `CreateVoiceGateway`: Factory that builds the complete gateway
- `ConfigService`: Merges env vars + overrides, validates config
- `WebFrameworkAdapter`: Bridge between your framework and ragent
- `UniversalSocketIOHandler`: Normalizes Socket.IO behavior across frameworks

## 🚀 Framework Implementations

### 1. FastAPI Implementation

FastAPI uses **ASGI** + **python-socketio** (async). Perfect for modern async applications.

#### FastAPI Adapter (`fastapi_adapter.py`)
<details>
<summary>Click to expand FastAPI adapter code</summary>

```python
import asyncio
from typing import Any, Optional

import socketio
import uvicorn
from fastapi import FastAPI

from ragent.voice_gateway.interfaces import WebApp, WebFrameworkAdapter, WebSocketHandler
from ragent.voice_gateway.infrastructure import UniversalSocketIOHandler


class FastAPIWebApp(WebApp):
    """Wraps FastAPI app to match ragent's WebApp interface"""
    def __init__(self, app: FastAPI):
        self._app = app

    def route(self, rule: str, **options):
        """FastAPI route decorator"""
        return self._app.get(rule, **options)

    def get_asgi_app(self):
        """Return ASGI app for uvicorn"""
        return self._app


class FastAPISocketHandler(WebSocketHandler):
    """Handles async Socket.IO operations for FastAPI"""
    def __init__(self, sio: socketio.AsyncServer):
        self._sio = sio
        self._handler = UniversalSocketIOHandler(sio)
        self._main_loop: Optional[asyncio.AbstractEventLoop] = None

    def set_main_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """Set main event loop for cross-thread emit"""
        self._main_loop = loop

    def on(self, event: str, handler=None):
        return self._handler.on(event, handler)

    def emit(self, event: str, data: Any = None, **kwargs) -> None:
        """Async emit with cross-thread support"""
        if "to" in kwargs:
            kwargs["room"] = kwargs.pop("to")
        
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._sio.emit(event, data, **kwargs))
        except RuntimeError:
            if self._main_loop and self._main_loop.is_running():
                future = asyncio.run_coroutine_threadsafe(
                    self._sio.emit(event, data, **kwargs),
                    self._main_loop
                )
                try:
                    future.result(timeout=5.0)
                except Exception:
                    pass


class FastAPIAdapter(WebFrameworkAdapter):
    """Complete FastAPI + Socket.IO adapter for ragent"""
    def __init__(self, cors_allowed_origins="*", async_mode="asgi"):
        self._app = FastAPI()
        self._sio = socketio.AsyncServer(
            cors_allowed_origins=cors_allowed_origins,
            async_mode=async_mode
        )
        self._sio.attach(self._app)
        
        self._web_app = FastAPIWebApp(self._app)
        self._websocket_handler = FastAPISocketHandler(self._sio)

    def get_app_instance(self) -> WebApp:
        return self._web_app

    def get_websocket_handler(self) -> WebSocketHandler:
        return self._websocket_handler

    def get_asgi_app(self):
        """Get the complete ASGI app for uvicorn"""
        return self._app
```
</details>

#### FastAPI Main Application (`main.py`)
<details>
<summary>Click to expand FastAPI main application</summary>

```python
import os
import asyncio
from ragent.voice_gateway import CreateVoiceGateway
from .adapters.fastapi_adapter import FastAPIAdapter

# 1. Create transcript callback
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    """Handle transcribed speech"""
    try:
        print(f"[{session_id}] User said: {transcript}")
        response = f"You said: {transcript}"
        TTS(response)  # Send to TTS
        
        return {
            "contextId": session_id,
            "message_log": chat_payload.get("metadata", {}).get("message_log", []),
        }
    except Exception as e:
        print(f"[{session_id}] ERROR: {e}")
        TTS(f"Sorry, error: {str(e)}")
        return {"contextId": session_id}

# 2. Create adapter
adapter = FastAPIAdapter(
    cors_allowed_origins="*",
    async_mode="asgi"
)

# 3. Create gateway
gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,
    config_overrides={
        "voice": "alloy",
        "model": "gpt-4o-realtime-preview"
    }
)

# 4. Get ASGI app and run
app = adapter.get_asgi_app()

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Set OPENAI_API_KEY environment variable")
        exit(1)
    
    asyncio.run(uvicorn.run(app, host="0.0.0.0", port=5000))
```
</details>

---

### 2. Flask Implementation

Flask uses **WSGI** + **Flask-SocketIO** (sync). Great for traditional synchronous apps.

#### Flask Adapter (`flask_adapter.py`)
<details>
<summary>Click to expand Flask adapter code</summary>

```python
from flask import Flask
from flask_socketio import SocketIO

from ragent.voice_gateway.interfaces import WebApp, WebFrameworkAdapter, WebSocketHandler
from ragent.voice_gateway.infrastructure import UniversalSocketIOHandler


class FlaskWebApp(WebApp):
    """Wraps Flask app to match ragent's WebApp interface"""
    def __init__(self, app: Flask):
        self._app = app

    def add_route(self, rule: str, endpoint: str, view_func, **options):
        self._app.add_url_rule(rule, endpoint=endpoint, view_func=view_func, **options)

    def route(self, rule: str, **options):
        return self._app.route(rule, **options)

    def get_wsgi_app(self):
        return self._app


class FlaskSocketHandler(WebSocketHandler):
    """Handles sync Socket.IO operations for Flask"""
    def __init__(self, socketio_instance: SocketIO):
        self._handler = UniversalSocketIOHandler(socketio_instance)

    def on(self, event: str, handler=None):
        return self._handler.on(event, handler)

    def emit(self, event: str, data=None, **kwargs):
        return self._handler.emit(event, data, **kwargs)


class FlaskAdapter(WebFrameworkAdapter):
    """Complete Flask + Socket.IO adapter for ragent"""
    def __init__(self, secret_key="dev", cors_allowed_origins="*", async_mode="threading"):
        self._app = Flask(__name__)
        self._app.secret_key = secret_key
        
        self._socketio = SocketIO(
            self._app,
            cors_allowed_origins=cors_allowed_origins,
            async_mode=async_mode
        )
        
        self._web_app = FlaskWebApp(self._app)
        self._websocket_handler = FlaskSocketHandler(self._socketio)

    def get_app_instance(self) -> WebApp:
        return self._web_app

    def get_websocket_handler(self) -> WebSocketHandler:
        return self._websocket_handler

    def get_socketio(self):
        """Get SocketIO instance for running the server"""
        return self._socketio
```
</details>

#### Flask Main Application (`main.py`)
<details>
<summary>Click to expand Flask main application</summary>

```python
import os
from ragent.voice_gateway import CreateVoiceGateway
from .adapters.flask_adapter import FlaskAdapter

# 1. Create transcript callback
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    """Handle transcribed speech"""
    try:
        print(f"[{session_id}] User said: {transcript}")
        response = f"You said: {transcript}"
        TTS(response)
        
        return {
            "contextId": session_id,
            "message_log": chat_payload.get("metadata", {}).get("message_log", []),
        }
    except Exception as e:
        print(f"[{session_id}] ERROR: {e}")
        TTS(f"Sorry, error: {str(e)}")
        return {"contextId": session_id}

# 2. Create adapter
adapter = FlaskAdapter(
    secret_key="your-secret-key",
    cors_allowed_origins="*",
    async_mode="threading"
)

# 3. Create gateway
gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,
    config_overrides={
        "voice": "alloy",
        "model": "gpt-4o-realtime-preview"
    }
)

# 4. Get Flask app and run
app = adapter.get_app_instance().get_wsgi_app()
socketio = adapter.get_socketio()

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Set OPENAI_API_KEY environment variable")
        exit(1)
    
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
```
</details>

---

### 3. Django Implementation

Django uses **WSGI** + **django-socketio** (sync). Best for Django projects with admin/ORM.

#### Django Adapter (`django_adapter.py`)
<details>
<summary>Click to expand Django adapter code</summary>

```python
import socket
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django_socketio import SocketIOConsumer

from ragent.voice_gateway.interfaces import WebApp, WebFrameworkAdapter, WebSocketHandler
from ragent.voice_gateway.infrastructure import UniversalSocketIOHandler


class DjangoWebApp(WebApp):
    """Wraps Django WSGI app to match ragent's WebApp interface"""
    def __init__(self, wsgi_app):
        self._app = wsgi_app

    def add_route(self, rule: str, endpoint: str, view_func, **options):
        """Django uses URL patterns, not dynamic routing"""
        raise NotImplementedError("Use Django's urls.py for routing")

    def route(self, rule: str, **options):
        raise NotImplementedError("Use Django's urls.py for routing")

    def get_wsgi_app(self):
        return self._app


class DjangoSocketHandler(WebSocketHandler):
    """Handles Socket.IO operations for Django"""
    def __init__(self):
        self._handler = UniversalSocketIOHandler(None)

    def on(self, event: str, handler=None):
        """Register Socket.IO event handler"""
        SocketIOConsumer.on(event, handler)

    def emit(self, event: str, data=None, **kwargs):
        """Emit to Socket.IO clients"""
        return self._handler.emit(event, data, **kwargs)


class DjangoAdapter(WebFrameworkAdapter):
    """Django adapter for ragent"""
    def __init__(self):
        # Django must be configured before using get_wsgi_application
        self._wsgi_app = get_wsgi_application()
        self._web_app = DjangoWebApp(self._wsgi_app)
        self._websocket_handler = DjangoSocketHandler()

    def get_app_instance(self) -> WebApp:
        return self._web_app

    def get_websocket_handler(self) -> WebSocketHandler:
        return self._websocket_handler
```
</details>

#### Django Configuration (`settings.py`)
<details>
<summary>Click to expand Django settings.py configuration</summary>

```python
# Add to your Django settings.py
INSTALLED_APPS = [
    # ... your existing apps
    'django_socketio',
    'voice_gateway',  # Your voice gateway app
]

# Socket.IO settings
SOCKETIO_HOST = '0.0.0.0'
SOCKETIO_PORT = 5000
SOCKETIO_ALLOWED_ORIGINS = ['*']
```
</details>

#### Django Main Application (`voice_gateway/views.py`)
<details>
<summary>Click to expand Django views.py example</summary>

```python
import os
from django.http import JsonResponse
from ragent.voice_gateway import CreateVoiceGateway
from .adapters.django_adapter import DjangoAdapter

# 1. Create transcript callback
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    """Handle transcribed speech"""
    try:
        print(f"[{session_id}] User said: {transcript}")
        response = f"You said: {transcript}"
        TTS(response)
        
        return {
            "contextId": session_id,
            "message_log": chat_payload.get("metadata", {}).get("message_log", []),
        }
    except Exception as e:
        print(f"[{session_id}] ERROR: {e}")
        TTS(f"Sorry, error: {str(e)}")
        return {"contextId": session_id}

# 2. Create adapter (singleton)
adapter = DjangoAdapter()

# 3. Create gateway
gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,
    config_overrides={
        "voice": "alloy",
        "model": "gpt-4o-realtime-preview"
    }
)

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({"status": "ok", "gateway": "active"})
```
</details>

#### Django URL Configuration (`voice_gateway/urls.py`)
<details>
<summary>Click to expand Django urls.py example</summary>

```python
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
]
```
</details>

#### Django Management Command (`manage.py runsocketio`)
<details>
<summary>Click to expand Django management command example</summary>

```python
# voice_gateway/management/commands/runsocketio.py
from django.core.management.base import BaseCommand
from django_socketio import runserver

class Command(BaseCommand):
    help = 'Run Django with Socket.IO support'

    def handle(self, *args, **options):
        if not os.getenv("OPENAI_API_KEY"):
            self.stdout.write("ERROR: Set OPENAI_API_KEY environment variable")
            return
        
        self.stdout.write("Starting Django voice gateway with Socket.IO...")
        runserver(host='0.0.0.0', port=5000)
```
</details>

---

## 📝 Common Callback Pattern

All frameworks use the same callback signature:

<details>
<summary>Click to expand common on_transcript callback template</summary>

```python
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    """
    Called by ragent when speech is transcribed
    
    Args:
        session_id: Unique voice session identifier
        transcript: Transcribed text from user speech
        chat_payload: Dict with conversation context/message_log
        event_emitter: For sending custom events to frontend
        TTS: Function to speak text back to user
    
    Returns:
        Dict with context updates (contextId, message_log, etc.)
    """
    # 1. Process the transcript (LLM, database, etc.)
    response = await your_business_logic(transcript)
    
    # 2. Send response to TTS (text-to-speech)
    TTS(response)
    
    # 3. Optionally emit custom events
    event_emitter.emit("custom_event", {"data": response})
    
    # 4. Return context updates
    return {
        "contextId": session_id,
        "message_log": [{"role": "assistant", "content": response}]
    }
```
</details>

---

## 🎯 Quick Setup Checklist

### For All Frameworks:
1. ✅ Set `OPENAI_API_KEY` environment variable
2. ✅ Install required packages:
   - FastAPI: `pip install fastapi uvicorn python-socketio`
   - Flask: `pip install flask flask-socketio`
   - Django: `pip install django django-socketio`
3. ✅ Create adapter implementation
4. ✅ Implement `on_transcript` callback
5. ✅ Start server and connect frontend

### Environment Variables:
<details>
<summary>Click to expand environment variables</summary>

```bash
export OPENAI_API_KEY="sk-..."
export VOICE_MODEL="gpt-4o-realtime-preview"  # Optional
export VOICE_NAME="alloy"  # Optional
```
</details>

---

## 🔄 Migration Between Frameworks

Switching frameworks is easy - just swap the adapter:

<details>
<summary>Click to expand migration snippet</summary>

```python
# FastAPI → Flask
from .adapters.flask_adapter import FlaskAdapter
adapter = FlaskAdapter(cors_allowed_origins="*")

# Flask → Django  
from .adapters.django_adapter import DjangoAdapter
adapter = DjangoAdapter()

# Keep the same callback!
gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,  # Reuse!
    config_overrides=config_overrides
)
```
</details>

---

## 📁 Project Structure

<details>
<summary>Click to expand suggested project structure</summary>

```
your_project/
├── adapters/
│   ├── __init__.py
│   ├── fastapi_adapter.py
│   ├── flask_adapter.py
│   └── django_adapter.py
├── main.py (or Django app)
├── static/
│   └── test_client.html
└── requirements.txt
```
</details>

---

## 🎨 Frontend Integration

All adapters expose the same Socket.IO interface. Use this HTML client:

<details>
<summary>Click to expand minimal frontend client</summary>

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
</head>
<body>
    <button onclick="startSession()">Start Voice Session</button>
    <button onclick="stopRecording()">Stop Recording</button>
    
    <script>
        const socket = io('http://localhost:5000');
        
        socket.on('connect', () => console.log('Connected'));
        socket.on('session_started', (data) => console.log('Session:', data));
        socket.on('ai_response', (data) => console.log('AI:', data));
        
        function startSession() {
            socket.emit('start_session', {config: {}});
        }
        
        function stopRecording() {
            socket.emit('commit_audio');
        }
    </script>
</body>
</html>
```
</details>

---

## 🚀 Production Considerations

### Security:
- Use HTTPS in production
- Restrict CORS origins: `cors_allowed_origins=["https://yourdomain.com"]`
- Validate session IDs
- Rate limit voice sessions

### Performance:
- Use Redis for session storage in production
- Configure proper WebSocket timeouts
- Monitor OpenAI API costs
- Add health checks

### Deployment:
<details>
<summary>Click to expand deployment commands</summary>

```bash
# FastAPI (Dockerfile)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

# Flask (Dockerfile)  
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "main:app"]

# Django (Dockerfile)
CMD ["python", "manage.py", "runsocketio"]
```
</details>

---

## 🔧 Troubleshooting

### Common Issues:
1. **"No voices loaded" (Linux)**: Install `sudo apt install espeak-ng speech-dispatcher`
2. **WebSocket connection failed**: Check CORS settings and port availability
3. **Async task warnings**: Ensure proper event loop handling in adapters
4. **OpenAI API errors**: Verify `OPENAI_API_KEY` is valid and has permissions

### Debug Mode:
<details>
<summary>Click to expand debug logging snippet</summary>

```python
# Add to your main.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```
</details>

---

## 📚 Advanced Topics

### Session Management
For production apps, track active sessions:

<details>
<summary>Click to expand session management example</summary>

```python
class SessionManager:
    def __init__(self):
        self.active_sessions = set()
    
    def start_session(self, session_id):
        self.active_sessions.add(session_id)
    
    def end_session(self, session_id):
        self.active_sessions.discard(session_id)
    
    def is_active(self, session_id):
        return session_id in self.active_sessions

# Use in callback
session_manager = SessionManager()

async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    if not session_manager.is_active(session_id):
        session_manager.start_session(session_id)
    
    # ... your logic here
    return {"contextId": session_id}
```
</details>

### Error Handling Patterns
<details>
<summary>Click to expand safe emit + error handling pattern</summary>

```python
def _safe_emit(event_emitter, event_name, payload):
    """Safe event emission with error handling"""
    if not event_emitter or not hasattr(event_emitter, "emit"):
        return False
    try:
        event_emitter.emit(event_name, payload)
        return True
    except Exception as e:
        logger.error(f"Failed to emit {event_name}: {e}")
        return False

async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    try:
        # Your business logic
        response = await process_transcript(transcript)
        
        # Safe TTS call
        TTS(response)
        
        # Safe event emission
        _safe_emit(event_emitter, "ai_response", {
            "response": response,
            "session_id": session_id
        })
        
        return {"contextId": session_id}
    except Exception as e:
        logger.error(f"Error in on_transcript: {e}")
        TTS("Sorry, I encountered an error")
        return {"contextId": session_id}
```
</details>

### Configuration Management
<details>
<summary>Click to expand configuration management snippet</summary>

```python
from ragent.voice_gateway import RealtimeConfig
from ragent.voice_gateway.config.config import ConfigService

# Load and validate configuration
config_overrides = RealtimeConfig.to_dict()
config_service = ConfigService(config_overrides=config_overrides)
server_config = config_service.get_server_config()

# Common config overrides for all frameworks
gateway_config = {
    "voice": "alloy",
    "model": "gpt-4o-realtime-preview",
    "temperature": 0.7,
    "max_tokens": 1000,
}
```
</details>

### Custom Events
Send custom events to frontend:

<details>
<summary>Click to expand custom events example</summary>

```python
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    # Process transcript
    response = await your_logic(transcript)
    
    # Send custom events
    event_emitter.emit("thinking_start", {"session_id": session_id})
    
    # Simulate processing delay
    await asyncio.sleep(1)
    
    event_emitter.emit("thinking_end", {"session_id": session_id})
    event_emitter.emit("ai_response", {"response": response})
    
    TTS(response)
    return {"contextId": session_id}
```
</details>

---

## 🎯 Complete Example: FastAPI + SQLite

Here's a full production-ready example:

#### `requirements.txt`
<details>
<summary>Click to expand requirements.txt</summary>

```
fastapi==0.104.1
uvicorn==0.24.0
python-socketio==5.10.0
ragent
sqlite3
```
</details>

#### `main.py`
<details>
<summary>Click to expand complete FastAPI + SQLite main.py example</summary>

```python
import os
import asyncio
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI
from ragent.voice_gateway import CreateVoiceGateway
from adapters.fastapi_adapter import FastAPIAdapter

# Database setup
def init_db():
    conn = sqlite3.connect('voice_sessions.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Session management
class SessionManager:
    def __init__(self):
        self.active_sessions = set()
        init_db()
    
    def start_session(self, session_id):
        self.active_sessions.add(session_id)
        conn = sqlite3.connect('voice_sessions.db')
        conn.execute('INSERT OR REPLACE INTO sessions (session_id) VALUES (?)', (session_id,))
        conn.commit()
        conn.close()
    
    def end_session(self, session_id):
        self.active_sessions.discard(session_id)
        conn = sqlite3.connect('voice_sessions.db')
        conn.execute('UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?', (session_id,))
        conn.commit()
        conn.close()

session_manager = SessionManager()

# Business logic
async def process_with_llm(transcript: str) -> str:
    """Replace with your LLM call"""
    # Example: Call OpenAI, Anthropic, or your own model
    return f"You said: {transcript}. This is a simulated response."

# Callback
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    try:
        # Start session if new
        if session_id not in session_manager.active_sessions:
            session_manager.start_session(session_id)
        
        # Process transcript
        response = await process_with_llm(transcript)
        
        # Send to TTS
        TTS(response)
        
        # Emit events
        event_emitter.emit("ai_response", {
            "response": response,
            "session_id": session_id
        })
        
        return {
            "contextId": session_id,
            "message_log": [{"role": "user", "content": transcript}, {"role": "assistant", "content": response}]
        }
    
    except Exception as e:
        print(f"Error in callback: {e}")
        TTS("Sorry, I encountered an error")
        return {"contextId": session_id}

# FastAPI app with lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Voice gateway starting...")
    yield
    print("Voice gateway shutting down...")

app = FastAPI(lifespan=lifespan)

# Create adapter and gateway
adapter = FastAPIAdapter(
    cors_allowed_origins=["http://localhost:3000"],  # Your frontend URL
    async_mode="asgi"
)

gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,
    config_overrides={
        "voice": "alloy",
        "model": "gpt-4o-realtime-preview",
        "temperature": 0.7
    }
)

# Mount Socket.IO
app.mount("/socket.io", adapter.get_asgi_app())

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "active_sessions": len(session_manager.active_sessions)}

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Set OPENAI_API_KEY environment variable")
        exit(1)
    
    print("Starting voice gateway on http://localhost:5000")
    asyncio.run(uvicorn.run(app, host="0.0.0.0", port=5000))
```
</details>

---

## 🚀 Next Steps

1. **Choose your framework** based on your project needs
2. **Copy the adapter** for your chosen framework  
3. **Implement your business logic** in the `on_transcript` callback
4. **Deploy and test** with the provided frontend client

The adapter pattern ensures you can switch between FastAPI, Flask, or Django without changing your core voice processing logic.

---

## 📞 Support

- **ragent documentation**: Check the package docs for advanced features
- **OpenAI Realtime API**: https://platform.openai.com/docs/guides/realtime
- **Socket.IO docs**: https://socket.io/docs/

Happy coding! 🎙️