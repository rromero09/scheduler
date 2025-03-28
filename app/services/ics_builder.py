from datetime import datetime, timedelta
import os
from ics import Calendar, Event, DisplayAlarm
from services.ics_settings import DAY_MAP, SHIFT_TIMES


def build_ics_for_worker(worker_name, shifts, week_start_date: datetime, output_dir="tmp"):
    calendar = Calendar()

    for shift in shifts:
        day_name = shift.get("day", "").strip().lower()
        shift_type = shift.get("shift", "").strip().upper()
        location = shift.get("location", "").strip().title()

        if day_name not in DAY_MAP:
            print(f"⚠️ Skipping unknown day: {day_name}")
            continue

        if shift_type not in SHIFT_TIMES:
            print(f"⚠️ Skipping unknown shift type: {shift_type}")
            continue

        shift_day = week_start_date + timedelta(days=DAY_MAP[day_name])
        is_weekend = day_name in ["saturday", "sunday"]
        time_key = "weekend" if is_weekend else "weekday"

        try:
            start_str, end_str = SHIFT_TIMES[shift_type][time_key]
            start_dt = datetime.strptime(f"{shift_day.date()} {start_str}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{shift_day.date()} {end_str}", "%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"❌ Error parsing shift times for {worker_name} on {day_name}: {e}")
            continue

        event = Event()
        event.name = f"{worker_name.title()} - {shift_type} Shift"
        event.begin = start_dt
        event.end = end_dt
        event.description = f"{shift_type} shift at {location}"
        event.location = location

        # Add alarm 15 minutes before the event starts
        alarm = DisplayAlarm(trigger=timedelta(minutes=-15), display_text="Upcoming work shift!")
        event.alarms.append(alarm)

        calendar.events.add(event)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{worker_name.lower().replace(' ', '_')}_schedule.ics")

    try:
        with open(filepath, "w") as f:
            f.writelines(calendar)
        print(f"✅ ICS file created for {worker_name}: {filepath}")
    except Exception as e:
        print(f"❌ Failed to write ICS file for {worker_name}: {e}")

    return filepath
