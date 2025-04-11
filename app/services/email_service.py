import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError


load_dotenv()
GMAIL_USER= os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def send_email_with_ics(to_email: str, to_name: str, ics_path: str):
    msg = EmailMessage()
    msg["Subject"] = "The Bakehouse Shifts scheduler automation"
    msg["From"] =GMAIL_USER
    msg["To"] = to_email

    msg.set_content(f"""
Hi {to_name},

Attached is your work shift schedule.

To add it to your Google Calendar:

**For iPhone users:**
1. If you're viewing this email through the Gmail app, tap the "Add to Calendar" button.
2. If you're using the Apple Mail app, open the attached `.ics` file using either the Apple Calendar app or the Google Calendar app.

**Note:** This method works best on Android devices, or if you have the Google Calendar app installed on your iPhone.

Thanks,  
The Bakehouse
""")

    # Attach the .ics file
    with open(ics_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(ics_path)
    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        smtp.send_message(msg)

    

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False