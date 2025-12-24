#!/bin/bash
set -e

IMAGE="restmon:latest"
CONTAINER="restmon_sigterm_test"

echo "[Starting container for integration tests...]"

docker rm -f $CONTAINER >/dev/null 2>&1 || true

# Run the container in the background
docker run -d \
--name $CONTAINER \
-p 5000:5000 \
$IMAGE

echo "[Waiting for container health...]"

# ⬇️ КЛЮЧЕВОЙ МОМЕНТ
for i in {1..30}; do
  STATUS=$(docker inspect \
    --format='{{.State.Health.Status}}' \
    $CONTAINER)

  echo "Health status: $STATUS"

  if [ "$STATUS" = "healthy" ]; then
    echo "[✔] Container is healthy!"
    break
  fi

  if [ "$STATUS" = "unhealthy" ]; then
    echo "[✖] Container became unhealthy"
    docker logs $CONTAINER
    exit 1
  fi

  sleep 1
done

if [ "$STATUS" != "healthy" ]; then
  echo "[✖] Container did not become healthy in time"
  docker logs $CONTAINER
  exit 1
fi

echo "[✔] Container started successfully!"

docker ps -a

echo "Sending SIGTERM"
docker kill --signal=SIGTERM $CONTAINER

sleep 1

echo "[Running sigterm test...]"
# Run the integration tests inside the container
docker exec $CONTAINER python3 -m pytest -c /dev/null/ -v tests_integration/test_sigterm.py
echo "[✔] SIGTERM test executed successfully!"

# Clean up
docker rm -f $CONTAINER
echo "[✔] Cleaned up the container!"