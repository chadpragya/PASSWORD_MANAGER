from app import create_app
import uuid

def test_register_and_login():
    app = create_app()
    with app.test_client() as client:
        # Register
        username = f"testuser-{uuid.uuid4()}"
        res = client.post("/api/register", json={"username": username, "master_password": "testpass"})
        assert res.status_code == 201

        # Login
        res = client.post("/api/login", json={"username": username, "master_password": "testpass"})
        assert res.status_code == 200
        assert "access_token" in res.get_json()
