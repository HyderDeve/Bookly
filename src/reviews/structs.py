from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid




class ReviewResponse(BaseModel):
    id : uuid.UUID
    rating :int = Field(lt = 5)
    review : str
    user_id : Optional[uuid.UUID]
    book_id : Optional[uuid.UUID]
    created_at : datetime
    updated_at : datetime


class ReviewCreateModel(BaseModel):
    rating : int = Field( lt = 5)
    review : str 