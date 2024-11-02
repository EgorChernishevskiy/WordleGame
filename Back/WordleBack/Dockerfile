# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем обновления и системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы pyproject.toml и poetry.lock в контейнер
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости, указывая Poetry использовать системное окружение
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем все остальные файлы проекта в контейнер
COPY . /app

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
