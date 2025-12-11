from fastapi import APIRouter
from src.schema.ai import Query

ai = APIRouter()


@ai.post("/ai/query")
async def query_response(query: Query):
    user_query = query.query
    return {}
