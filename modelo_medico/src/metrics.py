"""
Módulo de métricas y evaluación del modelo.
Proporciona funciones para evaluar el rendimiento del modelo.
"""


class ModelMetrics:
    """Calcula métricas de rendimiento del modelo"""
    
    @staticmethod
    def accuracy(y_true, y_pred):
        """
        Calcula la precisión (accuracy) del modelo.
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Predicciones del modelo
            
        Returns:
            float: Accuracy en rango [0, 1]
        """
        if len(y_true) == 0:
            return 0.0
        
        correctas = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        return correctas / len(y_true)
    
    @staticmethod
    def precision(y_true, y_pred, clase):
        """
        Calcula la precisión (precision) para una clase específica.
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Predicciones del modelo
            clase: Clase a evaluar
            
        Returns:
            float: Precision en rango [0, 1]
        """
        verdaderos_positivos = sum(
            1 for t, p in zip(y_true, y_pred) if p == clase and t == clase
        )
        positivos_predichos = sum(1 for p in y_pred if p == clase)
        
        if positivos_predichos == 0:
            return 0.0
        
        return verdaderos_positivos / positivos_predichos
    
    @staticmethod
    def recall(y_true, y_pred, clase):
        """
        Calcula el recall (sensibilidad) para una clase específica.
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Predicciones del modelo
            clase: Clase a evaluar
            
        Returns:
            float: Recall en rango [0, 1]
        """
        verdaderos_positivos = sum(
            1 for t, p in zip(y_true, y_pred) if p == clase and t == clase
        )
        positivos_reales = sum(1 for t in y_true if t == clase)
        
        if positivos_reales == 0:
            return 0.0
        
        return verdaderos_positivos / positivos_reales
    
    @staticmethod
    def f1_score(y_true, y_pred, clase):
        """
        Calcula el F1-score para una clase específica.
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Predicciones del modelo
            clase: Clase a evaluar
            
        Returns:
            float: F1-score en rango [0, 1]
        """
        precision = ModelMetrics.precision(y_true, y_pred, clase)
        recall = ModelMetrics.recall(y_true, y_pred, clase)
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
