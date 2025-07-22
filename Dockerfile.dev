FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Сначала копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install --upgrade pip && pip install poetry

# Настройка poetry и установка зависимостей
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-root

# Копируем остальные файлы проекта
COPY . .

# Открываем порт
EXPOSE 8000

# Запуск через uvicorn
CMD ["uvicorn", "src.currency_exchange_app.main:app", "--host", "0.0.0.0", "--port", "8000"]