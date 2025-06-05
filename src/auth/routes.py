from fastapi import APIRouter, Depends, HTTPException, status
from .structs import UserCreateModel


auth_router = APIRouter()


@auth_router.post("/signup")
async def create_user(user_data: UserCreateModel):
    pass 