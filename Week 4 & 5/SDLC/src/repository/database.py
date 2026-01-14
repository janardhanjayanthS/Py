from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, insert, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.core.config import settings
from src.core.exceptions import DatabaseException
from src.core.log import get_logger
from src.repository.utility import get_initial_data_from_csv

engine = create_engine(url=settings.DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

logger = get_logger(__name__)


def get_db():
    """Get database session dependency for FastAPI.

    Provides a database session with proper error handling and cleanup.
    Uses FastAPI's dependency injection pattern for database access.

    Yields:
        Session: SQLAlchemy database session instance.

    Raises:
        DatabaseException: If database connection fails.
    """
    db = session_local()
    try:
        yield db
    except Exception as e:
        logger.error(str(e))
        raise DatabaseException(
            message="Database connection failed",
            field_errors=[
                {"field": "database", "message": f"Database error: {str(e)}"}
            ],
        )
    finally:
        db.close()


def seed_db():
    """Seed database with initial data from CSV file.

    Reads inventory data from CSV file and populates database tables.
    Handles table seeding, sequence reset, and error recovery.
    Uses transaction management to ensure data consistency.

    Raises:
        DatabaseException: If seeding fails for any table or sequence reset.
    """
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
                    logger.error(f"Error seeding {tablename}: {str(e)}")
                    raise DatabaseException(
                        message=f"Failed to seed {tablename} table",
                        field_errors=[
                            {"field": tablename, "message": f"Seeding failed: {str(e)}"}
                        ],
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
            raise DatabaseException(
                message="Failed to reset database sequences",
                field_errors=[
                    {
                        "field": "sequences",
                        "message": f"Sequence reset failed: {str(e)}",
                    }
                ],
            )


def add_commit_refresh_db(object: BaseModel, db: Session):
    """Add, commit, and refresh database object.

    Performs the complete database transaction cycle for a new object:
    add to session, commit transaction, and refresh object with database values.

    Args:
        object: Pydantic model instance to insert into database.
        db: SQLAlchemy database session instance.
    """
    db.add(object)
    db.commit()
    db.refresh(object)


def commit_refresh_db(object: BaseModel, db: Session) -> None:
    """Commit and refresh database object.

    Commits transaction changes and refreshes object with updated database values.
    Used for updating existing objects without adding them to session.

    Args:
        object: Pydantic model instance to commit and refresh.
        db: SQLAlchemy database session instance.
    """
    db.commit()
    db.refresh(object)


def delete_commit_db(object: BaseModel, db: Session) -> None:
    """Delete and commit database object.

    Deletes object from database session and commits the transaction.
    Used for permanent removal of records from database.

    Args:
        object: Pydantic model instance to delete from database.
        db: SQLAlchemy database session instance.
    """
    db.delete(object)
    db.commit()


pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Uses passlib's CryptContext with bcrypt scheme for secure password hashing.
    Includes automatic salt generation and deprecated scheme handling.

    Args:
        password: Plain text password to hash.

    Returns:
        str: Bcrypt hash of the password.
    """
    return pwt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if plain text password matches bcrypt hash.

    Uses passlib's CryptContext to securely compare plain text password
    against stored bcrypt hash with automatic salt extraction.

    Args:
        plain_password: Plain text password to verify.
        hashed_password: Bcrypt hash to compare against.

    Returns:
        bool: True if password matches hash, False otherwise.
    """
    return pwt_context.verify(plain_password, hashed_password)
