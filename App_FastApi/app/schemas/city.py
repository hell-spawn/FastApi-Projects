from typing import Optional
from pydantic import BaseModel, ConfigDict

class CityBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    country: str
    population: Optional[int] = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int
    name: str
    country: str
    population: Optional[int] = None

    class Config:
        from_attributes = True
        populate_by_name = True
