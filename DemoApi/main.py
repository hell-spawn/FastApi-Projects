import datetime
from enum import Enum
from typing import List, Optional
from fastapi import Body, FastAPI, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field



app = FastAPI();

app.title = "Demo FastAPI" # Title api
app.version = "1.0.0" # Version api for docs

# Path swagger: /docs
# Path redoc: /redoc

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

class Movie(MovieUpdate): #Model for pydantic default movie
    id: int

movies: List[Movie] = [ 
        Movie.model_validate(
            {
                "id": 1,
                "title": "Iron Man",
                "overview": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
                "year": "2009",
                "rating": 7.8,
                "category": "Action"
                }
            ),
        Movie.model_validate(
            {
                "id": 2,
                "title": "Dune Part 1",
                "overview": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
                "year": "2021",
                "rating": 9.8,
                "category": "Science Fiction" 
                }
            ) 
        ]


@app.get('/')
def version():
    return {"Version": app.version}


@app.get('/movies', tags=['Movies'], response_model=List[Movie]) 
def get_movies():
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content) # Custom JsonResponse


@app.get('/movie/{id}', tags=['Movies']) # Path parameters /movies/2
def get_movies_by_id(id: int) -> Movie | dict :
    for movie in movies: 
        if movie.id == id:
            return movie
    return {} 


@app.get('/movie/', tags=['Movies']) # Query parameters /movies/?category=Action
def get_movies_by_category(category: CategoryEmun ) -> List[Movie]:
    return [movie for movie in movies if movie.category == category]


@app.post('/movies', tags=['Movies']) 
def create_movie(movie: Movie) -> List[Movie]: 
    movies.append(movie) 
    return movies;


@app.put('/movies/{id}', tags=["Movies"])
def update_movie(id: int = Path(gt=0), movie: MovieUpdate = Body())-> List[Movie]: 
    for current_movie in movies:
        if current_movie.id == id:
            current_movie.title = movie.title
            current_movie.overview = movie.overview
            current_movie.year = movie.year
            current_movie.rating = movie.rating 
            current_movie.category = movie.category
    return movies


@app.delete("/movies", tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies: 
        if movie.id == id:
            movies.remove(movie)
    return movies


