#!/bin/bash
set -e

echo "[+] Running integration tests..."

# Поднять контейнеры через docker compose
docker compose tests_integration/docker-compose.test.yml up -d --build

# Ждём готовности сервиса
URL="http://localhost:5001/platform"
for i in {1..30}; do
    if curl -s "$URL" > /dev/null; then
        echo "[+] Service is up"
        break
    fi
    sleep 1
done

# Запуск pytest с coverage
python3 -m pytest -v --cov=restmon --cov-report=xml:coverage/coverage.xml tests_integration

# Остановить контейнеры
docker compose tests_integration/docker-compose.test.yml down -v
echo "[+] Integration tests completed."