#!/bin/bash
set -e

echo "[Building docker image."

# Build the Docker image
docker build -t restmon:latest .

echo "[✔] Docker image built successfully!"

echo "[Starting container for integration tests...]"
# Run the container in the background
docker run -d --name restmon_test restmon:latest
echo "[✔] Container started successfully!"

docker ps -a

echo "[Running integration tests...]"
# Run the integration tests inside the container
docker exec restmon_test python3 -m pytest -v tests_integration
echo "[✔] Integration tests executed successfully!"

# Clean up
docker rm -f restmon_test
echo "[✔] Cleaned up the container!"