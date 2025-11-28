from fastapi import HTTPException
from pydantic import BaseModel
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
    existing_product = db.query(Product).filter_by(id=product.id).first()  # type: ignore
    if existing_product is not None:
        message = f"product with id {product.id} already exists"  # type: ignore
        log_error(message=message)
        raise HTTPException(status_code=400, detail={"message": message})


def handle_missing_product(product_id: str):
    """
    ensures if db returned a valid product,
    if not then logs & retruns error

    Args:
        product_id: fetched product id

    Returns:
        dict: fastapi response
    """
    message = f"product with id {product_id} not found"
    log_error(message=message)
    return {
        "status": "error",
        "message": {
            "response": message,
        },
    }


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

    db_product = Product(**product.model_dump())  # type: ignore
    add_commit_refresh_db(object=db_product, db=db)

    return {"status": "success", "message": {"inserted product": db_product}}


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
    if product is None:
        return handle_missing_product(product_id=str(product_id))

    return {"status": "success", "message": {"product": product}}


def put_product(product_id: str, product_update: BaseModel, db: Session) -> dict:
    """
    update product details

    Args:
        product_id: id of the product to update
        product: detail's of product to update
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        return handle_missing_product(product_id=product_id)

    update_data = product_update.model_dump(exclude_unset=True)  # type: ignore
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return {"status": "success", "message": {"updated product": db_product}}


def delete_product(product_id: str, db: Session) -> dict:
    """
    delete a product from db

    Args:
        product_id: id of the product to update
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        return handle_missing_product(product_id=product_id)

    db.delete(db_product)
    db.commit()
    return {"status": "success", "message": {"deleted product": db_product}}
