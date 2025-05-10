import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from database.queries import get_all_users

router = Router()


# Обработка кнопки "📋 Список пользователей"
@router.message(F.text == "📋 Список пользователей")
async def list_button(message: Message):
    await list_users(message)


# Команда /list — показ всех пользователей из базы
@router.message(Command('list'))
async def list_users(message: Message):
    try:
        users = get_all_users()
        if not users:
            await message.answer('Пока в базе нет никого.')
        else:
            text = '\n'.join([f"👤 {name}, {age} лет" for name, age in users])
            await message.answer(f'<b>Список пользователей:</b>\n{text}', parse_mode=ParseMode.HTML)

    except Exception as e:
        logging.exception(f'Ошибка при получении списка пользователей: {e}.')
        await message.answer("⚠️ Не удалось получить список пользователей. Попробуй позже.")