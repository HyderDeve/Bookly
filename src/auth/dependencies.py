from fastapi import Request
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.services import UserService
from typing import List
from src.db.models import User
from src.errors import (
    InvalidToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    InsufficientPermission
)

user_service = UserService()

class TokenBearer(HTTPBearer): 
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.validate_token(token):
            raise InvalidToken()
        
        self.verify_token_data(token_data)

        return token_data
    
    def validate_token(self, token:str) -> bool:

        token_data = decode_token(token)

        if token_data is not None:
            return True
        else:
            return False
        

class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self,token_data:dict) -> None:
         
        if token_data and token_data['refresh']: #checking if the token_data is not none & access token is present or not 
            raise AccessTokenRequired() 

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict) -> None:
         
        if token_data and not token_data['refresh']: #checking if the token_data is not none & refresh token is present or not 
            raise RefreshTokenRequired() 
        

async def get_current_user(token_data: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    """
    Get the current authenticated user from the token
    """
    try:
        user_id = token_data['user']['user_id']    

        user = await user_service.get_user_by_id(user_id,session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={'message':"User not found"}
            )
        
        return user
    
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message' : "Invalid token structure: missing user email"}
        )
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions with their original status code and detail
        raise http_exc
    except Exception as e:
        # Log unexpected errors here
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message':str(e)}
        )
    
class RoleChecker:
    def __init__(self, allowed_roles : List[str]) -> None:
        
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user : User = Depends(get_current_user)) -> any:
        
        if current_user.role in self.allowed_roles:

            return True

        raise InsufficientPermission()