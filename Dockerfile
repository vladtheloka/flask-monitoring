# syntax=docker/dockerfile:1.5
FROM python:3.12-slim

# Используем BuildKit cache для pip
ARG PIP_CACHE_DIR=/root/.cache/pip
ENV PIP_CACHE_DIR=${PIP_CACHE_DIR}

WORKDIR /app

# Устанавливаем docker-compose plugin (официальный)
RUN apt-get update && apt-get install -y \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# docker compose plugin (официальный способ)
RUN mkdir -p /usr/libexec/docker/cli-plugins && \
    curl -SL \
        https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 \
        -o /usr/libexec/docker/cli-plugins/docker-compose && \
    chmod +x /usr/libexec/docker/cli-plugins/docker-compose

# Копируем только requirements для кэширования зависимостей
COPY requirements.txt .

# Устанавливаем зависимости с использованием кэша
RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    --cache-dir $PIP_CACHE_DIR

# Копируем остальной код
COPY restmon/ ./restmon/
COPY tests ./tests/
COPY tests_integration ./tests_integration/
COPY pytest.ini ./

CMD ["python3", "-m", "restmon"]