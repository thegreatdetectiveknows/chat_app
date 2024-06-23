### Установка проекта

1. Клонируйте репозиторий и перейдите в папку.
```
git clone https://github.com/thegreatdetectiveknows/adam-app.git
cd adam-app
```
2. Создайте виртуальное окружение python и активируйте его (либо VSCode сам предложит включить виртуальное окружение):
```
python -m venv venv
venv/bin/activate
```
3. Установите модули: 
```
pip install -r requirements.txt
```
4. Создайте файл .env в папке src/config и заполните его:
```
TELEGRAM_BOT_TOKEN=YOURDATA
MONGODB_URI=YOURDATA
VK_BOT_TOKEN=YOURDATA
ROUTE_MESSAGE_URI=http://localhost:8001/route_message
STORAGE_MESSAGE_URI=http://localhost:8002/storage_message
```
5. __В процессе разработки__

### Важно!
Если в ходе разработки появились новые модули, нужно обновить requirements.txt: 
```
pip freeze > requirements.txt
```
