import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command

# Создаём роутер для модуля help
router = Router()


@router.message(F.text == 'ℹ️ Помощь')
async def help_button(message: Message):
    await help_command(message)


# Обработчик команды /help
@router.message(Command("help"))
async def help_command(message: Message):
    """
    Отвечает на команду /help.
    Показывает список доступных команд и их краткое описание.
    """
    logging.info(f'/help от пользователя {message.from_user.id}')
    await message.answer(
        "🛠 <b>Помощь</b>\n\n"
        "Этот бот умеет:\n"
        "➕ Зарегистрировать тебя\n"
        "✏️ Обновить возраст\n"
        "📋 Показать список пользователей\n"
        "❌ Удалить себя из базы\n\n"
        "🧭 Доступные команды:\n"
        "/start – главное меню\n"
        "/add – регистрация\n"
        "/update – обновить возраст\n"
        "/list – список пользователей\n"
        "/delete – удалить себя\n"
        "/cancel – отменить действие\n"
        "/help – помощь",
        parse_mode=ParseMode.HTML  # Используем HTML-разметку для форматирования
    )
