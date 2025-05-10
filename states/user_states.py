from aiogram.fsm.state import State, StatesGroup


# Состояния для FSM при добавлении пользователя
class AddUserState(StatesGroup):
    waiting_name_1 = State()  # Ожидается ввод имени
    waiting_age = State()  # Ожидается ввод возраста


# Состояния для FSM при обновлении возраста
class UpdateUserState(StatesGroup):
    waiting_for_new_age = State()  # Ожидается ввод нового возраста
