from os import getenv

from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = getenv("OPENAI_API_KEY")
DELIMITER = "####"
