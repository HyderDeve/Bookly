from fastapi import APIRouter, Depends, status
from src.db.models import User
from src.db.main import get_session
from .structs import ReviewCreateModel, ReviewResponse
from src.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import ReviewService
from fastapi.exceptions import HTTPException
from typing import List

review_service = ReviewService()
review_router = APIRouter()


@review_router.post('/book/{book_id}',response_model = ReviewResponse)
async def add_review(book_id:str, review_data : ReviewCreateModel, current_user: User = Depends(get_current_user), session : AsyncSession = Depends(get_session)):

    user_email_current = current_user.email

    new_review = await review_service.add_review(user_email = user_email_current,  review_data = review_data, book_id = book_id, session = session)

    return new_review

@review_router.get('/', response_model = List[ReviewResponse])
async def get_all_reviews(session : AsyncSession = Depends(get_session)):

    books = await review_service.get_all_reviews(session)

    return books