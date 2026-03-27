from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_health_returns_status_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_healthy_json():
    response = client.get("/health")
    assert response.json() == {"status": "healthy"}
