from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.constants import ResponseStatus
from src.core.database import add_commit_refresh_db, hash_password, verify_password
from src.core.log import log_error
from src.models.models import Product, User
from src.schema.product import ProductCreate
from src.schema.user import UserEdit, UserRegister


def check_existin_product_using_id(product: Optional[ProductCreate], db: Session):
    """
    Checks if product already exists in db,
    if so raises HTTP error

    Args:
        product: pydnatic product model with its details
        db: database instance in session
    """
    existing_product = db.query(Product).filter_by(id=product.id).first()  # type: ignore
    if existing_product is not None:
        message = f"product with id {product.id} already exists"  # type: ignore
        log_error(message=message)
        raise HTTPException(status_code=400, detail={"message": message})


def handle_missing_product(product_id: str):
    """
    ensures if db returned a valid product,
    if not then logs & retruns error

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
    existing_user = db.query(User).filter_by(email=user.email).first()
    return True if existing_user else False


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
    return ""


def update_user_password(current_user: User, update_details: UserEdit) -> str:
    """
    Update user's password to a new password

    Args:
        current_user: current logged in user's db instance
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
    return ""


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
    check_existin_product_using_id(product=product, db=db)

    if product and product.type == "regular":
        product.reset_regular_product_attributes()

    db_product = Product(**product.model_dump())  # type: ignore
    add_commit_refresh_db(object=db_product, db=db)

    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": user_email, "inserted product": db_product},
    }


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


def get_specific_product(user_email: str, product_id: str, db: Session) -> dict:
    """
    Fetches a specific product from db

    Args:
        user_email: current user's email id
        product_id: id to the product to select
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        return handle_missing_product(product_id=str(product_id))

    return {
        "status": ResponseStatus.S.value,
        "message": {"user_email": user_email, "product": product},
    }


def put_product(
    current_user: User, product_id: str, product_update: BaseModel, db: Session
) -> dict:
    """
    update product details

    Args:
        current_user: User instance of current user
        product_id: id of the product to update
        product: detail's of product to update
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
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
        "message": {"user email": current_user.email, "updated product": db_product},
    }


def delete_product(current_user: User, product_id: str, db: Session) -> dict:
    """
    delete a product from db

    Args:
        current_user: User instance of current user
        product_id: id of the product to update
        db: sqlalchemy db object

    Returns:
        dict: fastapi response
    """
    db_product = db.query(Product).filter_by(id=product_id).first()
    if db_product is None:
        return handle_missing_product(product_id=product_id)

    db.delete(db_product)
    db.commit()
    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user.email, "deleted product": db_product},
    }
