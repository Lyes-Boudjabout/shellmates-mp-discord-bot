from fastapi import APIRouter, HTTPException
from models import Joke
from database.mongo_config import jokes_collection
from typing import List
from bson import ObjectId

router = APIRouter(tags=["jokes"])

def serialize_joke(joke: dict) -> dict:
    joke["id"] = str(joke["_id"])
    del joke["_id"]
    return joke

@router.get("/", response_model=List[dict])
async def list_jokes():
    cursor = jokes_collection.find({})
    return [serialize_joke(doc) async for doc in cursor]

@router.get("/{jokes_id}", response_model=dict)
async def get_joke(joke_id: str):
    doc = await jokes_collection.find_one({"_id": ObjectId(joke_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="joke not found")
    return serialize_joke(doc)

@router.post("/", response_model=dict)
async def create_joke(joke: Joke):
    result = await jokes_collection.insert_one(joke.dict())
    return {**joke.dict(), "id": str(result.inserted_id)}

@router.put("/{joke_id}", response_model=dict)
async def update_joke(joke_id: str, update_data: dict):
    result = await jokes_collection.update_one(
        {"_id": ObjectId(joke_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="joke not found")
    updated_doc = await jokes_collection.find_one({"_id": ObjectId(joke_id)})
    return serialize_joke(updated_doc)

@router.delete("/{joke_id}", response_model=dict)
async def delete_joke(joke_id: str):
    result = await jokes_collection.delete_one({"_id": ObjectId(joke_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="joke not found")
    return {"detail": "joke deleted"}
