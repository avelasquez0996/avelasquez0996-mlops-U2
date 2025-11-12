"""
Tests del Pipeline MLOps usando pytest
10 tests sobre los elementos más importantes del aplicativo
"""

import pytest
import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture(autouse=True)
def limpiar_estadisticas():
    """Limpiar estadísticas antes y después de cada test"""
    try:
        from src.estadisticas import EstadisticasPredicciones
        stats = EstadisticasPredicciones()
        if Path(stats.ARCHIVO_STATS).exists():
            os.remove(stats.ARCHIVO_STATS)
        yield
        if Path(stats.ARCHIVO_STATS).exists():
            os.remove(stats.ARCHIVO_STATS)
    except Exception:
        yield


@pytest.fixture
def app_client():
    """Fixture para cliente de prueba Flask"""
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class Tests:
    """Tests sobre los elementos más importantes del aplicativo"""
    
    def validacion_datos_validos(self):
        """TEST 1: Validar que los datos válidos pasan la validación"""
        from src.validator import DataValidator
        
        validator = DataValidator()
        resultado = validator.validar({"edad": 30, "fiebre": 37.5, "dolor": 5})
        
        assert resultado["valido"] is True
    
    def validacion_edad_fuera_rango(self):
        """TEST 2: Rechazar edad fuera de rango [0-150]"""
        from src.validator import DataValidator
        
        validator = DataValidator()
        resultado = validator.validar({"edad": 200, "fiebre": 37.5, "dolor": 5})
        
        assert resultado["valido"] is False
    
    def preprocesamiento_normalizacion(self):
        """TEST 3: Preprocesar datos normalizándolos a [0, 1]"""
        from src.preprocessor import Preprocessor
        
        preprocessor = Preprocessor()
        datos_proc = preprocessor.procesar({"edad": 75, "fiebre": 40, "dolor": 5})
        
        # Verificar que todos los valores están en [0, 1]
        assert all(0 <= v <= 1 for v in datos_proc.values())
    
    def modelo_5_categorias(self):
        """TEST 4: Modelo predice 5 categorías incluyendo ENFERMEDAD TERMINAL"""
        from src.model import MedicalModel
        
        model = MedicalModel()
        assert len(model.CATEGORIAS) == 5
        assert "ENFERMEDAD TERMINAL" in model.CATEGORIAS
    
    def modelo_prediccion_correcta(self):
        """TEST 5: Modelo predice correctamente para casos extremos"""
        from src.model import MedicalModel
        from src.preprocessor import Preprocessor
        
        model = MedicalModel()
        preprocessor = Preprocessor()
        
        # Caso extremo: valores máximos → ENFERMEDAD TERMINAL
        datos_proc = preprocessor.procesar({"edad": 150, "fiebre": 45, "dolor": 10})
        prediccion = model.predecir(datos_proc)
        
        assert prediccion == "ENFERMEDAD TERMINAL"
    
    def api_endpoint_post_predecir(self, app_client):
        """TEST 6: API endpoint POST /predecir funciona correctamente"""
        datos = {"edad": 30, "fiebre": 37.5, "dolor": 5}
        response = app_client.post("/predecir", json=datos)
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert "resultado" in json_data
        assert "entrada" in json_data
    
    def api_validacion_entrada(self, app_client):
        """TEST 7: API rechaza datos inválidos (edad fuera de rango)"""
        datos_invalidos = {"edad": 200, "fiebre": 37.5, "dolor": 5}
        response = app_client.post("/predecir", json=datos_invalidos)
        
        assert response.status_code == 400
    
    def estadisticas_registro_prediccion(self):
        """TEST 8: Registrar predicción en estadísticas"""
        from src.estadisticas import EstadisticasPredicciones
        
        stats = EstadisticasPredicciones()
        stats.limpiar_estadisticas()
        
        stats.registrar_prediccion(30, 37.5, 5, "NO ENFERMO")
        resultado = stats.obtener_estadisticas()
        
        assert resultado["total_predicciones"] == 1
        assert resultado["por_categoria"]["NO ENFERMO"] == 1
    
    def estadisticas_endpoint_get(self, app_client):
        """TEST 9: API endpoint GET /estadisticas retorna estadísticas"""
        # Hacer una predicción
        datos = {"edad": 30, "fiebre": 37.5, "dolor": 5}
        app_client.post("/predecir", json=datos)
        
        # Obtener estadísticas
        response = app_client.get("/estadisticas")
        
        assert response.status_code == 200
        stats = response.get_json()
        assert "total_predicciones" in stats
        assert "por_categoria" in stats
        assert "ultimas_5_predicciones" in stats
    
    def pipeline_completo_end_to_end(self, app_client):
        """TEST 10: Pipeline completo: validar → procesar → predecir → registrar"""
        # Realizar múltiples predicciones con diferentes categorías
        test_cases = [
            {"edad": 20, "fiebre": 36.2, "dolor": 1},
            {"edad": 45, "fiebre": 38.5, "dolor": 7},
            {"edad": 150, "fiebre": 45, "dolor": 10},
        ]
        
        for datos in test_cases:
            response = app_client.post("/predecir", json=datos)
            assert response.status_code == 200
        
        # Verificar que se registraron las 3 predicciones
        response = app_client.get("/estadisticas")
        stats = response.get_json()
        assert stats["total_predicciones"] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
