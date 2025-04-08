from datetime import datetime, timedelta
import os
import uuid
from zoneinfo import ZoneInfo
from app.services.ics_settings import DAY_MAP, SHIFT_TIMES

def build_ics_for_worker(worker_name, shifts, week_start_date: datetime, output_dir="tmp"):
    # 📁 Make sure the tmp/ folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define organizer information
    organizer_name = "The Bake House"
    organizer_email = "thebakehousechicago@gmail.com"
    
    # Create worker email from name
    worker_email = f"{worker_name.lower().replace(' ', '.')}@thebakehouse.com"
    
    # Start building the ICS content with calendar header
    ics_content = """BEGIN:VCALENDAR
PRODID:-//TheBakeHouseChicago//WorkerSchedule//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:REQUEST
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
    
    # Process each shift and add as an event
    for shift in shifts:
        day_name = shift.get("day", "").strip().lower()
        shift_type = shift.get("shift", "").strip().upper()
        location = shift.get("location", "").strip().title()
        
        # Skip invalid shifts
        if day_name not in DAY_MAP or shift_type not in SHIFT_TIMES:
            continue
            
        # Calculate shift date and times
        shift_day = week_start_date + timedelta(days=DAY_MAP[day_name])
        is_weekend = day_name in ["saturday", "sunday"]
        time_key = "weekend" if is_weekend else "weekday"
        start_str, end_str = SHIFT_TIMES[shift_type][time_key]
        
        # Parse datetime objects
        start_dt = datetime.strptime(f"{shift_day.date()} {start_str}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{shift_day.date()} {end_str}", "%Y-%m-%d %H:%M")
        
        # Set timezone to Chicago
        tz = ZoneInfo("America/Chicago")
        start_dt = start_dt.replace(tzinfo=tz)
        end_dt = end_dt.replace(tzinfo=tz)
        
        # Format dates for ICS
        start_str = start_dt.strftime("%Y%m%dT%H%M%S")
        end_str = end_dt.strftime("%Y%m%dT%H%M%S")
        timestamp_now = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        
        # Generate unique UUID
        uid = str(uuid.uuid4())
        
        # Add event to ICS content
        event_content = f"""BEGIN:VEVENT
DTSTART;TZID=America/Chicago:{start_str}
DTEND;TZID=America/Chicago:{end_str}
DTSTAMP:{timestamp_now}
ORGANIZER;CN={organizer_name}:mailto:{organizer_email}
UID:{uid}
ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN={worker_name.title()}:mailto:{worker_email}
CREATED:{timestamp_now}
DESCRIPTION:{shift_type} shift at {location}
LAST-MODIFIED:{timestamp_now}
LOCATION:{location}
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:{worker_name.title()} - {shift_type} Shift
TRANSP:OPAQUE
X-MICROSOFT-CDO-BUSYSTATUS:BUSY
X-MICROSOFT-CDO-IMPORTANCE:1
X-MICROSOFT-DISALLOW-COUNTER:FALSE
X-MICROSOFT-DONOTFORWARDMEETING:FALSE
X-MICROSOFT-CDO-ALLDAYEVENT:FALSE
X-MICROSOFT-ISRESPONSEREQUESTED:TRUE
CLASS:PUBLIC
PRIORITY:5
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Reminder
TRIGGER:-PT1H
END:VALARM
END:VEVENT
"""
        ics_content += event_content
    
    # Close the calendar
    ics_content += "END:VCALENDAR"
    
    # Generate file path and write calendar to file
    filepath = os.path.join(output_dir, f"{worker_name.lower().replace(' ', '_')}_schedule.ics")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(ics_content)
        return filepath
    except Exception as e:
        print(f"❌ Failed to write ICS for {worker_name}: {str(e)}")
        return None