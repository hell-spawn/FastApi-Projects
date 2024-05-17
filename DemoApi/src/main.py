import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse 
from src.models.error_model import ErrorApiModel
from src.routes.movie_router import movie_router


app = FastAPI();

app.title = "Demo FastAPI" # Title api
app.version = "1.0.0" # Version api for docs

# Path swagger: /docs
# Path redoc: /redoc

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        return  await call_next(request)
    except HTTPException as e:
        error: ErrorApiModel = ErrorApiModel(status=e.status_code, 
                             message=e.detail, 
                             details=[e.__cause__], 
                             timestamp=datetime.now().__str__(), 
                             transaction_id=uuid.uuid4().hex, 
                             path=request.url.path)
        return JSONResponse(status_code=e.status_code, content=error.model_dump())
    except Exception as e:
        error: ErrorApiModel = ErrorApiModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             message="Internal Server Error", 
                             details=[e.__cause__], 
                             timestamp=datetime.now().__str__(), 
                             transaction_id=uuid.uuid4().hex, 
                             path=request.url.path)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error: ErrorApiModel = ErrorApiModel(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         message="Unprocessable Entity",
                         details= list(exc.errors()),
                         timestamp=datetime.now().__str__(), 
                         transaction_id=uuid.uuid4().hex,
                         path=request.url.path)
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error.model_dump())


@app.get('/')
def version():
    return {}


app.include_router(movie_router, prefix="/movies")
