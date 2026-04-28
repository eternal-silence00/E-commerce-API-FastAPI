from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_id(self, product_id:int):
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()
    
    async def get_all(self, category:str=None):
        if category:
            result = await self.session.execute(select(Product).where(Product.category == category))
            return result.scalars().all()
        else:
            result = await self.session.execute(select(Product))
            return result.scalars().all()
    
    async def create(self, name:str, description: str, price: float, stock: int, category: str):
        product = Product(
            name = name,
            description = description, 
            price = price, 
            stock = stock, 
            category = category
        )
        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)
        return product 