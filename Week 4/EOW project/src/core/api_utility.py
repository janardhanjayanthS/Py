from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.log import log_error
from src.models.models import Product
from src.schema.product import ProductCreate


def check_if_product_exists(product: ProductCreate, db: Session):
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


def add_commit_refresh_db(object: BaseModel, db: Session):
    """
    add, commit and refresh db after adding a row

    Args:
        object: to insert to db (pydantic model instance)
        db: database instance in session
    """
    db.add(object)
    db.commit()
    db.refresh(object)
