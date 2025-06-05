from fastapi import APIRouter, Depends, HTTPException, status
from .structs import UserCreateModel, UserResponse, UserLoginModel
from .services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, decode_token,verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse


auth_router = APIRouter()
user_service = UserService()  # Create an instance of UserService for handling user operations

REFRESH_TOKEN_EXPIRY = 2

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


@auth_router.post("/login", status_code = status.HTTP_201_CREATED)
async def login_user(login_data:UserLoginModel, session: AsyncSession = Depends(get_session)):
    
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid = verify_password(password, user.password)

        if password_valid:
            access_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_id': str(user.id)
                }
            )

            refresh_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_id': str(user.id)
                },
                refresh = True,
                expiry = timedelta(days = REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "email": user.email,
                        "user_id": str(user.id)
                    }
                }
            )
    
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Email Or Password"
    )
