from fastapi import APIRouter, HTTPException
from models import Quote
from database.mongo_config import quotes_collection
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/quotes", tags=["quotes"])

def serialize_quote(quote: dict) -> dict:
    quote["id"] = str(quote["_id"])
    del quote["_id"]
    return quote

@router.get("/", response_model=List[dict])
async def list_quotes():
    cursor = quotes_collection.find({})
    return [serialize_quote(doc) async for doc in cursor]

@router.get("/{quote_id}", response_model=dict)
async def get_quote(quote_id: str):
    doc = await quotes_collection.find_one({"_id": ObjectId(quote_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Quote not found")
    return serialize_quote(doc)

@router.post("/", response_model=dict)
async def create_quote(quote: Quote):
    result = await quotes_collection.insert_one(quote.dict())
    return {**quote.dict(), "id": str(result.inserted_id)}

@router.put("/{quote_id}", response_model=dict)
async def update_quote(quote_id: str, update_data: dict):
    result = await quotes_collection.update_one(
        {"_id": ObjectId(quote_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quote not found")
    updated_doc = await quotes_collection.find_one({"_id": ObjectId(quote_id)})
    return serialize_quote(updated_doc)

@router.delete("/{quote_id}", response_model=dict)
async def delete_quote(quote_id: str):
    result = await quotes_collection.delete_one({"_id": ObjectId(quote_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Quote not found")
    return {"detail": "Quote deleted"}