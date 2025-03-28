import pandas as pd
import requests
import re

SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTXg9gEJ1C6uHTQi1HxVFQQqf5wFn8JhGOjDG3srCU8yhiYrNtTQNXI4qYd_-BIOj_Y7k8jVmC69OkS/pub?output=csv'

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
