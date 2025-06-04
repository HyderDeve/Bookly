from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid # this is the unique id generator uuid is unique id

class Book(SQLModel, table=True):
    __tablename__ = "books"  # Define the table name in the database

    uid: uuid.UUID = Field(
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
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=(datetime.now))) 
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=(datetime.now))) 
    #Column is used to define a pydantic column in db
    #sa_column is used to define a sqlalchemy column in db

    def __repr__(self):
        return f"<Book {self.title}>"
    