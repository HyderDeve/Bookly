from fastapi import APIRouter, Depends, HTTPException, status
from .structs import UserCreateModel, UserResponse, UserLoginModel
from .services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, decode_token,verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse
from .dependencies import AccessTokenBearer, RefreshTokenBearer
from datetime import datetime, timedelta
from src.db.redis import add_jti_to_blocklist


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


@auth_router.get("/refresh-token")
async def access_token(token_details:dict = Depends(RefreshTokenBearer())):

    """
    Endpoint to refresh the access token using a valid refresh token.
    
    """

    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
        user_data = token_details['user']
        )
        return JSONResponse(content={
                "message": "Access token refreshed successfully.",
                "access_token": new_access_token
            })
    
    raise HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired refresh token."
    )

    return {}


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def revoke_token(token_details:dict = Depends(AccessTokenBearer)):
    
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            'message': 'Logout Successfully'
        }
    )