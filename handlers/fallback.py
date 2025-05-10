import logging

from aiogram import Router
from aiogram.types import Message

router = Router()


# Если пользователь отправил сообщение.
@router.message()
async def fallback_handler(message: Message):
    logging.info(f'Нераспознанная сообщение от {message.from_user.id}: {message.text}.')
    await message.answer("❗ Я тебя не понял. Выбери пункт из меню или нажми /start, чтобы начать заново. ")
