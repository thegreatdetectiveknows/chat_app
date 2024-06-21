import sys, os

# Добавляем папку с конфигурационным файлом в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем модуль с конфигурационными данными
from config.config_reader import config

# Импортируем библиотеку для работы с Telegram API
from aiogram import Bot, Dispatcher, types
import asyncio
import logging
import aiohttp
from aiogram.filters.command import Command


# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота
bot = Bot(token=config.telegram_bot_token.get_secret_value())

# Создание диспетчера
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    # Отправка приветственного сообщения
    await message.answer(f"Привет {message.from_user.full_name}!")


# Обработчик обычного сообщения
@dp.message()
async def handle_message(message: types.Message):
    # Подготовка данных для отправки
    data = {
        "userid": message.from_user.id,
        "platform": "Telegram",
        "name": message.from_user.full_name,
        "nickname": message.from_user.username,
        "message": message.text,
        "date": message.date.isoformat(),
    }

    # Адрес микросервиса по маршрутизации сообщений
    url = "http://localhost:8001/route_message"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status == 200:
                logging.info(
                    f"Сообщение успешно отправлено: {resp.status} - {await resp.text()}"
                )
                # Отправка уведомления пользователю
                await message.reply("Сообщение успешно отправлено")
            else:
                logging.error(
                    f"Ошибка при отправке сообщения: {resp.status} - {await resp.text()}"
                )
                # Отправка уведомления пользователю об ошибке
                await message.reply("Ошибка при отправке сообщения")


# Основной процесс бота
async def main():
    try:
        # Запуск диспетчера
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        # Логирование остановки бота
        logging.info("Бот остановлен!")


# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
