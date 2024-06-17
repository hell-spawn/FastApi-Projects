import uuid
from datetime import datetime
from typing import Any, List
from fastapi import APIRouter, Body, Path, Query, Request, status
from fastapi.responses import JSONResponse

from src.models.error_model import ErrorApiModel
from src.models.movie_model import CategoryEmun, Movie, MovieUpdate
from src.models.success_model import SuccessListApiModel, SuccessObjectApiModel

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


@movie_router.get('', tags=['Movies'], responses={
    200: {'model': SuccessListApiModel[Movie]},
    500: {'model': ErrorApiModel},
})
def get_movies(request: Request):
    current_movies: list[Movie] = [movie for movie in movies]
    response = SuccessListApiModel[Movie](
        status="Success",
        code=status.HTTP_200_OK,
        message="Request completed successfully",
        path=request.url.path,
        timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        transaction_id=uuid.uuid4().hex,
        data=current_movies
    )
    return response  # Custom JsonResponse


@movie_router.get('/{id}', tags=['Movies'], responses={  # Path parameters /2
    200: {'model': SuccessObjectApiModel[Movie]},
    404: {'model': SuccessObjectApiModel},
    422: {'model': ErrorApiModel},
    500: {'model': ErrorApiModel}
})
def get_movies_by_id(id: int, request: Request):
    response = SuccessObjectApiModel[Movie](
        status="Success",
        code=status.HTTP_200_OK,
        message="Request completed successfully",
        path=request.url.path,
        timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        transaction_id=uuid.uuid4().hex
    )
    for movie in movies:
        if movie.id == id:
            response.data = movie
            return response
    response.code = status.HTTP_404_NOT_FOUND
    response.message = "Movie not found"
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response.model_dump())


@movie_router.get('/categories/', tags=['Movies'], responses={
    200: {'model': SuccessListApiModel[Movie]},
    404: {'model': SuccessListApiModel},
    422: {'model': ErrorApiModel},
    500: {'model': ErrorApiModel}
})  # Query parameters /?category=Action
def get_movies_by_category(category: CategoryEmun, request: Request):
    response = SuccessListApiModel[Movie](
        status="Success",
        code=status.HTTP_404_NOT_FOUND,
        message="Movie not found",
        path=request.url.path,
        timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        transaction_id=uuid.uuid4().hex,
    )
    current_movies = [movie for movie in movies if movie.category == category]
    if current_movies:
        response.code = status.HTTP_200_OK
        response.message = "Request completed successfully"
        response.data = current_movies
        return response
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response.model_dump())
    
@movie_router.post('', tags=['Movies'], responses={
    200: {'model': SuccessObjectApiModel[Movie]},
    422: {'model': ErrorApiModel},
    500: {'model': ErrorApiModel}
    }) 
def create_movie(movie: Movie, request: Request): 
    response = SuccessObjectApiModel[Movie](
        status="Success",
        code=status.HTTP_200_OK,
        message="Request completed successfully",
        path=request.url.path,
        timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        transaction_id=uuid.uuid4().hex,
        data=movie
    )
    return response;


@movie_router.put('/{id}', tags=["Movies"], responses={
    200: {'model': SuccessListApiModel[Movie]},
    422: {'model': ErrorApiModel},
    404: {'model': SuccessListApiModel},
    500: {'model': ErrorApiModel}
    }) 
def update_movie(request: Request, id: int = Path(gt=0), movie: MovieUpdate = Body()): 
    movie_exist = False
    response = SuccessListApiModel[Movie](
        status="Success",
        code=status.HTTP_200_OK,
        message="Request completed successfully",
        path=request.url.path,
        timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        transaction_id=uuid.uuid4().hex,
    )
    for current_movie in movies:
        if current_movie.id == id:
            current_movie.title = movie.title
            current_movie.overview = movie.overview
            current_movie.year = movie.year
            current_movie.rating = movie.rating 
            current_movie.category = movie.category
            current_movie.language = movie.language
            movie_exist = True
            break
    
    if not movie_exist:
        response.code = status.HTTP_404_NOT_FOUND
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response.model_dump())

    response = SuccessListApiModel[Movie](
        status="Success",
        code=status.HTTP_200_OK,
        message="Request completed successfully",
        path=request.url.path,
        timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        transaction_id=uuid.uuid4().hex,
        data=movies
    )
    return response

@movie_router.delete("", tags=['Movies'], responses={
    200: {'model': SuccessListApiModel[Movie]},
    422: {'model': ErrorApiModel},
    500: {'model': ErrorApiModel}
    }) 
def delete_movie(request: Request, id: int):
    for movie in movies: 
        if movie.id == id:
            movies.remove(movie)

    response = SuccessListApiModel[Movie](
        status="Success",
        code=status.HTTP_200_OK,
        message="Request completed successfully",
        path=request.url.path,
        timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        transaction_id=uuid.uuid4().hex,
        data=movies
    )
    return response


