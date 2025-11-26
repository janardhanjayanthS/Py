from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine, insert
from sqlalchemy.engine import Connection
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import Table

from ..core.config import INVENTORY_CSV_FILEPATH
from ..core.utility import get_initial_product_data_from_csv

load_dotenv("../../.env")

postgresql_pwd = getenv("POSTGRESQL_PWD")

DATABASE_URL = (
    f"postgresql://postgres:{postgresql_pwd}@localhost:5432/inventory_manager"
)


engine = create_engine(url=DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


INITIAL_DATA = get_initial_product_data_from_csv(INVENTORY_CSV_FILEPATH)


def initialize_table(target: Table, connection: Connection):
    """
    Used for db seeding
    receives a target table, a connection and inserts
    data into that table

    Args:
        target: target table name
        connection: connection to db
        initial_data: dictionary containing data to insert into target table
    """
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        stmt = insert(target).values(INITIAL_DATA[tablename])
        connection.execute(stmt)
        connection.commit()
        print(
            f"Successfully seeded {len(INITIAL_DATA[tablename])} values to {tablename}"
        )
