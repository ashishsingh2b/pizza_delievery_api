from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] 
    is_active: Optional[bool]
    
    class Config:
        from_attrs = True
        json_schema_extra = {
            'example': {
                "id": 1,
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": False,
            }
        }
        

class Settings(BaseModel):
    authjwt_secret_key:str='802d528c5fc14a171a597fc10e0621a2d837a0fb8c50b78a396f637e2284ffd5'

class LoginModel(BaseModel):
    username : str
    password : str

class OrderModel(BaseModel):
    id :Optional[int]
    quantity :int
    order_status :Optional[str] = "PENDING"
    pizza_size :Optional[str] = "SMALL"
    user_id :Optional[int]
    
    class Config:
        from_attrs = True
        json_schema_extra = {
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }

class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"
    
    class Config:
        from_attrs = True
        json_schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }