from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from app.db.mongo import client, db
# Importing MongoDB modules from app/db/mongo.py 
router = APIRouter()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["scheduler_db"]
collection = db["echo_data"]

# Request model for incoming data
class RequestModel(BaseModel):
    name: str
    last_name: str

@router.post("/worker")
async def put_worker(request: RequestModel):
    try:
        result = collection.insert_one(request.dict())

        return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "inserted_id": str(result.inserted_id),
            "data": request.dict()  # convert the request data to a dictionary for response, otherwise it raises an error
        }
    )

    except Exception as e:
        print("Error occurred inserting into DB:", e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )
