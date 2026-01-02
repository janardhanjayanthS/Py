import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from mangum import Mangum

from src.loader import get_openai_key
from src.log import logger

load_dotenv()


app = FastAPI()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=get_openai_key(), temperature=0.5)


@app.post("/ai/{user_query:path}")
async def chat_with_ai(user_query: str):
    logger.info("ACCESSED THE 1&1ly route!")
    messages = [
        {"role": "system", "content": "you are a fun ai assistant"},
        {"role": "user", "content": user_query},
    ]
    response = await llm.ainvoke(messages)
    return {"response": response.content}


lambda_handler = Mangum(app, lifespan="off")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3015, reload=True)
