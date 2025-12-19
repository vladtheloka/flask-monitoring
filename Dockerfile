# syntax=docker/dockerfile:1.5
FROM python:3.12-slim

# Используем BuildKit cache для pip
ARG PIP_CACHE_DIR=/root/.cache/pip
ENV PIP_CACHE_DIR=${PIP_CACHE_DIR}

WORKDIR /app

# Копируем только requirements для кэширования зависимостей
COPY requirements.txt .

RUN apt-get update
RUN apt-get --yes install curl
# Устанавливаем зависимости с использованием кэша
RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    --cache-dir $PIP_CACHE_DIR

# Копируем остальной код
COPY restmon/ ./restmon/
COPY tests ./tests/
COPY tests_integration ./tests_integration/
COPY pytest.ini .
COPY run_int_test.sh .
COPY pyproject.toml .
COPY .coveragerc .
COPY gunicorn_conf.py .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
CMD curl --silent --fail http://localhost:5000/health/live || exit 1
# Start integration test runner
CMD ["gunicorn", "-c", "gunicorn_conf.py", "restmon.api:create_app()"]