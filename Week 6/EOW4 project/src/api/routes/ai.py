from fastapi import APIRouter

ai = APIRouter()


ai.post("/ai/query")


async def query_response():
    return {}
