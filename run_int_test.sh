#!/bin/bash
set -e

COMPOSE_FILE="docker-compose.test.yml"
COMPOSE_DIR="tests_integration"
SERVICE_URL="http://localhost:5001/platform"

echo "[+] Checking compose file..."
if [ ! -f "$COMPOSE_DIR/$COMPOSE_FILE" ]; then
    echo "ERROR: $COMPOSE_DIR/$COMPOSE_FILE not found!"
    exit 1
fi

echo "[+] Starting test compose environment..."
cd "$COMPOSE_DIR"
docker compose -f "$COMPOSE_FILE" -p restmon_test up -d --build
cd ..

echo "[+] Waiting for service to be ready..."
for i in {1..30}; do
    if curl -s "$SERVICE_URL" > /dev/null; then
        echo "[+] Service is up!"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo "ERROR: Service did not start!"
        exit 1
    fi
done

echo "[+] Running integration tests..."
pytest -v tests_integration

echo "[+] Stopping docker compose..."
cd "$COMPOSE_DIR"
docker compose -f "$COMPOSE_FILE" -p restmon_test down -v
cd ..

echo "[✓] Integration tests finished."