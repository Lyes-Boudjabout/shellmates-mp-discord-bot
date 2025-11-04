from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from models import Quiz
from database.mongo_config import quiz_collection

router = APIRouter(prefix="/quiz", tags=["CyberQuiz"])

def serialize_quiz(quiz: dict) -> dict:
    quiz["id"] = str(quiz["_id"])
    del quiz["_id"]
    return quiz

@router.get("/", response_model=List[dict])
async def list_quizzes():
    cursor = quiz_collection.find({})
    return [serialize_quiz(doc) async for doc in cursor]

@router.get("/{quiz_id}", response_model=dict)
async def get_quiz(quiz_id: str):
    doc = await quiz_collection.find_one({"_id": ObjectId(quiz_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return serialize_quiz(doc)

@router.post("/", response_model=dict)
async def create_quiz(quiz: Quiz):
    result = await quiz_collection.insert_one(quiz.dict())
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create quiz")
    return {"id": str(result.inserted_id), "message": "Quiz added successfully!"}

@router.put("/{quiz_id}", response_model=dict)
async def update_quiz(quiz_id: str, update_data: dict):
    result = await quiz_collection.update_one(
        {"_id": ObjectId(quiz_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiz not found")
    updated_doc = await quiz_collection.find_one({"_id": ObjectId(quiz_id)})
    return serialize_quiz(updated_doc)

@router.delete("/{quiz_id}", response_model=dict)
async def delete_quiz(quiz_id: str):
    result = await quiz_collection.delete_one({"_id": ObjectId(quiz_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"detail": "Quiz deleted successfully"}
