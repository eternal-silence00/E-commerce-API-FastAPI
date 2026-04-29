from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/products")
async def get_products(
    category: str = None,
    session: AsyncSession = Depends(get_db),
):  
    repo = ProductRepository(session)
    result = await repo.get_all(category)
    return result 

@router.get("/products/{id}")
async def get_product_by_id(
    id:int,
    session: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(session)
    result = await repo.get_by_id(id)
    return result 

@router.post('/products', response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
): 
        repo = ProductRepository(session)
        product = await repo.create(
            data.name,
            data.description,
            data.price,
            data.stock,
            data.category
        )
        return product

    