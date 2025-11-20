from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PatientInput(BaseModel):
    edad: float = Field(..., ge=0, le=150)
    fiebre: float = Field(..., ge=35, le=45)
    dolor: float = Field(..., ge=0, le=10)

class PredictionResponse(BaseModel):
    resultado: str
    entrada: PatientInput

class PredictionOut(BaseModel):
    id: int
    paciente_id: str
    prediction: str
    probability: float
    created_at: Optional[datetime] = None