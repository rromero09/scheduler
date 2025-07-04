from fastapi import APIRouter
from app.services.logger import log_event

router = APIRouter()

@router.get("/test-log")
async def test_log():
    log_event("Test log from /test-log endpoint")
    return {"message": "Log recorded (or printed if DB unavailable)"}