from fastapi import APIRouter
from app.services.csv_format import get_workers_from_csv
from app.services.email_service import send_email_with_ics, is_valid_email
import os
from fastapi.responses import JSONResponse
# Importing MongoDB modules from app/db/mongo.py 

router = APIRouter()





@router.post("/notify-workers")
def notify_workers():
    workers = get_workers_from_csv()
    sent_emails = []
    skipped_emails = []

    for name, email, _ in workers:
        if not is_valid_email(email):
            print(f"[!] Skipped (invalid email): {email}")
            skipped_emails.append({"name": name, "email": email, "reason": "invalid email"})
            continue

        ics_path = f"tmp/{name}.ics"
        if not os.path.exists(ics_path):
            print(f"[!] Skipped (missing .ics): {ics_path}")
            skipped_emails.append({"name": name, "email": email, "reason": "missing .ics"})
            continue

        try:
            send_email_with_ics(email, name, ics_path)
            print(f"[✓] Sent email to: {email}")
            sent_emails.append({"name": name, "email": email})
        except Exception as e:
            print(f"[X] Failed to send email to {email}: {e}")
            skipped_emails.append({"name": name, "email": email, "reason": str(e)})

    return {
        "message": "Email job completed",
        "sent": sent_emails,
        "skipped": skipped_emails
    }