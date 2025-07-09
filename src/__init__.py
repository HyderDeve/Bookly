from fastapi import FastAPI, status
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tag_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.errors import (
    create_error_handler,
    InsufficientPermission,
    InvalidToken,
    InvalidCredentials,
    RefreshTokenRequired,
    AccessTokenRequired,
    UserAlreadyExists,
    UserNotFound,
    BookNotFound,
    RevokedToken,
    TagNotFound,
    TagAlreadyExists
)

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is Starting up the application...")
    await init_db()
    yield
    print(f"Server is Shutting down the application...")

    
version = 'v1'

app = FastAPI(
    title= "Bookly",
    description= "A RESTAPI for a book review web service",
    version = version,
    # lifespan=life_span # This is like the main function in golang
)

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


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"]) # This is like the router group or the api group
# or public groups like we defined in golang
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix = f'/api/{version}/reviews', tags = ['reviews'])
app.include_router(tag_router, prefix = f'/api/{version}/tags', tags = ['tags'])