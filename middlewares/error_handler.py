from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError
import logging


class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except TelegramAPIError as e:
            logging.error(f'Ошибка Telegram API:{e}')
            if isinstance(event, Message):
                await event.answer("⚠️ Ошибка Telegram. Попробуйте позже.")

        except Exception as e:
            logging.exception('Необработанная ошибка.')
            if isinstance(event, Message):
                await event.answer("⚠️ Что-то пошло не так. Мы уже разбираемся!")

