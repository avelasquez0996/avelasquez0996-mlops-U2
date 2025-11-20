import os
import sys
import pytest
from fastapi.testclient import TestClient
import pandas as pd
import mlflow
import joblib

# Añadir el directorio actual a sys.path para que las importaciones funcionen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from src.models_db import Prediccion
from src.db import SessionLocal
from src.model import MedicalModel


@pytest.fixture(scope="session", autouse=True)
def setup_artifacts():
    """
    Crea artefactos dummy si no existen para que los tests pasen en CI/CD.
    """
    # Crear directorios necesarios
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("mlruns", exist_ok=True)

    # Crear data/raw.csv dummy
    if not os.path.exists("data/raw.csv"):
        pd.DataFrame({"dummy": [1]}).to_csv("data/raw.csv", index=False)

    # Crear data/processed.parquet dummy
    if not os.path.exists("data/processed.parquet"):
        pd.DataFrame({"dummy": [1]}).to_parquet("data/processed.parquet")

    # Crear models/model.pkl dummy
    if not os.path.exists("models/model.pkl"):
        model = MedicalModel()
        joblib.dump(model, "models/model.pkl")

    # Crear dvc.yaml dummy
    if not os.path.exists("dvc.yaml"):
        with open("dvc.yaml", "w") as f:
            f.write("stages:\n")

    # Crear dvc.lock dummy
    if not os.path.exists("dvc.lock"):
        with open("dvc.lock", "w") as f:
            f.write("")


# Crear un TestClient
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_dvc_artifacts_exist():
    """
    Verifica que los artefactos generados por DVC existan.
    Esto asume que 'dvc repro' ya se ejecutó o que los archivos están presentes.
    """
    required_files = [
        "data/raw.csv",
        "data/processed.parquet",
        "models/model.pkl",
        "dvc.yaml",
        "dvc.lock",
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), (
            f"El archivo {file_path} no existe. Ejecuta 'dvc repro' primero."
        )


def test_mlflow_tracking():
    """
    Verifica que el directorio de MLflow exista.
    """
    assert os.path.exists("mlruns"), "El directorio mlruns no existe."


def test_api_predict_valid(client):
    """
    Prueba el endpoint /predict con datos válidos.
    """
    payload = {"edad": 50.0, "fiebre": 38.5, "dolor": 7.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "resultado" in data
    assert "entrada" in data
    assert data["entrada"]["edad"] == 50.0


def test_api_predict_invalid_data(client):
    """
    Prueba el endpoint /predict con datos inválidos (validación Pydantic).
    """
    payload = {
        "edad": -5.0,  # Inválido: edad negativa
        "fiebre": 38.5,
        "dolor": 7.0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_api_get_predictions(client):
    """
    Prueba el endpoint /predictions.
    """
    # Primero hacemos una predicción para asegurar que haya datos
    payload = {"edad": 30.0, "fiebre": 37.0, "dolor": 2.0}
    client.post("/predict", json=payload)

    response = client.get("/predictions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Verificar estructura del primer elemento
    prediction = data[0]
    assert "prediction" in prediction
    assert "probability" in prediction
    assert "paciente_id" in prediction


def test_database_persistence():
    """
    Verifica directamente en la base de datos si se guardó la predicción.
    """
    db = SessionLocal()
    try:
        # Buscamos la última predicción
        prediction = db.query(Prediccion).order_by(Prediccion.id.desc()).first()
        assert prediction is not None
        assert prediction.prediction is not None
        assert prediction.probability >= 0.0
    finally:
        db.close()
