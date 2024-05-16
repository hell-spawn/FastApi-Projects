from fastapi import FastAPI 
from src.routes.movie_router import movie_router


app = FastAPI();

app.title = "Demo FastAPI" # Title api
app.version = "1.0.0" # Version api for docs

# Path swagger: /docs
# Path redoc: /redoc


@app.get('/')
def version():
    return {"Version": app.version}


app.include_router(movie_router, prefix="/movies")
