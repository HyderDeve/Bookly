from fastapi import APIRouter


review_router = APIRouter()


@review_router.post('/book/{book_id}')
async def add_review():
    pass