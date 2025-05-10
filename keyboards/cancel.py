from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопка отмены действия
cancel_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='❌ Отмена')]
],
    resize_keyboard=True,
    one_time_keyboard=True
)
