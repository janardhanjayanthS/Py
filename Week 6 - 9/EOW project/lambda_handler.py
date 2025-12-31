import uvicorn
from fastapi import FastAPI
from mangum import Mangum

from src.api.routes import ai, chat, data, user
from src.core.config import lifespan
from src.core.constants import logger

app = FastAPI(lifespan=lifespan)
app.include_router(ai.ai)
app.include_router(chat.chat)
app.include_router(data.data)
app.include_router(user.user)


@app.get("/")
async def hw():
    return {"jello": "world111  x`x`"}


def handler(event, context):
    """
    Main Lambda handler that routes requests to appropriate handlers.
    Handles both HTTP API Gateway and WebSocket API Gateway events.
    """
    logger.info(f"Processing event with context: {context}")
    logger.info(f"Event keys: {list(event.keys())}")

    # For HTTP API Gateway events (including /chat), use Mangum
    logger.info("Detected HTTP API Gateway event - routing to FastAPI via Mangum")
    mangum_handler = Mangum(app, lifespan="off")
    return mangum_handler(event, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)
