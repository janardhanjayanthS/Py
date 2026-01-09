from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, insert, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from src.core.config import settings
from src.core.log import get_logger, log_error
from src.core.utility import get_initial_data_from_csv

engine = create_engine(url=settings.DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

logger = get_logger(__name__)


def get_db():
    db = session_local()
    try:
        yield db
    except Exception as e:
        log_error(str(e))
        raise
    finally:
        db.close()


def seed_db():
    initial_data = get_initial_data_from_csv(settings.INVENTORY_CSV_FILEPATH)
    with engine.connect() as connection:
        for tablename in ["product_category", "product"]:
            if tablename in initial_data and len(initial_data[tablename]) > 0:
                target = Base.metadata.tables[tablename]
                stmt = insert(target).values(initial_data[tablename])
                try:
                    connection.execute(stmt)
                    connection.commit()
                    logger.info(
                        f"Successfully seeded {len(initial_data[tablename])} values to {tablename}"
                    )
                except Exception as e:
                    connection.rollback()
                    logger.info(
                        f"Error: Unexpected exception when interacting with db. {e}"
                    )

        # Reset sequences with COALESCE to handle empty tables
        try:
            connection.execute(
                text(
                    "SELECT setval(pg_get_serial_sequence('product', 'id'), "
                    "COALESCE((SELECT MAX(id) FROM product), 1), true);"
                )
            )
            connection.execute(
                text(
                    "SELECT setval(pg_get_serial_sequence('product_category', 'id'), "
                    "COALESCE((SELECT MAX(id) FROM product_category), 1), true);"
                )
            )
            connection.commit()
            logger.info("Successfully reset sequences")
        except Exception as e:
            connection.rollback()
            logger.error(f"Error resetting sequences: {e}")


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
