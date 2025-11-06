"""
Run this file ONCE to populate the database with sample quotes.
Place this file in the backend/ folder and run: python populate_quotes.py
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


async def populate_quotes():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    quotes_collection = db["quotes"]

    # Sample cybersecurity quotes
    sample_quotes = [
        {
            "content": "The only truly secure system is one that is powered off, cast in a block of concrete and sealed in a lead-lined room.",
            "author": "Gene Spafford"
        },
        {
            "content": "Security is not a product, but a process.",
            "author": "Bruce Schneier"
        },
        {
            "content": "To be secure, you must be paranoid, but not crazy.",
            "author": "Kevin Mitnick"
        },
        {
            "content": "Passwords are like underwear: don't let people see it, change it often, and don't share it.",
            "author": "Chris Pirillo"
        },
        {
            "content": "There are two types of companies: those that have been hacked, and those who don't know they have been hacked.",
            "author": "John Chambers"
        },
        {
            "content": "Hacking is not a crime, it's a skill. It's what you do with that skill that determines if you're a criminal or not.",
            "author": "Unknown"
        },
        {
            "content": "The best way to predict the future is to invent it.",
            "author": "Alan Kay"
        },
        {
            "content": "In God we trust. All others must bring data.",
            "author": "W. Edwards Deming"
        },
        {
            "content": "Privacy is not about having something to hide. It's about having something to protect.",
            "author": "Unknown"
        },
        {
            "content": "The Internet is becoming the town square for the global village of tomorrow.",
            "author": "Bill Gates"
        }
    ]

    # Check if quotes already exist
    count = await quotes_collection.count_documents({})
    if count > 0:
        print(f"⚠️  Database already has {count} quotes. Skipping population.")
        return

    # Insert sample quotes
    result = await quotes_collection.insert_many(sample_quotes)
    print(f"✅ Successfully added {len(result.inserted_ids)} quotes to the database!")

    client.close()


if __name__ == "__main__":
    asyncio.run(populate_quotes())