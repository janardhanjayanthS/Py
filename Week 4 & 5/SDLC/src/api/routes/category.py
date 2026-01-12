from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.jwt import required_roles
from src.core.log import get_logger
from src.models.category import Category
from src.repository.database import add_commit_refresh_db, get_db
from src.schema.category import (
    CategoryCreate,
    CategoryRead,
    CategoryResponse,
    CategoryUpdate,
)
from src.schema.user import UserRole
from src.services.category_service import (
    check_existing_category_using_id,
    check_existing_category_using_name,
    get_category_by_id,
    get_category_by_name,
)
from src.services.models import ResponseStatus

category = APIRouter()

logger = get_logger(__name__)


@category.get("/category/all", response_model=CategoryResponse)
@required_roles(UserRole.STAFF, UserRole.MANAGER, UserRole.ADMIN)
async def get_all_category(request: Request, db: Session = Depends(get_db)):
    current_user_email = request.state.email
    logger.debug(f"Fetching all categories, requested by: {current_user_email}")
    all_categories = db.query(Category).all()
    logger.info(f"Retrieved {len(all_categories)} categories")
    categories_data = [CategoryRead.model_validate(cat) for cat in all_categories]
    return {
        "status": ResponseStatus.S.value,
        "message": {
            "current user's email": current_user_email,
            "all categories": [cat.model_dump() for cat in categories_data],
        },
    }


@category.get("/category", response_model=CategoryResponse)
@required_roles(UserRole.STAFF, UserRole.MANAGER, UserRole.ADMIN)
async def get_specifc_category(
    request: Request, category_id: int, db: Session = Depends(get_db)
):
    logger.debug(f"Fetching category with id: {category_id}")
    category = db.query(Category).filter_by(id=category_id).first()
    if not category:
        logger.warning(f"Category not found with id: {category_id}")
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "response": f"Unable to find category with id - {category_id}",
            },
        }

    category_data = CategoryRead.model_validate(category)
    logger.info(f"Retrieved category: {category.name}")
    return {
        "status": ResponseStatus.S.value,
        "message": {
            "requested category": category_data.model_dump(),
        },
    }


@category.post("/category", response_model=CategoryResponse)
@required_roles(UserRole.MANAGER, UserRole.ADMIN)
async def add_category(
    request: Request, category_create: CategoryCreate, db: Session = Depends(get_db)
):
    logger.debug(f"Create category request: {category_create.name}")
    check_existing_category_using_name(category=category_create, db=db)
    check_existing_category_using_id(category=category_create, db=db)
    db_category = Category(**category_create.model_dump())
    add_commit_refresh_db(object=db_category, db=db)
    logger.info(f"Created new category: {db_category.name}")
    category_data = CategoryRead.model_validate(db_category)
    return {
        "status": ResponseStatus.S.value,
        "message": {
            "new category": category_data.model_dump(),
        },
    }


@category.put("/category/update", response_model=CategoryResponse)
@required_roles(UserRole.MANAGER, UserRole.ADMIN)
async def update_category(
    request: Request, category_update: CategoryUpdate, db: Session = Depends(get_db)
):
    logger.debug(f"Update category request for id: {category_update.id}")
    existing_category = get_category_by_id(category_id=category_update.id, db=db)
    if not existing_category or existing_category is None:
        logger.warning(f"Category not found with id: {category_update.id}")
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "response": f"Unable to find category with id - {category_update.id}",
            },
        }

    category_by_name = get_category_by_name(category_name=category_update.name, db=db)
    if category_by_name is not None and category_by_name.id != category_update.id:
        logger.warning(
            f"Category name '{category_update.name}' already exists with different id"
        )
        category_data = CategoryRead.model_validate(category_by_name)
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "response": "found existing category with same name",
                "category": category_data.model_dump(),
            },
        }

    existing_category.name = category_update.name.lower()
    db.commit()
    db.refresh(existing_category)
    logger.info(
        f"Category {category_update.id} updated to name: {existing_category.name}"
    )

    updated_category_data = CategoryRead.model_validate(existing_category)
    return {
        "status": ResponseStatus.S.value,
        "message": {
            "updated category details": updated_category_data.model_dump(),
        },
    }


@category.delete("/category/delete", response_model=CategoryResponse)
@required_roles(UserRole.ADMIN)
async def delete_category(
    request: Request,
    category_id: int,
    db: Session = Depends(get_db),
):
    logger.debug(f"Delete category request for id: {category_id}")
    category = get_category_by_id(category_id=category_id, db=db)
    if not category or category is None:
        logger.warning(f"Category not found with id: {category_id}")
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "response": f"Unable to find category with id - {category_id}",
            },
        }

    category_data = CategoryRead.model_validate(category)

    db.delete(category)
    db.commit()
    logger.info(f"Category {category.name} (id: {category_id}) deleted")

    return {
        "status": ResponseStatus.S.value,
        "message": {"deleted category": category_data.model_dump()},
    }
