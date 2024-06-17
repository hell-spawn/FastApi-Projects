from typing import Any, Sequence
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, status
import fastapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware import Middleware
from src.models.error_model import ErrorApiModel
from src.routes.movie_router import movie_router
from src.utils.api_middleware import HttpErrorHandler  


app = FastAPI()

app.title = "Demo FastAPI"  # Title api
app.version = "1.0.0"  # Version api for docs

# Path swagger: /docs
# Path redoc: /redoc


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as e:
        error: ErrorApiModel = ErrorApiModel(status="error",
                                             code=e.status_code,
                                             message=e.detail,
                                             details=[],
                                             timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                             transaction_id=uuid.uuid4().hex,
                                             path=request.url.path)
        return JSONResponse(status_code=e.status_code, content=error.model_dump())
    except Exception as e:
        error: ErrorApiModel = ErrorApiModel(status="error",
                                             code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="Internal Server Error",
                                             details=list(e.args),
                                             timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                             transaction_id=uuid.uuid4().hex,
                                             path=request.url.path)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f'Paso por el manejo de error')
    error: ErrorApiModel = ErrorApiModel[Sequence[Any]](status="error",
                                         code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                         message="Unprocessable Entity",
                                         details=exc.errors(),
                                         timestamp=datetime.now().__str__(),
                                         transaction_id=uuid.uuid4().hex,
                                         path=request.url.path)
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error.model_dump())


@app.get('/')
def version():
    return {"version":"1.0.0"}


app.include_router(movie_router, prefix="/movies")
