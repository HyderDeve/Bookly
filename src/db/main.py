from sqlmodel import  create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config
import ssl



ssl_context = ssl.create_default_context()


engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True,  # Echo SQL statements to the console for debugging + logging purposes
    connect_args={'ssl' : ssl_context}
))



#DB connection function 
async def init_db():
    async with engine.begin() as conn: #connection object created
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)  # Create all tables in the database migrations jesa hai golang ki hisab se
        

async def get_session() -> AsyncSession:

    Session = sessionmaker(
        bind = engine,
        class_ = AsyncSession,
        expire_on_commit = False,  # This means that the session will not expire the objects after commit, allowing you to access them later without reloading from the database
    )

    async with Session() as session:
        yield session # This will yield the session object to be used in the route handlers, allowing you to use it in your CRUD operations
        # The session will be automatically closed after the block is exited
