from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import event

from src.core.config import lifespan
from src.core.database import initialize_table
from src.core.excptions import WeakPasswordException
from src.models.models import Product

from .routes import product, user

load_dotenv()

TESTING = getenv("TESTING")

if TESTING != "1":
    event.listen(Product.__table__, "after_create", initialize_table)

app = FastAPI(lifespan=lifespan)

app.include_router(product.product)
app.include_router(user.user)


@app.exception_handler(WeakPasswordException)
async def handle_weak_password(request: Request, error: WeakPasswordException):
    return JSONResponse(
        status_code=400, content={"status": "Error", "message": error.message}
    )


@app.get("/")
def home():
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
