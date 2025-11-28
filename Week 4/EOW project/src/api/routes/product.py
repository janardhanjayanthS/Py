from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from src.core.api_utility import (
    delete_product,
    get_all_products,
    get_specific_product,
    post_product,
    put_product,
)
from src.core.db_config import get_db
from src.schema.product import ProductCreate, ProductUpdate

product = APIRouter()


@product.get("/products")
@product.post("/products")
async def products(
    request: Request,
    product_id: Optional[str] = "",
    product: Optional[ProductCreate] = None,
    db: Session = Depends(get_db),
):
    if request.method == "POST":
        return post_product(product=product, db=db)

    elif request.method == "GET":
        if product_id and product_id is not None:
            return get_specific_product(product_id=product_id, db=db)
        return get_all_products(db=db)

    return {
        "status": "error",
        "message": {"response": f"Unrecognized HTTP method {request.method}"},
    }


@product.put("/product")
async def update_product(
    product_id: str, product_update: ProductUpdate, db: Session = Depends(get_db)
):
    """
    To update product information

    Args:
        product_id: id of the product to update
        product_update: update product schema
        db: sqlalchemy db object. Defaults to Depends(get_db).
    """
    return put_product(product_id=product_id, product_update=product_update, db=db)


@product.delete("/product")
async def remove_product(product_id: str, db: Session = Depends(get_db)):
    """
    To update product information

    Args:
        product_id: id of the product to update
        db: sqlalchemy db object. Defaults to Depends(get_db).
    """
    return delete_product(product_id=product_id, db=db)
