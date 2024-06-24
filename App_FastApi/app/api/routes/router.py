from fastapi import APIRouter

from . import cities  # Import the missing modules

base_router = APIRouter()

# Define routes for the missing modules
base_router.include_router( cities.router, tags=["cities"], prefix="/v1")  
