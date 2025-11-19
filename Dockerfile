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

# Устанавливаем зависимости для Python и Docker
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        git \
        iproute2 \
        iputils-ping \
        unzip \
        sudo \
        lsb-release \
        software-properties-common \
        gnupg \
        build-essential \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

# Устанавливаем Docker CLI и Docker Compose v2
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/*

# Копируем остальной код
COPY restmon/ ./restmon/
COPY tests ./tests/
COPY tests_integration ./tests_integration/
COPY pytest.ini .
COPY run_int_test.sh .

# Добавляем docker и curl для интеграционных тестов
RUN apt-get update && apt-get install -y \
    docker.io curl && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]