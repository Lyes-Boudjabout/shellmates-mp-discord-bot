from fastapi import APIRouter, HTTPException
from models import Fact
from database.mongo_config import facts_collection
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/facts", tags=["facts"])

def serialize_fact(fact: dict) -> dict:
    fact["id"] = str(fact["_id"])
    del fact["_id"]
    return fact

@router.get("/", response_model=List[dict])
async def list_facts():
    cursor = facts_collection.find({})
    return [serialize_fact(doc) async for doc in cursor]

@router.get("/{fact_id}", response_model=dict)
async def get_fact(fact_id: str):
    doc = await facts_collection.find_one({"_id": ObjectId(fact_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Fact not found")
    return serialize_fact(doc)

@router.post("/", response_model=dict)
async def create_fact(fact: Fact):
    result = await facts_collection.insert_one(fact.dict())
    return {**fact.dict(), "id": str(result.inserted_id)}

@router.put("/{fact_id}", response_model=dict)
async def update_fact(fact_id: str, update_data: dict):
    result = await facts_collection.update_one(
        {"_id": ObjectId(fact_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Fact not found")
    updated_doc = await facts_collection.find_one({"_id": ObjectId(fact_id)})
    return serialize_fact(updated_doc)

@router.delete("/{fact_id}", response_model=dict)
async def delete_fact(fact_id: str):
    result = await facts_collection.delete_one({"_id": ObjectId(fact_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Fact not found")
    return {"detail": "Fact deleted"}
