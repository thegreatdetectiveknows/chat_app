import sys, os

# Добавляем папку с конфигурационным файлом в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем модуль с конфигурационными данными
from config.config_reader import config

# Импортируем библиотеку FastAPI для создания HTTP-сервера
from fastapi import FastAPI, Request

# Импортируем клиент для работы с MongoDB
from pymongo import MongoClient

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Создаем клиента MongoDB и подключаемся к базе данных
client = MongoClient(config.mongodb_uri)
db = client["chat_db"]
users_collection = db["users"]
message_collection = db["messages"]


@app.post("/store_message")
async def store_message(request: Request):
    """
    Обработчик POST-запросов на "/store_message".
    Принимает JSON-данные из запроса и сохраняет их в коллекции MongoDB.
    Возвращает JSON-ответ с статусом "success".
    """
    # Получаем JSON-данные из запроса
    data = await request.json()

    # Извлекаем данные из запроса
    user_id = data["userid"]
    platform = data["platform"]
    name = data["name"]
    nickname = data["nickname"]
    message_id = data["messageid"]
    message_text = data["message"]
    date = data["date"]
    sender = data["sender"]

    # Проверяем, существует ли пользователь
    user = users_collection.find_one({"userId": user_id})
    if not user:
        # Если пользователь не существует, добавляем его в коллекцию users
        users_collection.insert_one({
            "userId": user_id, # Идентификатор пользователя в платформе
            "platform": platform, # Telegram, VK, etc.
            "name": name, # Имя пользователя
            "nickname": nickname, # Никнейм пользователя
            "registeredAt": date, # Дата регистрации
            "lastMessageAt": date # Дата последнего сообщения
        })
    else:
        # Если пользователь существует, обновляем дату последнего сообщения
        users_collection.update_one(
            {"userId": user_id},
            {"$set": {"lastMessageAt": date}}
        )

    # Сохраняем сообщение в коллекции messages
    message_collection.insert_one({
        "messageId": message_id,
        "userId": user_id,
        "text": message_text,
        "sentAt": date,
        "sender": sender
    })

    # Возвращаем JSON-ответ с статусом "success"
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn

    # Запускаем приложение FastAPI на порту 8002 с перезагрузкой при изменении кода
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
