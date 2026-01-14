# ragent Voice Gateway - Complete Beginner's Guide

## What is ragent?

**ragent** is a Python package that provides a **Voice Gateway** - a bridge between your web application and **OpenAI's Realtime API**. It handles all the complex parts of real-time voice communication:

- **Speech-to-Text (STT)**: Converts user's voice to text
- **Text-to-Speech (TTS)**: Converts your AI's response back to voice
- **WebSocket Management**: Maintains persistent connections to OpenAI
- **Session Management**: Tracks multiple concurrent voice conversations
- **Audio Streaming**: Handles real-time audio data flow

---

## The Big Picture: How Voice Chat Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           YOUR WEB APPLICATION                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BROWSER (Frontend)                              │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────────────────────┐ │
│  │ Microphone  │───►│ JavaScript   │───►│ Socket.IO Client                │ │
│  │ (Audio In)  │    │ Audio API    │    │ (sends audio_data events)       │ │
│  └─────────────┘    └──────────────┘    └─────────────────────────────────┘ │
│                                                        │                     │
│  ┌─────────────┐    ┌──────────────┐                  │                     │
│  │ Speaker     │◄───│ Audio Player │◄─────────────────┼─────────────────────┤
│  │ (Audio Out) │    │              │    (audio_delta) │                     │
│  └─────────────┘    └──────────────┘                  │                     │
└───────────────────────────────────────────────────────┼─────────────────────┘
                                                        │
                                    Socket.IO WebSocket │
                                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         YOUR BACKEND (FastAPI + ragent)                      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      ragent Voice Gateway                             │   │
│  │                                                                       │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐  │   │
│  │  │ Socket.IO       │    │ VoiceHandler    │    │ WebSocket Client │  │   │
│  │  │ Event Manager   │───►│ (Orchestrator)  │───►│ to OpenAI        │  │   │
│  │  │                 │    │                 │    │                  │  │   │
│  │  │ - connect       │    │ - start_session │    │ - Send audio     │  │   │
│  │  │ - audio_data    │    │ - handle_audio  │    │ - Receive text   │  │   │
│  │  │ - end_session   │    │ - end_session   │    │ - Receive audio  │  │   │
│  │  └─────────────────┘    └────────┬────────┘    └──────────────────┘  │   │
│  │                                  │                                    │   │
│  │                                  ▼                                    │   │
│  │                    ┌─────────────────────────┐                        │   │
│  │                    │   YOUR CALLBACK         │                        │   │
│  │                    │   on_transcript()       │                        │   │
│  │                    │                         │                        │   │
│  │                    │   - Get transcript      │                        │   │
│  │                    │   - Run your AI logic   │                        │   │
│  │                    │   - Call TTS(response)  │                        │   │
│  │                    └─────────────────────────┘                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          OpenAI Realtime API                                 │
│                                                                              │
│  - Receives audio from user                                                  │
│  - Transcribes speech to text (STT)                                         │
│  - Generates voice response (TTS)                                           │
│  - Streams audio back                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Package Structure Explained

```
ragent/voice_gateway/
├── __init__.py              # Exports: CreateVoiceGateway, RealtimeConfig, etc.
├── gateway.py               # Main factory class (CreateVoiceGateway)
│
├── interfaces/              # Abstract interfaces (contracts)
│   ├── web_framework.py     # WebApp, WebSocketHandler, WebFrameworkAdapter
│   └── interfaces.py        # IAudioService, ISessionService, IWebSocketService
│
├── infrastructure/          # Implementations
│   ├── universal_socketio.py    # UniversalSocketIOHandler (sync/async)
│   ├── websocket_client.py      # RealtimeWebSocketClient (to OpenAI)
│   └── services.py              # AudioService, SessionService, WebSocketService
│
├── core/                    # Core logic
│   ├── voice_handler.py     # VoiceHandler - main orchestrator
│   └── app_managers.py      # Routes, events, ApplicationOrchestrator
│
├── domain/                  # Business logic
│   └── domain_services.py   # ConversationOrchestrator, TTSService
│
├── handlers/                # Message processors
│   └── message_handlers.py  # Handle OpenAI message types
│
├── config/                  # Configuration
│   ├── config.py            # ConfigService, RealtimeConfig
│   └── constants.py         # Default values, OpenAI settings
│
└── utils/                   # Helpers
    ├── async_helpers.py     # safe_emit, async utilities
    └── exceptions.py        # Custom exceptions
```

---

## Core Components Explained

### 1. `CreateVoiceGateway` (gateway.py)

This is the **main entry point**. It's a factory class that sets up everything:

```python
gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,      # Your FastAPI/Flask adapter
    on_transcript=callback,         # Your business logic
    config_overrides={...},         # Optional settings
)
```

**What it does internally:**
1. Validates your configuration
2. Gets the app and websocket from your adapter
3. Creates a `VoiceHandler` (the brain)
4. Creates an `ApplicationOrchestrator` (wires everything together)
5. Registers HTTP routes (`/health`, `/session-config`)
6. Registers Socket.IO events (`connect`, `audio_data`, etc.)

