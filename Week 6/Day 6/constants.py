from os import getenv

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
PG_PWD = getenv("POSTGRESQL_PWD")

connection = f"postgresql+psycopg://postgres:{PG_PWD}@localhost:5432/vector_db"
