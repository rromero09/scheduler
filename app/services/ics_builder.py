from datetime import datetime, timedelta
import os
import uuid
from ics import Calendar, Event, DisplayAlarm
from zoneinfo import ZoneInfo
from services.ics_settings import DAY_MAP, SHIFT_TIMES

def build_ics_for_worker(worker_name, shifts, week_start_date: datetime, output_dir="tmp"):
    # Create a calendar with Apple-friendly properties
    calendar = Calendar()
    calendar.creator = "TheBakeHouseChicago"
    
    # Essential properties for Apple compatibility
    calendar.extra.append("CALSCALE:GREGORIAN")
    # Use REQUEST method instead of PUBLISH for invitation-style calendar events
    calendar.extra.append("METHOD:REQUEST")
    
    # Add worker email from their name for invitation purposes
    worker_email = f"{worker_name.lower().replace(' ', '.')}@thebakehouse.com"
    
    # Define the organizer
    organizer_name = "The Bake House"
    organizer_email = "thebakehousechicago@gmail.com"
    
    for shift in shifts:
        day_name = shift.get("day", "").strip().lower()
        shift_type = shift.get("shift", "").strip().upper()
        location = shift.get("location", "").strip().title()
        
        if day_name not in DAY_MAP or shift_type not in SHIFT_TIMES:
            continue
            
        # Calculate date for shift
        shift_day = week_start_date + timedelta(days=DAY_MAP[day_name])
        is_weekend = day_name in ["saturday", "sunday"]
        time_key = "weekend" if is_weekend else "weekday"
        start_str, end_str = SHIFT_TIMES[shift_type][time_key]
        
        start_dt = datetime.strptime(f"{shift_day.date()} {start_str}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{shift_day.date()} {end_str}", "%Y-%m-%d %H:%M")
        
        # Assign timezone (Chicago)
        tz = ZoneInfo("America/Chicago")
        start_dt = start_dt.replace(tzinfo=tz)
        end_dt = end_dt.replace(tzinfo=tz)
        
        # Create and add event with Apple-compatible properties
        event = Event()
        event.name = f"{worker_name.title()} - {shift_type} Shift"
        event.begin = start_dt
        event.end = end_dt
        event.location = location
        event.description = f"{shift_type} shift at {location}"
        
        # Set a unique UID format (important for Apple Calendar)
        event.uid = str(uuid.uuid4())
        
        # Set organizer and attendee with specific roles
        # Note: The ics library might not support this directly, so we use extra properties
        event.organizer = f"mailto:{organizer_email}"
        event.extra.append(f"ORGANIZER;CN={organizer_name}:mailto:{organizer_email}")
        
        # Add the worker as an attendee who needs to respond
        event.extra.append(f"ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN={worker_name.title()}:mailto:{worker_email}")
        
        # Add Microsoft-specific properties that help with Apple compatibility
        event.extra.append("X-MICROSOFT-CDO-BUSYSTATUS:BUSY")
        event.extra.append("X-MICROSOFT-CDO-IMPORTANCE:1")
        event.extra.append("X-MICROSOFT-DISALLOW-COUNTER:FALSE")
        event.extra.append("X-MICROSOFT-DONOTFORWARDMEETING:FALSE")
        event.extra.append("X-MICROSOFT-CDO-ALLDAYEVENT:FALSE")
        event.extra.append("X-MICROSOFT-ISRESPONSEREQUESTED:TRUE")
        event.extra.append("CLASS:PUBLIC")
        event.extra.append("PRIORITY:5")
        event.extra.append("STATUS:CONFIRMED")
        event.extra.append("TRANSP:OPAQUE")
        
        # Add a reminder
        event.alarms.append(DisplayAlarm(trigger=timedelta(hours=-1), display_text="Upcoming work shift!"))
        
        calendar.events.add(event)
    
    # Save calendar to a file
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{worker_name.lower().replace(' ', '_')}_schedule.ics")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(calendar.serialize())
    
    return filepath