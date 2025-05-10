import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu
from states.user_states import AddUserState, UpdateUserState

# Роутер для команды /start и кнопки Отмена
router = Router()


# Обработка команды /start — выводит приветствие и меню
@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    logging.info(f'/start от пользователя {message.from_user.id}')

    # Очистка состояния (если пользователь был в процессе чего-то)
    await state.clear()
    await message.answer(
        f'Привет, <b>{message.from_user.full_name}</b>! Выбери действие через кнопки 👇',
        parse_mode=ParseMode.HTML, reply_markup=main_menu)


# Обработка нажатия кнопки "❌ Отмена" в разных состояниях FSM
@router.message(UpdateUserState.waiting_for_new_age, F.text == "❌ Отмена")
@router.message(AddUserState.waiting_age, F.text == "❌ Отмена")
@router.message(AddUserState.waiting_name_1, F.text == "❌ Отмена")
async def cancel_handler(message: Message, state: FSMContext):
    # Проверяем активное состояние
    current_state = await state.get_state()
    if current_state:
        await state.clear()  # Сброс состояния
        await message.answer("🚫 Операция отменена. Возвращаемся в меню!", reply_markup=main_menu)
    else:
        await message.answer("❗ Не в каком-либо процессе, чтобы отменить.")
