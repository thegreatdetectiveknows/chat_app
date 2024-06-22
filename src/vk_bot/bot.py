import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import config

import asyncio

import aiohttp
import vk_api
import logging
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime

# Импортируйте ваш модуль config_reader для чтения конфигурационных данных


logging.basicConfig(level=logging.INFO)

# Авторизация в VK
vk_session = vk_api.VkApi(token=config.vk_bot_token.get_secret_value())
session_api = vk_session.get_api()
# Инициализация LongPoll
longpoll = VkLongPoll(vk_session)

last_message = {}

async def handle_message(event):
    
    """
    Обработчик сообщений VK.
    Отправляет полученное сообщение в микросервис по маршрутизации сообщений.
    При успешной отправке отправляет уведомление пользователю в VK.
    При ошибке отправки сообщения в микросервис отправляет уведомление об ошибке пользователю в VK.
    """

    # Проверяем, что полученное событие является сообщением от пользователя и не является системным 
    if event.type == VkEventType.MESSAGE_NEW and event.from_user:
        # Получаем данные о сообщении
        user_id = event.user_id
        message_text = event.text

        # Получаем последнее отправленное сообщение пользователя
        last_sent_message = last_message.get(user_id)

        # Проверяем, было ли отправлено последнее сообщение и совпадает ли оно с текущим
        if last_sent_message and last_sent_message == message_text:
            return  # Если совпадает, игнорируем это сообщение
        
        # Проверяем, что сообщение не является системным
        if event.random_id == 0:
            return
        
        # Получаем данные о пользователе
        user_info = session_api.users.get(user_ids=user_id, fields="screen_name")
        username = user_info[0].get("screen_name", None)
        user_get = session_api.users.get(user_ids=user_id)[0]
        name = f"{user_get['first_name']} {user_get['last_name']}"
        message_id = event.message_id 
        # Ваша обработка сообщения здесь
        logging.info(f"Пользователь {user_id} отправил сообщение с message_id {message_id}: {message_text}")

        # Подготовка данных для отправки
        data = {
            "userid": user_id,
            "platform": "vk",
            "name": name,
            "nickname": username,
            "messageid": message_id,
            "message": message_text,
            "date": datetime.fromtimestamp(event.timestamp).isoformat(),
        }

        # Адрес микросервиса по маршрутизации сообщений
        url = "http://localhost:8001/route_message"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=data) as resp:
                    if resp.status == 200:
                        logging.info(f"Сообщение успешно отправлено: {resp.status} - {await resp.text()}")
                        # Обновляем последнее отправленное сообщение пользователя
                        last_message[user_id] = message_text
                        # Отправляем ответное сообщение в VK
                        session_api.messages.send(
                            user_id=user_id,
                            message="Сообщение успешно отправлено",
                            random_id=0,
                        )
                    else:
                        logging.error(f"Ошибка при отправке сообщения: {resp.status} - {await resp.text()}")
                        # Отправляем сообщение об ошибке в VK
                        session_api.messages.send(
                            user_id=user_id,
                            message="Ошибка при отправке сообщения",
                            random_id=0,
                        )
            except aiohttp.ClientError as e:
                logging.error(f"Исключение при отправке сообщения: {e}")
                session_api.messages.send(
                    user_id=user_id,
                    message="Ошибка соединения с сервером",
                    random_id=event.random_id,
                )

# Основной процесс обработки событий VK
async def main():
    logging.info("Бот запущен!")
    try:
        for event in longpoll.listen():
            await handle_message(event)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")

# Запуск основного процесса
if __name__ == "__main__":
    asyncio.run(main())
