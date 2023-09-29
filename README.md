# Тестовое фуллстек

## Приложение, состоящее из API, Telegram-бота и веб-приложения

### 1. API

Реализовано на FastAPI. БД - PostgreSQL, sqlalchemy 2.

### 2. Бот

Реализован на aiogram 3.

### 3. Веб-приложение

Реализовано на VueJS 3.

## Запуск

1. Переменные окружения

   ```shell
   cp .env.example .env
   ```
   В файле .env определить переменные, необходимые для подключения к БД, а также токен Telegram-бота, идентификаторы
   администраторов, перечисленные через запятую и URL API.

2. Локальный запуск приложения

   ```shell
   cd ./backend
   
   # Если используется poetry
   poetry shell
   poetry install
   # Если используется pip
   python -m venv venv
   ./venv/Scripts/activate
   pip install -r requirements.txt
   
   # Миграция БД
   alembic upgrade head
   
   # Далее через две вкладки терминала по одной команде
   uvicorn src.api.main:app --reload  # Запуск API
   python ./src/bot/main.py  # Запуск бота
   ```

   ```shell
   # Еще одна вкладка терминала
   cd ./frontend
   
   npm install
   npm run dev
   ```

3. Запуск приложения в Docker

   *TODO*