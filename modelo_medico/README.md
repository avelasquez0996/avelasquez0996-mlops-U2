# Modelo Médico: MLOps Pipeline

[![DVC](https://dvc.org/badge.svg)](https://dvc.org) [![MLflow](https://img.shields.io/badge/MLflow-2.10-blue.svg)](https://mlflow.org) [![FastAPI](https://img.shields.io/badge/FastAPI-0.115-brightgreen.svg)](https://fastapi.tiangolo.com) [![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg)](https://www.docker.com/)

## Resumen

Implementación completa del pipeline MLOps con DVC, MLflow, FastAPI, SQLAlchemy (SQLite), Docker.

Ver [docs/IMPLEMENTATION_PLAN.md](../docs/IMPLEMENTATION_PLAN.md) para detalles de fases.

## Pipeline Overview
```mermaid
graph TD
    A[DVC: data/raw.csv] --> B[Stage: prepare - src/prepare.py → data/processed.parquet]
    B --> C[Stage: train - train.py + MLflow log → models/model.pkl]
    C --> D[FastAPI App: Load model.pkl, Pydantic validate, predict, SQLite insert]
    D --> E[SQLite: predicciones.db]
    F[mlruns/] --> G[MLflow UI: Compare experiments]
```

## Uso Rápido

1. **Ejecutar pipeline completo**:
   ```bash
   ./run_pipeline.sh
   ```

2. **Tests E2E** (dvc repro + MLflow + API + DB):
   ```bash
   pytest test_pipeline.py -v
   ```

3. **Servicios**:
   | Servicio | URL | Descripción |
   |----------|-----|-------------|
   | FastAPI | http://localhost:8000/docs | Swagger UI, POST /predict |
   | MLflow UI | http://localhost:5000 | Experiments & models |

4. **Verificación Manual**:
   ```bash
   # 1. Pipeline DVC
   dvc repro
   
   # 2. Test API
   curl -X POST "http://localhost:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{"edad":50.0, "fiebre":38.5, "dolor":7.0}'
   
   # 3. Check DB populated
   sqlite3 predicciones.db "SELECT COUNT(*) FROM prediccion;"
   
   # 4. MLruns populated
   ls -la mlruns/0/
   ```

## Docker

`docker compose up --build`

- Volumes: data/, models/, mlruns/, predicciones.db
- Healthchecks: API ready.

## Estructura

```
modelo_medico/
├── dvc.yaml       # Pipeline stages
├── params.yaml    # Hyperparams
├── run_pipeline.sh # One-command start
├── app.py         # FastAPI
├── test_pipeline.py # E2E pytest
├── src/           # prepare.py, model_utils.py, db.py, schemas.py...
├── data/          # raw.csv, processed.parquet
├── models/        # model.pkl, predicciones.db
└── mlruns/        # MLflow tracking