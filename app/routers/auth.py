from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.user import UserRepository
from app.services.auth import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/auth/register", response_model=UserResponse, status_code=201)
async def register_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepository(session)
    user = await repo.get_by_email(data.email)
    
    if user:
        raise HTTPException(status_code=400, detail="User already exsists")
    
    hashed_password = hash_password(data.password)
    user = await repo.create(data.email, hashed_password)
    return user
    
@router.post("/auth/login")
async def login_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepository(session)
    user = await repo.get_by_email(data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
        
    