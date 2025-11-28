from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.api_utility import get_all_products, get_specific_product, post_product
from src.core.db_config import get_db
from src.schema.product import ProductCreate

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
