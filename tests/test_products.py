from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    response = client.post(
        "/api/auth/token",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    return response.json()["access_token"]


def test_products_endpoint():

    token = get_token()

    response = client.get(
        "/api/products",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)