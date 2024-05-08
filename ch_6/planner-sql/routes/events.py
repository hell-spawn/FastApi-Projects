from fastapi import APIRouter, Body, HTTPException, status, Depends
from typing import List, Sequence
from sqlalchemy import event

from sqlalchemy.orm import session
from sqlmodel import Session, select
from models.events import Event, EventUpdate
from database.connection import get_session


event_router = APIRouter(tags=["events"])

old_events: List[Event] = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session: Session = Depends(get_session)) -> Sequence[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

@event_router.post("/new" )
async def create_event(new_event: Event, session: Session = Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "Event successfully created"}

@event_router.put("edit/{id}", response_model=Event)
async def update_event(id:int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.model_dump(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)

        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
            

@event_router.delete("/{id}")
async def delete_event(id: int, session: Session=Depends(get_session)) -> dict: 
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()

        return {
            "message": "Event deleted successfully"
        }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

@event_router.delete("/")
async def delete_all_events() -> dict:
    old_events.clear()
    return{
            "message": "Events delete successfully"
            }
