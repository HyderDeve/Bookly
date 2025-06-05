from fastapi import APIRouter, Depends, HTTPException, status
from .structs import UserCreateModel, UserResponse
from .services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


auth_router = APIRouter()
user_service = UserService()  # Create an instance of UserService for handling user operations


@auth_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel,session: AsyncSession = Depends(get_session)):
    
    email = user_data.email 

    user_exists = await user_service.user_exists(email, session)  # Check if the user already exists in the database

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists."
        )
    
    new_user = await user_service.create_user(user_data,session)

    return new_user