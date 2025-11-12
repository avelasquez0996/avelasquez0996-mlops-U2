# API Médica - Pipeline MLOps Completo

## Descripción

Este proyecto implementa un **pipeline completo de Machine Learning** para predicción de enfermedades médicas, siguiendo las mejores prácticas de MLOps. El servicio predice el estado de un paciente según: **edad**, **fiebre** y **nivel de dolor**.

**Características principales**:
- Pipeline MLOps completo (Diseño → Producción)
- Modelo mockeado con lógica médica realista
- API REST con validación de datos
- Preprocesamiento y normalización de datos
- Análisis Exploratorio de Datos (EDA)
- Entrenamiento y validación con métricas
- Containerización con Docker
- Preparado para monitoreo y reentrenamiento

## Estructura del Proyecto

```
.
├── README.md                      # Este archivo
└── modelo_medico/
    ├── app.py                     # API Flask (Etapa 5)
    ├── train.py                   # Entrenamiento (Etapas 4-5)
    ├── eda.py                     # Análisis exploratorio (Etapa 3)
    ├── Dockerfile                 # Containerización
    ├── requirements.txt           # Dependencias Python
    └── src/
        ├── __init__.py
        ├── model.py               # Modelo de ML mockeado (Etapa 4)
        ├── preprocessor.py        # Preprocesamiento (Etapa 3)
        ├── validator.py           # Validación de datos
        ├── data_loader.py         # Carga y limpieza (Etapa 2)
        └── metrics.py             # Cálculo de métricas (Etapa 5)
```

## Etapas del Pipeline Implementadas

| Etapa | Descripción | Archivos |
|-------|-------------|----------|
| 1. **Diseño** | Definición de métricas y restricciones | `src/validator.py` |
| 2. **Ingesta de Datos** | Recolección, limpieza, anonimización | `src/data_loader.py` |
| 3. **Análisis Exploratorio** | EDA y preprocesamiento | `eda.py`, `src/preprocessor.py` |
| 4. **Entrenamiento** | Entrenamiento y validación del modelo | `train.py`, `src/model.py` |
| 5. **Despliegue** | API REST, Docker, monitoreo | `app.py`, `Dockerfile` |

## API REST

### Endpoint: POST /predecir

Predice la enfermedad basado en síntomas del paciente.

**Entrada**:
```json
{
  "edad": 20,
  "fiebre": 36.2,
  "dolor": 9
}
```

**Respuesta exitosa** (200):
```json
{
  "resultado": "ENFERMEDAD CRÓNICA",
  "entrada": {
    "edad": 20,
    "fiebre": 36.2,
    "dolor": 9
  }
}
```

**Validaciones**:
- `edad`: 0-150 años
- `fiebre`: 35-45°C
- `dolor`: 0-10

**Códigos de error**:
- `400`: Faltan campos o datos inválidos
- `500`: Error interno del servidor

## Instalación y Ejecución

### 1. Opción Local (Sin Docker)

#### Instalar dependencias
```bash
cd modelo_medico
pip install -r requirements.txt
```

#### Ejecutar Análisis Exploratorio
```bash
python eda.py
```

#### Entrenar y Validar Modelo
```bash
python train.py
```

#### Iniciar API
```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

### 2. Opción Docker

#### Construir imagen
```bash
docker build -t modelo-medico:latest .
```

#### Ejecutar contenedor
```bash
docker run -d -p 5000:5000 --name api-medica modelo-medico:latest
```

#### Ver logs
```bash
docker logs -f api-medica
```

#### Detener contenedor
```bash
docker stop api-medica
docker rm api-medica
```

## Testing de la API

### Con cURL

```bash
# Consultar raíz
curl http://localhost:5000/

# Realizar predicción
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"edad": 20, "fiebre": 36.2, "dolor": 9}'
```

### Con Postman

1. **URL**: `http://localhost:5000/predecir`
2. **Método**: POST
3. **Headers**: `Content-Type: application/json`
4. **Body** (JSON):
```json
{
  "edad": 20,
  "fiebre": 36.2,
  "dolor": 9
}
```

## Categorías de Enfermedad

El modelo predice 4 categorías basadas en síntomas:

| Categoría | Descripción | Trigger |
|-----------|-------------|---------|
| **NO ENFERMO** | Sin signos de enfermedad | Puntuación < 0.2 |
| **ENFERMEDAD LEVE** | Síntomas leves | 0.2 ≤ Puntuación < 0.4 |
| **ENFERMEDAD AGUDA** | Síntomas agudos | 0.4 ≤ Puntuación < 0.7 |
| **ENFERMEDAD CRÓNICA** | Síntomas severos/crónicos | Puntuación ≥ 0.7 |

## Modelo Mockeado

El modelo utiliza reglas arbitrarias que simulan un modelo de ML real:

```python
puntuación = (
    fiebre * 0.40 +              # 40% Fiebre
    dolor * 0.45 +               # 45% Dolor
    edad * 0.15 +                # 15% Edad
    fiebre * dolor * 0.10        # Sinergia entre síntomas
)
```

## Tecnologías Utilizadas

- **Flask 3.0.0**: Framework web API REST
- **NumPy 1.24.3**: Cálculos numéricos
- **scikit-learn 1.3.0**: Utilidades de ML
- **Docker**: Containerización y despliegue
- **Python 3.11**: Lenguaje de programación