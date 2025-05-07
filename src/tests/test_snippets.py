import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from models.user import User
from models.snippet import Snippet
from services.auth_service import register_user, authenticate_user
from core.security import get_password_hash

@pytest.fixture
async def test_user():
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    user = await register_user(user_data)
    return user

@pytest.fixture
async def authenticated_client(test_user: User):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/auth/login", data={
            "username": test_user.username,
            "password": "testpassword"
        })
        token = response.json().get("access_token")
        client.headers.update({"Authorization": f"Bearer {token}"})
        yield client
