# syntax=docker/dockerfile:1.5
FROM python:3.12-slim

# Используем BuildKit cache для pip
ARG PIP_CACHE_DIR=/root/.cache/pip
ENV PIP_CACHE_DIR=${PIP_CACHE_DIR}

WORKDIR /app

# Копируем только requirements для кэширования зависимостей
COPY requirements.txt .

# Устанавливаем зависимости с использованием кэша
RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    --cache-dir $PIP_CACHE_DIR

# Копируем остальной код
COPY restmon/ ./restmon/
COPY tests ./tests/
COPY tests_integration ./tests_integration/
COPY pytest.ini .
COPY run_int_test.sh .

CMD ["python3", "-m", "restmon/api.py"]