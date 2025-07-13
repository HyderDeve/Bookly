from fastapi import status, FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from typing import Any, Callable

class BooklyException(Exception):
    pass

class InvalidToken(BooklyException):
    """User has provided an Invalid Token"""
    pass

class InvalidCredentials(BooklyException):
    """Invalid Email or Password"""
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


class TagAlreadyExists(BooklyException):
    """Tag with provided ID already exists"""
    pass

def create_error_handler(status_code : int , initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:

    async def error_handler(request: Request, exc: BooklyException):

        return JSONResponse(
            status_code = status_code,
            content = initial_detail
        )
    
    return error_handler # returns the result of the async func just created




def register_all_errors(app : FastAPI):

    
    app.add_exception_handler(
        UserAlreadyExists,
        create_error_handler(
            status_code = status.HTTP_403_FORBIDDEN,
            initial_detail = {
                'message' : 'User with email already exists'
            }
        )
    )


    app.add_exception_handler(
        UserNotFound,
        create_error_handler(
            status_code = status.HTTP_404_NOT_FOUND,
            initial_detail = {
                'message' : 'User not found'
            }
        )
    )


    app.add_exception_handler(
        BookNotFound,
        create_error_handler(
            status_code = status.HTTP_404_NOT_FOUND,
            initial_detail = {
                'message' : 'Book not found'
            }
        )
    )

    app.add_exception_handler(
        TagNotFound,
        create_error_handler(
            status_code = status.HTTP_404_NOT_FOUND,
            initial_detail = {
                'message' : 'Tag not found'
            }
        )
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_error_handler(
            status_code = status.HTTP_403_FORBIDDEN,
            initial_detail = {
                'message' : 'Tag already exists'
            }
        )
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_error_handler(
            status_code = status.HTTP_400_BAD_REQUEST,
            initial_detail = {
                'message' : 'Invalid Email or Password'
            }
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_error_handler(
            status_code = status.HTTP_403_FORBIDDEN,
            initial_detail = {
                'message' : 'Token is invalid or expired'
            }
        )
    )

    app.add_exception_handler(
        RevokedToken,
        create_error_handler(
            status_code = status.HTTP_401_UNAUTHORIZED,
            initial_detail = {
                'message' : 'Token is either expired or has been revoked'
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_error_handler(
            status_code = status.HTTP_403_FORBIDDEN,
            initial_detail = {
                'message' : 'Please provide a valid access token',
                'Resolution' : 'Create or get a new access token'
            }
        )
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_error_handler(
            status_code = status.HTTP_403_FORBIDDEN,
            initial_detail = {
                'message' : 'Please provide a valid refresh token',
                'Resolution' : 'Create or get a new refresh token'
            }
        )
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_error_handler(
            status_code = status.HTTP_403_FORBIDDEN,
            initial_detail = {
                'message' : 'Your account does not have sufficient permissions to perform this action',
                'Resolution' : 'Upgrade your account or contact support'
            }
        )
    )