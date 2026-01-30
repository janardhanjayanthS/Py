from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.repository.database import Base


class Category(Base):
    __tablename__ = "product_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), unique=True)

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )
