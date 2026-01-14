from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.decorator_pattern import ConcretePrice, DiscountDecorator, TaxDecorator
from src.core.exceptions import DatabaseException
from src.core.log import get_logger
from src.models.category import Category
from src.models.product import Product
from src.repository.database import add_commit_refresh_db
from src.schema.product import ProductCreate
from src.services.category_service import handle_missing_category
from src.services.models import ResponseStatus
from src.services.utility import check_id_type

logger = get_logger(__name__)


def check_existing_product_using_name(product: Optional[ProductCreate], db: Session):
    """Check if product already exists in database.

    Args:
        product: Pydantic product model with details.
        db: Database session instance.

    Raises:
        DatabaseException: If product already exists.
    """
    existing_product = db.query(Product).filter_by(name=product.name).first()
    if existing_product is not None:
        message = f"product with name {product.name} already exists"
        logger.error(message=message)
        raise DatabaseException(
            message=message,
            field_errors=[
                {
                    "field": "product name",
                    "message": f"{product.name} already exists in DB",
                }
            ],
        )


def check_existing_product_using_id(product: Optional[ProductCreate], db: Session):
    """Check if product already exists in database by ID.

    Args:
        product: Pydantic product model with details.
        db: Database session instance.

    Raises:
        DatabaseException: If product already exists.
    """
    existing_product = db.query(Product).filter_by(id=product.id).first()
    if existing_product is not None:
        message = f"product with id {product.id} already exists"
        logger.error(message=message)
        raise DatabaseException(
            message=message,
        )


def handle_missing_product(product_id: str):
    """
    logs & retruns error of missing product

    Args:
        product_id: fetched product id

    Returns:
        dict: fastapi response
    """
    message = f"product with id {product_id} not found"
    logger.error(message=message)
    return {
        "status": ResponseStatus.E.value,
        "message": {
            "response": message,
        },
    }


def post_product(
    user_email: str, product: Optional[ProductCreate], db: Session
) -> dict:
    """
    Inserts product into db

    Args:
        user_email: current user's email id
        product: Pydnatic product model
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    logger.debug(f"Creating product: {product.name if product else 'None'}")
    check_existing_product_using_name(product=product, db=db)
    check_existing_product_using_id(product=product, db=db)

    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        return handle_missing_category(category_id=product.category_id)

    db_product = Product(**product.model_dump())
    if product.id is not None:
        db_product = apply_discount_or_tax(product=db_product)

    add_commit_refresh_db(object=db_product, db=db)
    logger.info(f"Product '{db_product.name}' created successfully")

    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": user_email, "inserted product": db_product},
    }


def apply_discount_or_tax(product: Product) -> Product:
    """
    Applies dicount or tax to product's price

    Args:
        product: db product object

    Returns:
        Product: db product object
    """
    price = ConcretePrice(amount=product.price)
    if product.id % 2 == 0:
        price = TaxDecorator(price=price, tax_percentage=0.2)
        product.price_type = "taxed"
    else:
        price = DiscountDecorator(price=price, discount_percentage=0.2)
        product.price_type = "discounted"
    product.price = price.get_amount()
    logger.info(f"Applied {product.price_type} to {price.get_amount()}")
    return product


def get_all_products(user_email: str, db: Session) -> dict:
    """
    To fetch all products from database

    Args:
        user_email: current user's email id
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    products = db.query(Product).all()
    logger.info(f"Retrieved {len(products)} products")
    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": user_email, "products": products},
    }


def get_specific_product(user_email: str, product_id: int, db: Session) -> dict:
    """
    Fetches a specific product from db

    Args:
        user_email: current user's email id
        product_id: id to the product to select
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    logger.debug(f"Fetching product with id: {product_id}")
    check_id_type(id=product_id)
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        logger.warning(f"Product not found with id: {product_id}")
        return handle_missing_product(product_id=str(product_id))

    logger.info(f"Retrieved product: {product.name}")
    return {
        "status": ResponseStatus.S.value,
        "message": {"user_email": user_email, "product": product},
    }


def get_category_specific_products(user_email: str, category_id: int, db: Session):
    """
    Fetches a products under a specific category from db

    Args:
        user_email: current user's email id
        category_id: category id to filter
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    logger.debug(f"Fetching products for category_id: {category_id}")
    products = db.query(Product).filter_by(category_id=category_id).all()
    logger.info(f"Retrieved {len(products)} products for category_id: {category_id}")
    return {
        "status": ResponseStatus.S.value,
        "message": {
            "user_email": user_email,
            f"products with category id: {category_id}": products,
        },
    }


def put_product(
    current_user_email: str, product_id: int, product_update: BaseModel, db: Session
) -> dict:
    """
    update product details

    Args:
        current_user_email: email id of user in session
        product_id: id of the product to update
        product: detail's of product to update
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    logger.debug(f"Updating product with id: {product_id}")
    check_id_type(id=product_id)
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        logger.warning(f"Product not found for update: {product_id}")
        return handle_missing_product(product_id=product_id)

    update_data = product_update.model_dump(exclude_unset=True)  # type: ignore
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    logger.info(f"Product '{db_product.name}' updated successfully")
    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "updated product": db_product},
    }


def delete_product(current_user_email: str, product_id: int, db: Session) -> dict:
    """
    delete a product from db

    Args:
        current_user_email: email id of user in session
        product_id: id of the product to update
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    logger.debug(f"Deleting product with id: {product_id}")
    check_id_type(id=product_id)
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        logger.warning(f"Product not found for deletion: {product_id}")
        return handle_missing_product(product_id=product_id)

    db.delete(db_product)
    db.commit()
    logger.info(f"Product '{db_product.name}' (id: {product_id}) deleted successfully")
    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "deleted product": db_product},
    }
