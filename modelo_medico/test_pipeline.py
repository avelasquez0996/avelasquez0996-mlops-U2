
"""
Tests para el nuevo stack de DVC, pandas, MLflow, etc.
"""

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestPipeline:
    def test_model_load(self):
        from src.model_utils import load_model
