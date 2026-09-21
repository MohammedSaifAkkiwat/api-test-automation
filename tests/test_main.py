import pytest
from fastapi.testclient import TestClient

from app.main import app, users

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_users():
    users.clear()
    yield
    users.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user():
    payload = {
        "username": "saif",
        "email": "saif@example.com",
        "age": 22
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 201
    assert response.json() == payload


def test_duplicate_email():
    payload = {
        "username": "saif",
        "email": "saif@example.com",
        "age": 22
    }

    client.post("/users", json=payload)
    response = client.post("/users", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_get_existing_user():
    payload = {
        "username": "saif",
        "email": "saif@example.com",
        "age": 22
    }

    client.post("/users", json=payload)
    response = client.get("/users/saif")

    assert response.status_code == 200
    assert response.json() == payload


def test_get_missing_user():
    response = client.get("/users/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_valid_login():
    response = client.post(
        "/login",
        params={"username": "tester", "password": "test123"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"


def test_invalid_login():
    response = client.post(
        "/login",
        params={"username": "tester", "password": "wrong"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_invalid_user_input():
    payload = {
        "username": "saif",
        "email": "saif@example.com",
        "age": "not-a-number"
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 422