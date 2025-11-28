from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.api_utility import get_all_products, get_specific_product, post_product
from src.core.db_config import get_db
from src.core.log import log_error
from src.models.models import Product
from src.schema.product import ProductCreate, ProductResponse

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


# @product.get("/products")
# async def products(db: Session = Depends(get_db)):


# @product.get("/products/{product_id}")
# async def product_with_id(product_id: str, db: Session = Depends(get_db)):
#     product = db.query(Product).filter_by(id=product_id).first()

#     if product is None:
#         message = f"product with id {product_id} not found"
#         log_error(message=message)
#         return {
#             "status": "error",
#             "message": {
#                 "response": message,
#             },
#         }

#     return {"status": "success", "message": {"product": product}}


# @product.post("/add_product", response_model=ProductResponse)
# async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
#     check_if_product_exists(product=product, db=db)

#     if product and product.type == "regular":
#         product.reset_regular_product_attributes()

#     db_product = Product(**product.model_dump())
#     add_commit_refresh_db(object=db_product, db=db)

#     return {"status": "success", "message": {"inserted_product": db_product}}
