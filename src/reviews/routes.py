from fastapi import APIRouter, Depends, status
from src.db.models import User
from src.db.main import get_session
from .structs import ReviewCreateModel, ReviewResponse
from src.auth.dependencies import get_current_user, AccessTokenBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import ReviewService
from fastapi.exceptions import HTTPException
from typing import List

review_service = ReviewService()
review_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@review_router.post('/book/{book_id}',status_code = status.HTTP_201_CREATED, response_model = ReviewResponse, responses = {
    500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error Message"}}}},
    403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Token is invalid or expired"}}}},
    404:{'description' : 'Book Not Found', 'content':{'application/json' : {'example' : 
      {
        'message' : "Book not found"}}}}
})
async def add_review(book_id:str, review_data : ReviewCreateModel, current_user: User = Depends(get_current_user), session : AsyncSession = Depends(get_session)):

    user_email_current = current_user.email

    new_review = await review_service.add_review(user_email = user_email_current,  review_data = review_data, book_id = book_id, session = session)

    return new_review

@review_router.get('/', response_model = List[ReviewResponse], responses = {
    500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error Message"}}}},
    403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Token is invalid or expired"}}}}
})
async def get_all_reviews(token_details = Depends(access_token_bearer),session : AsyncSession = Depends(get_session)):

    books = await review_service.get_all_reviews(session)

    return books

@review_router.get('/{review_id}', response_model = ReviewResponse, responses = {
    500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error Message"}}}},
    403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Token is invalid or expired"}}}},
    404:{'description' : 'Review Not Found', 'content':{'application/json' : {'example' : 
      {
        'message' : "Review not found"}}}}
})
async def get_review_by_id(review_id : str,  token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):

    review = await review_service.get_review_by_id(review_id, session)

    return review


@review_router.delete('/{review_id}', responses = {
      200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Review deleted successfully"
                    }
                }
            }
        },
      500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error Message"}}}},
      403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Token is invalid or expired"}}}},    
      404:{'description' : 'Book Not Found', 'content':{'application/json' : {'example' : 
      {
        'message' : "Review not found"}}}}
    })
async def delete_review(review_id : str,  token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
    
    deleted_review = await review_service.delete_review(review_id, session)

    if deleted_review is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = {'message' : 'Review not found'}
        )
    else:
        return {'message' : 'Review deleted successfully'}