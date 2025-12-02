from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[str] = mapped_column(
        String(10), primary_key=True, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    days_to_expire: Mapped[int | None] = mapped_column(nullable=True)
    is_vegetarian: Mapped[bool | None] = mapped_column(nullable=True)
    warranty_in_years: Mapped[float | None] = mapped_column(nullable=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_category.id"), nullable=False
    )
    category = Mapped["Category"] = relationship()


class Category(Base):
    __tablename__ = "product_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), unique=True)
