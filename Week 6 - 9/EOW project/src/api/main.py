import uvicorn  # noqa: F401
from fastapi import FastAPI
from mangum import Mangum

from src.api.routes import ai, chat, data, user
from src.core.config import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(ai.ai)
app.include_router(chat.chat)
app.include_router(data.data)
app.include_router(user.user)


@app.get("/")
async def hw():
    return {"jello": "world111  x`x`"}


lambda_handler = Mangum(app, lifespan="off")


# TO RUN LOCALLY
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)
