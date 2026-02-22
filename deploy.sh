#!/bin/bash
set -e

echo "=== Maturity Model — Deploy ==="

git pull

docker compose down
docker compose build --no-cache
docker compose up -d

echo ""
docker compose ps
echo ""
echo "=== Deployed at https://maturity-model.matge.com ==="
