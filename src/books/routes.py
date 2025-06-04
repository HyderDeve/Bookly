from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.book_data import books
from src.books.structs import Book, BookUpdateModel


book_router = APIRouter()



#GET /books
@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books # the list of books will be returned as a JSON response

#POST /books
@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_books(book_data:Book):
    new_book = book_data.model_dump()  # Convert Pydantic model to dictionary

    books.append(new_book)  # Append the new book to the list

    return new_book


#GET /books/{id}
@book_router.get("/{book_id}",status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id:int):
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with id {book_id} not found.")

#PUT /books/{id}
@book_router.patch("/{book_id}")
async def update_book(book_id:int, book_update_data:BookUpdateModel) -> dict:
    
    for book in books:
        
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with id {book_id} not found.")


    

#DELETE /books/{id}
@book_router.delete("/{book_id}")
async def delete_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

