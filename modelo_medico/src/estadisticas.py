"""
Módulo de estadísticas de predicciones.
Mantiene un registro de todas las predicciones realizadas.
"""

from datetime import datetime
import json
import os


class EstadisticasPredicciones:
    """
    Gestiona estadísticas de predicciones realizadas.
    Almacena en archivo JSON para persistencia.
    """

    # Archivo donde se guardan las estadísticas
    ARCHIVO_STATS = "predicciones_stats.json"

    def __init__(self):
        self.estadisticas = self._cargar_estadisticas()

    def _cargar_estadisticas(self):
        """
        Carga las estadísticas desde archivo o crea estructura vacía.

        Returns:
            dict: Estructura de estadísticas
        """
        if os.path.exists(self.ARCHIVO_STATS):
            try:
                with open(self.ARCHIVO_STATS, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._estructura_vacia()

        return self._estructura_vacia()

    @staticmethod
    def _estructura_vacia():
        """
        Crea estructura vacía de estadísticas.

        Returns:
            dict: Estructura inicial
        """
        return {
            "total_predicciones": 0,
            "por_categoria": {
                "NO ENFERMO": 0,
                "ENFERMEDAD LEVE": 0,
                "ENFERMEDAD AGUDA": 0,
                "ENFERMEDAD CRÓNICA": 0,
                "ENFERMEDAD TERMINAL": 0,
            },
            "ultimas_5": [],
            "ultima_prediccion": None,
        }

    def registrar_prediccion(self, edad, fiebre, dolor, resultado):
        """
        Registra una nueva predicción en las estadísticas.

        Args:
            edad (float): Edad del paciente
            fiebre (float): Temperatura del paciente
            dolor (float): Nivel de dolor (0-10)
            resultado (str): Categoría predicha
        """
        # Incrementar totales
        self.estadisticas["total_predicciones"] += 1
        self.estadisticas["por_categoria"][resultado] += 1

        # Registrar nueva predicción
        prediccion = {
            "timestamp": datetime.now().isoformat(),
            "entrada": {"edad": edad, "fiebre": fiebre, "dolor": dolor},
            "resultado": resultado,
        }

        # Mantener últimas 5 predicciones
        self.estadisticas["ultimas_5"].insert(0, prediccion)
        if len(self.estadisticas["ultimas_5"]) > 5:
            self.estadisticas["ultimas_5"] = self.estadisticas["ultimas_5"][:5]

        # Actualizar última predicción
        self.estadisticas["ultima_prediccion"] = {
            "timestamp": prediccion["timestamp"],
            "resultado": resultado,
        }

        # Guardar en archivo
        self._guardar_estadisticas()

    def _guardar_estadisticas(self):
        """Guarda las estadísticas en archivo JSON."""
        try:
            with open(self.ARCHIVO_STATS, "w") as f:
                json.dump(self.estadisticas, f, indent=2)
        except IOError as e:
            print(f"Error al guardar estadísticas: {e}")

    def obtener_estadisticas(self):
        """
        Obtiene un resumen de las estadísticas.

        Returns:
            dict: Estadísticas formateadas
        """
        return {
            "total_predicciones": self.estadisticas["total_predicciones"],
            "por_categoria": self.estadisticas["por_categoria"],
            "ultimas_5_predicciones": self.estadisticas["ultimas_5"],
            "ultima_prediccion": self.estadisticas["ultima_prediccion"],
        }

    def obtener_total_predicciones(self):
        """Retorna el total de predicciones realizadas."""
        return self.estadisticas["total_predicciones"]

    def obtener_por_categoria(self):
        """Retorna conteos por categoría."""
        return self.estadisticas["por_categoria"]

    def obtener_ultimas_5(self):
        """Retorna las últimas 5 predicciones."""
        return self.estadisticas["ultimas_5"]

    def obtener_ultima_prediccion(self):
        """Retorna información de la última predicción."""
        return self.estadisticas["ultima_prediccion"]

    def limpiar_estadisticas(self):
        """Limpia todas las estadísticas (resetea)."""
        self.estadisticas = self._estructura_vacia()
        self._guardar_estadisticas()
