# 1. Adopción de DVC para Versionado de Datos

* **Estado**: Aceptado
* **Fecha**: 2025-11-19
* **Contexto**: Necesidad de reproducibilidad en modelos de enfermedades huérfanas.

## Contexto y Problema
Actualmente, los datasets médicos se gestionan como archivos estáticos en el repositorio o localmente. Esto genera problemas graves:
1. No podemos saber qué versión exacta de los datos entrenó un modelo específico.
2. El dataset de enfermedades huérfanas crecerá con el tiempo, y necesitamos rastrear esa evolución.
3. Git no está diseñado para archivos grandes.

## Decisión
Utilizaremos **DVC (Data Version Control)** para gestionar los datos y los pipelines de entrenamiento.
- Los archivos de datos reales (`.csv`, `.parquet`) se excluirán de Git.
- Se versionarán los archivos de metadatos `.dvc`.
- Se configurará un almacenamiento remoto (inicialmente local o carpeta compartida, escalable a S3/MinIO).

## Consecuencias
* **Positivas**:
    * Reproducibilidad total: Código + Datos = Modelo.
    * Gestión eficiente de almacenamiento sin inflar el repositorio Git.
    * Independencia del entorno de desarrollo.
* **Negativas**:
    * Curva de aprendizaje adicional para el equipo.
    * Requiere configuración de almacenamiento remoto compartido para colaboración.

## Implementación
Completada en Phases 1-2: DVC init, data versioning, pipelines (dvc.yaml).

**Fecha**: 2025-11-20
**Verificación**: `dvc repro`, `dvc status` clean, data/processed.parquet present.