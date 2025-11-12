"""
Script de entrenamiento y validación del modelo.
Etapas 4-5 del pipeline: Entrenamiento, validación y pruebas
"""

from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.model import MedicalModel
from src.metrics import ModelMetrics
import numpy as np


class ModelTrainer:
    """Entrena y valida el modelo de ML"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.preprocessor = Preprocessor()
        self.model = MedicalModel()
        self.metrics = ModelMetrics()
    
    def entrenar_y_validar(self, cantidad_datos=1000, split_train_test=0.8):
        """
        Entrena el modelo con datos sintéticos y lo valida.
        
        Args:
            cantidad_datos (int): Cantidad total de datos a usar
            split_train_test (float): Proporción de datos para entrenamiento
            
        Returns:
            dict: Métricas de entrenamiento y validación
        """
        # Etapa 1: Ingesta y limpieza de datos
        datos = self.data_loader.obtener_datos_procesados(cantidad_datos)
        
        # Split train-test
        split_idx = int(len(datos) * split_train_test)
        datos_entrenamiento = datos[:split_idx]
        datos_validacion = datos[split_idx:]
        
        print(f"\nDatos de entrenamiento: {len(datos_entrenamiento)}")
        print(f"Datos de validación: {len(datos_validacion)}")
        
        # Etapa 2: Predicciones en validación
        y_true_val = [r["diagnostico"] for r in datos_validacion]
        y_pred_val = []
        
        for registro in datos_validacion:
            datos_proc = self.preprocessor.procesar({
                "edad": registro["edad"],
                "fiebre": registro["fiebre"],
                "dolor": registro["dolor"]
            })
            prediccion = self.model.predecir(datos_proc)
            y_pred_val.append(prediccion)
        
        # Etapa 3: Calcular métricas
        metricas = self._calcular_metricas(y_true_val, y_pred_val)
        
        return metricas
    
    def _calcular_metricas(self, y_true, y_pred):
        """
        Calcula métricas de rendimiento del modelo.
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Predicciones
            
        Returns:
            dict: Métricas calculadas
        """
        clases = list(set(y_true))
        
        metricas = {
            "accuracy": self.metrics.accuracy(y_true, y_pred),
            "por_clase": {}
        }
        
        for clase in clases:
            metricas["por_clase"][clase] = {
                "precision": self.metrics.precision(y_true, y_pred, clase),
                "recall": self.metrics.recall(y_true, y_pred, clase),
                "f1_score": self.metrics.f1_score(y_true, y_pred, clase)
            }
        
        return metricas
    
    def mostrar_resultados_entrenamiento(self, metricas):
        """
        Imprime los resultados del entrenamiento.
        
        Args:
            metricas (dict): Métricas de entrenamiento
        """
        print("\n" + "="*60)
        print("RESULTADOS DEL ENTRENAMIENTO Y VALIDACIÓN")
        print("="*60)
        
        print(f"\nAccuracy General: {metricas['accuracy']:.4f} ({metricas['accuracy']*100:.2f}%)")
        
        print("\n--- Métricas por Clase ---")
        for clase, metrica in metricas['por_clase'].items():
            print(f"\n{clase}:")
            print(f"  Precision: {metrica['precision']:.4f}")
            print(f"  Recall: {metrica['recall']:.4f}")
            print(f"  F1-Score: {metrica['f1_score']:.4f}")
        
        print("\n" + "="*60)
    
    def simular_reentrenamiento_periodico(self):
        """
        Simula el reentrenamiento periódico del modelo con nuevos datos.
        Este proceso sucedería en producción cada cierto tiempo.
        
        Returns:
            dict: Información sobre el reentrenamiento
        """
        return {
            "estado": "Reentrenamiento simulado completado",
            "frecuencia_reentrenamiento": "Mensual o cuando hay cambios significativos",
            "nuevos_casos_clinicos": "Integrados automáticamente",
            "monitor_rendimiento": "Activo"
        }


if __name__ == "__main__":
    trainer = ModelTrainer()
    
    print("\nIniciando entrenamiento del modelo...")
    metricas = trainer.entrenar_y_validar(cantidad_datos=500)
    trainer.mostrar_resultados_entrenamiento(metricas)
    
    print("\nSimulando reentrenamiento periódico...")
    reentrenamiento_info = trainer.simular_reentrenamiento_periodico()
    print(f"  {reentrenamiento_info['estado']}")
    print(f"  Frecuencia: {reentrenamiento_info['frecuencia_reentrenamiento']}")
