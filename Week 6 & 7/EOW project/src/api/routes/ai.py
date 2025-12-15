from fastapi import APIRouter, File, HTTPException, UploadFile, status
from langchain_core.messages import HumanMessage
from src.core.ai_utility import (
    calculate_token_cost,
    clean_llm_output,
    get_agent,
    get_conversational_rag_chain,
    update_history,
)
from src.core.constants import HISTORY, MESSAGES, AIModels, ResponseType, logger
from src.core.database import (
    add_file_as_embedding,
    add_web_content_as_embedding,
)
from src.schema.ai import BlogLink, Query

ai = APIRouter()


@ai.post("/ai/query")
async def query_response(query: Query):
    MESSAGES.append(HumanMessage(content=query.query))

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
        message = f"Error {e}"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


@ai.post("/ai/upload_file")
async def upload_pdf_to_db(file: UploadFile = File(...)):
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
                "db response": file_add_response,
            },
        }
    except Exception as e:
        message = f"Error {e}"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


@ai.post("/ai/upload_blog")
async def upload_blog_to_db(blog_url: BlogLink):
    try:
        web_upload_result = add_web_content_as_embedding(url=str(blog_url.url))
        return {
            "response": ResponseType.SUCCESS.value,
            "message": {
                "db response": web_upload_result,
            },
        }
    except Exception as e:
        message = f"Error {e}"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
