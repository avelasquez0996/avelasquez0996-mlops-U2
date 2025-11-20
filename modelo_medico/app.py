from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.model_utils import load_model
import json
from contextlib import asynccontextmanager

from src.db import engine, SessionLocal
from src.models_db import Base, Prediccion
from src.preprocessor import Preprocessor
from src.schemas import PatientInput, PredictionResponse, PredictionOut
from typing import List

model = None
preprocessor = Preprocessor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global model
    Base.metadata.create_all(bind=engine)
    model = load_model("models/model.pkl")
    yield
    # Shutdown


app = FastAPI(title="API de predicción médica", version="1.0", lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "mensaje": "API de predicción médica",
        "version": "1.0",
        "uso": "POST /predict con JSON {'edad': number, 'fiebre': number, 'dolor': number}",
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientInput, db: Session = Depends(get_db)):
    processed = preprocessor.procesar(patient.model_dump())
    result = model.predecir_con_scores(processed)
    pred = result["prediccion"]
    proba = max(result["scores"].values())

    prediccion = Prediccion(
        paciente_id=json.dumps(patient.model_dump()), prediction=pred, probability=proba
    )
    db.add(prediccion)
    db.commit()
    db.refresh(prediccion)
    return PredictionResponse(resultado=pred, entrada=patient)


@app.get("/predictions", response_model=List[PredictionOut])
def get_predictions(db: Session = Depends(get_db)):
    return db.query(Prediccion).order_by(Prediccion.created_at.desc()).all()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("modelo_medico.app:app", host="0.0.0.0", port=8000, reload=True)
