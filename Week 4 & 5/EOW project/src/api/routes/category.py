from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.api_utility import check_existing_category_using_name
from src.core.constants import ResponseStatus
from src.core.database import add_commit_refresh_db, get_db
from src.models.models import Category
from src.schema.category import CategoryCreate

category = APIRouter()


@category.get("/category/all")
async def get_all_category(db: Session = Depends(get_db)):
    all_categories = db.query(Category).all()
    return {
        "status": ResponseStatus.S.value,
        "message": {"all categories": all_categories},
    }


@category.get("/category")
async def get_specifc_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter_by(id=category_id).first()
    if not category:
        return {
            "status": ResponseStatus.E.value,
            "message": {"response": f"Unable to find category with id - {category_id}"},
        }

    return {
        "status": ResponseStatus.S.value,
        "message": {"requested category": category},
    }


@category.post("/category")
async def add_category(category_create: CategoryCreate, db: Session = Depends(get_db)):
    check_existing_category_using_name(category=category_create, db=db)
    db_category = Category(**category_create.model_dump())
    add_commit_refresh_db(object=db_category, db=db)
    return {
        "status": ResponseStatus.S.value,
        "message": {"new category": db_category},
    }
