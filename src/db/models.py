from sqlmodel import SQLModel,Field,Column,Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid # this is the unique id generator uuid is unique id
from datetime import datetime, date
from typing import List, Optional



class User(SQLModel,table=True):
    __tablename__ = "users"
    id : uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4 # Automatically generate a new UUID for each user
    ))
    username : str
    password : str = Field(exclude=True)  # Exclude password from the model representation
    email:str  # Email should be unique, consider adding a unique constraint in the database
    first_name:str
    last_name:str
    role : str = Field(sa_column = Column(pg.VARCHAR, nullable = False, server_default = 'user')) # Default role is user, can be updated later
    is_verified:bool = Field(default=False)  # Default to False, can be updated later
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    books : List['Book']  = Relationship(back_populates = 'user',sa_relationship_kwargs = {'lazy': 'selectin'})
    reviews : List['Review']  = Relationship(back_populates = 'user',sa_relationship_kwargs = {'lazy': 'selectin'})

    def __repr__(self):
        return f"<User {self.username}>" 
    

class BookTags(SQLModel, table = True):
    
    book_id : uuid.UUID = Field(
            primary_key = True,
            foreign_key = 'books.id',
            default = None
        )
    
    tag_id : uuid.UUID = Field(
                primary_key = True,
                foreign_key = 'tags.id',
                default = None
        )



class Tag(SQLModel, table = True):

    __tablename__ = 'tags'

    id : uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    name : str
    created_at : datetime = Field(sa_column = Column(pg.TIMESTAMP, default = datetime.now()))
    #updated at not created tags aren't updated they are either used or unused 
    books : List['Book'] = Relationship( # created for filteration purposes usally
        link_model = BookTags,
        back_populates = 'tags',
        sa_relationship_kwargs = {'lazy' : 'selectin'},
    )

    def __repr__(self):
        return f'<Tag {self.name}>'


class Book(SQLModel, table=True):
    __tablename__ = "books"  # Define the table name in the database

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,  # Automatically generate a unique & random ID
        )
    )
    title: str
    author: str
    published_date: date # all fields data must match the type defined in the model
    page_count: int
    language: str
    user_id : Optional[uuid.UUID] = Field(default = None, foreign_key = 'users.id')
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=(datetime.now))) 
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=(datetime.now))) 
    user : Optional['User']  = Relationship(back_populates = 'books')
    reviews : List['Review']  = Relationship(back_populates = 'book',sa_relationship_kwargs = {'lazy': 'selectin'}) #back_populates contains the key name defined in the origin model
    tags : List['Tag'] = Relationship(
        link_model = BookTags,
        back_populates = 'books',
        sa_relationship_kwargs = {'lazy': 'selectin'}, 
    )
    
    #Column is used to define a pydantic column in db
    #sa_column is used to define a sqlalchemy column in db

    def __repr__(self):
        return f"<Book {self.title}>"

class Review(SQLModel, table=True):
    __tablename__ = "reviews"  # Define the table name in the database

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,  # Automatically generate a unique & random ID
        )
    )
    rating : int = Field(lt = 5)
    review : str = Field(sa_column = Column(pg.VARCHAR, nullable = False))
    user_id : Optional[uuid.UUID] = Field(default = None, foreign_key = 'users.id')
    book_id : Optional[uuid.UUID] = Field(default = None, foreign_key = 'books.id')
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=(datetime.now))) 
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=(datetime.now))) 
    user : Optional['User']  = Relationship(back_populates = 'reviews')
    book : Optional['Book']  = Relationship(back_populates = 'reviews')
    #Column is used to define a pydantic column in db
    #sa_column is used to define a sqlalchemy column in db

    def __repr__(self):
        return f"<Review for book {self.book_id} by user {self.user_id}>"
    
