from fastapi import FastAPI
from .routes import users

app = FastAPI()

app.include_router(users.user)


@app.get("/")
async def home():
    return {"message": "Jello world"}