### 2. `WebFrameworkAdapter` (interfaces/web_framework.py)

This is an **abstract class** (interface) that defines what ragent needs from any web framework:

```python
class WebFrameworkAdapter(ABC):
    def create_app(self, **config) -> T:
        """Create a web app (FastAPI, Flask, etc.)"""
        
    def create_websocket_handler(self, app, **kwargs) -> WebSocketHandler:
        """Create Socket.IO handler"""
        
    def get_app_instance(self) -> WebApp:
        """Return wrapped app"""
        
    def get_websocket_handler(self) -> WebSocketHandler:
        """Return wrapped socket handler"""
```

**Why it exists:** ragent is framework-agnostic. By defining this interface, ragent can work with Flask, FastAPI, Django, or any framework - you just implement the adapter.

### 3. `UniversalSocketIOHandler` (infrastructure/universal_socketio.py)

This clever class **auto-detects** whether you're using:
- **Flask-SocketIO** (synchronous)
- **python-socketio** (asynchronous)

And handles both the same way:

```python
handler = UniversalSocketIOHandler(socketio_instance)
handler.emit('event', {'data': 'value'})  # Works for both!
handler.on('audio_data', my_handler)      # Works for both!
```

**How it detects:**
- Checks for `async_mode` attribute
- Checks if `emit` is a coroutine function
- Checks class name for "Async"

### 4. `VoiceHandler` (core/voice_handler.py)

The **brain** of the voice gateway. It orchestrates:

```python
class VoiceHandler:
    def start_session(self, client_id, emit_callback, chat_payload):
        """Start a new voice session"""
        # 1. Create session in SessionService
        # 2. Connect WebSocket to OpenAI
        # 3. Send session configuration to OpenAI
        
    def handle_audio_data(self, client_id, audio_data):
        """Process incoming audio from browser"""
        # 1. Validate audio format
        # 2. Accumulate in buffer
        # 3. Forward to OpenAI WebSocket
        
    def end_session(self, client_id):
        """Clean up session"""
        # 1. Disconnect WebSocket
        # 2. Clear session data
```

### 5. `RealtimeWebSocketClient` (infrastructure/websocket_client.py)

Manages the **persistent WebSocket connection to OpenAI**:

```python
client = RealtimeWebSocketClient(
    url="wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview",
    headers={"Authorization": "Bearer sk-...", ...},
    on_message_callback=handle_openai_message,
    on_error_callback=handle_error,
    on_close_callback=handle_close,
)
client.connect()
client.send({"type": "input_audio_buffer.append", "audio": "base64..."})
```

### 6. Message Handlers (handlers/message_handlers.py)

Process different message types from OpenAI:

| Message Type | Handler | What It Does |
|-------------|---------|--------------|
| `conversation.item.input_audio_transcription.completed` | `TranscriptionCompletedHandler` | Calls your `on_transcript` callback |
| `response.audio.delta` | `AudioDeltaHandler` | Forwards audio chunks to browser |
| `response.done` | `ResponseDoneHandler` | Signals response complete |
| `error` | `ErrorHandler` | Emits error to browser |
| `response.function_call_arguments.done` | `FunctionCallHandler` | Executes function calls |

---

## Socket.IO Events Flow

### Events FROM Browser → Backend:

| Event | Data | Description |
|-------|------|-------------|
| `connect` | - | Browser connected |
| `start_session` | `{chat_payload: {...}}` | Start voice session |
| `audio_data` | `{audio: "base64..."}` | Audio chunk from microphone |
| `commit_audio` | - | Signal end of speech |
| `end_session` | - | End voice session |
| `disconnect` | - | Browser disconnected |

### Events FROM Backend → Browser:

| Event | Data | Description |
|-------|------|-------------|
| `session_created` | `{session_id, status}` | Session initialized |
| `session_started` | `{session_id, message}` | OpenAI connected, ready |
| `audio_delta` | `{audio: "base64...", index}` | AI voice audio chunk |
| `ai_response` | `{transcript, response}` | Text of conversation |
| `response_complete` | `{response_id}` | AI finished speaking |
| `error` | `{message, code}` | Error occurred |
| `session_ended` | `{status}` | Session cleaned up |

---

## The `on_transcript` Callback

This is **YOUR code** - where your business logic lives:

```python
async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    """
    Called when OpenAI transcribes user speech.
    
    Parameters:
    -----------
    session_id : str
        Unique identifier for this voice session
        
    transcript : str
        What the user said (transcribed text)
        
    chat_payload : dict
        Conversation context:
        {
            "contextId": "session-123",
            "kind": "message",
            "metadata": {
                "message_log": [...]  # Previous messages
            },
            "parts": [{"kind": "text", "text": "..."}],
            "role": "user"
        }
        
    event_emitter : EventEmitterWrapper
        For sending custom events to browser:
        event_emitter.emit("my_event", {"key": "value"})
        
    TTS : Callable
        Function to speak text back to user:
        await TTS("Hello, how can I help?")
        
    Returns:
    --------
    dict (optional)
        Context updates to persist:
        {
            "contextId": "session-123",
            "message_log": [...]
        }
    """
    # YOUR LOGIC HERE
    # Example: Call your AI
    response = await my_ai_agent.process(transcript)
    
    # Speak the response
    await TTS(response)
    
    return {"contextId": session_id}
```

