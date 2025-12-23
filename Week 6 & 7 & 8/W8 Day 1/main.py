import time
from os import getenv

from dotenv import load_dotenv
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")


# Manual caching -> not efficient
cache = {}
# In memory caching -> uses RAM
# set_llm_cache(InMemoryCache())
# SQLite caching -> auto-creates and uses a sqlite db
set_llm_cache(SQLiteCache(database_path="langchain.db"))


def get_llm_response(query: str, cache_toggle: bool) -> str:
    # if cache_toggle and check_cache(query):
    #     return cache[query]

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
    # if cache_toggle:
    #     cache_if_new_query(query, response)
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
    print(result)
    print("above llm call took: ", end - start)


if __name__ == "__main__":
    call_agent()
    call_agent(cache_toggle=True)
    call_agent(cache_toggle=True)
