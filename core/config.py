import os
from functools import lru_cache

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')

load_dotenv()

# CREDENTIALS for EMAIL
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_TLS=True,
    MAIL_SSL=False,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER
)


class Settings(BaseSettings):
    database_async_url: str
    database_sync_url: str
    bot_token: str
    chat_id: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
