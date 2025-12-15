from fastapi import APIRouter, File, HTTPException, UploadFile, status
from langchain_core.messages import HumanMessage
from src.core.ai_utility import calculate_token_cost, get_agent
from src.core.constants import MESSAGES, AIModels, ResponseType, logger
from src.core.database import (
    add_file_as_embedding,
    get_formatted_ai_response,
    query_relavent_contents,
)
from src.schema.ai import Query

ai = APIRouter()


@ai.post("/ai/query")
async def query_response(query: Query):
    user_query = query.query
    MESSAGES.append(HumanMessage(content=user_query))

    ai_model: AIModels = AIModels.GPT_4o_MINI

    try:
        agent = get_agent(ai_model=ai_model)
        agent_response = agent.invoke(MESSAGES)

        ai_reply = agent_response.content
        token_cost = calculate_token_cost(
            agent_response.usage_metadata, ai_model=ai_model
        )

        return {
            "response": ResponseType.SUCCESS.value,
            "message": {"ai response": ai_reply, "token cost": token_cost},
        }
    except Exception as e:
        return {
            "response": ResponseType.ERROR.value,
            "message": f"{e}",
        }


@ai.post("/ai/db_query")
async def search_from_db(query: Query):
    try:
        query_result = query_relavent_contents(query=query)
        if query_result[0]:
            agent_response = get_formatted_ai_response(
                results=query_result[1],
                query=query,
                ai_model=get_agent(ai_model=AIModels.GPT_4o_MINI),
            )
            token_cost = calculate_token_cost(
                agent_response.usage_metadata, ai_model=AIModels.GPT_4o_MINI
            )
            return {
                "response": ResponseType.SUCCESS.value,
                "message": {
                    "token cost": token_cost,
                    "query response": agent_response.content,
                },
            }
        return {
            "response": ResponseType.ERROR.value,
            "message": {
                "query response": "cannot find results for your query",
            },
        }
    except Exception as e:
        message = f"Error {e}"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


@ai.post("/ai/upload_file")
async def upload_to_db(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        message = "Only supports pdf files"
        logger.error(message)
        return {
            "response": ResponseType.ERROR.value,
            "message": message,
        }

    try:
        contents = await file.read()
        file_add_response = add_file_as_embedding(
            contents=contents, filename=file.filename
        )
        return {
            "response": ResponseType.SUCCESS.value,
            "message": {
                "file response": file_add_response,
            },
        }
    except Exception as e:
        message = f"Error {e}"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
