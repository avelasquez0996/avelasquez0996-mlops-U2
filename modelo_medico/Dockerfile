# Imagen base oficial de Python
FROM python:3.12-slim

# Instalar herramientas de compilación necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app/modelo_medico

# Copiar archivos necesarios
COPY modelo_medico/requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación completa
COPY modelo_medico/ .

# Exponer el puerto donde corre Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
