from fastapi import Request
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token


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

