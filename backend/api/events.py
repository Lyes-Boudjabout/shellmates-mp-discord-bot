from fastapi import APIRouter, HTTPException
from models import Event
from database.mongo_config import events_collection
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/events", tags=["events"])

def serialize_event(event: dict) -> dict:
    """Convert MongoDB document to JSON-friendly dict."""
    event["id"] = str(event["_id"])
    del event["_id"]
    return event

@router.get("/", response_model=List[dict])
async def list_events():
    cursor = events_collection.find({})
    return [serialize_event(doc) async for doc in cursor]

@router.get("/{event_id}", response_model=dict)
async def get_event(event_id: str):
    doc = await events_collection.find_one({"_id": ObjectId(event_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Event not found")
    return serialize_event(doc)

@router.post("/", response_model=dict)
async def create_event(event: Event):
    result = await events_collection.insert_one(event.dict())
    return {**event.dict(), "id": str(result.inserted_id)}

@router.put("/{event_title}", response_model=dict)
async def update_event(event_title: str, update_data: dict):
    result = await events_collection.update_one(
        {"title": event_title}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    
    updated_doc = await events_collection.find_one({"title": event_title})
    return serialize_event(updated_doc)

@router.delete("/{event_title}", response_model=dict)
async def delete_event(event_title: str):
    result = await events_collection.delete_one({"title": event_title})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"detail": "Event deleted"}
