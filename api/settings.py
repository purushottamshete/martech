import os

# Comment this is production
from dotenv import load_dotenv
load_dotenv("../.env")

DATABASE_URL = os.environ.get('DATABASE_URL', '')
SECRET_KEY = os.environ.get('SECRET_KEY', '')
ALGORITHM = os.environ.get('ALGORITHM', '')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '')
EMAIL_USERNAME=os.environ.get('EMAIL_USERNAME', '')
EMAIL_PASSWORD=os.environ.get('EMAIL_PASSWORD', '')
EMAIL_SERVER=os.environ.get('EMAIL_SERVER', '')
EMAIL_FROM=os.environ.get('EMAIL_FROM', '')
LOG_FILE=os.environ.get('LOG_FILE', '')