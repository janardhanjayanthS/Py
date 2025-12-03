from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.api_utility import (
    delete_product,
    get_all_products,
    get_category_specific_products,
    get_specific_product,
    post_product,
    put_product,
)
from src.core.constants import ResponseStatus
from src.core.database import get_db
from src.core.decorators import auth_user, get_current_user
from src.models.models import User
from src.schema.product import ProductCreate, ProductUpdate

product = APIRouter()


@product.get("/products")
@product.post("/products")
@auth_user
async def products(
    request: Request,
    product_id: Optional[str] = "",
    category_id: Optional[int] = None,
    product: Optional[ProductCreate] = None,
    db: Session = Depends(get_db),
):
    current_user_email: str = request.state.email
    if request.method == "POST":
        return post_product(user_email=current_user_email, product=product, db=db)

    elif request.method == "GET":
        if product_id and product_id is not None:
            return get_specific_product(
                user_email=current_user_email, product_id=product_id, db=db
            )
        elif category_id and category_id is not None:
            return get_category_specific_products(
                user_email=current_user_email, category_id=category_id, db=db
            )
        return get_all_products(user_email=current_user_email, db=db)

    return {
        "status": ResponseStatus.S.value,
        "message": {"response": f"Unrecognized HTTP method {request.method}"},
    }


@product.put("/product")
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    To update product information

    Args:
        product_id: id of the product to update
        product_update: update product schema
        db: sqlalchemy db object. Defaults to Depends(get_db).
        current_user: user object returned from JWT
    """
    return put_product(
        current_user=current_user,
        product_id=product_id,
        product_update=product_update,
        db=db,
    )


@product.delete("/product")
async def remove_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    To delete a product from db

    Args:
        product_id: id of the product to delete
        db: sqlalchemy db object. Defaults to Depends(get_db).
        current_user: user object returned from JWT
    """
    return delete_product(current_user=current_user, product_id=product_id, db=db)
