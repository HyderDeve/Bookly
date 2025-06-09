from sqlmodel.ext.asyncio.session import AsyncSession
from .structs import BookCreateModel, BookUpdateModel
from .models import Book
from sqlmodel import select, desc
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession): #this session is an obj used for interaction with db
        statement = select(Book).order_by(desc(Book.created_at))  #this is the ORM use in python where SQLMODEL allows sql in form of python code
        
        result = await session.exec(statement)  #exec is used to execute the statement in db

        return result.all()
    

    async def get_user_books(self, user_id: str, session: AsyncSession):
        statement = select(Book).where(Book.user_id == user_id).order_by(desc(Book.created_at))  #this is the ORM use in python where SQLMODEL allows sql in form of python code
        
        result = await session.exec(statement)  #exec is used to execute the statement in db

        return result.all()
    
    async def get_book_by_id(self, book_id:str, session: AsyncSession):
        statement = select(Book).where(Book.id == book_id)

        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None  #if book is not found then return None

    async def create_book(self, book_data: BookCreateModel, user_id: str, session: AsyncSession):
        book_data_dict = book_data.model_dump()  # Convert Pydantic model to dictionary

        new_book = Book(
            **book_data_dict  # Unpack the dictionary into the Book model basically how we used to assign 
            #response body to the model in fastapi & golang
        )

        new_book.user_id = user_id # Set the user ID from the token details

        new_book.published_date = datetime.strptime(book_data_dict['published_date'],"%Y-%m-%d")  # Set the published date to today

        session.add(new_book)  # Add the new book to the session
        await session.commit() #commits the changes to the db

        return new_book

    async def update_book(self, book_id: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book_by_id(book_id, session)

        if book_to_update is not None:
            book_update_dict = update_data.model_dump()

            for key, values in book_update_dict.items(): #this gets both key and value of the dict
                setattr(book_to_update, key, values) #this sets the value of every key to the value provided in the update_body
            
            await session.commit()  # Commit the changes to the database

            return book_to_update
        else:
            print(f"Book with ID {book_id} not found.")  # If book is not found, return None or handle as needed
            return None
        

    async def delete_book(self, book_id: str, session: AsyncSession):
        book_to_delete = await self.get_book_by_id(book_id, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            
            await session.commit()

            return {}

        else:
            return None  # If book is not found, return None or handle as needed
