#!/bin/bash
set -e

echo "[+] Running integration tests..."
pytest -v tests_integration

echo "[✓] Integration tests completed."
