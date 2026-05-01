from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse
from app.services.auth import get_current_user
import json
import redis.asyncio as redis
import os

redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses = True
)

router = APIRouter()

@router.get("/products")
async def get_products(
    category: str = None,
    session: AsyncSession = Depends(get_db),
):  
    cache_key = f"products:{category or 'all'}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    repo = ProductRepository(session)
    result = await repo.get_all(category)
    
    result_dict = [ProductResponse.model_validate(p).model_dump(mode="json") for p in result]
    await redis_client.set(cache_key, json.dumps(result_dict), ex=300)
    
    return result_dict

@router.get("/products/{id}")
async def get_product_by_id(
    id:int,
    session: AsyncSession = Depends(get_db)
):
    cache_key = f"product:{id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = ProductRepository(session)
    result = await repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    
    result_dict = ProductResponse.model_validate(result).model_dump(mode='json')
    await redis_client.set(cache_key, json.dumps(result_dict), ex=300)
    
    return result_dict

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

    