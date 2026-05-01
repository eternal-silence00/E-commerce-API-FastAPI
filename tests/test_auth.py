import pytest

async def test_register(async_client):
    response = await async_client.post(
        "/auth/register",
        json={"email": "test@test.com", "password":"secret"}
    )
    assert response.status_code == 201
    
async def test_login(async_client):
    response = await async_client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "secret"}
    )
    assert response.status_code == 200
    
async def test_register_duplicate_email(async_client):
    await async_client.post(
        "/auth/register",
        json={"email":"test@test.com", "password":"secret"}
    )
    
    response = await async_client.post(
        "/auth/register",
        json={"email":"test@test.com", "password":"secret"}
    )
    assert response.status_code == 400