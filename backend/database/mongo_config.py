import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

# === Load Environment Variables === #
load_dotenv()
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME: str = os.getenv("DB_NAME", "cyberbot_db")

# === Logging Configuration === #
logger = logging.getLogger("mongo_config")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# === MongoDB Client Singleton === #
class MongoDB:
    _client: AsyncIOMotorClient = None
    _db: AsyncIOMotorDatabase = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            cls._client = AsyncIOMotorClient(MONGO_URI)
            logger.info(f"Connected to MongoDB")
        return cls._client

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        if cls._db is None:
            cls._db = cls.get_client()[DB_NAME]
            logger.info(f"Using database: {DB_NAME}")
        return cls._db

# === Collections === #
db = MongoDB.get_db()
events_collection = db["events"]
facts_collection = db["facts"]
jokes_collection = db["jokes"]
quiz_collection = db["quizzes"]
