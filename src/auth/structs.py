from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import List
from src.db.models import Book  # As Book model is defined in src/books/models.py
from src.reviews.structs import ReviewResponse


class UserCreateModel(BaseModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)



class UserResponse(BaseModel):
    id : uuid.UUID
    username : str
    email:str
    password : str = Field(exclude=True)
    first_name:str
    last_name:str
    role : str
    is_verified:bool
    created_at: datetime 
    updated_at: datetime 


class UserBooks(UserResponse):
    books : List[Book]
    reviews : List[ReviewResponse]


class UserLoginModel(BaseModel):
    email: str
    password: str

class EmailRequest(BaseModel):
    addresses : List[str]

class PasswordResetRequest(BaseModel):
    email : str