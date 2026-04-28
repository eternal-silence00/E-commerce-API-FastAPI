from pydantic import BaseModel
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id:int
    quantity:int
    
class OrderCreate(BaseModel):
    items:list[OrderItemCreate]
    
class OrderResponse(BaseModel):
    id:int
    status:str
    total:float
    created_at:datetime
    
    class Config:
        from_attributes = True