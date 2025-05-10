import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu
from keyboards.cancel import cancel_button
from database.queries import add_user, user_exists_by_id
from states.user_states import AddUserState

router = Router()


# Обработка кнопки "➕ Зарегистрироваться"
@router.message(F.text == '➕ Зарегистрироваться')
async def register_button(message: Message, state: FSMContext):
    await add_user_handler(message, state)


# Команда /add — регистрация пользователя
@router.message(Command("add"))
async def add_user_handler(message: Message, state: FSMContext):
    logging.info(f'Начало регистрации {message.from_user.id}')
    try:

        if user_exists_by_id(message.from_user.id):
            logging.warning(f'{message.from_user.id} зарегистрирован.')
            await message.answer(
                'Ты уже зарегистрирован! Используй кнопку "Обновить возраст" или команду /update, чтобы изменить данные.',
                reply_markup=main_menu)
            return

        await message.answer("👤 Введи своё имя", reply_markup=cancel_button)
        await state.set_state(AddUserState.waiting_name_1)

    except Exception as e:
        logging.exception(f'ошибка инициализации регистрации: {e}.')
        await message.answer("⚠️ Ошибка при начале регистрации. Попробуй позже.")

# Получаем имя пользователя и переходим к запросу возраста
@router.message(AddUserState.waiting_name_1)
async def get_name_1(message: Message, state: FSMContext):
    name = message.text
    logging.debug(f'{message.from_user.id} ввёл имя {name}')
    await state.update_data(name=message.text.strip())
    await message.answer("📅 Введи свой возраст:", reply_markup=cancel_button)
    await state.set_state(AddUserState.waiting_age)


# Получаем возраст, проверяем, добавляем в базу
@router.message(AddUserState.waiting_age)
async def get_age(message: Message, state: FSMContext):
    age_input = message.text
    logging.debug(f'{message.from_user.id} ввёл возраст: {age_input}')
    try:
        if not message.text.isdigit():
            logging.warning(f'{message.from_user.id} ввёл нечисловой возраст {age_input}')
            await message.answer("❗ Возраст должен быть числом. Попробуй снова.")
            return

        age = int(message.text)
        if not (5 <= age <= 120):
            await message.answer("❗ Возраст должен быть от 5 до 120 лет. Попробуй снова.")
            return

        data = await state.get_data()
        name = data.get("name")
        add_user(message.from_user.id, name, age)
        await message.answer(f'✅ Пользователь {name}, {age} лет добавлен.', reply_markup=main_menu)
        logging.info(f'Пользователь {message.from_user.id} зарегистрирован.')
        await state.clear()

    except Exception as e:
        logging.exception(f"Ошибка при регистрации: {e}")
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуй снова.")