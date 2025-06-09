from fastapi import Request
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.services import UserService


class TokenBearer(HTTPBearer): 
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.validate_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )
        
        self.verify_token_data(token_data)

        return token_data
    
    def validate_token(self, token:str) -> bool:

        token_data = decode_token(token)

        if token_data is not None:
            return True
        else:
            return False
    
    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Override This Method In Child Classes.")


class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self,token_data:dict) -> None:
         
        if token_data and token_data['refresh']: #checking if the token_data is not none & access token is present or not 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide a valid access token",
            ) 

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict) -> None:
         
        if token_data and not token_data['refresh']: #checking if the token_data is not none & refresh token is present or not 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide a valid refresh token",
            ) 




async def get_current_user(
    token_data: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Get the current authenticated user from the token
    """
    try:
        user_service = UserService()
        user_id = token_data.get('user', {}).get('user_id')
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token"
            )
            
        user = await user_service.get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

async def role_checker(
    token_data: dict = Depends(AccessTokenBearer())
) -> bool:
    """
    Check if the user has the required role
    """
    try:
        user_data = token_data.get('user', {})
        user_role = user_data.get('role')
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role not found in token"
            )
        
        # Add your role-based logic here
        # For example, checking if user is admin
        if user_role not in ['admin', 'user']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid role"
            )
            
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )