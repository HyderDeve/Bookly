import uuid
from datetime import datetime 
from typing import List
from pydantic import BaseModel



class TagResponse(BaseModel):
    id : uuid.UUID
    name : str
    created_at : datetime


class TagCreateRequest(BaseModel):
    name : str

class TagAddRequest(BaseModel):
    tags : List[TagCreateRequest]