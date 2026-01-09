from typing import Any, Optional

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.config import ResponseStatus
from src.core.database import add_commit_refresh_db, hash_password, verify_password
from src.core.decorator_pattern import ConcretePrice, DiscountDecorator, TaxDecorator
from src.core.log import get_logger, log_error
from src.models.models import Category, Product, User
from src.schema.category import BaseCategory
from src.schema.product import ProductCreate
from src.schema.user import UserEdit, UserRegister

logger = get_logger(__name__)


def check_id_type(id: Any):
    """Validate that the id parameter is an integer type.

    Args:
        id: The id value to validate.

    Raises:
        HTTPException: If id is not None/falsy and not an integer, raises 422
            Unprocessable Content error with details about the type mismatch.
    """
    if id and not isinstance(id, int):
        logger.error("ID should be numbers(integers)")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"id should be type int but got type: {id.__class__.__name__}",
        )


def get_category_by_id(category_id: int, db: Session) -> Category | None:
    """
    Gets category by id

    Args:
        category_id: category id to search db
        db: database instance in session

    Returns:
        returns category object if exists else None
    """
    return db.query(Category).filter_by(id=category_id).first()


def check_existing_category_using_name(category: BaseCategory, db: Session):
    """
    checks db if category exists by name

    Args:
        category: category pydantic model
        db: database instance in session

    Raises:
        HTTPException: if no category in db
    """
    existing_category = get_category_by_name(category_name=category.name, db=db)
    if existing_category is not None:
        message = f"Category with name - {category.name} - already exists in db"
        log_error(message=message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"message": message}
        )


def check_existing_category_using_id(category: BaseCategory, db: Session):
    """
    checks db if category exists by name

    Args:
        category: category pydantic model
        db: database instance in session

    Raises:
        HTTPException: if no category in db
    """
    existing_category = get_category_by_id(category_id=category.id, db=db)
    if existing_category is not None:
        message = f"Category with id - {category.id} - already exists in db"
        log_error(message=message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"message": message}
        )


def get_category_by_name(category_name: str, db: Session) -> Category | None:
    """
    Gets category (db object) using name

    Args:
        category_name: name of category to look for
        db: database instance in session

    Returns:
        category from db if exists else None
    """
    existing_category = (
        db.query(Category).filter(Category.name == category_name).first()
    )
    return existing_category if existing_category else None


def check_existing_product_using_name(product: Optional[ProductCreate], db: Session):
    """
    Checks if product already exists in db,
    if so raises HTTP error

    Args:
        product: pydnatic product model with its details
        db: database instance in session
    Raises:
        HTTPException: if product does not exist
    """
    existing_product = db.query(Product).filter_by(name=product.name).first()
    if existing_product is not None:
        message = f"product with name {product.name} already exists"
        log_error(message=message)
        raise HTTPException(status_code=400, detail={"message": message})


def check_existing_product_using_id(product: Optional[ProductCreate], db: Session):
    """
    Checks if product already exists in db,
    if so raises HTTP error

    Args:
        product: pydnatic product model with its details
        db: database instance in session
    Raises:
        HTTPException: if product does not exist
    """
    existing_product = db.query(Product).filter_by(id=product.id).first()
    if existing_product is not None:
        message = f"product with id {product.id} already exists"
        log_error(message=message)
        raise HTTPException(status_code=400, detail={"message": message})


def handle_missing_product(product_id: str):
    """
    logs & retruns error of missing product

    Args:
        product_id: fetched product id

    Returns:
        dict: fastapi response
    """
    message = f"product with id {product_id} not found"
    log_error(message=message)
    return {
        "status": ResponseStatus.E.value,
        "message": {
            "response": message,
        },
    }


def check_existing_user_using_email(user: UserRegister, db: Session) -> bool:
    """
    Checks if user's email address already exists in db
    Args:
        user: User object containing user details
        db: sqlalchemy db object

    Returns:
        bool: true if user already exists, false otherwise
    """
    existing_user = fetch_user_by_email(email_id=user.email, db=db)
    return True if existing_user else False


def fetch_user_by_email(email_id: str, db: Session) -> User | None:
    """
    gets User object with specific email from db

    Args:
        email_id: email id of user to search
        db: sqlalchemy db object

    Returns:
        User | None: user object if user exists else None
    """
    return db.query(User).filter_by(email=email_id).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Verify user credentials,
    return user if authenticate

    Args:
        db: sqlalchemy db object
        email: user's email id
        password: user's passowrd

    Returns:
        User: valid user object with user data
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(plain_password=password, hashed_password=str(user.password)):
        return None

    return user


def update_user_name(current_user: User, update_details: UserEdit) -> str:
    """
    Update user's name to a new name

    Args:
        current_user: current logged in user's db instance
        update_details: user details to update

    Returns:
        str: update message if name is updated or empty string
    """
    if (
        update_details.new_name is not None
        and current_user.name != update_details.new_name
    ):
        current_user.name = update_details.new_name
        return f"updated user's name to {update_details.new_name}. "
    return "existing name and new name are same. "


def update_user_password(current_user: User, update_details: UserEdit) -> str:
    """
    Update user's password to a new password

    Args:
        current_user: current logged in user's db instance tf
        update_details: user details to update

    Returns:
        str: update message if name is updated or empty string
    """
    if (
        update_details.new_password is not None
        and current_user.password != hash_password(update_details.new_password)
    ):
        current_user.password = hash_password(update_details.new_password)
        return "password updated"
    return "same password"


def handle_missing_user(user_id: int) -> dict:
    """
    Log and return response for missing user

    Args:
        user_id: missing user's id

    Returns:
        dict: response describing missing user
    """
    message = f"Unable to find user with id: {user_id}"
    log_error(message)
    return {
        "status": ResponseStatus.E.value,
        "message": {"response": message},
    }


def handle_missing_category(category_id: int):
    """
    Log and return response for missing category

    Args:
        category_id: missing category's id

    Returns:
        dict: response describing missing category
    """
    message = f"Cannot find category with id: {category_id}"
    log_error(message)
    return {
        "status": ResponseStatus.E.value,
        "message": {"response": message},
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
    check_existing_product_using_name(product=product, db=db)
    check_existing_product_using_id(product=product, db=db)

    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        return handle_missing_category(category_id=product.category_id)

    db_product = Product(**product.model_dump())
    if product.id is not None:
        db_product = apply_discount_or_tax(product=db_product)

    add_commit_refresh_db(object=db_product, db=db)

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
    check_id_type(id=product_id)
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        return handle_missing_product(product_id=str(product_id))

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
    products = db.query(Product).filter_by(category_id=category_id).all()
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
    check_id_type(id=product_id)
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        return handle_missing_product(product_id=product_id)

    update_data = product_update.model_dump(exclude_unset=True)  # type: ignore
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
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
    check_id_type(id=product_id)
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        return handle_missing_product(product_id=product_id)

    db.delete(db_product)
    db.commit()
    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "deleted product": db_product},
    }
