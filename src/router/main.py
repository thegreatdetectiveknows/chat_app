from fastapi import FastAPI, Request
import aiohttp
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Создание приложения FastAPI
app = FastAPI()


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
    url = "http://localhost:8002/store_message"

    # Отправка POST-запроса с данными в микросервис
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status == 200:
                # Логирование успешного перенаправления
                logging.info(
                    f"Сообщение было перенаправлено в микросервис {url}: {resp.status} - {await resp.text()}"
                )
            else:
                # Логирование ошибки перенаправления
                logging.error(
                    f"Ошибка при перенаправлении сообщения в микросервис {url}: {resp.status} - {await resp.text()}"
                )

    # Возвращение ответа с успешным статусом
    return {"status": "success"}


# Запуск приложения FastAPI на порту 8001 с перезагрузкой при изменении кода
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
