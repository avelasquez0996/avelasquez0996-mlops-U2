# 4. Persistencia de Predicciones con SQLite

* **Estado**: Aceptado
* **Fecha**: 2025-11-19
* **Contexto**: Requisito de almacenar historial de predicciones para monitoreo y estadísticas.

## Contexto y Problema
El sistema necesita guardar cada predicción realizada (inputs y resultado) para calcular estadísticas y detectar desviaciones (Drift). Actualmente no hay persistencia. Se requiere una solución que funcione tanto en la laptop del médico (sin internet/infraestructura compleja) como en un servidor.

## Decisión
Utilizar **SQLite** como motor de base de datos único.
- La base de datos será un archivo local (`predicciones.db`).
- Se accederá mediante un ORM (SQLAlchemy) para desacoplar la lógica de la base de datos específica.

## Consecuencias
* **Positivas**:
    * **Simplicidad**: No requiere instalar un servidor de base de datos adicional (Docker container extra).
    * **Portabilidad**: El archivo `.db` se puede copiar/mover fácilmente.
    * **Suficiencia**: Para el volumen esperado de un consultorio o clínica pequeña, SQLite es más que suficiente.
* **Negativas**:
    * No apto para alta concurrencia de escritura (múltiples instancias de la API escribiendo a la vez).
    * Migración necesaria si el sistema escala a nivel hospitalario regional.