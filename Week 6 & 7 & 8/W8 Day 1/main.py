import logging
import time
from decimal import Decimal
from os import getenv

from dotenv import load_dotenv
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_openai import ChatOpenAI

logger = logging.basicConfig(leve=logging.info)

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    message = "OPENAI_API_KEY not found in .env file"
    logger.error(message)
    raise ValueError(message)


# In memory caching -> uses RAM
# set_llm_cache(InMemoryCache())
# SQLite caching -> auto-creates and uses a sqlite db
set_llm_cache(SQLiteCache(database_path="langchain.db"))


def get_llm_response(query: str) -> str:
    agent = ChatOpenAI(
        api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0, cache=True
    )
    messages = [
        {
            "role": "system",
            "content": "You are a helpful ai assistant, answer mindfully",
        },
        {"role": "user", "content": query},
    ]
    response = agent.invoke(messages).content
    return response


def check_cache(query: str) -> bool:
    if query in cache:
        return True
    return False


def cache_if_new_query(query: str, response: str) -> None:
    global cache
    if query not in cache:
        cache[query] = response


def call_agent(cache_toggle: bool = False):
    input_prompt = input("Enter prompt: ")
    start = time.time()
    result = get_llm_response(query=input_prompt, cache_toggle=cache_toggle)
    end = time.time()
    logger.info(result)
    logger.info("above llm call took: ", Decimal(end - start))


if __name__ == "__main__":
    call_agent()
    call_agent()
