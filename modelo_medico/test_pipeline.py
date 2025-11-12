"""
Script de prueba de la API
Valida que todos los módulos funcionen correctamente
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

def test_validator():
    """Prueba el módulo de validación"""
    print("\n" + "="*60)
    print("TEST 1: Validación de Datos")
    print("="*60)
    
    from src.validator import DataValidator
    
    validator = DataValidator()
    
    # Caso válido
    datos_validos = {"edad": 25, "fiebre": 37.5, "dolor": 5}
    resultado = validator.validar(datos_validos)
    print(f"\n✓ Datos válidos: {resultado}")
    assert resultado["valido"], "Datos válidos debería ser True"
    
    # Caso inválido - edad fuera de rango
    datos_invalidos = {"edad": 200, "fiebre": 37.5, "dolor": 5}
    resultado = validator.validar(datos_invalidos)
    print(f"✓ Datos inválidos (edad=200): {resultado}")
    assert not resultado["valido"], "Datos inválidos debería ser False"
    
    # Caso incompleto
    datos_incompletos = {"edad": 25, "fiebre": 37.5}
    resultado = validator.validar(datos_incompletos)
    print(f"✓ Datos incompletos: {resultado}")
    assert not resultado["valido"], "Datos incompletos debería ser False"
    
    print("\n✅ Tests de validación PASADOS")


def test_preprocessor():
    """Prueba el módulo de preprocesamiento"""
    print("\n" + "="*60)
    print("TEST 2: Preprocesamiento de Datos")
    print("="*60)
    
    from src.preprocessor import Preprocessor
    
    preprocessor = Preprocessor()
    
    # Procesar datos
    datos = {"edad": 75, "fiebre": 40, "dolor": 5}
    datos_procesados = preprocessor.procesar(datos)
    
    print(f"\nDatos originales: {datos}")
    print(f"Datos procesados: {datos_procesados}")
    
    # Verificar que están normalizados
    for valor in datos_procesados.values():
        assert 0 <= valor <= 1, f"Valor {valor} no está normalizado"
    
    print("\n✅ Tests de preprocesamiento PASADOS")


def test_model():
    """Prueba el modelo de ML"""
    print("\n" + "="*60)
    print("TEST 3: Modelo de ML")
    print("="*60)
    
    from src.model import MedicalModel
    from src.preprocessor import Preprocessor
    
    model = MedicalModel()
    preprocessor = Preprocessor()
    
    # Test 1: Caso sin enfermedad
    datos = {"edad": 20, "fiebre": 36.5, "dolor": 1}
    datos_proc = preprocessor.procesar(datos)
    prediccion = model.predecir(datos_proc)
    print(f"\nTest 1 - Sin enfermedad (fiebre=36.5, dolor=1):")
    print(f"  Predicción: {prediccion}")
    assert prediccion == "NO ENFERMO", f"Esperaba NO ENFERMO, recibí {prediccion}"
    
    # Test 2: Enfermedad crónica
    datos = {"edad": 60, "fiebre": 39.5, "dolor": 9}
    datos_proc = preprocessor.procesar(datos)
    prediccion = model.predecir(datos_proc)
    print(f"\nTest 2 - Enfermedad crónica (fiebre=39.5, dolor=9):")
    print(f"  Predicción: {prediccion}")
    assert prediccion == "ENFERMEDAD CRÓNICA", f"Esperaba ENFERMEDAD CRÓNICA, recibí {prediccion}"
    
    # Test 3: Enfermedad terminal
    datos = {"edad": 80, "fiebre": 40.5, "dolor": 10}
    datos_proc = preprocessor.procesar(datos)
    prediccion = model.predecir(datos_proc)
    print(f"\nTest 3 - Enfermedad terminal (fiebre=40.5, dolor=10):")
    print(f"  Predicción: {prediccion}")
    assert prediccion == "ENFERMEDAD TERMINAL", f"Esperaba ENFERMEDAD TERMINAL, recibí {prediccion}"
    
    # Test 4: Con scores
    datos = {"edad": 30, "fiebre": 37.5, "dolor": 5}
    datos_proc = preprocessor.procesar(datos)
    resultado = model.predecir_con_scores(datos_proc)
    print(f"\nTest 4 - Con scores (fiebre=37.5, dolor=5):")
    print(f"  Predicción: {resultado['prediccion']}")
    print(f"  Scores: {resultado['scores']}")
    
    print("\n✅ Tests de modelo PASADOS")


def test_data_loader():
    """Prueba el cargador de datos"""
    print("\n" + "="*60)
    print("TEST 4: Cargador de Datos")
    print("="*60)
    
    from src.data_loader import DataLoader
    
    loader = DataLoader()
    
    # Cargar datos
    datos = loader.cargar_datos_sinteticos(cantidad=100)
    print(f"\n✓ Datos sintéticos cargados: {len(datos)} registros")
    
    # Limpiar datos
    datos_limpios = loader.limpiar_datos(datos)
    print(f"✓ Datos limpios: {len(datos_limpios)} registros")
    
    # Anonimizar datos
    datos_anonimos = loader.anonimizar_datos(datos_limpios)
    print(f"✓ Datos anonimizados: {len(datos_anonimos)} registros")
    
    # Obtener datos procesados completos
    datos_procesados = loader.obtener_datos_procesados(cantidad=100)
    print(f"✓ Datos completamente procesados: {len(datos_procesados)} registros")
    
    # Verificar estructura
    if datos_procesados:
        print(f"✓ Estructura de registro: {list(datos_procesados[0].keys())}")
    
    print("\n✅ Tests de cargador de datos PASADOS")


def test_metrics():
    """Prueba el módulo de métricas"""
    print("\n" + "="*60)
    print("TEST 5: Métricas")
    print("="*60)
    
    from src.metrics import ModelMetrics
    
    metrics = ModelMetrics()
    
    # Datos de prueba
    y_true = ["NO ENFERMO", "ENFERMEDAD LEVE", "ENFERMEDAD AGUDA", "ENFERMEDAD CRÓNICA",
              "NO ENFERMO", "ENFERMEDAD LEVE"]
    y_pred = ["NO ENFERMO", "ENFERMEDAD LEVE", "ENFERMEDAD CRÓNICA", "ENFERMEDAD CRÓNICA",
              "NO ENFERMO", "ENFERMEDAD AGUDA"]
    
    # Calcular accuracy
    acc = metrics.accuracy(y_true, y_pred)
    print(f"\n✓ Accuracy: {acc:.4f} ({acc*100:.2f}%)")
    
    # Calcular métricas por clase
    clase = "NO ENFERMO"
    prec = metrics.precision(y_true, y_pred, clase)
    rec = metrics.recall(y_true, y_pred, clase)
    f1 = metrics.f1_score(y_true, y_pred, clase)
    
    print(f"✓ Métricas para '{clase}':")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall: {rec:.4f}")
    print(f"  F1-Score: {f1:.4f}")
    
    print("\n✅ Tests de métricas PASADOS")


def test_api():
    """Prueba básica de la API Flask"""
    print("\n" + "="*60)
    print("TEST 6: API Flask")
    print("="*60)
    
    from app import app
    
    client = app.test_client()
    
    # Test GET /
    response = client.get("/")
    print(f"\n✓ GET / → Status: {response.status_code}")
    assert response.status_code == 200, "GET / debería retornar 200"
    
    # Test POST /predecir - Caso válido
    datos = {"edad": 20, "fiebre": 36.2, "dolor": 9}
    response = client.post("/predecir", json=datos)
    print(f"✓ POST /predecir (válido) → Status: {response.status_code}")
    assert response.status_code == 200, "POST válido debería retornar 200"
    
    respuesta = response.get_json()
    print(f"  Resultado: {respuesta['resultado']}")
    print(f"  Entrada: {respuesta['entrada']}")
    
    # Test POST /predecir - Datos inválidos
    datos_invalidos = {"edad": 200, "fiebre": 36.2, "dolor": 9}
    response = client.post("/predecir", json=datos_invalidos)
    print(f"✓ POST /predecir (inválido) → Status: {response.status_code}")
    assert response.status_code == 400, "POST inválido debería retornar 400"
    
    # Test POST /predecir - Faltan campos
    datos_incompletos = {"edad": 20}
    response = client.post("/predecir", json=datos_incompletos)
    print(f"✓ POST /predecir (incompleto) → Status: {response.status_code}")
    assert response.status_code == 400, "POST incompleto debería retornar 400"
    
    print("\n✅ Tests de API PASADOS")


def test_estadisticas():
    """Prueba el módulo de estadísticas"""
    print("\n" + "="*60)
    print("TEST 7: Estadísticas de Predicciones")
    print("="*60)
    
    from app import app, estadisticas
    
    # Limpiar estadísticas previas
    estadisticas.limpiar_estadisticas()
    
    client = app.test_client()
    
    # Verificar estadísticas iniciales vacías
    response = client.get("/estadisticas")
    print(f"\n✓ GET /estadisticas (inicial) → Status: {response.status_code}")
    assert response.status_code == 200
    
    stats = response.get_json()
    print(f"  Total predicciones: {stats['total_predicciones']}")
    assert stats['total_predicciones'] == 0, "Debería haber 0 predicciones inicialmente"
    
    # Realizar 3 predicciones
    datos_tests = [
        {"edad": 20, "fiebre": 36.2, "dolor": 1, "esperado": "NO ENFERMO"},
        {"edad": 45, "fiebre": 38.5, "dolor": 7, "esperado": "ENFERMEDAD AGUDA"},
        {"edad": 80, "fiebre": 40.5, "dolor": 10, "esperado": "ENFERMEDAD TERMINAL"}
    ]
    
    for datos in datos_tests:
        response = client.post("/predecir", json={
            "edad": datos["edad"],
            "fiebre": datos["fiebre"],
            "dolor": datos["dolor"]
        })
        assert response.status_code == 200
    
    # Verificar estadísticas después de predicciones
    response = client.get("/estadisticas")
    stats = response.get_json()
    
    print(f"\n✓ Después de 3 predicciones:")
    print(f"  Total predicciones: {stats['total_predicciones']}")
    print(f"  Conteos por categoría: {stats['por_categoria']}")
    print(f"  Últimas 5: {len(stats['ultimas_5_predicciones'])} registradas")
    print(f"  Última predicción: {stats['ultima_prediccion']}")
    
    assert stats['total_predicciones'] == 3, "Debería haber 3 predicciones"
    assert len(stats['ultimas_5_predicciones']) == 3, "Debería haber 3 en últimas 5"
    assert stats['ultima_prediccion'] is not None, "Debería haber última predicción"
    
    print("\n✅ Tests de estadísticas PASADOS")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("PRUEBAS COMPLETAS DEL PIPELINE MLOps")
    print("="*60)
    
    try:
        test_validator()
        test_preprocessor()
        test_model()
        test_data_loader()
        test_metrics()
        test_api()
        test_estadisticas()
        
        print("\n" + "="*60)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("="*60 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ ERROR EN LOS TESTS: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
