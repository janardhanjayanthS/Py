import uvicorn
from fastapi import FastAPI

from src.api.routes import ai, chat, data
from src.core.config import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(ai.ai)
app.include_router(chat.chat)
app.include_router(data.data)


@app.get("/")
async def hw():
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)
