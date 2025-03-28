from datetime import datetime
from utils.date_utils import get_current_week_start
from app.db.mongo import get_workers_from_db
from services.csv_format import get_reshaped_schedule
from services.ics_builder import build_ics_for_worker
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/schedule/generate")
async def generate_schedule():
    try:
        schedule = get_reshaped_schedule()
        if not schedule:
            raise HTTPException(status_code=500, detail="Error reshaping the schedule")

        # 🧠 Assume exact match only (no aliases)
        workers = get_workers_from_db()
        worker_names = {worker["name"].lower() for worker in workers}

        shifts_by_worker = {}
        unmatched = []

        for entry in schedule:
            name = entry["worker"].lower()

            if name in worker_names:
                shifts_by_worker.setdefault(name, []).append(entry)
            else:
                unmatched.append(name)

        # 📆 Get start of current week in Chicago time
        week_start = get_current_week_start("America/Chicago")

        ics_files = []
        for worker_name, shifts in shifts_by_worker.items():
            path = build_ics_for_worker(worker_name, shifts, week_start)
            ics_files.append(path)

        return {
            "status": "success",
            "ics_created": len(ics_files),
            "unmatched_workers": list(set(unmatched)),
            "ics_file_paths": ics_files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
