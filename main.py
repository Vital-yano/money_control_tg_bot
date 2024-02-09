from telegram import Update
from telegram.ext import ApplicationBuilder

from config import BOT_TOKEN
from src.container import RedisContainer
from src.handlers import conv_handler
from src.logging_setup import configure_logging


if __name__ == "__main__":
    configure_logging()
    redis_container = RedisContainer()
    redis_container.init_resources()
    redis_container.wire(modules=["src.handlers"])
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
