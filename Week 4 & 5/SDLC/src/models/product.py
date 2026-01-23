from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.repository.database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    price_type: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default="regular"
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_category.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
