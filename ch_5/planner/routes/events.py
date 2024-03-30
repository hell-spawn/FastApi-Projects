from fastapi import APIRouter, Body, HTTPException, status
from typing import List
from models.events import Event


event_router = APIRouter(tags=["events"])

events: List[Event] = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

@event_router.post("/new" )
async def create_event(event: Event) -> dict:
    events.append(event)
    return {"message": "Event successfully created"}

@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Event successfully deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return{
            "message": "Events delete successfully"
            }
