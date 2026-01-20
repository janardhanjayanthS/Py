from sqlalchemy.orm import Session

from src.core.exceptions import DatabaseException
from src.core.log import get_logger
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
    """Check if category exists by name in database.

    Args:
        category: Category pydantic model.
        db: Database session instance.

    Raises:
        DatabaseException: If category already exists.
    """
    existing_category = get_category_by_name(category_name=category.name, db=db)
    if existing_category is not None:
        message = f"Category with name - {category.name} - already exists in db"
        logger.error(message)
        raise DatabaseException(
            message=message,
            field_errors=[
                {
                    "field": "category name",
                    "message": f"{category.name} already exists in DB",
                }
            ],
        )


def check_existing_category_using_id(category: BaseCategory, db: Session):
    """Check if category exists by ID in database.

    Args:
        category: Category pydantic model.
        db: Database session instance.

    Raises:
        DatabaseException: If category already exists.
    """
    existing_category = get_category_by_id(category_id=category.id, db=db)
    if existing_category is not None:
        message = f"Category with id - {category.id} - already exists in db"
        logger.error(message)
        raise DatabaseException(
            message=message,
            field_errors=[
                {
                    "field": "category id",
                    "message": f"{category.id} already exists in DB",
                }
            ],
        )


def get_category_by_name(category_name: str, db: Session) -> Category | None:
    """Get category by name from database.

    Args:
        category_name: Name of category to search.
        db: Database session instance.

    Returns:
        Category object if found, None otherwise.
    """

    logger.debug(f"Fetching category by name: {category_name}")
    existing_category = (
        db.query(Category).filter(Category.name == category_name).first()
    )
    return existing_category if existing_category else None


def handle_missing_category(category_id: int):
    """Log and return response for missing category.

    Args:
        category_id: Missing category ID.

    Returns:
        Dictionary with error response for missing category.
    """
    message = f"Cannot find category with id: {category_id}"
    logger.error(message)
    return {
        "status": ResponseStatus.E.value,
        "message": {"response": message},
    }
