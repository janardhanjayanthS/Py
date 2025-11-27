from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.api_utility import add_commit_refresh_db, check_if_product_exists
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
    check_if_product_exists(product=product, db=db)

    if product and product.type == "regular":
        product.reset_regular_product_attributes()

    db_product = Product(**product.model_dump())
    add_commit_refresh_db(object=db_product, db=db)

    return db_product
