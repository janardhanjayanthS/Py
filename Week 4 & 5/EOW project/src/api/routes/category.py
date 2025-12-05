from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.api_utility import (
    check_existing_category_using_id,
    check_existing_category_using_name,
    get_category_by_id,
    get_category_by_name,
)
from src.core.constants import ResponseStatus
from src.core.database import add_commit_refresh_db, get_db
from src.core.decorators import required_roles
from src.models.models import Category
from src.schema.category import CategoryCreate, CategoryUpdate
from src.schema.user import UserRole

category = APIRouter()


@category.get("/category/all")
@required_roles(UserRole.STAFF, UserRole.MANAGER, UserRole.ADMIN)
async def get_all_category(request: Request, db: Session = Depends(get_db)):
    current_user_email = request.state.email
    all_categories = db.query(Category).all()
    return {
        "status": ResponseStatus.S.value,
        "message": {
            "current user's email": current_user_email,
            "all categories": all_categories,
        },
    }


@category.get("/category")
@required_roles(UserRole.STAFF, UserRole.MANAGER, UserRole.ADMIN)
async def get_specifc_category(
    request: Request, category_id: int, db: Session = Depends(get_db)
):
    current_user_email = request.state.email
    category = db.query(Category).filter_by(id=category_id).first()
    if not category:
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "current user's email": current_user_email,
                "response": f"Unable to find category with id - {category_id}",
            },
        }

    return {
        "status": ResponseStatus.S.value,
        "message": {
            "current user's email": current_user_email,
            "requested category": category,
        },
    }


@category.post("/category")
@required_roles(UserRole.MANAGER, UserRole.ADMIN)
async def add_category(
    request: Request, category_create: CategoryCreate, db: Session = Depends(get_db)
):
    current_user_email = request.state.email
    check_existing_category_using_name(category=category_create, db=db)
    check_existing_category_using_id(category=category_create, db=db)
    db_category = Category(**category_create.model_dump())
    add_commit_refresh_db(object=db_category, db=db)
    return {
        "status": ResponseStatus.S.value,
        "message": {
            "current user's email": current_user_email,
            "new category": db_category,
        },
    }


@category.put("/category/update")
@required_roles(UserRole.MANAGER, UserRole.ADMIN)
async def update_category(
    request: Request, category_update: CategoryUpdate, db: Session = Depends(get_db)
):
    current_user_email = request.state.email
    existing_category = get_category_by_id(category_id=category_update.id, db=db)
    if not existing_category or existing_category is None:
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "current user's email": current_user_email,
                "response": f"Unable to find category with id - {category_update.id}",
            },
        }

    category_by_name = get_category_by_name(category_name=category_update.name, db=db)
    if category_by_name is not None:
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "current user's email": current_user_email,
                "response": "found existing category with same name",
                "category": category_by_name,
            },
        }

    existing_category.name = category_update.name.lower()
    db.commit()
    db.refresh(existing_category)

    return {
        "status": ResponseStatus.S.value,
        "message": {
            "current user's email": current_user_email,
            "updated category details": category_update,
        },
    }


@category.delete("/category/delete")
@required_roles(UserRole.ADMIN)
async def delete_category(
    request: Request,
    category_id: int,
    db: Session = Depends(get_db),
):
    current_user_email = request.state.email
    category = get_category_by_id(category_id=category_id, db=db)
    if not category or category is None:
        return {
            "status": ResponseStatus.E.value,
            "message": {
                "user email": current_user_email,
                "response": f"Unable to find category with id - {category_id}",
            },
        }

    db.delete(category)
    db.commit()

    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "deleted category": category},
    }
