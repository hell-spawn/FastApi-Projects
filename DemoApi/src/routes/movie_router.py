from typing import Any, List
from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse

from src.models.movie_model import CategoryEmun, Movie, MovieUpdate

movies: List[Movie] = [ 
        Movie.model_validate(
            {
                "id": 1,
                "title": "Iron Man",
                "overview": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
                "year": "2009",
                "rating": 7.8,
                "category": "Action",
                "language": "Spanish"
                }
            ),
        Movie.model_validate(
            {
                "id": 2,
                "title": "Dune Part 1",
                "overview": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
                "year": "2021",
                "rating": 9.8,
                "category": "Science Fiction",
                "language": "English"
                }
            ) 
        ]

movie_router = APIRouter()

@movie_router.get('', tags=['Movies'], response_model=List[Movie]) 
def get_movies():
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content) # Custom JsonResponse


@movie_router.get('/{id}', tags=['Movies']) # Path parameters /2
def get_movies_by_id(id: int) -> Movie | dict :
    for movie in movies: 
        if movie.id == id:
            return movie
    return {} 


@movie_router.get('/search', tags=['Movies']) # Query parameters /?category=Action
def get_movies_by_category() -> JSONResponse:
    return JSONResponse(content='{}')
    #return [movie for movie in movies if movie.category == category]


@movie_router.post('', tags=['Movies']) 
def create_movie(movie: Movie) -> List[Movie]: 
    movies.append(movie) 
    print(movie.language)
    return movies;


@movie_router.put('/{id}', tags=["Movies"])
def update_movie(id: int = Path(gt=0), movie: MovieUpdate = Body()) -> List[Movie]: 
    for current_movie in movies:
        if current_movie.id == id:
            current_movie.title = movie.title
            current_movie.overview = movie.overview
            current_movie.year = movie.year
            current_movie.rating = movie.rating 
            current_movie.category = movie.category
            current_movie.language = movie.language
    return movies


@movie_router.delete("", tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies: 
        if movie.id == id:
            movies.remove(movie)
    return movies


