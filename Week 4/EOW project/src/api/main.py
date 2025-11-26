import uvicorn
from fastapi import FastAPI
from sqlalchemy import event

from ..core.app_config import lifespan
from ..core.db_config import initialize_table
from ..models.models import Product

event.listen(Product.__tablename__, "after_create", initialize_table)

app = FastAPI(lifespan=lifespan)


@app.route("/")
def home() -> dict:
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
