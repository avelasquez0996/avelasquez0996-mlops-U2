"""
Módulo de preprocesamiento de datos.
Se encarga de normalizar y preparar los datos para el modelo.
"""

import numpy as np


class Preprocessor:
    """Preprocesa los datos del paciente para el modelo"""

    def __init__(self):
        # Parámetros de normalización (calculados en etapa de análisis exploratorio)
        self.normalizacion = {
            "edad": {"min": 0, "max": 150},
            "fiebre": {"min": 35, "max": 45},
            "dolor": {"min": 0, "max": 10},
        }

    def procesar(self, datos):
        """
        Preprocesa los datos normalizando los valores.

        Args:
            datos (dict): Diccionario con edad, fiebre y dolor

        Returns:
            dict: Datos normalizados
        """
        datos_procesados = {}

        # Normalizar cada característica a rango [0, 1]
        for campo, valor in datos.items():
            if campo in self.normalizacion:
                norm_params = self.normalizacion[campo]
                valor_normalizado = self._normalizar(
                    valor, norm_params["min"], norm_params["max"]
                )
                datos_procesados[campo] = valor_normalizado
            else:
                datos_procesados[campo] = valor

        return datos_procesados

    @staticmethod
    def _normalizar(valor, min_val, max_val):
        """
        Normaliza un valor a rango [0, 1] usando min-max scaling.

        Args:
            valor: Valor a normalizar
            min_val: Valor mínimo del rango original
            max_val: Valor máximo del rango original

        Returns:
            float: Valor normalizado entre 0 y 1
        """
        if max_val == min_val:
            return 0.0
        return (valor - min_val) / (max_val - min_val)

    def desnormalizar_scores(self, scores_normalizados):
        """
        Convierte scores normalizados en probabilidades porcentuales.

        Args:
            scores_normalizados (dict): Scores en rango [0, 1]

        Returns:
            dict: Scores en porcentaje [0, 100]
        """
        return {
            clave: round(valor * 100, 2) for clave, valor in scores_normalizados.items()
        }
