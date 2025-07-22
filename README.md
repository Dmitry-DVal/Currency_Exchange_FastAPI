# Обмен валюты на FastAPI

### Описание
Веб-приложение (REST API) для управления валютами и обменными курсами.
Позволяет:
- добавлять, редактировать и просматривать валюты;
- добавлять, редактировать и просматривать курсы обмена (в том числе прямые, обратные и кросс-курсы);
- рассчитывать конвертацию произвольной суммы из одной валюты в другую.
[Деплой приложения(доступен временно)](http://217.114.15.7:8801/)

[📄 Подробнее про ТЗ проекта](https://zhukovsd.github.io/python-backend-learning-course/projects/currency-exchange/)


### Мотивация проекта
- Изучение архитектуры FastAPI-приложений с чистым разделением слоёв
- Реализация бизнес-логики без фреймворков
- Работа с базой данных PostgreSQL и SQLAlchemy
- Настройка тестирования, CORS, Docker и деплой


### Запуск проекта
#### 1. Клонируйте репозиторий
```bash
git clone https://github.com/Dmitry-DVal/Currency_Exchange_FastAPI
```

#### 2. Создайте `.env` файл по аналогии с `.env-example`

#### 3. Соберите и запустите контейнеры
```bash
docker compose -f docker-compose.dev.yml up --build

docker compose -f docker-compose.prod.yml up --build -d
```


### Автор
[Дмитрий Валюженич](https://t.me/Dmitry_D321)
Mitya0777@gmail.com

### Стек
- Python 
- Poetry
- Pytest
- FastAPI 
- PostgreSQL
- Docker
- SQLAlchemy
- alembic
- Pydantic
- Uvicorn
- Poetry

