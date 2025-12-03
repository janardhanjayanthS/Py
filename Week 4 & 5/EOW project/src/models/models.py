from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class Category(Base):
    __tablename__ = "product_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), unique=True)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_category.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped["Category"] = relationship()
