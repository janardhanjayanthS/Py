from os import getenv

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")


response_model = init_chat_model("gpt-4o", temperature=0)
