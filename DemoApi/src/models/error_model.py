from typing import Any, Generic, TypeVar
from pydantic import BaseModel

from src.models.generic_model import BaseGenericResponse


M = TypeVar("M", bound=BaseModel | Any)

class ErrorApiModel(BaseGenericResponse, Generic[M]):
    details: M 
