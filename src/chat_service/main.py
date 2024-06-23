'''
Chat Service

Взаимодействие с коллекцией chats в MongoDB.
'''

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import config
from config.models import Chat, ID_Date

from fastapi import FastAPI, HTTPException

from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# Настройка подключения к MongoDB
client = MongoClient(config.mongodb_uri)
db = client["chat_db"]
chats_collection = db["chats"]

app = FastAPI()


# Эндпоинт для создания нового чата
@app.post("/chats")
async def create_chat(chat: Chat):

    existing_user = chats_collection.find_one({"user_id": chat.user_id})

    if existing_user:
        raise HTTPException(status_code=400, detail="Чат уже существует")

    result = chats_collection.insert_one(chat.model_dump())
    return {"_id": str(result.inserted_id)}


# Эндпоинт для получения пользователя по _id из коллекции user
@app.get("/chats")
async def get_chat(user_id: str):
    chat = chats_collection.find_one({"user_id": user_id})

    if chat is None:
        raise HTTPException(status_code=404, detail="Чат не найден")

    chat["_id"] = str(chat["_id"])
    return chat


# Эндпоинт для обновления чата по id в теле запроса
@app.put("/chats")
async def update_chat(id_date: ID_Date):
    try:
        # Конвертация ID в ObjectId
        chat_id = ObjectId(id_date.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {e}")

    result = chats_collection.update_one(
        {"_id": chat_id}, {"$set": {"updated_at": id_date.date}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Чат не найден")
    return {"status": "Время чата обновлено"}


# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8004, reload=True)
