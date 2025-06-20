from src.db.models import Tag, BookTags
from fastapi.responses import JSONResponse
from .structs import TagCreateRequest, TagAddRequest, TagResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


class TagService:

    pass


