from fastapi import APIRouter, HTTPException, status
from src.core.ai_utility import (
    calculate_token_cost,
    clean_llm_output,
    get_conversational_rag_chain,
    update_history,
)
from src.core.constants import HISTORY, AIModels, ResponseType, logger
from src.schema.ai import Query

chat = APIRouter()


@chat.post("/chat")
async def search_from_db(query: Query):
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
    try:
        result = get_conversational_rag_chain().invoke(
            {"question": query.query, "chat_history": HISTORY}
        )
        update_history(result=result, query=query)
        token_cost = calculate_token_cost(
            result.usage_metadata, ai_model=AIModels.GPT_4o_MINI
        )

        return {
            "response": ResponseType.SUCCESS.value,
            "message": {
                "token cost": token_cost,
                "query response": clean_llm_output(result.content),
            },
        }
    except Exception as e:
        logger.error(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while chatting with AI, please try again.",
        )
