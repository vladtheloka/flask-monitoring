#!/bin/bash
set -e

echo "[+] Running integration tests..."
python3 -m pytest -v tests_integration --maxfail=1 --disable-warnings
echo "[+] Integration tests passed!"