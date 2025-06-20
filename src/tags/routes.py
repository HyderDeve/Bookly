from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from src.auth.dependencies import AccessTokenBearer
from .services import TagService
from .structs import TagCreateRequest, TagAddRequest, TagResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from typing import List

tag_router = APIRouter()
tags_service = TagService()
access_token_bearer = AccessTokenBearer()



@tag_router.get('/', response_model = List[TagResponse])
async def get_all_tags(token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
    
    try:
        tags = await tags_service.get_all_tags(session)
    
        return tags
    
    except Exception as e:

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )
    
@tag_router.get('/{tag_id}',response_model = TagResponse)
async def get_tag_by_id(tag_id : str, token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
    
    try:
        tag = await tags_service.get_tag_by_id(tag_id,session)
    
        return tag
    
    except Exception as e:

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )
    

@tag_router.post('/', response_model = TagResponse)
async def create_tag(tag_data : TagCreateRequest, token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
        
        tag = await tags_service.create_tag(tag_data, session)

        return tag

@tag_router.delete('/{tag_id}')
async def delete_tags(tag_id : str, token_details = Depends(access_token_bearer), session : AsyncSession = Depends(get_session)):
    
    tag = await tags_service.delete_tag(session)
    
    if tag is not None:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'message' : 'Tag deleted successfully'}
        )
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Tag not found'
        ) #baki errors service mein daal dena hai