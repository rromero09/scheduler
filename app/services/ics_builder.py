# services/ics_builder.py

import uuid
from datetime import datetime, timedelta
from pathlib import Path
import pytz

from app.services.ics_settings import DAY_MAP, SHIFT_TIMES

CENTRAL = pytz.timezone("America/Chicago")
ORGANIZER_EMAIL = "thebakehousechicago@gmail.com"
ORGANIZER_NAME = "The Bake House"

def get_shift_times(shift: str, day: str) -> tuple[str, str]:
    shift = shift.upper()
    day_type = "weekend" if day.lower() in ["saturday", "sunday"] else "weekday"
    return SHIFT_TIMES[shift][day_type]

def create_event_ics(uid: str, dtstart: datetime, dtend: datetime, summary: str, description: str, location: str, worker_name: str) -> str:
    # Use the current time for created/modified timestamps
    timestamp_now = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    
    # Format dates with timezone ID for Apple Calendar
    local_start = f"{dtstart.strftime('%Y%m%dT%H%M%S')}"
    local_end = f"{dtend.strftime('%Y%m%dT%H%M%S')}"
    
    # Start with the header
    ics_content = """BEGIN:VCALENDAR
PRODID:-//TheBakeHouseChicago//WorkerSchedule//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VTIMEZONE
TZID:America/Chicago
X-LIC-LOCATION:America/Chicago
BEGIN:DAYLIGHT
TZOFFSETFROM:-0600
TZOFFSETTO:-0500
TZNAME:CDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0500
TZOFFSETTO:-0600
TZNAME:CST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE
"""
    
    # Add the event
    ics_content += f"""BEGIN:VEVENT
DTSTART;TZID=America/Chicago:{local_start}
DTEND;TZID=America/Chicago:{local_end}
DTSTAMP:{timestamp_now}
ORGANIZER;CN={ORGANIZER_NAME}:mailto:{ORGANIZER_EMAIL}
UID:{uid}@thebakehouse.com
ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE;CN={worker_name.capitalize()}:mailto:{worker_name.lower()}@thebakehouse.com
CREATED:{timestamp_now}
DESCRIPTION:{description}
LAST-MODIFIED:{timestamp_now}
LOCATION:{location}
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:{summary}
TRANSP:OPAQUE
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Reminder
TRIGGER:-PT1H
END:VALARM
END:VEVENT
END:VCALENDAR"""
    
    return ics_content

def build_ics_for_worker(worker_name: str, shifts: list[dict], base_date: datetime) -> list[str]:
    """
    Builds individual ICS files for each shift and returns a list of file paths.
    Files are organized in a subfolder named after the worker.
    """
    # Create base output directory
    output_dir = Path("output_ics")
    output_dir.mkdir(exist_ok=True)
    
    # Create worker-specific subdirectory
    worker_dir = output_dir / worker_name.lower()
    worker_dir.mkdir(exist_ok=True)
    
    ics_paths = []
    
    for shift_index, shift in enumerate(shifts):
        day_index = DAY_MAP[shift["day"].lower()]
        start_date = base_date + timedelta(days=day_index)
        start_time, end_time = get_shift_times(shift["shift"], shift["day"])
        dtstart = CENTRAL.localize(datetime.strptime(f"{start_date.date()} {start_time}", "%Y-%m-%d %H:%M"))
        dtend = CENTRAL.localize(datetime.strptime(f"{start_date.date()} {end_time}", "%Y-%m-%d %H:%M"))

        uid = str(uuid.uuid4())
        summary = f"{worker_name.capitalize()} - {shift['shift'].upper()} Shift"
        description = f"{shift['shift'].upper()} shift at {shift['location'].capitalize()}"
        location = shift["location"].capitalize()
        
        # Create ICS content for this specific shift
        ics_content = create_event_ics(uid, dtstart, dtend, summary, description, location, worker_name)
        
        # Generate filename using date and shift info for uniqueness and readability
        filename = f"{start_date.strftime('%Y-%m-%d')}_{shift['shift'].lower()}_{shift_index}.ics"
        ics_path = worker_dir / filename
        
        # Write the file
        with open(ics_path, "w", encoding="utf-8") as f:
            f.write(ics_content)
        
        ics_paths.append(str(ics_path))
    
    return ics_paths