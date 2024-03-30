from pydantic import BaseModel, ConfigDict
from typing import List


class Event(BaseModel):

    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    model_config  = {
            'json_schema_extra': {
                'example': {
                    'id': 1,
                    'title': 'FastAPI Book Launch',
                    'image': 'https://fastapi.tiangolo.com/img/fastapi-logo.png',
                    'description': 'We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!',
                    'tags': ['python', 'fastapi', 'web'],
                    'location': 'Online'
                    } 
                }
            }
