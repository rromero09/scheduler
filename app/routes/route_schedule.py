from datetime import datetime, timedelta
import pytz
from app.services.csv_format import get_reshaped_schedule, get_workers_from_csv
from app.services.ics_builder import build_ics_for_worker
from fastapi import APIRouter, HTTPException
import traceback

router = APIRouter()

@router.get("/schedule/generate")
async def generate_schedule():
    try:
        # Get and reshape schedule data
        schedule = get_reshaped_schedule()
        if not schedule:
            raise HTTPException(status_code=500, detail="Error reshaping the schedule")
        
        # Get workers from CSV instead of DB
        workers_data = get_workers_from_csv()
        worker_names = {worker["name"].lower() for worker in workers_data}
        
        # Organize shifts by worker
        shifts_by_worker = {}
        unmatched = []
        for entry in schedule:
            name = entry["worker"].lower()
            if name in worker_names:
                shifts_by_worker.setdefault(name, []).append(entry)
            else:
                unmatched.append(name)
        
        # Get start of current week in Chicago time
        chicago_tz = pytz.timezone("America/Chicago")
        today = datetime.now(chicago_tz)  # Current time in Chicago timezone
        
        # Convert to naive datetime for proper week start calculation
        # This is important to prevent timezone issues
        today_naive = today.replace(tzinfo=None)
        week_start = today_naive - timedelta(days=today_naive.weekday())
        
        # Build ICS files for each worker
        all_ics_files = []
        ics_count = 0
        worker_ics_map = {}
        
        for worker_name, shifts in shifts_by_worker.items():
            try:
                # Now returns a list of paths instead of a single path
                worker_paths = build_ics_for_worker(worker_name, shifts, week_start)
                all_ics_files.extend(worker_paths)
                ics_count += len(worker_paths)
                worker_ics_map[worker_name] = worker_paths
            except Exception as worker_error:
                print(f"Error creating ICS for {worker_name}: {str(worker_error)}")
                # Continue with next worker instead of failing completely
        
        return {
            "status": "success",
            "ics_created": ics_count,
            "unmatched_workers": list(set(unmatched)),
            "ics_file_paths": all_ics_files,
            "worker_ics_map": worker_ics_map  # Added to show files organized by worker
        }
    except Exception as e:
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Schedule generation error: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))