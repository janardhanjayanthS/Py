import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.ai_utility import (
    calculate_token_cost,
    clean_llm_output,
    get_conversational_rag_chain,
    update_history,
)
from src.core.cache import get_cached_response, save_to_cache
from src.core.constants import HISTORY, AIModels, ResponseType, logger
from src.core.database import get_db
from src.core.jwt_utility import authenticate_user_from_token
from src.core.utility import CacheDetails, get_elapsed_time_till_now_in_ms
from src.models.user import User
from src.schema.ai import Query
from src.schema.response import APIResponse

chat = APIRouter()


@chat.post("/chat", response_model=APIResponse)
async def search_from_db(
    query: Query,
    current_user: User = Depends(authenticate_user_from_token),
    db: Session = Depends(get_db),
):
    """
    Performs a query using a Conversational RAG chain against the vector database.

    The query is answered based on the documents stored in the database,
    maintaining conversational history. The chat history is updated after
    the response is generated. Calculates and returns the token cost.

    Args:
        query: The user's query wrapped in a Query schema object.

    Returns:
        A dictionary with the response status and a message containing the
        cleaned AI's response and the calculated token cost.

    Raises:
        HTTPException: If an error occurs during the RAG chain invocation,
                       a 400 Bad Request is raised.
    """
    start_time: float = time.perf_counter()
    logger.info(f"CURRENT USER EMAIL: {current_user.email}")
    try:
        cached_response = get_cached_response(
            details=CacheDetails(
                db=db,
                user_id=current_user.id,
                question=query.query,
            )
        )

        if cached_response:
            return APIResponse(
                response=ResponseType.SUCCESS,
                message={
                    "response time": f"{get_elapsed_time_till_now_in_ms(start_time=start_time):.0f}ms",
                    "query response": clean_llm_output(cached_response),
                },
            )

        logger.info("Invoking RAG chain")
        result = get_conversational_rag_chain().invoke(
            {
                "question": query.query,
                "chat_history": HISTORY,
                "user_id": current_user.id,
            }
        )
        update_history(result=result, query=query)
        token_cost = calculate_token_cost(
            result.usage_metadata, ai_model=AIModels.GPT_4o_MINI
        )

        save_to_cache(
            details=CacheDetails(
                db=db,
                user_id=current_user.id,
                question=query.query,
            ),
            response=clean_llm_output(result.content),
        )

        return APIResponse(
            response=ResponseType.SUCCESS,
            message={
                "response time": f"{get_elapsed_time_till_now_in_ms(start_time=start_time):.0f}ms",
                "token cost": token_cost,
                "query response": clean_llm_output(result.content),
            },
        )
    except Exception as e:
        logger.error(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while chatting with AI, please try again.",
        )
