# 2. Adopción de MLflow para Tracking y Registro

* **Estado**: Aceptado
* **Fecha**: 2025-11-19
* **Contexto**: Falta de trazabilidad en experimentos y gestión de artefactos.

## Contexto y Problema
El entrenamiento actual imprime métricas en consola. No existe un historial centralizado que permita comparar si el modelo de hoy es mejor que el de ayer, ni un repositorio central de modelos ("Model Registry") para gestionar versiones (staging vs production).

## Decisión
Implementar **MLflow** para:
1. **Tracking**: Registrar hiperparámetros, métricas (precisión, recall) y artefactos (gráficos EDA).
2. **Model Registry**: Versionar los binarios del modelo (`.pkl` o formato MLflow) y gestionar su ciclo de vida.

## Consecuencias
* **Positivas**:
    * Visibilidad completa del rendimiento de los experimentos.
    * Facilidad para comparar modelos y seleccionar el mejor para producción.
    * Estandarización del formato de empaquetado del modelo.
* **Negativas**:
    * Requiere infraestructura adicional (servidor MLflow) para el escenario de servidor (en local puede ser basado en archivos).

## Implementación
Completada en Phase 3: Integración en train.py (log params/metrics/model).

**Fecha**: 2025-11-20
**Verificación**: `mlflow ui`, runs en mlruns/0/, model artifacts logged.