import pandas as pd
import re
from dotenv import load_dotenv
import os

# Loading environment variables from .env file
load_dotenv()

# Get connection settings with default values
SHEET_URL = os.getenv("SHEET_URL")

# Split worker names based on common separators
def split_workers(raw_value):
    if pd.isna(raw_value):
        return []
    return [name.strip() for name in re.split(r'[+&/|,]', str(raw_value)) if name.strip()]

# Reshape the matrix-style schedule
def reshape_schedule_matrix_style(df):
    if df.empty:
        raise ValueError("Filtered schedule is empty. No AM/PM shift data found.")

    reshaped = []

    for _, row in df.iterrows():
        location = str(row.get("location", "")).strip().lower()
        shift = str(row.get("shift", "")).strip().lower()

        if shift not in ["am", "pm"]:
            continue

        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            raw_workers = row.get(day)
            if pd.isna(raw_workers):
                continue

            for name in split_workers(raw_workers):
                reshaped.append({
                    "worker": name.lower(),
                    "day": day,
                    "shift": shift,
                    "location": location
                })

    if not reshaped:
        raise ValueError("Reshaped schedule is empty. No valid worker data found.")

    return reshaped

# Public interface for the app to use

def get_reshaped_schedule():
    try:
        df = pd.read_csv(SHEET_URL)
        if df.empty:
            raise ValueError("The CSV file is empty or malformed.")

        df_filtered = df[df['shift'].isin(['AM', 'PM'])]
        return reshape_schedule_matrix_style(df_filtered)

    except Exception as e:
        raise RuntimeError(f"Failed to fetch or reshape schedule: {e}")
# Optional: clean phone numbers or emails if needed
def clean_string(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()

# Public method to return reshaped list of worker info
def get_workers_from_csv():
    try:
        df = pd.read_csv(SHEET_URL)
        if df.empty:
            raise ValueError("Worker CSV is empty or malformed.")

        workers = []
        for _, row in df.iterrows():
            worker = {
                "name": clean_string(row.get("name")),
                "email": clean_string(row.get("email")),
                "phone": clean_string(row.get("phone")),
            }
            if worker["name"]:  # Only add if name exists
                workers.append(worker)

        if not workers:
            raise ValueError("No valid worker entries found.")

        return workers

    except Exception as e:
        raise RuntimeError(f"Failed to fetch worker info: {e}") 