# Backend HR-service dev

## Настройка
Установка виртуального окружения и зависимостей
```shell
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

## Миграции
```shell
alembic init -t async alembic

alembic revision --autogenerate -m "Create test base table"  

alembic upgrade head
```

## Запуск проекта
```shell
uvicorn src.main:app --reload --host localhost --port 80
```
