# API Médica 

## Descripción
Este servicio simula un modelo médico capaz de predecir el estado de un paciente según tres valores de entrada: **edad**, **fiebre** y **nivel de dolor**. El modelo es simulado, pero representa cómo un médico podría consultar un modelo de ML contenedorizado.

Se utiliza Flask para la API con la cual se expone el modelo de ML.

## Estructura
```
.
├── MLOPS2.md
├── modelo_medico
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── pipeline.md
└── README.md
```

## Cómo construir y ejecutar la imagen

### 1. Construir la imagen
Desde el directorio del proyecto:

```bash
docker build -t modelo-medico 
```

### 2. Correr la Imagen
```bash
docker run -d -p 5000:5000 modelo-medico
```

O puede optarse por ejecutarlo desde docker desktop

### 3. Detener la ejecucion
```bash
docker stop <id del contenedor>
```

Por ejemplo: `docker stop 4b0057b0a102468f87febae2d2e3a04eb9c24a38d220d0ea06ce8cfd7959e363`. También pueden indicarse los primeros caracteres del ID: `docker stop 4b0057`