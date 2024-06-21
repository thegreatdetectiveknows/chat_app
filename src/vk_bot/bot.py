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

response_sent = False


async def handle_message(event):

    if event.type == VkEventType.MESSAGE_NEW and event.from_user:
        user_id = event.user_id
        message_text = event.text

        # Проверяем, был ли уже отправлен ответ на это сообщение
        if response_sent:
            logging.info(
                f"Ответ на сообщение от пользователя {user_id} уже был отправлен, пропускаем..."
            )
            return

        try:
            user_info = session_api.users.get(user_ids=user_id, fields="screen_name")
            username = user_info[0].get("screen_name", None)
        except Exception as e:
            logging.error(
                f"Ошибка получения информации о пользователе {user_id}: {str(e)}"
            )
            username = None
        user_get = session_api.users.get(user_ids=user_id)
        user_get = user_get[0]
        name = user_get["first_name"] + user_get["last_name"]

        data = {
            "userid": user_id,
            "platform": "VK",
            "name": name,
            "nickname": username,
            "message": message_text,
            "date": datetime.fromtimestamp(event.timestamp).isoformat(),
        }

        url = "http://localhost:8001/route_message"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                if resp.status == 200:
                    logging.info(
                        f"Сообщение успешно отправлено: {resp.status} - {await resp.text()}"
                    )
                    # Отправляем ответное сообщение в VK
                    session_api.messages.send(
                        user_id=user_id,
                        message="Сообщение успешно отправлено",
                        random_id=0,
                    )
                else:
                    logging.error(
                        f"Ошибка при отправке сообщения: {resp.status} - {await resp.text()}"
                    )
                    # Отправляем сообщение об ошибке в VK
                    session_api.messages.send(
                        user_id=user_id,
                        message="Ошибка при отправке сообщения",
                        random_id=0,
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
