from fastapi import FastAPI, status
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tag_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.errors import register_all_errors
from .middleware import register_middleware

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
    license_info = {
       'name':'MIT', 
       'url':'https://opensource.org/license/mit'
    },
    contact = {
        'name' : 'Hyder Ali Hashmi',
        'email' : 'hyderhashmi17@gmail.com',
        'url' : 'https://github.com/hyderdeve/bookly',
        },
        redoc_url = f'/api/{version}/docs'
    # lifespan=life_span # This is like the main function in golang
)

#---------------------Custom Error Handlers added---------------------#
register_all_errors(app)
#---------------------Custom Error Handlers ended---------------------#

#--------------------- Middleware Handled---------------------#
register_middleware(app)
#--------------------- Middleware Handled---------------------#


#------------------All Routers Handled------------------#

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"]) # This is like the router group or the api group
# or public groups like we defined in golang
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix = f'/api/{version}/reviews', tags = ['reviews'])
app.include_router(tag_router, prefix = f'/api/{version}/tags', tags = ['tags'])

#------------------All Routers Handled------------------#