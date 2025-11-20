"""
Script de entrenamiento y validación del modelo.
Etapas 4-5 del pipeline: Entrenamiento, validación y pruebas
"""

import pandas as pd
import yaml
from src.model_utils import save_model
import os
import numpy as np
from sklearn.model_selection import train_test_split
import mlflow
 
from src.model import MedicalModel
from src.metrics import ModelMetrics


class ModelTrainer:
    """Entrena y valida el modelo de ML"""
    
    def __init__(self):
        self.model = MedicalModel()
        self.metrics = ModelMetrics()
    
    def entrenar_y_validar(self):
        """
        Entrena el modelo con datos procesados y lo valida.
        """
        # Load params
        with open('params.yaml', 'r') as f:
            params_dict = yaml.safe_load(f)
        test_size = params_dict['train']['test_size']
        random_state = params_dict['train']['random_state']
        
        # Load processed data
        df = pd.read_parquet('data/processed.parquet')
        
        # Features and labels
        X = df[['edad_norm', 'fiebre_norm', 'dolor_norm']]
        y = df['diagnostico']
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        mlflow.log_param("n_samples", len(df))
        mlflow.log_param("n_train", len(X_train))
        mlflow.log_param("n_test", len(X_test))
        
        print(f"\nDatos de entrenamiento: {len(X_train)}")
        print(f"Datos de validación: {len(X_test)}")
        
        # Predictions
        y_pred_val = []
        for _, row in X_test.iterrows():
            datos_proc = {
                "edad": row['edad_norm'],
                "fiebre": row['fiebre_norm'],
                "dolor": row['dolor_norm']
            }
            prediccion = self.model.predecir(datos_proc)
            y_pred_val.append(prediccion)
        
        # Metrics
        y_true_val = y_test.tolist()
        metricas = self._calcular_metricas(y_true_val, y_pred_val)
        
        self.mostrar_resultados_entrenamiento(metricas)
        
        return metricas
    
    def _calcular_metricas(self, y_true, y_pred):
        """
        Calcula métricas de rendimiento del modelo.
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
        """
        print("RESULTADOS DEL ENTRENAMIENTO Y VALIDACIÓN")
        
        print(f"\nAccuracy General: {metricas['accuracy']:.4f} ({metricas['accuracy']*100:.2f}%)")
        
        print("\n Métricas por Clase ")
        for clase, metrica in metricas['por_clase'].items():
            print(f"\n{clase}:")
            print(f"  Precision: {metrica['precision']:.4f}")
            print(f"  Recall: {metrica['recall']:.4f}")
            print(f"  F1-Score: {metrica['f1_score']:.4f}")
    
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
    mlflow.set_tracking_uri("./mlruns")
    with open('params.yaml', 'r') as f:
        params_dict = yaml.safe_load(f)
    with mlflow.start_run():
        mlflow.log_params(params_dict['train'])
        mlflow.log_param("raw.max_samples", params_dict['raw']['max_samples'])
        
        trainer = ModelTrainer()
        
        print("\nIniciando entrenamiento del modelo...")
        metricas = trainer.entrenar_y_validar()
        
        # Log metrics
        mlflow.log_metric("accuracy", metricas['accuracy'])
        for clase, metrica in metricas['por_clase'].items():
            mlflow.log_metric(f"precision_{clase}", metrica['precision'])
            mlflow.log_metric(f"recall_{clase}", metrica['recall'])
            mlflow.log_metric(f"f1_{clase}", metrica['f1_score'])
        
        # Save model
        os.makedirs('models', exist_ok=True)
        save_model(trainer.model, 'models/model.pkl')
        print("Modelo guardado en models/model.pkl")
        mlflow.log_artifact("models/model.pkl", "model")
        
        print("\nSimulando reentrenamiento periódico...")
        reentrenamiento_info = trainer.simular_reentrenamiento_periodico()
        print(f"  {reentrenamiento_info['estado']}")
        print(f"  Frecuencia: {reentrenamiento_info['frecuencia_reentrenamiento']}")
