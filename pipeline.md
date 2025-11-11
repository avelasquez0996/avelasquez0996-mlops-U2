# Pipeline Modelo de Machine Learning

En la actualidad en la practica medica la cantidad de información sobre los pacientes a crecido debido a los avances tecnológicos. Sin embargo, existen las llamadas enfermedades huérfanas, enfermedades poco comunes, para las cuales los datos son escasos.

Mediante este proyecto proponemos un modelo de Machine Learning capaz de predecir, a partir de los síntomas de un paciente, la posibilidad de padecer una enfermedad, considerando tanto enfermedades comunes como huérfanas. 

El proceso completo para el desarrollo de modelo se divide en tres grandes etapas descritas a continuación:

1.	Diseño

En esta etapa definimos el problema, las limitaciones y el tipo de información con la que trabajamos.
-	Restricciones y Limitaciones
    - Escasez de datos para enfermedades huérfanas
    - Necesidad de anonimizar y proteger los datos médicos
    - Variabilidad de los datos
-	Tipos de datos
    - Estructurados como: edad, sexo, signos vitales, resultados de laboratorio
    - No estructurados como: descripción de síntomas, notas clínicas
    - Etiquetas: diagnostico confirmado o tipo de enfermedad

2.	Desarrollo

En esta etapa construimos y validamos el modelo de aprendizaje automático, identificamos las siguientes fuentes de datos
- Registros clínicos electrónicos (EHRs)
- Bases de datos abiertas 
- Datos sintéticos usados para compensar la falta en enfermedades raras

Así también identificamos una serie de etapas:

1.	Ingesta y limpieza de datos: corregimos valores nulos, estandarizamos los diferentes formatos y anonimizar los datos
2.	Análisis exploratorio: útil para estudiar la correlación entre las variables y visualizar síntomas frecuentes
3.	Preprocesamiento: normalizar valores, codificar categorías y balancear clases de ser necesario
4.	Entrenamiento del modelo
5.	Validación y pruebas (métricas)

3.	Producción

En esta etapa buscamos desplegar el modelo y mantenerlo operativo. 
-	Para el despliegue puede exponerse el modelo mediante una API
-	Realizamos una revisión continua del rendimiento del modelo y cambios de patrones
-	Reentrenar el modelo cada cierto tiempo con nuevos datos o casos clínicos
-	Proveer a los médicos de una interfaz donde ingresar los síntomas y recibir un diagnóstico probable.

Podemos resumir este proceso en el siguiente diagrama:

```mermaid
graph LR
    A[1. Diseño del modelo: definición de métricas y datos] --> B[2. Ingesta de datos: recolección, limpieza, anonimización]
    B --> C[3. Preprocesamiento: normalización, balanceo, encoding]
    C --> D[4. Entrenamiento y validación del modelo (ML / deep learning)]
    D --> E[5. Despliegue en prod: Docker / API / Flask, monitoreo y feedback]
```