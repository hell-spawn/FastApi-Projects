from pydantic import BaseModel

class BaseGenericResponse(BaseModel):
    status: str 
    code: int
    message: str
    timestamp: str 
    transaction_id: str
    path: str

