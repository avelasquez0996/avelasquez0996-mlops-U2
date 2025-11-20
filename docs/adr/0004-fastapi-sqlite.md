# 4. Adopción de FastAPI con Persistencia SQLite

* **Estado**: Aceptado
* **Fecha**: 2025-11-19
* **Contexto**: Modernizar la API desde Flask y asegurar persistencia de predicciones en entornos locales.

## Contexto y Problema

La implementación original usaba Flask (síncrono, sin validación nativa fuerte, sin docs automáticas). Se requiere:
- API async para futuro escalado.
- Validación type-safe de inputs médicos.
- Persistencia automática de cada predicción.
- Documentación interactiva para el médico/DS.

## Decisión

Adoptar **FastAPI** + **Pydantic** (schemas) + **SQLAlchemy** (ORM sobre SQLite, ver [0003-persistencia-sqlite.md](../adr/0003-persistencia-sqlite.md)).

- Migrar `app.py` a FastAPI.
- Nuevos endpoints: POST /predecir, GET /estadisticas.
- Carga de modelo desde `models/model.pkl` (DVC).
- Insert asíncrono en DB post-predicción.
- Server: `uvicorn app:app`.

## Consecuencias

* **Positivas**:
    * Rendimiento async y bajo latency.
    * Validación automática + error HTTP 422.
    * Swagger UI en `/docs` y `/redoc`.
    * Integración seamless con DVC/MLflow/SQLite.
* **Negativas / Riesgos**:
    * Dependencias nuevas: fastapi, uvicorn, pydantic, sqlalchemy.
    * Refactor de endpoints existentes.
    * Concurrency limits de SQLite (ver guía migración).

## Implementación

- **Fases**: 4 (DB layer), 5 (FastAPI migration), 6 (model load), 8 (Docker).
- **Verificación**: `uvicorn app:app`, curl POST /predecir, query predicciones.db, pytest.
- **Estado**: Completado. Ver [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md).
