import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_reader import config

from fastapi import FastAPI, Request
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

@app.post("/route_message")
async def route_message(request: Request):
    """
    Обработчик POST-запросов на "/route_message".
    Принимает JSON-данные из запроса и перенаправляет их в микросервис на порту 8002.
    Возвращает JSON-ответ с статусом "success".
    """
    # Получение JSON-данных из запроса
    data = await request.json()

    # URL микросервиса для обработки сообщений
    url = config.storage_message_uri

    # Отправка POST-запроса с данными в микросервис
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
                await resp.text()  # Выполняем запрос и читаем ответ для завершения запроса

    # Возвращение ответа с успешным статусом
    return {"status": "success"}


# Запуск приложения FastAPI на порту 8001 с перезагрузкой при изменении кода
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
