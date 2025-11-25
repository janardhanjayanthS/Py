from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv
from os import getenv

load_dotenv("../../.env")

postgresql_pwd = getenv("POSTGRESQL_PWS")

DATABASE_URL = (
    f"postgresql://postgres:{postgresql_pwd}@localhost:5432/inventory_manager"
)

engine = create_engine(url=DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
