from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from models.events import Event


class User(BaseModel):
    email: EmailStr 
    username: str
    password: str
    events: Optional[List[Event]] = Field(default=None, description="List of events created by the user")

    model_config = {
            'json_schema_extra': {
                'example': {
                    'email': 'example@example.com',
                    'username': 'example',
                    'password': 'example',
                    'events': []
                    }            
            }
    }

class UserSingIn(BaseModel):
    email: EmailStr
    password: str

    model_config = {
            'json_schema_extra': {
                'example': {
                    'email': 'example@example.com',
                    'password': 'example',
                    'events': [],
                    }            
            }
    }
