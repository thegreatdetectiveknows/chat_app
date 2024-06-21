import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_reader import config

from aiogram import Bot, Dispatcher, types
import asyncio
import logging
import aiohttp
from aiogram.filters.command import Command


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.telegram_bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}!")


@dp.message()
async def handle_message(message: types.Message):
    data = {
        "userid": message.from_user.id,
        "platform": "Telegram",
        "name": message.from_user.full_name,
        "nickname": message.from_user.username,
        "message": message.text,
        "date": message.date.isoformat(),
    }

    url = "http://localhost:8001/route_message"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status == 200:
                logging.info(
                    f"Сообщение успешно отправлено: {resp.status} - {await resp.text()}"
                )
                await message.reply("Сообщение успешно отправлено")
            else:
                logging.error(
                    f"Ошибка при отправке сообщения: {resp.status} - {await resp.text()}"
                )
                await message.reply("Ошибка при отправке сообщения")


# Основной процесс бота
async def main():
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")


# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
