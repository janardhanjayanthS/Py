from sqlalchemy import Column, String, Integer, Float, Boolean

from ..core.db_config import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String, nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(String(10), primary_key=True, unique=True, index=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    type = Column(String(10), nullable=False)
    days_to_expire = Column(Integer, nullable=True)
    is_vegetarian = Column(Boolean, nullable=True)
    warranty_in_years = Column(Float, nullable=True)