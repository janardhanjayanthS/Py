from typing import Optional

from sqlalchemy.orm import Session

from src.core.constants import AIModels, logger
from src.models.cache import UserLLMCache


def save_to_cache(
    db: Session,
    user_id: int,
    question: str,
    response: str,
    llm: str = AIModels.GPT_4o_MINI.value,
    idx: int = 0,
):
    """
    Save response to cache.

    Args:
        db: Database session
        user_id: User ID
        question: User's question
        response: LLM response to cache
        llm: LLM model name
        idx: Response index (default 0 for single responses)
    """
    existing = (
        db.query(UserLLMCache)
        .filter_by(
            user_id=user_id, prompt=question, llm=llm, idx=idx, response=response
        )
        .first()
    )

    if existing:
        existing.response = response
        logger.info(f"Updated cache for user id: {user_id}")
    else:
        new_cache = UserLLMCache(
            user_id=user_id, prompt=question, llm=llm, idx=idx, response=response
        )
        db.add(new_cache)
        logger.info(f"Cached new response for user id: {user_id}")

    db.commit()


def get_cached_response(
    db: Session, user_id: int, question: str, llm: str = AIModels.GPT_4o_MINI.value
) -> Optional[str]:
    cached = (
        db.query(UserLLMCache)
        .filter_by(user_id=user_id, prompt=question, llm=llm)
        .first()
    )

    if cached:
        logger.info(f"Cache HIT for user: {user_id}")
        return cached.response

    logger.info(f"Cache HIT for user: {user_id}")
    return None
