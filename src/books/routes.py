from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from typing import List
from src.books.structs import BookUpdateModel, BookCreateModel, BookResponse
from src.db.main import get_session
from src.books.services import BookService
from src.auth.dependencies import AccessTokenBearer
from src.auth.dependencies import RoleChecker

book_router = APIRouter()
book_service = BookService() #declared service struct for connection purposes to bring service functions here
access_token_bearer = AccessTokenBearer()  # Initialize the AccessTokenBearer for token validation
role_checker = Depends(RoleChecker(['admin','user']))


#GET /books
@book_router.get("/", response_model=List[BookResponse],dependencies = [role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer)
    ):
    books = await book_service.get_all_books(session)  # Fetch all books using the service layer
    return books # the list of books will be returned as a JSON response


#GET /books/user/{user_id}
@book_router.get("/user/{user_id}", response_model=List[BookResponse],dependencies = [role_checker])
async def get_user_books(
    user_id : str,
    session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer),
    ):
    books = await book_service.get_user_books(user_id,session)  # Fetch all books using the service layer
    return books # the list of books will be returned as a JSON response


#POST /books
@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponse,dependencies = [role_checker])
async def post_books(book_data:BookCreateModel,session: AsyncSession = Depends(get_session),token_details : dict = Depends(access_token_bearer)):
    
    user_id = token_details.get('user')['user_id']

    new_book = await book_service.create_book(book_data, user_id, session)  # Create a new book using the service layer

    # new_book = book_data.model_dump()  # Convert Pydantic model to dictionary

    # books.append(new_book)  # Append the new book to the list

    return new_book


#GET /books/{id}
@book_router.get("/{book_id}",status_code=status.HTTP_200_OK,response_model=BookResponse,dependencies = [role_checker])
async def get_book_by_id(book_id:str, session: AsyncSession = Depends(get_session),token_details : dict = Depends(access_token_bearer)):
    
    book = await book_service.get_book_by_id(book_id,session)

    if book:
        return book # Return the book if found
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {book_id} not found.")

#PUT /books/{id}
@book_router.patch("/{book_id}",response_model=BookResponse,dependencies = [role_checker])
async def update_book(book_id:str, book_update_data:BookUpdateModel,session: AsyncSession = Depends(get_session),token_details : dict = Depends(access_token_bearer)) -> dict:
    
    updated_book =await book_service.update_book(book_id,book_update_data, session)
    
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with id {book_id} not found.")


    

#DELETE /books/{id}
@book_router.delete("/{book_id}",dependencies = [role_checker])
async def delete_book(book_id:str,session: AsyncSession = Depends(get_session),token_details : dict = Depends(access_token_bearer)):
    delete_book = await book_service.delete_book(book_id, session)

    if delete_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return {"message": "Book deleted successfully."}