---

## Two Modes of Operation

### Mode 1: Agent Wrapper Mode (on_transcript)

Use this when you have your own AI/LLM logic:

```python
async def my_callback(session_id, transcript, chat_payload, event_emitter, TTS):
    response = await my_custom_ai(transcript)
    await TTS(response)
    return {"contextId": session_id}

gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=my_callback,  # Your callback
)
```

### Mode 2: Function Calling Mode (tools)

Use this when you want OpenAI to call functions directly:

```python
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }
]

def get_weather(location: str) -> dict:
    return {"temperature": 72, "condition": "sunny"}

gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    tools=tools,
    function_map={"get_weather": get_weather},
)
```

**Note:** You cannot use both modes simultaneously.

---

## Configuration Options

```python
config_overrides = {
    # Voice Settings
    "voice": "alloy",           # alloy, echo, fable, onyx, nova, shimmer
    "model": "gpt-4o-realtime-preview",
    
    # Turn Detection (when to process speech)
    "turn_detection_mode": "normal",  # "normal", "disabled", "aggressive"
    "turn_detection_params": {
        "threshold": 0.5,
        "prefix_padding_ms": 300,
        "silence_duration_ms": 500,
    },
    
    # Transcription
    "transcription_model": "whisper-1",
    
    # Output
    "max_output_tokens": "inf",  # or integer like 4096
    
    # Instructions (system prompt for OpenAI)
    "instructions": "You are a helpful assistant...",
}
```

---

## Complete Example: AI Assistant

```python
"""Full example with LangChain integration"""
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from ragent.voice_gateway import CreateVoiceGateway
from adapters import FastAPIAdapter

# Initialize LangChain
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Store conversation history per session
conversations = {}

async def on_transcript(session_id, transcript, chat_payload, event_emitter, TTS):
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    history = conversations[session_id]
    
    # Add user message
    history.append(HumanMessage(content=transcript))
    
    # Call LLM
    response = await llm.ainvoke(history)
    
    # Add AI response to history
    history.append(AIMessage(content=response.content))
    
    # Speak the response
    await TTS(response.content)
    
    # Emit to frontend for display
    event_emitter.emit("ai_response", {
        "user": transcript,
        "assistant": response.content,
    })
    
    return {
        "contextId": session_id,
        "message_log": [{"role": m.type, "content": m.content} for m in history]
    }

# Setup
adapter = FastAPIAdapter()
gateway = CreateVoiceGateway.create(
    framework_adapter=adapter,
    on_transcript=on_transcript,
    config_overrides={
        "voice": "nova",
        "instructions": "You are a friendly AI assistant. Keep responses concise.",
    },
)

app = adapter.get_asgi_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

---

## Frontend Integration (JavaScript)

```javascript
// Connect to your backend
const socket = io('http://localhost:5000');

// Handle events
socket.on('connect', () => {
    console.log('Connected to voice gateway');
});

socket.on('session_started', (data) => {
    console.log('Session ready:', data.session_id);
    startRecording(); // Begin capturing audio
});

socket.on('audio_delta', (data) => {
    // Play AI voice response
    playAudioChunk(data.audio);
});

socket.on('ai_response', (data) => {
    // Display text
    console.log('User:', data.transcript);
    console.log('AI:', data.response);
});

socket.on('error', (data) => {
    console.error('Error:', data.message);
});

// Start a voice session
function startSession() {
    socket.emit('start_session', {
        chat_payload: {
            contextId: 'session-' + Date.now(),
            metadata: { message_log: [] }
        }
    });
}

// Send audio data (from MediaRecorder)
function sendAudio(base64Audio) {
    socket.emit('audio_data', { audio: base64Audio });
}

// End session
function endSession() {
    socket.emit('end_session');
}
```

---

## Summary

| Component | Purpose |
|-----------|---------|
| `CreateVoiceGateway` | Factory to create the gateway |
| `WebFrameworkAdapter` | Interface for web frameworks |
| `FastAPIAdapter` | Your FastAPI implementation of the adapter |
| `VoiceHandler` | Orchestrates voice sessions |
| `UniversalSocketIOHandler` | Handles sync/async Socket.IO |
| `RealtimeWebSocketClient` | Connects to OpenAI |
| `on_transcript` | YOUR business logic callback |
| `TTS()` | Function to speak responses |
| `event_emitter` | Send custom events to browser |

**The flow:**
1. Browser connects via Socket.IO
2. User starts session → ragent connects to OpenAI
3. User speaks → audio sent to backend → forwarded to OpenAI
4. OpenAI transcribes → ragent calls your `on_transcript`
5. You process and call `TTS(response)`
6. OpenAI generates voice → ragent streams audio to browser
7. User hears AI response

That's it! ragent handles all the WebSocket complexity, audio streaming, and session management. You just write your business logic in `on_transcript`.
