import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


class CategoryEmun(str, Enum):
    terror = "Terror"
    action = "Action"
    science_fiction =  "Science Fiction"


class MovieUpdate(BaseModel): #Model for pydantic update movie
    title: str = Field(min_length=5, max_length=15) #Field Validation
    overview: str = Field(default="This movie is about ...")
    year: int = Field(ge=1900, le=datetime.date.today().year)
    rating: float
    category: CategoryEmun
    language: str

    @validator('language')
    def validator_language(cls, value):
        if value is None or len(value) < 5 :
            raise ValueError("Language field must have minimun 5 characters")
        return value


class Movie(MovieUpdate): #Model for pydantic default movie
    id: int

