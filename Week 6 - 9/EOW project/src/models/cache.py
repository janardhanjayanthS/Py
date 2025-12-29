from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class UserLLMCache(Base):
    __tablename__ = "user_llm_cache"

    idx: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    llm: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, primary_key=True, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (Index("idx_user_prompt", "user_id", "prompt"),)
