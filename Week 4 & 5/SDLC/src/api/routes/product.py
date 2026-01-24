from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.core.jwt import required_roles
from src.core.log import get_logger
from src.models.product import Product
from src.repository.database import commit_refresh_db, get_db
from src.schema.product import ProductCreate, ProductUpdate
from src.schema.user import UserRole
from src.services.category_service import get_category_by_id
from src.services.models import ResponseStatus
from src.services.product_service import (
    delete_product,
    get_all_products,
    get_category_specific_products,
    get_specific_product,
    handle_missing_product,
    post_product,
    put_product,
)
from src.services.utility import check_id_type

product = APIRouter()

logger = get_logger(__name__)


@product.get("/products")
@required_roles(UserRole.ADMIN, UserRole.MANAGER, UserRole.STAFF)
async def get_products(
    request: Request,
    product_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve products based on optional filters.

    Args:
        request: HTTP request object.
        product_id: Optional product ID to filter by.
        category_id: Optional category ID to filter by.
        db: Database session dependency.

    Returns:
        Product response based on provided filters.
    """
    current_user_email: str = request.state.email
    logger.debug(
        f"Get products request by: {current_user_email}, product_id: {product_id}, category_id: {category_id}"
    )
    if product_id and product_id is not None:
        check_id_type(id=product_id)
        return await get_specific_product(
            user_email=current_user_email, product_id=product_id, db=db
        )
    elif category_id and category_id is not None:
        check_id_type(id=category_id)
        logger.info(f"Fetching products for category_id: {category_id}")
        return await get_category_specific_products(
            user_email=current_user_email, category_id=category_id, db=db
        )
    logger.info("Fetching all products")
    return await get_all_products(user_email=current_user_email, db=db)


@product.post("/products")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def post_products(
    request: Request,
    product: Optional[ProductCreate] = None,
    db: Session = Depends(get_db),
):
    """Create a new product.

    Args:
        request: HTTP request object.
        product: Product data to create.
        db: Database session dependency.

    Returns:
        Created product response.
    """
    current_user_email: str = request.state.email
    logger.debug(f"Create product request by: {current_user_email}")
    logger.info(f"Creating new product: {product.name if product else 'None'}")
    return await post_product(user_email=current_user_email, product=product, db=db)


@product.put("/product")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def update_product(
    request: Request,
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    """Update product information.

    Args:
        request: HTTP request object.
        product_id: ID of the product to update.
        product_update: Product update data.
        db: Database session dependency.

    Returns:
        Updated product response.
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
    """Delete a product from the database.

    Args:
        request: HTTP request object.
        product_id: ID of the product to delete.
        db: Database session dependency.

    Returns:
        Deletion response.
    """
    check_id_type(id=product_id)
    current_user_email = request.state.email
    logger.debug(
        f"Delete product request for product_id: {product_id} by: {current_user_email}"
    )
    logger.info(f"Deleting product with id: {product_id}")
    return await delete_product(current_user_email, product_id=product_id, db=db)


@product.patch("/product/update_category")
@required_roles(UserRole.ADMIN, UserRole.MANAGER)
async def update_product_category(
    request: Request,
    product_id: int,
    category_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Update product category assignment.

    Args:
        request: HTTP request object.
        product_id: ID of the product to update.
        category_id: New category ID for the product.
        db: Database session dependency.

    Returns:
        Updated product category response.
    """
    current_user_email = request.state.email
    logger.debug(
        f"Update product category request: product_id={product_id}, category_id={category_id} by: {current_user_email}"
    )
    check_id_type(id=category_id)
    category = await get_category_by_id(category_id=category_id, db=db)
    logger.debug(f"retrieved category: {category}")
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

    # REPO
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalars().first()
    logger.debug(f"Product found: {product}")

    if not product:
        logger.warning(f"Product not found with id: {product_id}")
        return handle_missing_product(product_id=product_id)

    product.category_id = category.id

    await commit_refresh_db(object=product, db=db)
    logger.info(f"Product {product_id} category updated to {category.name}")

    return {
        "status": ResponseStatus.S.value,
        "message": {
            "user email": current_user_email,
            f"updated product to {category.name} category": product,
        },
    }
