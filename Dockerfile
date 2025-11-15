# syntax=docker/dockerfile:1.5
FROM python:3.12-slim

# Используем BuildKit cache для pip
ARG PIP_CACHE_DIR=/root/.cache/pip
ENV PIP_CACHE_DIR=${PIP_CACHE_DIR}

WORKDIR /app

# Копируем только requirements для кэширования зависимостей
COPY app/requirements.txt .

# Устанавливаем зависимости с кэшем
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]