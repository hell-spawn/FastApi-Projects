from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []

@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Todo add sucessfully"}


@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todo() -> dict:
    return {"todos": todo_list}

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="The ID of the todo to retrieve.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with id: {todo_id} was not found."
            )


@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: str, todo_id: int = Path(..., title="The ID of the todo to update.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data
            return {
                "todo": todo
            }

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with supplied ID doesn't exist."
            )

@todo_router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int = Path(..., title="The ID of the todo to delete.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo_list.remove(todo)
            return { "message": "Todo deleted sucessfully" }
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with supplied ID doesn't exist.",
            )


@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return { "message": "Todos deleted successfully." }
