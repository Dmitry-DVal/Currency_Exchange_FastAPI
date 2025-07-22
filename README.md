# Обмен валюты на FastAPI

### Описание

REST API для описания валют и обменных курсов. Позволяет просматривать и редактировать списки валют и обменных курсов, и
совершать расчёт конвертации произвольных сумм из одной валюты в другую.
[Подробнее про ТЗ проекта](https://zhukovsd.github.io/python-backend-learning-course/projects/weather-viewer/)

### Автор

[Дмитрий Валюженич](https://t.me/Dmitry_D321)
Mitya0777@gmail.com


ЗАПУСК ПРОД ВЕРСИИ

1. Скачать репозиторий
git clone https://github.com/Dmitry-DVal/Currency_Exchange_FastAPI

2. Создать .env по аналогии с .env-example

3. Собрать образ
docker compose -f docker-compose.dev.yml up --build
docker compose -f docker-compose.prod.yml up --build -d

4. Всё готово
Фронтенд доступен по адресу
http://localhost/
Свагер по http://localhost:8000/docs


