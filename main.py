import asyncio
import config
import logging

from database.queries import init_db
from aiogram import Bot, Dispatcher
from handlers import start, register, update, delete, list_users, fallback, help
from middlewares.error_handler import ErrorMiddleware

# настройка логирования
error_handler = logging.FileHandler("errors.log", encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))

info_handler = logging.FileHandler("app.log", encoding="utf-8")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
))


# Создаём экземпляр бота с токеном из конфига
bot = Bot(token=config.BOT_TOKEN)
# Создаём диспетчер для обработки сообщений
dp = Dispatcher()


# Главная асинхронная функция запуска бота
async def main():
    # Подключаем все роутеры
    dp.include_router(start.router)
    dp.include_router(register.router)
    dp.include_router(update.router)
    dp.include_router(delete.router)
    dp.include_router(list_users.router)
    dp.include_router(help.router)
    dp.include_router(fallback.router)
    dp.message.middleware(ErrorMiddleware())

    # Инициализация базы данных (создание таблицы, если её нет)
    init_db()

    # Удаляем все ожидающие обновления (если бот перезапущен)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info('Бот запущен')
    # Запускаем цикл обработки апдейтов
    await dp.start_polling(bot)


# Запуск скрипта
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        handlers=[error_handler, info_handler, console_handler]
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Остановка бота пользователем')
        print('\nВыход')
