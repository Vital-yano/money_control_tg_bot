import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "fdfd573463dfh$#4")

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6381,
    "password": "redis_local",
    "decode_responses": True,
}


SEND_CODE_URL = "http://0.0.0.0:8000/user/send_code"
CREATE_USER_URL = "http://0.0.0.0:8000/user/create"
