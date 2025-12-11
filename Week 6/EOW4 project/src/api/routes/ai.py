from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from src.core.ai_utility import calculate_token_cost, get_agent
from src.core.constants import MESSAGES, AIModels, ResponseType
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


@ai.post("/ai/pdf")
async def search_from_pdf(query: Query): ...
