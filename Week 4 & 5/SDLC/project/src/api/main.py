import uuid

import uvicorn
from fastapi import FastAPI, Request

from src.core.app_utility import lifespan
from src.core.exception_handler import add_exception_handlers_to_app
from src.core.log import correlation_id, get_logger

from .routes import category, product, user

logger = get_logger(__name__)

app = FastAPI(lifespan=lifespan)

app.include_router(product.product)
app.include_router(user.user)
app.include_router(category.category)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    """Middleware for logging requests with correlation IDs.

    Args:
        request: Incoming HTTP request.
        call_next: Next middleware in the chain.

    Returns:
        HTTP response with correlation ID tracking.
    """
    request_id = str(uuid.uuid4())
    token = correlation_id.set(request_id)

    logger.info("Request started", path=request.url.path, method=request.method)

    try:
        response = await call_next(request)
        return response
    finally:
        correlation_id.reset(token)


add_exception_handlers_to_app(app=app)


@app.get("/")
def home():
    """Home endpoint returning a simple greeting.

    Returns:
        Dictionary with a greeting message.
    """
    logger.info("HELLO WORLD")
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
