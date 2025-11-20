from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Prediccion(Base):
    __tablename__ = "prediccion"

    id = Column(Integer, primary_key=True)
    paciente_id = Column(String(50), nullable=False, index=True)
    prediction = Column(String(20), nullable=False)
    probability = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
