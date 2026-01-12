import uuid

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.app_utility import lifespan
from src.core.excptions import WeakPasswordException
from src.core.log import correlation_id, get_logger

from .routes import category, product, user

logger = get_logger(__name__)

app = FastAPI(lifespan=lifespan)

app.include_router(product.product)
app.include_router(user.user)
app.include_router(category.category)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    token = correlation_id.set(request_id)

    logger.info("Request started", path=request.url.path, method=request.method)

    try:
        response = await call_next(request)
        return response
    finally:
        correlation_id.reset(token)


@app.exception_handler(WeakPasswordException)
async def handle_weak_password(request: Request, error: WeakPasswordException):
    return JSONResponse(
        status_code=400, content={"status": "Error", "message": error.message}
    )


@app.get("/")
def home():
    logger.info("HELLO WORLD")
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
