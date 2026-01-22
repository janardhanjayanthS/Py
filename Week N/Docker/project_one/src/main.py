from os import getenv

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

load_dotenv(find_dotenv())

app = FastAPI()


@app.get("/")
async def hw() -> dict[str, str]:
    print(f"ENV VAR: {getenv('sample')}")
    return {"response": "jello world"}


if __name__ == "__main__":
    uvicorn.run(app, host=getenv("host", "0.0.0.0"), port=int(getenv("port", 5003)))
