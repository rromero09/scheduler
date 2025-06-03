from datetime import datetime
from app.db.mongo import db  # Reuse the DB connection

def log_event(message: str, level: str = "INFO"):
    if db is None:
        print(f"[LOG - {level}] {message}")
        return

    try:
        db["logs"].insert_one({
            "message": message,
            "level": level,
            "timestamp(utc)": datetime.utcnow()
        })
    except Exception as e:
        print(f"[LOGGING ERROR] {e}")