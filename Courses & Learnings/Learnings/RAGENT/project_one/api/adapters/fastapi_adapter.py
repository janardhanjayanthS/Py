"""
FastAPI Adapter for ragent Voice Gateway

This adapter bridges FastAPI + python-socketio with ragent's framework-agnostic
voice gateway. It implements the required interfaces so ragent can work with FastAPI.
"""

import asyncio
from typing import Any, Callable, Optional

import socketio
from fastapi import FastAPI
from ragent.voice_gateway.infrastructure import UniversalSocketIOHandler
from ragent.voice_gateway.interfaces import (
    WebApp,
    WebFrameworkAdapter,
    WebSocketHandler,
)


class FastAPIWebApp(WebApp):
    """
    Wraps a FastAPI application to match ragent's WebApp interface.

    ragent needs a standard way to add routes to ANY web framework.
    This class translates ragent's route requests into FastAPI's format.
    """

    def __init__(self, app: FastAPI):
        self._app = app

    def add_route(
        self, rule: str, endpoint: str, view_func: Callable, **options
    ) -> None:
        """
        Add a URL route to FastAPI.

        Args:
            rule: The URL path (e.g., "/health")
            endpoint: Name for the route
            view_func: The function to handle requests
            **options: Additional options like methods=["GET", "POST"]
        """
        methods = options.get("methods", ["GET"])
        for method in methods:
            self._app.add_api_route(
                rule,
                view_func,
                methods=[method],
                name=endpoint,
            )

    def route(self, rule: str, **options):
        """
        Decorator to add a route (Flask-style).

        ragent uses this decorator pattern: @app.route("/health")

        Args:
            rule: The URL path (e.g., "/health")
            **options: Additional options like methods=["GET", "POST"]
        """
        methods = options.get("methods", ["GET"])

        def decorator(view_func: Callable):
            for method in methods:
                self._app.add_api_route(
                    rule,
                    view_func,
                    methods=[method],
                )
            return view_func

        return decorator

    def run(self, host: str = "0.0.0.0", port: int = 5000, **options) -> None:
        """Run the FastAPI app (typically you'd use uvicorn externally)."""
        import uvicorn

        uvicorn.run(self._app, host=host, port=port, **options)

    def get_wsgi_app(self):
        """Return the FastAPI app (it's ASGI, not WSGI, but ragent uses this generically)."""
        return self._app


class FastAPISocketHandler(WebSocketHandler):
    """
    Wraps python-socketio's AsyncServer for ragent's WebSocketHandler interface.

    Handles the tricky case where ragent calls emit() from background threads
    (OpenAI WebSocket handlers) but Socket.IO AsyncServer needs an event loop.
    """

    def __init__(self, sio: socketio.AsyncServer):
        self._sio = sio
        self._handler = UniversalSocketIOHandler(sio)
        self._current_sid: Optional[str] = None
        self._main_loop: Optional[asyncio.AbstractEventLoop] = None

    def set_main_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """Store reference to main event loop for cross-thread emit."""
        self._main_loop = loop

    def on(self, event: str, handler: Callable) -> None:
        """Register an event handler for Socket.IO events."""
        self._handler.on(event, handler)

    def on_error(self, handler: Callable) -> None:
        """Register an error handler."""
        self._handler.on_error(handler)

    def emit(self, event: str, data: Any = None, **kwargs) -> None:
        """
        Emit an event to connected clients.

        Handles cross-thread emit by using run_coroutine_threadsafe when
        called from a thread different from the main event loop.
        """
        # Convert 'to' to 'room' for python-socketio compatibility
        if "to" in kwargs:
            kwargs["room"] = kwargs.pop("to")

        try:
            # Try to get the running loop in current thread
            loop = asyncio.get_running_loop()
            # We're in an async context, create task
            loop.create_task(self._sio.emit(event, data, **kwargs))
        except RuntimeError:
            # No running loop in this thread - we're in a background thread
            # Use the main loop if available
            if self._main_loop and self._main_loop.is_running():
                future = asyncio.run_coroutine_threadsafe(
                    self._sio.emit(event, data, **kwargs), self._main_loop
                )
                # Wait for completion with timeout to ensure it finishes
                try:
                    future.result(timeout=5.0)
                except Exception:
                    pass  # Best effort emit
            else:
                # Fallback: try to run in new loop (not ideal but prevents crash)
                try:
                    asyncio.run(self._sio.emit(event, data, **kwargs))
                except Exception:
                    pass

    def get_current_client_id(self) -> str:
        """Get the current client's session ID."""
        return self._handler.get_current_client_id()


class FastAPIAdapter(WebFrameworkAdapter):
    """
    Main adapter that creates and configures FastAPI + Socket.IO for ragent.

    This is what you pass to CreateVoiceGateway.create().

    Usage:
        adapter = FastAPIAdapter(
            cors_allowed_origins="*",
            async_mode="asgi"
        )
        gateway = CreateVoiceGateway.create(
            framework_adapter=adapter,
            on_transcript=my_callback,
        )
    """

    def __init__(
        self, cors_allowed_origins: str = "*", async_mode: str = "asgi", **config
    ):
        """
        Initialize the FastAPI adapter.

        Args:
            cors_allowed_origins: CORS setting for Socket.IO ("*" allows all)
            async_mode: Socket.IO async mode ("asgi" for FastAPI)
            **config: Additional configuration options
        """
        self._config = config
        self._cors_allowed_origins = cors_allowed_origins
        self._async_mode = async_mode

        # Create the FastAPI app and Socket.IO server
        self._fastapi_app = self.create_app()
        self._socketio = self.create_websocket_handler(self._fastapi_app)

        # Wrap them in ragent's interfaces
        self._web_app = FastAPIWebApp(self._fastapi_app)
        self._websocket_handler = FastAPISocketHandler(self._socketio)

    def create_app(self, **config) -> FastAPI:
        """Create a new FastAPI application instance."""
        return FastAPI(title="Voice Gateway API")

    def create_websocket_handler(self, app: FastAPI, **kwargs) -> socketio.AsyncServer:
        """Create an AsyncServer for Socket.IO with FastAPI."""
        sio = socketio.AsyncServer(
            cors_allowed_origins=self._cors_allowed_origins,
            async_mode=self._async_mode,
        )
        # Mount Socket.IO ASGI app onto FastAPI
        socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
        # Store reference for later access
        self._asgi_app = socket_app
        return sio

    def get_app_instance(self) -> WebApp:
        """Get the wrapped FastAPI application."""
        return self._web_app

    def get_websocket_handler(self) -> WebSocketHandler:
        """Get the wrapped Socket.IO handler."""
        return self._websocket_handler

    def get_asgi_app(self):
        """Get the combined ASGI app (Socket.IO + FastAPI) for uvicorn."""
        return self._asgi_app

    def get_socketio(self) -> socketio.AsyncServer:
        """Get the raw Socket.IO server for direct access if needed."""
        return self._socketio
