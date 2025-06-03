from fastapi import APIRouter
from app.services.csv_format import get_workers_from_csv
from app.services.email_service import send_email_with_ics, is_valid_email
from app.services.logger import log_event
import os
from fastapi.responses import JSONResponse
# Importing MongoDB modules from app/db/mongo.py 

router = APIRouter()





@router.post("/worker/notify")
def notify_workers():
    workers = get_workers_from_csv() #fetching clean workers from csv into a json format
    sent_emails = []
    skipped_emails = []

    for worker in workers:
        name = worker["name"]
        email = worker["email"]
        ics_path = f"tmp/{name}_schedule.ics"

        if not is_valid_email(email):
            msg = f"Invalid email format for {name}: {email}"
            print(f"[!] Skipped invalid email: {email}")
            skipped_emails.append({"name": name, "email": email, "reason": "invalid email"})
            log_event(msg, level="WARNING")
            continue

        if not os.path.exists(ics_path):
            msg = f"ICS file not found for {name}: {ics_path}"
            log_event(msg, level="WARNING")
            ics_path = f"tmp/{name.lower().replace(' ', '_')}_schedule.ics" # adjusting path for case sensitivity
            print(f"[!] Skipped missing .ics: {ics_path}")
            skipped_emails.append({"name": name, "email": email, "reason": "missing .ics"})
            continue

        try:
            # Attempt to send the email with the ICS attachment
            log_event(f"Sending email to {name} at {email}", level="INFO")
        
            send_email_with_ics(email, name, ics_path)
            print(f"[✓] Sent email to: {email}")
            sent_emails.append({"name": name, "email": email})
        except Exception as e:
            msg= f"Failed to send email to {name} at {email}: {str(e)}"
            log_event(msg, level="ERROR")
            print(f"[X] Failed to send to {email}: {e}")
            skipped_emails.append({"name": name, "email": email, "reason": str(e)})

    return {
        "message": "Email job completed",
        "sent": sent_emails,
        "skipped": skipped_emails
    }
