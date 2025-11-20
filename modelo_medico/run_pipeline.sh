#!/bin/bash
set -euo pipefail

echo "Iniciando Pipeline MLOps Completo para modelo_medico"

echo "1. Extrayendo caché DVC más reciente..."
dvc pull

echo "2. Reproduciendo pipeline completo (prepare + train con MLflow)..."
dvc repro

echo "3. Iniciando servicios Docker (FastAPI + UI MLflow)..."
docker compose up -d

echo "¡Todo listo!"

echo ""
echo "Endpoints:"
echo "  Swagger API: http://localhost:8000/docs"
echo "  UI MLflow:  http://localhost:5000"
echo "  DB Predicciones: ./predicciones.db (SQLite)"
echo ""

echo "Verificación:"
echo "  pytest test_pipeline.py -v"
echo "  curl -X POST \"http://localhost:8000/predict\" \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"edad\":50.0, \"fiebre\":38.5, \"dolor\":7.0}'"