from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.order import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    data: OrderCreate,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    repo = OrderRepository(session)
    order = await repo.create(
        user.id,
        data.items,
        total=0
    )
    return order

@router.get("/orders")
async def get_orders(
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    repo = OrderRepository(session)
    result = await repo.get_user_orders(user.id)
    return result 

@router.patch("/orders/{id}/status", response_model=OrderResponse, status_code=200)
async def order_status_patch(
    id: int,
    status: str,
    session: AsyncSession = Depends(get_db)
):
    repo = OrderRepository(session)
    order = await repo.update_status(id, status)
    return order