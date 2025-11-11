# API Médica 

## Descripción
Este servicio simula un modelo médico capaz de predecir el estado de un paciente
según tres valores de entrada: **edad**, **fiebre** y **nivel de dolor**.  
El modelo es simulado, pero representa cómo un médico podría consultar un modelo de ML
contenedorizado.

## Estructura
```
modelo_medico/
├── Dockerfile
├── app.py
└── requirements.txt
```


## Cómo construir y ejecutar la imagen

### 1. Construir la imagen
Desde el directorio del proyecto:

docker build -t modelo-medico 

### 2. Correr la Imagen
docker run -d -p 5000:5000 modelo-medico

O puede optarse por ejecutarlo desde docker desktop

### 3. Detener la ejecucion
docker stop <id del contenedor>

ejemplo: "docker stop 4b0057b0a102468f87febae2d2e3a04eb9c24a38d220d0ea06ce8cfd7959e363"

o basta también con solo los primeros caracteres del id

"docker stop 4b0057"