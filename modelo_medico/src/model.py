"""
Módulo del modelo de Machine Learning.
Contiene un modelo mockeado que simula predicciones médicas.
"""

import numpy as np


class MedicalModel:
    """
    Modelo mockeado de Machine Learning para predicción de enfermedades.
    
    Categorías de salida:
    - NO ENFERMO: Sin signos de enfermedad
    - ENFERMEDAD LEVE: Síntomas leves
    - ENFERMEDAD AGUDA: Síntomas agudos
    - ENFERMEDAD CRÓNICA: Síntomas crónicos o severos
    """
    
    CATEGORIAS = [
        "NO ENFERMO",
        "ENFERMEDAD LEVE",
        "ENFERMEDAD AGUDA",
        "ENFERMEDAD CRÓNICA",
        "ENFERMEDAD TERMINAL"
    ]
    
    def __init__(self):
        # Semilla para reproducibilidad
        np.random.seed(42)
    
    def predecir(self, datos_procesados):
        """
        Predice la enfermedad basado en síntomas normalizados.
        
        Args:
            datos_procesados (dict): Diccionario con edad, fiebre y dolor normalizados
            
        Returns:
            str: Categoría de enfermedad predicha
        """
        # Extraer características normalizadas
        edad_norm = datos_procesados.get("edad", 0)
        fiebre_norm = datos_procesados.get("fiebre", 0)
        dolor_norm = datos_procesados.get("dolor", 0)
        
        # Calcular puntuación de enfermedad basada en síntomas
        # Este es un modelo mockeado con reglas heurísticas
        puntuacion = self._calcular_puntuacion_enfermedad(
            edad_norm,
            fiebre_norm,
            dolor_norm
        )
        
        # Clasificar basado en la puntuación
        categoria = self._clasificar(puntuacion)
        
        return categoria
    
    def _calcular_puntuacion_enfermedad(self, edad_norm, fiebre_norm, dolor_norm):
        """
        Calcula una puntuación de enfermedad combinando síntomas.
        
        Args:
            edad_norm (float): Edad normalizada [0, 1]
            fiebre_norm (float): Fiebre normalizada [0, 1]
            dolor_norm (float): Dolor normalizado [0, 1]
            
        Returns:
            float: Puntuación de enfermedad [0, 1]
        """
        # Pesos calibrados basados en importancia clínica
        peso_fiebre = 0.4
        peso_dolor = 0.45
        peso_edad = 0.15
        
        # Fiebre: factor importante en diagnóstico
        # Dolor: factor crítico en severidad
        # Edad: factor de riesgo
        
        puntuacion = (
            (fiebre_norm * peso_fiebre) +
            (dolor_norm * peso_dolor) +
            (edad_norm * peso_edad)
        )
        
        # Ajuste por sinergia: si hay múltiples síntomas, el efecto es mayor
        sinergia = (fiebre_norm * dolor_norm * 0.1)
        puntuacion += sinergia
        
        # Normalizar a rango [0, 1]
        puntuacion = min(puntuacion, 1.0)
        
        return puntuacion
    
    def _clasificar(self, puntuacion):
        """
        Clasifica la enfermedad basada en la puntuación.
        
        Umbrales:
        - < 0.2: NO ENFERMO
        - 0.2-0.4: ENFERMEDAD LEVE
        - 0.4-0.65: ENFERMEDAD AGUDA
        - 0.65-0.85: ENFERMEDAD CRÓNICA
        - >= 0.85: ENFERMEDAD TERMINAL
        
        Args:
            puntuacion (float): Puntuación de enfermedad [0, 1]
            
        Returns:
            str: Categoría de enfermedad
        """
        if puntuacion < 0.2:
            return self.CATEGORIAS[0]  # NO ENFERMO
        elif puntuacion < 0.4:
            return self.CATEGORIAS[1]  # ENFERMEDAD LEVE
        elif puntuacion < 0.65:
            return self.CATEGORIAS[2]  # ENFERMEDAD AGUDA
        elif puntuacion < 0.85:
            return self.CATEGORIAS[3]  # ENFERMEDAD CRÓNICA
        else:
            return self.CATEGORIAS[4]  # ENFERMEDAD TERMINAL
    
    def predecir_con_scores(self, datos_procesados):
        """
        Predice con scores de confianza para cada categoría.
        
        Args:
            datos_procesados (dict): Diccionario con edad, fiebre y dolor normalizados
            
        Returns:
            dict: {
                "prediccion": str,
                "scores": dict con scores para cada categoría
            }
        """
        edad_norm = datos_procesados.get("edad", 0)
        fiebre_norm = datos_procesados.get("fiebre", 0)
        dolor_norm = datos_procesados.get("dolor", 0)
        
        puntuacion = self._calcular_puntuacion_enfermedad(
            edad_norm,
            fiebre_norm,
            dolor_norm
        )
        
        # Generar distribución de probabilidad
        scores = self._generar_scores(puntuacion)
        
        prediccion = self._clasificar(puntuacion)
        
        return {
            "prediccion": prediccion,
            "scores": scores
        }
    
    def _generar_scores(self, puntuacion):
        """
        Genera scores de confianza para cada categoría basado en la puntuación.
        
        Args:
            puntuacion (float): Puntuación de enfermedad [0, 1]
            
        Returns:
            dict: Scores para cada categoría
        """
        # Distribución gaussiana centrada en la categoría predicha
        scores = {}
        
        # Calcular desviación estándar para distribución suave
        std = 0.15
        
        for i, categoria in enumerate(self.CATEGORIAS):
            # Centro de cada categoría
            centro = i / 3
            
            # Probabilidad gaussiana
            prob = np.exp(-0.5 * ((puntuacion - centro) / std) ** 2)
            scores[categoria] = round(prob / 3, 3)  # Normalizar
        
        # Normalizar para que sume 1
        total = sum(scores.values())
        if total > 0:
            scores = {k: round(v / total, 3) for k, v in scores.items()}
        
        return scores
