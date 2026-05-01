# E-commerce API

REST API для интернет-магазина с авторизацией, каталогом товаров и управлением заказами.

## Стек
- **FastAPI** — веб-фреймворк
- **PostgreSQL + SQLAlchemy** — база данных
- **Redis** — кэширование каталога
- **Celery** — фоновая отправка email
- **Docker** — контейнеризация
- **pytest** — тестирование

## Возможности
- JWT авторизация (регистрация, логин)
- Каталог товаров с кэшированием через Redis
- Создание и управление заказами
- Фоновая отправка email при создании заказа

## Запуск через Docker
```bash
docker-compose up --build
```

## Запуск локально
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Эндпоинты
| Метод | URL | Описание |
|-------|-----|----------|
| POST | /auth/register | Регистрация |
| POST | /auth/login | Авторизация |
| GET | /products | Каталог товаров |
| GET | /products/{id} | Товар по id |
| POST | /products | Создать товар |
| POST | /orders | Создать заказ |
| GET | /orders | Мои заказы |
| PATCH | /orders/{id}/status | Обновить статус |

## Тесты
```bash
pytest
```