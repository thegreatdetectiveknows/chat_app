# Чат-приложение с использованием FastAPI и Vue.js

Этот проект представляет собой простое чат-приложение, построенное с использованием FastAPI для бэкенда и Vue.js для фронтенда. Приложение позволяет пользователям отправлять сообщения через веб-интерфейс и отображать их в окне чата.


### Установка проекта

1. Клонируйте репозиторий и перейдите в папку.
```
git clone https://github.com/thegreatdetectiveknows/fastapi-vuejs-app.git
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
```
5. __В процессе разработки__

### Важно!
Если в ходе разработки появились новые модули, нужно обновить requirements.txt: 
```
pip freeze > requirements.txt
```
# текущая реализация
Осталось реализовать фронтенд.
![текущая реализация](image.png)