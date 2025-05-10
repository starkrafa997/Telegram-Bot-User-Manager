import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.queries import delete_user_by_id

router = Router()


# Обработка кнопки "❌ Удалить себя из базы"
@router.message(F.text == "❌ Удалить себя из базы")
async def delete_button(message: Message):
    await delete_user(message)


# Удаление пользователя из базы по команде /delete
@router.message(Command('delete'))
async def delete_user(message: Message):
    try:
        success = delete_user_by_id(message.from_user.id)
        if success:
            await message.answer("🗑️ Твои данные успешно удалены из базы.")
        else:
            await message.answer("❗ Ты ещё не зарегистрирован.")
    except Exception as e:
        logging.exception(f'Ошибка при удалении пользователя: {e}.')
        await message.answer("⚠️ Ошибка при удалении. Попробуй позже.")
