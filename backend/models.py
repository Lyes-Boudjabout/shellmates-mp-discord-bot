from pydantic import BaseModel

class Event(BaseModel):
    title: str
    date: str
    description: str
    location: str

class Fact(BaseModel):
    content: str

class Joke(BaseModel):
    content: str