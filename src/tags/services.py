from sqlmodel import select, desc
from src.db.models import Tag, BookTags
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from .structs import TagCreateRequest, TagAddRequest
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.services import BookService
from src.errors import TagNotFound, BookNotFound, TagAlreadyExists

book_service = BookService()


class TagService:

    async def get_all_tags(self,session: AsyncSession):

        try:
            statement = select(Tag).order_by(desc(Tag.created_at))

            tags = await session.exec(statement)

            return tags.all()
        
        except Exception as e:

            return JSONResponse(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                content = {'message' : str(e)}
            )
    
    async def get_tag_by_id(self, tag_id : str, session: AsyncSession):

        try:
            statement = select(Tag).where(Tag.id == tag_id)

            tag = await session.exec(statement)

            if tag is not None:
                return tag.first()
            else:
                raise TagNotFound()
        
        except Exception as e:

            return JSONResponse(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                content = {'message' : str(e)}
            )


    async def create_tag(self, tag_data : TagCreateRequest, session : AsyncSession):

        try:
            
            statement = select(Tag).where(Tag.name == tag_data.name)

            result = await session.exec(statement)

            tag = result.first()

            if tag:
                raise TagAlreadyExists()
            
            new_tag = Tag(name = tag_data.name)
            
            session.add(new_tag)

            await session.commit()

            return new_tag
        
        except Exception as e:

            JSONResponse(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                content = {'message' : str(e)}
            )

    async def add_tag_to_book(self, book_id: str, tag_data: TagAddRequest, session: AsyncSession):
        
        try:
            book = await book_service.get_book_by_id(book_id=book_id, session=session)

            if not book:
                raise BookNotFound()

            for tag_item in tag_data.tags:
                # Find tag by name
                statement = select(Tag).where(Tag.name == tag_item.name)
                result = await session.exec(statement)
                tag = result.one_or_none()

                if not tag:
                    tag = Tag(name=tag_item.name)
                    
                book.tags.append(tag)

            session.add(book)

            await session.commit()
            
            await session.refresh(book)

                
            return book
        
        except Exception as e:

            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = {'message' : str(e)}
            )

    async def update_tag(self, tag_id: str, tag_data : TagCreateRequest, session: AsyncSession):

        try:
            tag = await self.get_tag_by_id(tag_id = tag_id, session = session)

            if tag is not None:

                update_data_dict = tag_data.model_dump()

                for key, value in update_data_dict.items():
                    
                    setattr(tag, key, value)


                    await session.commit()

                    await session.refresh(tag)
                
                return tag
            
            else:

                raise TagNotFound()
            
        except Exception as e:
            
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = {'message' : str(e)}
            )
    
    async def delete_tag(self, tag_id : str, session : AsyncSession):

        delete_tag = await self.get_tag_by_id(tag_id = tag_id, session = session)

        if delete_tag is not None:
            await session.delete(delete_tag)

            await session.commit()

            return {'message' : 'Tag Successfully deleted'}
        else:
            raise TagNotFound()
