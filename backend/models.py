from pydantic import BaseModel
from typing import List

class Event(BaseModel):
    title: str
    date: str
    description: str
    location: str

class Fact(BaseModel):
    content: str

class Joke(BaseModel):
    content: str

class Quiz(BaseModel):
    question: str
    options: List[str]
    correct_option: int    
