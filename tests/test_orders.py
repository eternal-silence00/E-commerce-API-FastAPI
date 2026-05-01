import pytest

async def test_create_order_unauthorized(async_client):
    response = await async_client.post(
        "/orders",
        json={"items":[{"product_id": 1, "quantity":2}]}
    )
    assert response.status_code == 401
    
async def test_get_orders_unauthorized(async_client):
    response = await async_client.get(
        "/orders"
    )
    assert response.status_code == 401