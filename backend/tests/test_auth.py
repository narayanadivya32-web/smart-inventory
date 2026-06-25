
from fastapi.testclient import TestClient
from app.routes.main import app

client = TestClient(app)


def test_auth_endpoint_exists():

    response = client.post(
        "/api/auth/token",
        json={
            "username": "testuser",
            "password": "TestPass123!"
        }
    )

    assert response.status_code in [200, 401]