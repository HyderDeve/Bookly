from src.db.models import Review
from src.auth.services import UserService
from src.books.services import BookService
from sqlmodel.ext.asyncio.session import AsyncSession 
from .structs import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status


book_service = BookService
user_service = UserService

class ReviewService:

    async def add_review(self,user_email : str, review_data : ReviewCreateModel, book_id : str, session : AsyncSession):
        try:
            
            book = await book_service.get_book_by_id(self, book_id = book_id, session = session)

            user = await user_service.get_user_by_email(self, email = user_email, session = session)

            review_data_dict = review_data.model_dump()
            
            new_review = Review(
                **review_data_dict
            ) #unpacking the fields in the dict

            if not book:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = 'Book not fouund' 
                )
            
            if not user:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = 'User not found'
                )


            new_review.user = user

            new_review.book = book

            session.add(new_review)

            await session.commit()

            return new_review

        except Exception as e:
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = str(e)
            )