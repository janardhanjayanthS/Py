from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db_config import get_db
from src.models.models import Product
from src.schema.product import ProductCreate, ProductResponse

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


@product.post("/add_product", response_model=ProductResponse)
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    print(product)

    existing_product = db.query(Product).filter_by(id=product.id).first()

    if existing_product is not None:
        raise HTTPException(status_code=400, detail="Product id already exists")

    if product and product.type == "regular":
        product.is_vegetarian = product.days_to_expire = product.warranty_in_years = (
            None
        )

    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product
