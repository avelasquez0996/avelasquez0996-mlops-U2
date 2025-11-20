# Changelog - Refactor Producción

## ✨ Nuevas Características

### Arquitectura MLOps
- **DVC (Data Version Control)**:
  - Implementado pipeline reproducible en `dvc.yaml` (etapas: `prepare`, `train`).
  - Versionado de datos crudos (`data/raw.csv.dvc`) y modelos (`models/model.pkl.dvc`).
  - Configuración centralizada de hiperparámetros en `params.yaml`.
- **MLflow**:
  - Integración en `train.py` para tracking automático de métricas, parámetros y artefactos.
  - Servicio de MLflow UI configurado en `docker-compose.yml` (puerto 5000).
- **Docker Compose**:
  - Orquestación de servicios (API + MLflow) con volúmenes persistentes.

### API y Backend
- **FastAPI**: Migración completa desde Flask.
  - Documentación automática (Swagger UI) en `/docs`.
  - Validación de datos robusta con **Pydantic** (`src/schemas.py`).
- **Persistencia**:
  - Implementación de **SQLAlchemy ORM** (`src/db.py`, `src/models_db.py`).
  - Base de datos SQLite (`predicciones.db`) para historial de predicciones.
  - Endpoints asíncronos y gestión de sesiones de base de datos.

### Documentación
- **Propuesta de Arquitectura**: `docs/PROPUESTA_ARQUITECTURA.md` con diagramas Mermaid.
- **ADRs (Architectural Decision Records)**:
  - `0001-adopcion-dvc.md`
  - `0002-adopcion-mlflow.md`
  - `0003-persistencia-sqlite.md`
  - `0004-fastapi-sqlite.md`

## 🛠 Cambios (Changed)

### Código Fuente
- **`modelo_medico/app.py`**: Se reescribió la lógica para usar FastAPI, inyección de dependencias (`Depends`) y esquemas Pydantic.
- **`modelo_medico/train.py`**:
  - Lectura de parámetros desde `params.yaml`.
  - Logging de experimentos a MLflow.
  - Carga de datos procesados desde `data/processed.parquet`.
- **`modelo_medico/requirements.txt`**: Actualizado con `fastapi`, `uvicorn`, `sqlalchemy`, `dvc`, `mlflow`.
- **`modelo_medico/Dockerfile`**: Optimizado para instalar nuevas dependencias y exponer puertos adecuados.

### Estructura de Datos
- **Preprocesamiento**: Separado en `src/prepare.py` como etapa independiente del pipeline DVC.
- **Datos**: Introducción de formato Parquet (`processed.parquet`) para eficiencia.

## 📂 Archivos Modificados

### Nuevos Archivos
- `docs/PROPUESTA_ARQUITECTURA.md`
- `docs/adr/*.md`
- `modelo_medico/dvc.yaml`
- `modelo_medico/dvc.lock`
- `modelo_medico/params.yaml`
- `modelo_medico/docker-compose.yml`
- `modelo_medico/src/db.py`
- `modelo_medico/src/models_db.py`
- `modelo_medico/src/schemas.py`
- `modelo_medico/src/prepare.py`
- `modelo_medico/src/model_utils.py`

### Archivos Modificados
- `modelo_medico/app.py` (Refactor total)
- `modelo_medico/train.py` (Integración MLflow/DVC)
- `modelo_medico/requirements.txt` (Nuevas libs)
- `modelo_medico/Dockerfile` (Configuración entorno)
- `README.md` (Documentación actualizada)
