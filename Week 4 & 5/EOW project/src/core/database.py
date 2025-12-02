from os import getenv

from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, insert
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.schema import Table

from src.core.constants import INVENTORY_CSV_FILEPATH
from src.core.log import log_error
from src.core.utility import get_initial_product_data_from_csv

load_dotenv()

postgresql_pwd = getenv("POSTGRESQL_PWD")

DATABASE_URL = (
    f"postgresql://postgres:{postgresql_pwd}@localhost:5432/inventory_manager"
)


engine = create_engine(url=DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    except Exception as e:
        log_error(str(e))
        raise
    finally:
        db.close()


def initialize_table(target: Table, connection: Connection, **kw):
    """
    Used for db seeding
    receives a target table, a connection and inserts
    data into that table

    Args:
        target: target table name
        connection: connection to db
        initial_data: dictionary containing data to insert into target table
    """
    tablename = target.name
    INITIAL_DATA = get_initial_product_data_from_csv(INVENTORY_CSV_FILEPATH)

    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        stmt = insert(target).values(INITIAL_DATA[tablename])
        try:
            connection.execute(stmt)
            connection.commit()
            print(
                f"Successfully seeded {len(INITIAL_DATA[tablename])} values to {tablename}"
            )
        except Exception as e:
            print(f"Error: Unexpected exception when interacting with db. {e}")


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


pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt

    Args:
        password: plain text password

    Returns:
        str: hash of the password
    """
    return pwt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if plain text matches a hash

    Args:
        plain_password: plain text password
        hashed_password: hashed password

    Returns:
        bool: True if match, False otherwise
    """
    return pwt_context.verify(plain_password, hashed_password)
