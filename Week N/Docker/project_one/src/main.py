import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hw() -> dict[str, str]:
    return {"response": "jello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5003)
