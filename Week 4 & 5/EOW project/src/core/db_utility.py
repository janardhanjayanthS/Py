from pydantic import BaseModel
from sqlalchemy.orm import Session


def add_commit_refresh_db(object: BaseModel, db: Session):
    """
    add, commit and refresh db after adding a row

    Args:
        object: to insert to db (pydantic model instance)
        db: database instance in session
    """
    db.add(object)
    db.commit()
    db.refresh(object)
