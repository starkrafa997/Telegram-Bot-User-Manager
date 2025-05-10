from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки основного меню
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='➕ Зарегистрироваться'), KeyboardButton(text='✏️ Обновить возраст')],
    [KeyboardButton(text='📋 Список пользователей'), KeyboardButton(text='❌ Удалить себя из базы')],
    [KeyboardButton(text='ℹ️ Помощь')]
],
    resize_keyboard=True,
)
