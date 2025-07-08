from fastapi import status, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from typing import Any, Callable

class BooklyException(Exception):
    pass

class InvalidToken(BooklyException):
    """User has provided an Invalid Token"""
    pass

class RevokedToken(BooklyException):
    """User has provided a Revoked Token"""
    pass

class AccessTokenRequired(BooklyException):
    """User has not provided an Access Token"""
    pass

class RefreshTokenRequired(BooklyException):
    """User has not provided a Refresh Token"""
    pass

class UserAlreadyExists(BooklyException):
    """User with the provided email already exists"""
    pass

class InsufficientPermission(BooklyException):
    """User does not have sufficient permissions to perform this action"""
    pass

class BookNotFound(BooklyException):
    """Book with provided ID does not exist"""
    pass

class UserNotFound(BooklyException):
    """User with provided ID does not exist"""
    pass

class TagNotFound(BooklyException):
    """Tag with provided ID does not exist"""
    pass


def create_error_handler(status_code : int , initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:

    async def error_handler(request: Request, exc: BooklyException):

        return JSONResponse(
            status_code = status_code,
            content = initial_detail
        )
    
    return error_handler # returns the result of the async func just created