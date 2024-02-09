from datetime import UTC, datetime

from dependency_injector.wiring import Provide, inject
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.api_requests import _create_user, _send_code
from src.container import RedisContainer
from src.dal import UserRedisDAL
from src.keyboards import (
    reply_markup_contact_keyboard,
)

PHONE_NUMBER, VERIFICATION_CODE = range(2)

VERIFICATION_CODE_PATTERN = "^\\d{4}$"


@inject
async def register(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    redis_service: UserRedisDAL = Provide[RedisContainer.redis_user_dal],
):
    # Проверки update.message и подобные нужны, чтобы не ругался pyright
    if update.message and update.message.from_user:
        user_tg_id = str(update.message.from_user.id)
        await redis_service.add_fields_to_user_data(
            tg_id=user_tg_id,
            user_data={
                "tg_id": user_tg_id,
                "tg_nickname": f"{update.message.from_user.username}",
            },
        )
        await update.message.reply_text(
            "Для регистрации нужен ваш номер телефона",
            reply_markup=reply_markup_contact_keyboard,
        )

    return PHONE_NUMBER


@inject
async def store_phone_number_and_nickname(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    redis_service: UserRedisDAL = Provide[RedisContainer.redis_user_dal],
) -> int:
    if update.message and update.message.contact and update.message.from_user:
        user_tg_id = str(update.message.from_user.id)
        redis_user = await redis_service.add_fields_to_user_data(
            tg_id=user_tg_id,
            user_data={"phone_number": f"+{update.message.contact.phone_number}"},
        )
        response = await _send_code(redis_user)
        if response["status_code"] == 200:
            await update.message.reply_text(
                "Введите последние 4 цифры номера",
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            await update.message.reply_text(
                f"Произошла ошибка: {response['detail']}. Попробуйте повторить регистрацию",
                reply_markup=ReplyKeyboardRemove(),
            )

    return VERIFICATION_CODE


@inject
async def check_verification_code(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    redis_service: UserRedisDAL = Provide[RedisContainer.redis_user_dal],
):
    if update.message and update.message.from_user and update.message.text:
        user_tg_id = str(update.message.from_user.id)
        redis_user = await redis_service.add_fields_to_user_data(
            tg_id=user_tg_id,
            user_data={
                "verification_code": update.message.text,
                "registration_time": datetime.strftime(
                    datetime.now(UTC), "%Y-%m-%d %H:%M:%S"
                ),
            },
        )
        response = await _create_user(redis_user)
        if response["status_code"] == 201:
            await update.message.reply_text(
                "Вы были зарегистрированы", reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text(
                f"Произошла ошибка: {response['detail']}. Попробуйте повторить регистрацию",
                reply_markup=ReplyKeyboardRemove(),
            )
        await redis_service.clean_redis(user_tg_id)
    return ConversationHandler.END


async def check_incorrect_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Вы ввели некорректный код. Попробуйте ввести еще раз"
        )

    return VERIFICATION_CODE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Регистрация была прервана!",
            reply_markup=ReplyKeyboardRemove(),
        )

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register)],
    states={
        PHONE_NUMBER: [
            MessageHandler(filters.CONTACT, store_phone_number_and_nickname)
        ],
        VERIFICATION_CODE: [
            MessageHandler(
                filters.Regex(VERIFICATION_CODE_PATTERN), check_verification_code
            ),
            MessageHandler(
                ~(filters.Regex(VERIFICATION_CODE_PATTERN))
                & ~(filters.Regex("^\\/cancel$")),
                check_incorrect_data,
            ),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
