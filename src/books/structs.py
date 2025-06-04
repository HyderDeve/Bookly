from pydantic import BaseModel
import uuid 
from datetime import datetime, date

class BookResponse(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    published_date: date  # all fields data must match the type defined in the model
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime



class BookCreateModel(BaseModel):
    title:str
    author:str
    page_count:int
    language:str
    published_date:str

class BookUpdateModel(BaseModel):
    title:str
    author:str
    page_count:int
    language:str
