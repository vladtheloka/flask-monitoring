#!/bin/bash
set -e

echo "[+] Running integration tests..."
python3 -m pytest -v tests_integration
echo "[+] Integration tests passed!"