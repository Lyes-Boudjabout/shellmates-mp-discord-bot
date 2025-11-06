from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    title: str
    date: str
    description: str
    location: str

class Fact(BaseModel):
    content: str

class Quote(BaseModel):
    content: str
    author: Optional[str] = "Unknown"
