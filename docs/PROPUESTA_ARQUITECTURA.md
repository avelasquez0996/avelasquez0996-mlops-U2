# Propuesta de Arquitectura MLOps - Nivel 2

Este documento detalla la arquitectura técnica para la implementación de DVC, MLflow, FastAPI y SQLite, cubriendo tanto el escenario de uso local (Médico) como el de servidor (MLOps/Entrenamiento).

## 1. Diagramas de Secuencia

### 1.1. Flujo de Predicción (Inferencia)
Este flujo describe cómo interactúa el médico con el sistema para obtener un diagnóstico.

```mermaid
sequenceDiagram
    actor Medico
    participant API as FastAPI (App)
    participant Validator as Pydantic Schema
    participant Model as Modelo ML (Pickle)
    participant DB as SQLite (Historial)

    Medico->>API: POST /predecir {datos_paciente}
    activate API
    API->>Validator: Validar tipos y rangos
    alt Datos Inválidos
        Validator-->>API: Error de Validación
        API-->>Medico: 422 Unprocessable Entity
    else Datos Válidos
        API->>Model: model.predict(datos)
        activate Model
        Model-->>API: predicción (ej. "Enfermedad Rara")
        deactivate Model
        
        par Persistencia Asíncrona
            API->>DB: INSERT INTO predicciones (inputs, output, timestamp)
        end
        
        API-->>Medico: 200 OK {predicción, probabilidad}
    end
    deactivate API
```

### 1.2. Flujo de Entrenamiento y Versionado

Este flujo describe cómo el Data Scientist actualiza el modelo asegurando reproducibilidad.

```mermaid
sequenceDiagram
    actor DS as Data Scientist
    participant DVC as DVC (Data Versioning)
    participant Train as Script Entrenamiento
    participant MLflow as MLflow Tracking
    participant Registry as Model Registry

    DS->>DVC: dvc add data/raw.csv
    DVC-->>DS: Genera data/raw.csv.dvc
    DS->>Train: Ejecutar pipeline (train.py)
    activate Train
    Train->>DVC: dvc pull (Obtener datos correctos)
    Train->>Train: Preprocesamiento & Fit
    Train->>MLflow: Log Metrics (Accuracy, Recall)
    Train->>MLflow: Log Params (Hyperparameters)
    Train->>MLflow: Log Model Artifact
    deactivate Train
    
    MLflow-->>Registry: Registrar nueva versión de modelo
    DS->>Registry: Promover a "Staging" / "Production"
```

## 2. Arquitectura de Despliegue

### 2.1. Escenario Local (Consultorio Médico)

Diseñado para simplicidad y bajos recursos. Todo corre en la máquina del médico o un servidor local pequeño.

```mermaid
graph TD
    subgraph "Host del Médico (Laptop/PC)"
        direction TB
        A[Cliente Web / Postman] -->|HTTP| B(Contenedor Docker: API)
        
        subgraph "Contenedor Docker: API"
            B1[FastAPI]
            B2[Modelo Cargado en RAM]
            B1 <--> B2
        end
        
        B1 -->|Lectura/Escritura| C[(Archivo SQLite: predicciones.db)]
        B1 -->|Lectura| D[Archivo Modelo: model.pkl]
    end
```

### 2.2. Escenario Servidor (Infraestructura MLOps)
Diseñado para el equipo de ingeniería, reentrenamiento y monitoreo centralizado.

```mermaid
graph TD
    subgraph "Servidor de Entrenamiento & Monitoreo"
        A[Airflow / GitHub Actions] -->|Trigger| B[Job de Entrenamiento]
        B -->|Log| C[Servidor MLflow]
        B -->|Pull Data| D[Storage DVC (S3/MinIO)]
        C -->|Store Artifacts| E[Artifact Store]
    end
    
    subgraph "Servidor de Producción"
        F[Load Balancer] --> G[Instancia API 1]
        F --> H[Instancia API 2]
        G & H -->|Write| I[(PostgreSQL Centralizado)]
        G & H -->|Load| E
    end
```

## 3. Guía de Migración: SQLite a PostgreSQL
Si el volumen de datos crece o se requiere concurrencia alta, se sugiere migrar de SQLite a PostgreSQL.

### Pasos para la migración
1. Infraestructura: Añadir un servicio db (PostgreSQL) en el docker-compose.yml.
2. Dependencias: Instalar psycopg2-binary en requirements.txt.
3. Configuración (Variables de Entorno): Cambiar la DATABASE_URL en el archivo .env.
    - Antes: sqlite:///./predicciones.db
    - Después: postgresql://user:password@db:5432/mlops_db
4. Código (SQLAlchemy): Gracias al uso de SQLAlchemy (ORM), no es necesario cambiar el código de la aplicación. El ORM abstrae el dialecto SQL. Solo debe asegurarse que al iniciar la app se ejecute Base.metadata.create_all(bind=engine) para crear las tablas en Postgres automáticamente.
5. Migración de Datos (Opcional): Si se desean conservar los datos históricos de SQLite, es posible usar herramientas como pgloader o scripts de exportación CSV -> importación SQL.

