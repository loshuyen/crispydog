from fastapi.testclient import TestClient
from routers import user
from app import app
from unittest.mock import patch
from datetime import datetime

client = TestClient(app)

def test_generate_token():
    with patch("datetime.datetime") as mock_time:
        mock_time.now.return_value = datetime(2024, 10, 10, 9, 10, 15)
        mock_time.timestamp = datetime.timestamp
        assert user.generate_token({"id": 1, "username": "test_user"}) == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3MjkxMjc0MTV9.oL-Rz9dqi-pE6mdXNLnQ4wVu9hyALHkq2ckZFJjdySQ"
        assert user.generate_token({"id": 5, "username": "user_2"}) == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwidXNlcm5hbWUiOiJ1c2VyXzIiLCJleHAiOjE3MjkxMjc0MTV9.PjvMhyoEl6axVHBblR-sgcW1z5mTgtej-QPTdYNXg4A"

def mock_get_auth_user_success():
    return {"id": 1, "username": "test_user"}

def mock_get_auth_user_failure():
    return None

def override(old_dependency, new_dependency):
    def deco(cb):
        def wrapper():
            app.dependency_overrides[old_dependency] = new_dependency
            cb()
            app.dependency_overrides = {}
        return wrapper
    return deco

@override(user.get_auth_user, mock_get_auth_user_success)
def test_get_current_user_success():
    response = client.get("/api/user/auth")
    assert response.json() == {"data": {"id": 1, "username": "test_user"}}

@override(user.get_auth_user, mock_get_auth_user_failure)
def test_get_current_user_failure():
    response = client.get("/api/user/auth")
    assert response.json() == {"data": None}

def test_login_success():
    with patch("database.user.verify_password") as mock_verify_password, patch("routers.user.generate_token") as mock_generate_token:
        mock_verify_password.return_value = {"id": 1, "username": "test_user"}
        mock_generate_token.return_value = "test_token"
        response = client.put("/api/user/auth", json={"username": "test_user", "password": "test_password"})
        assert response.json() == {"token": "test_token"}

def test_login_failure():
    with patch("database.user.verify_password") as mock_verify_password:
        mock_verify_password.return_value = None
        response = client.put("/api/user/auth", json={"username": "test_user", "password": "test_password"})
        assert response.json() == {"error": True, "message": "登入失敗，Email、密碼錯誤或尚未註冊"}


