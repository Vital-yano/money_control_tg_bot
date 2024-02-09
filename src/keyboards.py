from telegram import KeyboardButton, ReplyKeyboardMarkup

contact_keyboard = [[KeyboardButton(text="поделиться", request_contact=True)]]
reply_markup_contact_keyboard = ReplyKeyboardMarkup(
    contact_keyboard, resize_keyboard=True, one_time_keyboard=True
)
