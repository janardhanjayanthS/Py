from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.db_utility import add_commit_refresh_db
from src.core.log import log_error
from src.models.models import Product
from src.schema.product import ProductCreate


def check_if_product_exists(product: ProductCreate | None, db: Session):
    """
    Checks if product already exists in db,
    if so raises HTTP error

    Args:
        product: pydnatic product model with its details
        db: database instance in session
    """
    existing_product = db.query(Product).filter_by(id=product.id).first()
    if existing_product is not None:
        message = f"product with id {product.id} already exists"
        log_error(message=message)
        raise HTTPException(status_code=400, detail=message)


def post_product(product: ProductCreate | None, db: Session) -> dict:
    """
    Inserts product into db

    Args:
        product: Pydnatic product model
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    check_if_product_exists(product=product, db=db)

    if product and product.type == "regular":
        product.reset_regular_product_attributes()

    db_product = Product(**product.model_dump())
    add_commit_refresh_db(object=db_product, db=db)

    return {"status": "success", "message": {"inserted_product": db_product}}


def get_all_products(db: Session) -> dict:
    """
    To fetch all products from database

    Args:
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    products = db.query(Product).all()
    return {"status": "success", "message": {"products": products}}


def get_specific_product(product_id: str, db: Session) -> dict:
    """
    Fetches a specific product from db

    Args:
        product_id: id to the product to select
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    product = db.query(Product).filter_by(id=product_id).first()
    ensure_product_found(product_id=str(product.id), product=product) # type: ignore

    return {"status": "success", "message": {"product": product}}


def ensure_product_found(product_id: str, product: Product):
    """
    ensures if db returned a valid product,
    if not then logs & retruns error

    Args:
        product_id: fetched product id
        product: fetched product sqlalchemy object

    Returns:
        dict: fastapi response
    """
    if product is None:
        message = f"product with id {product_id} not found"
        log_error(message=message)
        return {
            "status": "error",
            "message": {
                "response": message,
            },
        }
