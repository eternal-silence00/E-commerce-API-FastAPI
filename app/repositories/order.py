from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order, OrderItem

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(self, user_id: int, items: list, total: float):
        order = Order(user_id=user_id,status = "pending", total = total)
        self.session.add(order)
        await self.session.flush()
        
        for item in items:
            order_item = OrderItem(
                order_id = order.id,
                product_id = item.product_id,
                quantity = item.quantity,
                price = item.price
            )
            self.session.add(order_item)
            
        await self.session.flush()
        await self.session.refresh(order)
        return order
    
    async def get_by_id(self, order_id: int):
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()
    
    async def get_user_orders(self, user_id: int):
        result = await self.session.execute(select(Order).where(Order.user_id == user_id))
        return result.scalars().all()
    
    async def update_status(self, order_id, status):
        order = await self.session.get(Order, order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        order.status = status
        await self.session.flush()
        await self.session.refresh(order)
        return order
        