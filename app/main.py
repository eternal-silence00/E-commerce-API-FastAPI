from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import auth, orders, products
from app.database import engine
from app.models.user import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
        
        
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(products.router)