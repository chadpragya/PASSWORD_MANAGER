import pytest
from app.app import create_app
import uuid

@pytest.fixture
def test_client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_store_and_retrieve_password(test_client):
    # Register and login
    register_headers = {"Content-Type": "application/json"}
    username = f"user-{uuid.uuid4()}"
    register_res = test_client.post("/api/register", json={"username": username, "master_password": "pass"}, headers=register_headers)
    assert register_res.status_code == 201

    login_res = test_client.post("/api/login", json={"username": username, "master_password": "pass"}, headers=register_headers)
    assert login_res.status_code == 200
    token = login_res.get_json()["access_token"]

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "X-Master-Password": "pass"}

    # Store password
    res = test_client.post("/api/passwords", json={"site": "gmail", "username": "testuser", "password": "secret123"}, headers=headers)
    assert res.status_code == 201

    # Retrieve password
    res = test_client.get("/api/passwords", headers=headers)
    assert res.status_code == 200
    passwords = res.get_json()
    for p in passwords:
        if p["site"] == "gmail":
            assert p["password"] == "secret123"
            break
    else:
        assert False, "Gmail password not found"
