#!/bin/bash
set -e

echo "[+] Running integration tests..."

docker compose -f tests_integration/docker-compose.test.yml down -v || true
docker compose -f tests_integration/docker-compose.test.yml up -d --build

# ждать готовности сервиса
echo "[+] Waiting for service..."
for i in {1..30}; do
    if curl -s http://localhost:5001/platform > /dev/null; then
        echo "[+] Service is UP"
        break
    fi
    sleep 1
done

python3 -m pytest -v tests_integration

docker compose -f tests_integration/docker-compose.test.yml down -v
echo "[+] Integration tests completed."