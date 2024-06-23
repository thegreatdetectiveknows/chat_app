'''
User Service

Взаимодействие с коллекцией users в MongoDB.
'''

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import config
from config.models import User

from fastapi import FastAPI, HTTPException

from datetime import datetime
from pymongo import MongoClient


# Настройка подключения к MongoDB
client = MongoClient(config.mongodb_uri)
db = client["chat_db"]
users_collection = db["users"]

app = FastAPI()


# Эндпоинт для создания нового пользователя
@app.post("/users")
async def create_user(user: User):

    existing_user = users_collection.find_one(
        {"user_id": user.user_id, "platform": user.platform}
    )

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    result = users_collection.insert_one(user.model_dump())
    return {"_id": str(result.inserted_id)}


# Эндпоинт для получения пользователя по user_platform_id и platform
@app.get("/users")
async def get_user(user_id: int, platform: str):

    user = users_collection.find_one({"user_id": user_id, "platform": platform})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    return user


# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)
