from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db_config import get_db
from src.models.models import Product

product = APIRouter()


@product.get("/products")
async def products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@product.get("/products/{product_id}")
async def product_with_id(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()

    if product is None:
        return {"response": f"product with id {product_id} not found"}

    return product