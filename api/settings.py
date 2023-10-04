import os

# Comment this is production
from dotenv import load_dotenv
load_dotenv("../.env")

DATABASE_URL = os.environ.get('DATABASE_URL', '')
SECRET_KEY = os.environ.get('SECRET_KEY', '')
ALGORITHM = os.environ.get('ALGORITHM', '')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '')