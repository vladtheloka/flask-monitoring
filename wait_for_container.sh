#!/usr/bin/env bash
set -e

URL=${1:-http://localhost:5000/health/ready}
TIMEOUT=${2:-30}

echo "[wait] Waiting for $URL"

for i in $(seq 1 $TIMEOUT); do
  if curl -sf "$URL" > /dev/null; then
    echo "[wait] Service is ready"
    exit 0
  fi
  sleep 1
done

echo "[wait] Timeout waiting for service"
exit 1