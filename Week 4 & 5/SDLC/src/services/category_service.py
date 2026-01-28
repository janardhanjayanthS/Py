from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.log import get_logger, log_error
from src.models.category import Category
from src.schema.category import BaseCategory
from src.services.models import ResponseStatus

logger = get_logger(__name__)


def get_category_by_id(category_id: int, db: Session) -> Category | None:
    """
    Gets category by id

    Args:
        category_id: category id to search db
        db: database instance in session

    Returns:
        returns category object if exists else None
    """
    logger.debug(f"Fetching category by id: {category_id}")
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
    logger.debug(f"Fetching category by name: {category_name}")
    existing_category = (
        db.query(Category).filter(Category.name == category_name).first()
    )
    return existing_category if existing_category else None


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
