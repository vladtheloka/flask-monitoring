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

# Install Docker CLI + Docker Compose v2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/debian $(. /etc/os-release; echo $VERSION_CODENAME) stable" \
        > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/*

# Копируем остальной код
COPY restmon/ ./restmon/
COPY tests ./tests/
COPY tests_integration ./tests_integration/
COPY pytest.ini .
COPY run_int_test.sh .
COPY Dockerfile .

CMD ["/bin/bash"]