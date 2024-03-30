from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    item: str  
    
    model_config = {
            'json_schema_extra': {
                'example': 
                {
                    'id': 1,
                    'item': 'Buy milk'
                    }


                } 
            }

class TodoItem(BaseModel):
    item: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'item': 'Buy milk'
            }
        }
    }

class TodoItems(BaseModel):
    todos: list[TodoItem]

    model_config = {
        'json_schema_extra': {
            'example': {
                'todos': [
                    {
                        'item': 'Buy milk'
                    },
                    {
                        'item': 'Buy eggs'
                    }
                ]
            }
        }
    }
