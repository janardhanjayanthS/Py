from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.core.jwt import required_roles
from src.core.log import get_logger
from src.models.product import Product
from src.repository.database import get_db
from src.schema.product import ProductCreate, ProductUpdate
from src.schema.user import UserRole
from src.services.api_utility import (
    ResponseStatus,
    check_id_type,
    delete_product,
    get_all_products,
    get_category_by_id,
    get_category_specific_products,
    get_specific_product,
    handle_missing_product,
    post_product,
    put_product,
)

product = APIRouter()

logger = get_logger(__name__)


@product.get("/products")
@required_roles(UserRole.ADMIN, UserRole.MANAGER, UserRole.STAFF)
async def get_products(
    request: Request,
    product_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    current_user_email: str = request.state.email
    logger.debug(
        f"Get products request by: {current_user_email}, product_id: {product_id}, category_id: {category_id}"
    )
    if product_id and product_id is not None:
        check_id_type(id=product_id)
        return get_specific_product(
            user_email=current_user_email, product_id=product_id, db=db
        )
    elif category_id and category_id is not None:
        check_id_type(id=category_id)
        logger.info(f"Fetching products for category_id: {category_id}")
        return get_category_specific_products(
            user_email=current_user_email, category_id=category_id, db=db
        )
    logger.info("Fetching all products")
    return get_all_products(user_email=current_user_email, db=db)


@product.post("/products")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def post_products(
    request: Request,
    product: Optional[ProductCreate] = None,
    db: Session = Depends(get_db),
):
    current_user_email: str = request.state.email
    logger.debug(f"Create product request by: {current_user_email}")
    logger.info(f"Creating new product: {product.name if product else 'None'}")
    return post_product(user_email=current_user_email, product=product, db=db)


@product.put("/product")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def update_product(
    request: Request,
    product_id: int,
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
    current_user_email = request.state.email
    logger.debug(
        f"Update product request for product_id: {product_id} by: {current_user_email}"
    )
    logger.info(f"Updating product with id: {product_id}")
    return put_product(
        current_user_email=current_user_email,
        product_id=product_id,
        product_update=product_update,
        db=db,
    )


@product.delete("/product")
@required_roles(UserRole.ADMIN)
async def remove_product(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    To delete a product from db

    Args:
        product_id: id of the product to delete
        db: sqlalchemy db object. Defaults to Depends(get_db).
        current_user: user object returned from JWT
    """
    check_id_type(id=product_id)
    current_user_email = request.state.email
    logger.debug(
        f"Delete product request for product_id: {product_id} by: {current_user_email}"
    )
    logger.info(f"Deleting product with id: {product_id}")
    return delete_product(current_user_email, product_id=product_id, db=db)


@product.patch("/product/update_category")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def update_product_category(
    request: Request,
    product_id: int,
    category_id: int,
    db: Session = Depends(get_db),
):
    current_user_email = request.state.email
    logger.debug(
        f"Update product category request: product_id={product_id}, category_id={category_id} by: {current_user_email}"
    )
    check_id_type(id=category_id)
    category = get_category_by_id(category_id=category_id, db=db)
    if not category:
        logger.warning(f"Category not found with id: {category_id}")
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "user email": current_user_email,
                "response": f"Cannot find category with id: {category_id}",
            },
        }

    check_id_type(id=product_id)
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        logger.warning(f"Product not found with id: {product_id}")
        return handle_missing_product(product_id=product_id)

    product.category_id = category.id
    db.commit()
    db.refresh(product)
    logger.info(f"Product {product_id} category updated to {category.name}")

    return {
        "status": ResponseStatus.S.value,
        "message": {
            "user email": current_user_email,
            f"updated product to {category.name} category": product,
        },
    }
