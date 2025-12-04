from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.api_utility import (
    delete_product,
    get_all_products,
    get_category_by_id,
    get_category_specific_products,
    get_specific_product,
    handle_missing_product,
    post_product,
    put_product,
)
from src.core.constants import ResponseStatus
from src.core.database import get_db
from src.core.decorators import (
    authorize_admin,
    authorize_manager_and_above,
    authorize_staff_and_above,
)
from src.models.models import Product
from src.schema.product import ProductCreate, ProductUpdate

product = APIRouter()


@product.get("/products")
@authorize_staff_and_above
async def get_products(
    request: Request,
    product_id: Optional[str] = "",
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    current_user_email: str = request.state.email
    if product_id and product_id is not None:
        return get_specific_product(
            user_email=current_user_email, product_id=product_id, db=db
        )
    elif category_id and category_id is not None:
        return get_category_specific_products(
            user_email=current_user_email, category_id=category_id, db=db
        )
    return get_all_products(user_email=current_user_email, db=db)


@product.post("/products")
@authorize_manager_and_above
async def post_products(
    request: Request,
    product: Optional[ProductCreate] = None,
    db: Session = Depends(get_db),
):
    current_user_email: str = request.state.email
    return post_product(user_email=current_user_email, product=product, db=db)


@product.put("/product")
@authorize_manager_and_above
async def update_product(
    request: Request,
    product_id: str,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    """
    To update product information

    Args:
        product_id: id of the product to update
        product_update: update product schema
        db: sqlalchemy db object. Defaults to Depends(get_db).
    """
    current_user_email = request.state.user_email
    return put_product(
        current_user=current_user_email,
        product_id=product_id,
        product_update=product_update,
        db=db,
    )


@product.delete("/product")
@authorize_admin
async def remove_product(
    request: Request,
    product_id: str,
    db: Session = Depends(get_db),
):
    """
    To delete a product from db

    Args:
        product_id: id of the product to delete
        db: sqlalchemy db object. Defaults to Depends(get_db).
        current_user: user object returned from JWT
    """
    current_user_email = request.state.email
    return delete_product(current_user=current_user_email, product_id=product_id, db=db)


@product.patch("/product/update_category")
@authorize_manager_and_above
async def update_product_category(
    request: Request,
    product_id: str,
    category_id: int,
    db: Session = Depends(get_db),
):
    current_user_email = request.state.email
    category = get_category_by_id(category_id=category_id, db=db)
    if not category:
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "user email": current_user_email,
                "response": f"Cannot find category with id: {category_id}",
            },
        }

    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        return handle_missing_product(product_id=product_id)

    product.category_id = category.id
    db.commit()
    db.refresh(product)

    return {
        "status": ResponseStatus.S.value,
        "message": {
            "user email": current_user_email,
            f"updated product to {category.name} category": product,
        },
    }
