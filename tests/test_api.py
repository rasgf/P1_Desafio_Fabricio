import os
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"
from sensor_api.main import app

client = TestClient(app)

# TDD: Test-Driven Development (Testando API)
def test_criar_leitura_postura_correta():
    payload = {"dispositivo_id": "ESP-01", "distancia_cm": 50.0}
    response = client.post("/leituras", json=payload)
    assert response.status_code == 201
    assert response.json()["postura_correta"] == True

def test_criar_leitura_postura_incorreta():
    # Pela regra de negócio no Use Case, distancia < 10 é False
    payload = {"dispositivo_id": "ESP-01", "distancia_cm": 8.0}
    response = client.post("/leituras", json=payload)
    assert response.status_code == 201
    assert response.json()["postura_correta"] == False
