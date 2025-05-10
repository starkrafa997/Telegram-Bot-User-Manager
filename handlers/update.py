from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu
from keyboards.cancel import cancel_button
from database.queries import update_user_age_by_id, user_exists_by_id, get_user_name_by_id
from states.user_states import UpdateUserState

router = Router()


# Обработка кнопки "✏️ Обновить возраст"
@router.message(F.text == '✏️ Обновить возраст')
async def update_button(message: Message, state: FSMContext):
    if not user_exists_by_id(message.from_user.id):
        await message.answer("❗ Ты ещё не зарегистрирован. Сначала /add.")
        return
    await message.answer("📅 Введи новый возраст:", reply_markup=cancel_button)
    await state.set_state(UpdateUserState.waiting_for_new_age)


# Обработка команды /update — обновление возраста
@router.message(Command('update'))
async def update_user(message: Message, state: FSMContext):
    if not user_exists_by_id(message.from_user.id):
        await message.answer(f"❗ Пользователь с именем {name} не найден.")
        return
    await message.answer("📅 Введи новый возраст:", reply_markup=cancel_button)
    await state.set_state(UpdateUserState.waiting_for_new_age)


# Получение нового возраста и обновление в базе
@router.message(UpdateUserState.waiting_for_new_age)
async def get_new_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Возраст должен быть числом. Попробуй снова.")
        return
    new_age = int(message.text)
    name = get_user_name_by_id(message.from_user.id)
    update_user_age_by_id(message.from_user.id, new_age)
    await message.answer(f"✅ Возраст пользователя {name} обновлён: {new_age} лет.", reply_markup=main_menu)
    await state.clear()
