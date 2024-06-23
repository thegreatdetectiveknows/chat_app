"""
Message Service

Принимает сообщение с Bot Integration Service.
Взаимодействует с User Service и Chat Service.
Сохраняет сообщение в коллекции messages в MongoDB.

TODO: реализовать принятие сообщений с веб
"""

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import config
from config.models import MessageFromBot, User, Chat, Message, ID_Date, AdminMessage, MessageToBot

from fastapi import FastAPI, HTTPException
from datetime import datetime
from pymongo import MongoClient
import aiohttp
import logging

from fastapi.middleware.cors import CORSMiddleware

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Создание приложения FastAPI
app = FastAPI()

# Настройка middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

client = MongoClient(config.mongodb_uri)
db = client["chat_db"]
messages_collection = db["messages"]


async def get_user_id_from_db(message: MessageFromBot):
    async with aiohttp.ClientSession() as session:
        # Получание _id пользователя, путем обращения в микросервис пользователей
        user_url = f"http://localhost:8003/users?user_id={message.userid}&platform={message.platform}"
        async with session.get(user_url) as resp:
            # Если пользователь не существует
            if resp.status == 404:
                # Создание нового пользователя
                user_data = User(
                    user_id=message.userid,
                    platform=message.platform,
                    name=message.name,
                    nickname=message.nickname,
                    registeredAt=message.date,
                )
                async with session.post(
                    "http://localhost:8003/users/", json=user_data.model_dump()
                ) as create_resp:
                    if create_resp.status != 200:
                        raise HTTPException(
                            status_code=create_resp.status,
                            detail="Ошибка при создании пользователя",
                        )
                    create_resp_json = await create_resp.json()
                    user_id = create_resp_json["_id"]

            # Если пользователь существует
            else:
                user = await resp.json()
                user_id = user["_id"]
    return user_id


async def get_chat_id_from_db(data: ID_Date):
    async with aiohttp.ClientSession() as session:
        # Проверка существования чата
        chat_url = f"http://localhost:8004/chats?user_id={data.id}"
        async with session.get(chat_url) as chat_resp:
            if chat_resp.status == 404:
                # Создание нового чата
                chat_data = Chat(
                    user_id=data.id,
                    # admin_id": "default_admin",  # Замените на фактический ID администратора
                    created_at=data.date,
                    updated_at=data.date,
                )
                async with session.post(
                    "http://localhost:8004/chats", json=chat_data.model_dump()
                ) as create_chat_resp:
                    if create_chat_resp.status != 200:
                        raise HTTPException(
                            status_code=create_chat_resp.status,
                            detail="Ошибка при создании чата",
                        )
                    create_chat_resp_json = await create_chat_resp.json()
                    chat_id = create_chat_resp_json["_id"]
            else:
                chat = await chat_resp.json()
                chat_id = chat["_id"]

    return chat_id


async def update_chat(data: ID_Date):
    async with aiohttp.ClientSession() as session:
        chat_url = f"http://localhost:8004/chats"
        async with session.put(chat_url, json=data.model_dump()) as chat_resp:
            if chat_resp.status != 200:
                raise HTTPException(
                    status_code=chat_resp.status, detail="Ошибка при обновлении чата"
                )


async def get_user_id_from_chat_id(chat_id: str):
    async with aiohttp.ClientSession() as session:
        # Получение _id пользователя по _id чата из Chat Service
        chat_url = f"http://localhost:8004/chats/{chat_id}"
        async with session.get(chat_url) as chat_resp:
            if chat_resp.status == 404:
                raise HTTPException(status_code=404, detail="Chat not found")
            chat = await chat_resp.json()
            user_id = chat["user_id"]
            
            # Получение user_id пользователя на платформе из User Service
            user_url = f"http://localhost:8003/users/{user_id}"
            async with session.get(user_url) as user_resp:
                if user_resp.status == 404:
                    raise HTTPException(status_code=404, detail="User not found")
                user = await user_resp.json()
                platform_user_id = user["user_id"]

    return platform_user_id

@app.get("/messages")
async def get_messages():
    messages = list(messages_collection.find())
    for message in messages:
        message["_id"] = str(message["_id"])
    return messages

@app.post("/messages/from_user")
async def receive_message(message: MessageFromBot):

    user_id = await get_user_id_from_db(message)
    logging.info("_id from user: " + user_id)

    chat_id = await get_chat_id_from_db(ID_Date(id=user_id, date=message.date))
    logging.info("_id from chat: " + chat_id)

    # Сохраняем сообщение в MongoDB
    message_data = Message(
        chat_id=chat_id,
        sender_id=user_id,
        message_text=message.message,
        date=message.date,
    )

    result = messages_collection.insert_one(message_data.model_dump())

    # Обновление даты последнего сообщения в чате
    await update_chat(ID_Date(id=chat_id, date=message.date))

    # Уведомление пользователя через Bot Gateway Service,
    # что сообщение сохранено в базе данных, и вот его _id
    return {"_id": str(result.inserted_id)}


### РЕАЛИЗУЙ ЭТО!
@app.post("/messages/from_admin")
async def receive_message_from_admin(message: AdminMessage):
    message_data = Message(
        chat_id = message.chat_id,
        sender_id = "default_admin123",
        message_text = message.message_text,
        date = message.date,
    )
    result = messages_collection.insert_one(message_data.model_dump())

    # Обновление даты последнего сообщения в чате
    await update_chat(ID_Date(id=message.chat_id, date=message.date))

    # Уведомление пользователя через Bot Gateway Service
    async with aiohttp.ClientSession() as session:
        
        
        user_message_data = MessageToBot(
            userid = await get_user_id_from_chat_id(message.chat_id),  # Здесь должно быть user id платформы
            text = message.message_text
        )
        
        await session.post("http://localhost:8001/bot/send", json=user_message_data.model_dump())

    return {"_id": str(result.inserted_id)}


# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
