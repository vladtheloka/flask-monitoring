#!/bin/bash
set -e

echo "[+] Running integration tests..."

# Поднимаем тестовый docker-compose
docker compose -f tests_integration/docker-compose.test.yml up -d --build

# Ждём готовности сервиса
URL="http://localhost:5001/platform"
for i in {1..30}; do
    if curl -s "$URL" >/dev/null; then
        echo "[+] Service is ready"
        break
    fi
    sleep 1
done

# Запускаем pytest на готовом имедже
docker run --rm -v "$PWD":/app -w /app restmon \
    pytest -v --cov=restmon --cov-report=xml:coverage.xml tests_integration

# Останавливаем тестовый compose
docker compose -f tests_integration/docker-compose.test.yml down -v