from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from src.auth.dependencies import AccessTokenBearer
from .services import TagService
from .structs import TagCreateRequest, TagAddRequest, TagResponse
from src.books.structs import BookResponse,BookDetailResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from typing import List
from src.errors import TagNotFound, BookNotFound

tag_router = APIRouter()
tags_service = TagService()
access_token_bearer = AccessTokenBearer()



@tag_router.get('/', response_model = List[TagResponse], responses = {
      500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error"}}}},
      403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Token is invalid or expired"}}}}
    }
)
async def get_all_tags(token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
    
    try:
        tags = await tags_service.get_all_tags(session)
    
        return tags
    
    except Exception as e:

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )
    
@tag_router.get('/{tag_id}',response_model = TagResponse, responses = {
      500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error Message"}}}},
      403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Token is invalid or expired"}}}},    
      404:{'description' : 'Tag Not Found', 'content':{'application/json' : {'example' : 
      {
        'message' : "Tag not found"}}}}
    }
  )
async def get_tag_by_id(tag_id : str, token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):

    tag = await tags_service.get_tag_by_id(tag_id,session)

    if tag is not None:

        return tag

    else:
        raise TagNotFound()

    

@tag_router.post('/',status_code = status.HTTP_201_CREATED, response_model = TagResponse, responses ={
    500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error Message"}}}},
    403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Tag already exists"}}}},
})
async def create_tag(tag_data : TagCreateRequest, token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
        
        tag = await tags_service.create_tag(tag_data, session)

        return tag


@tag_router.post('/book/{book_id}', status_code = status.HTTP_201_CREATED, response_model = BookDetailResponse, responses = {
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
async def add_tags_to_book(book_id : str, tag_data : TagAddRequest, token_details = Depends(access_token_bearer), session :AsyncSession = Depends(get_session)):

    book_with_tag = await tags_service.add_tag_to_book(book_id = book_id, tag_data = tag_data, session = session)

    if book_with_tag is not None:

        return book_with_tag
    
    else:

        raise BookNotFound() 
    


@tag_router.patch('/{tag_id}', response_model = TagResponse, responses = {
    500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Customized Error Message"}}}},
    403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Token is invalid or expired"}}}},    
    404:{'description' : 'Tag Not Found', 'content':{'application/json' : {'example' : 
      {
        'message' : "Tag not found"}}}}
})
async def update_tag(tag_id : str, tag_data : TagCreateRequest, token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):

    tag = await tags_service.update_tag(tag_id, tag_data, session)

    if tag is not None:

        return tag 
    
    else:
        
        raise TagNotFound()

@tag_router.delete('/{tag_id}', responses = {
    200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Tag deleted successfully"
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
    404:{'description' : 'Tag Not Found', 'content':{'application/json' : {'example' : 
      {
        'message' : "Tag not found"}}}}})
async def delete_tags(tag_id : str, token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
    
    tag = await tags_service.delete_tag(session)
    
    if tag is not None:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'message' : 'Tag deleted successfully'}
        )
    else:
        raise TagNotFound() #baki errors service mein daal dena hai