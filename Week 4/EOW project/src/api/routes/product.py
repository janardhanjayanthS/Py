from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db_config import get_db
from src.models.models import Product

product = APIRouter()


@product.get("/products")
async def products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
