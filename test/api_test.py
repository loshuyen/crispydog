from fastapi.testclient import TestClient
from fastapi import Depends
from routers.user import get_auth_user
from app import app

client = TestClient(app)

def test_fetch_products():
    response = client.get("/api/products")
    assert response.status_code == 200

def test_fetch_reviews():
    response = client.get("/api/reviews/product/1?page=0")
    assert response.status_code == 200
    response = client.get("/api/reviews/product/2")
    assert response.status_code == 422

