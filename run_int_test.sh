#!/bin/bash
set -e

echo "🚀 Starting integration tests..."

docker compose up -d --build tests_integration/docker-compose.test.yml

echo "⏳ Waiting for API to start..."

# Wait for service to respond
RETRIES=20
until curl -s http://localhost:5001/ >/dev/null 2>&1; do
    ((RETRIES--))
    if [ $RETRIES -le 0 ]; then
        echo "❌ ERROR: Service did not start!"
        exit 1
    fi
    sleep 1
done

echo "✅ API is UP — running integration tests"

pytest -v tests_integration

docker compose down tests_integration/docker-compose.test.yml
echo "✅ Integration tests completed"