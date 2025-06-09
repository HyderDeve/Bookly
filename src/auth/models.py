from sqlmodel import SQLModel,Field,Column,Relationship
import sqlalchemy.dialects.postgresql as pg
from src.books import models
import uuid
from datetime import datetime
from typing import List



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
    is_verified:bool = Field(default=False)  # Default to False, can be updated later
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    books : List['models.Book']  = Relationship(back_populates = 'user',sa_relationship_kwargs = {'lazy': 'selectin'})

    def __repr__(self):
        return f"<User {self.username}>" 