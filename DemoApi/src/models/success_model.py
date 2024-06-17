from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field 

from src.models.generic_model import BaseGenericResponse

M = TypeVar("M", bound= BaseModel)

class SuccessObjectApiModel(BaseGenericResponse, Generic[M] ):
    data: Optional[ M | dict ] = {}


class SuccessListApiModel(BaseGenericResponse, Generic[M]):
    data: Optional[list[M]] = list() 
