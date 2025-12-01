from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import event

from src.core.app_config import lifespan
from src.core.db_config import initialize_table
from src.models.models import Product

from .routes import product
from .routes import user

load_dotenv()

TESTING = getenv("TESTING")

if TESTING != "1":
    event.listen(Product.__table__, "after_create", initialize_table)

app = FastAPI(lifespan=lifespan)

app.include_router(product.product)
app.include_router(user.user)


@app.get("/")
def home():
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
