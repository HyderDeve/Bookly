from src.db.models import Tag, BookTags
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from .structs import TagCreateRequest, TagAddRequest, TagResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


class TagService:

    async def get_all_tags(self,session: AsyncSession = Depends(get_session)):

        try:
            statement = 'select * from tags order by created_at desc;'

            tags = await session.exec(statement)

            return tags.all()
        
        except Exception as e:

            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message' : str(e)}
            )
    
    async def get_tag_by_id(self, tag_id : str, session: AsyncSession = Depends(get_session)):

        try:
            statement = f'select * from tags where id = \'{tag_id}\' ;'

            tag = await session.exec(statement)

            return tag.first()
        
        except Exception as e:

            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message' : str(e)}
            )


    async def create_tag(self,tag_data : TagAddRequest, session : AsyncSession = Depends(get_session)):

        try:

            tag_dict = tag_data.model_dump()

            new_tag = Tag(
                **tag_dict
                )
            

            session.add(new_tag)

            await session.commit()

            return new_tag
        
        except Exception as e:

            JSONResponse(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                content = {'message' : str(e)}
            )
    
    async def delete_tag(self, tag_id : str, session : AsyncSession = Depends(get_session)):

        delete_tag = await self.get_tag_by_id(tag_id = tag_id, session = session)

        if delete_tag is not None:
            await session.delete(delete_tag)

            await session.commit()

            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {'message' : 'Tag deleted successfully'}
            )
        
        else:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message' : 'Tag not found service error'}
            )
