from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is Starting up the application...")
    await init_db()
    yield
    print(f"Server is Shutting down the application...")

    
version = 'v1'

app = FastAPI(
    title= "Bookly",
    description= "A RESTAPI for a book review web service",
    version = version,
    lifespan=life_span # This is like the main function in golang
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"]) # This is like the router group or the api group
# or public groups like we defined in golang
