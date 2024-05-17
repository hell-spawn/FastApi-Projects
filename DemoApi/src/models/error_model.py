from pydantic import BaseModel


class ErrorApiModel(BaseModel):
    status: int
    message: str
    details: list
    timestamp: str 
    transaction_id: str
    path: str

