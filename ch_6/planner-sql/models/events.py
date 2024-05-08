from re import I
from pydantic import ConfigDict
from sqlmodel import JSON, Column, Field, SQLModel
from typing import List, Optional


class Event(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    model_config = ConfigDict( arbitrary_types_allowed=True, json_schema_extra={
        'example': {
            'title': 'FastAPI Book Launch',
            'image': 'https://fastapi.tiangolo.com/img/fastapi-logo.png',
            'description': 'We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!',
            'tags': ['python', 'fastapi', 'web'],
            'location': 'Online'
            } 

        })


class EventUpdate(SQLModel):

    title: str | None = None 
    image: str | None = None
    description: str | None = None
    tags: List[str] | None = None
    location: str | None = None


    model_config = ConfigDict(json_schema_extra={
        "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        })

    
