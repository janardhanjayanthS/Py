import uvicorn
from fastapi import FastAPI
from src.api.routes import ai

app = FastAPI()
app.include_router(ai.ai)


@app.get("/")
async def hw():
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)
