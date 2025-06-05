from pydantic import BaseModel, Field
import datetime
import uuid


class UserCreateModel(BaseModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)



class UserResponse(BaseModel):
    id : uuid.UUID
    username : str
    password : str 
    email:str  
    first_name:str
    last_name:str
    is_verified:bool
    created_at: datetime 
    updated_at: datetime 
