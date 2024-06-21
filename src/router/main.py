from fastapi import FastAPI, Request
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/route_message")
async def route_message(request: Request):
    data = await request.json()

    url = "http://localhost:8002/store_message"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status == 200:
                logging.info(f"Сообщение было перенаправлено в микросервис {url}: {resp.status} - {await resp.text()}")
            else:
                logging.error(f"Ошибка при перенаправлении сообщения в микросервис {url}: {resp.status} - {await resp.text()}")
    
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

