import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_reader import config


from fastapi import FastAPI, Request
from pymongo import MongoClient

app = FastAPI()
client = MongoClient(config.mongodb_uri)
db = client["message_db"]
collection = db["messages"]


@app.post("/store_message")
async def store_message(request: Request):
    data = await request.json()
    collection.insert_one(data)
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
