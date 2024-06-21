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
db = client["message_db"]
collection = db["messages"]


@app.post("/store_message")
async def store_message(request: Request):
    """
    Обработчик POST-запросов на "/store_message".
    Принимает JSON-данные из запроса и сохраняет их в коллекции MongoDB.
    Возвращает JSON-ответ с статусом "success".
    """
    # Получаем JSON-данные из запроса
    data = await request.json()

    # Сохраняем данные в коллекции MongoDB
    collection.insert_one(data)

    # Возвращаем JSON-ответ с статусом "success"
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn

    # Запускаем приложение FastAPI на порту 8002 с перезагрузкой при изменении кода
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
