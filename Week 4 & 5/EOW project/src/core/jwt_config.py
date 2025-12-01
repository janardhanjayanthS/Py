from os import getenv
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
ALGORITHM = "SHA256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
