"""
Bot Gateway Service
    
Взаимодействует с ботами Telegram и VK.
Получает сообщения от пользователей через ботов и пересылает их в Message Service.
Отправляет сообщения ботам через их API.

TODO: самого вк бота и его интеграцию в send_message_to_user
"""

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import config

from fastapi import FastAPI, Request
import aiohttp
import logging

from config.models import MessageFromBot, MessageToBot


TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.telegram_bot_token.get_secret_value()}/sendMessage"
VK_API_URL = "https://api.vk.com/method/messages.send"

# Настройка логгера
logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/bot/message")
async def receive_message_from_bot(message: MessageFromBot):
    """
    Обработчик, который принимает сообщения от пользователей через ботов,
    и пересылает их в микросервис Message Service.
    Принимает на вход объект MessageFromBot.
    """

    logging.info(message.model_dump())

    # Адрес Message Service
    url = "http://localhost:8002/messages/from_user"

    # Отправка POST-запроса с данными в микросервис
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=message.model_dump()) as resp:
            await resp.text()  # Выполняем запрос и читаем ответ для завершения запроса

    return {"status": "ok"}


@app.post("/bot/send")
async def send_message_to_user(message: MessageToBot):
    """
    Метод отправляет сообщение пользователю через Telegram API.
    Принимает на вход объект MessageToBot, содержащий идентификатор пользователя и текст сообщения.
    Отправляет POST-запрос с данными в Telegram API, полученные из объекта MessageToBot.
    Возвращает статус отправки сообщения.
    """

    # Подготовка требуемых телеграмом данных для отправки
    data = {"chat_id": message.userid, "text": message.text}

    # URL апи телеграма
    url = TELEGRAM_API_URL

    # Отправка POST-запроса в телеграм апи для отправки сообщения в бот
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            await resp.text()  # Выполняем запрос и читаем ответ для завершения запроса
    return {"status": "message sent"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
