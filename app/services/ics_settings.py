# services/ics_settings.py

# Day names (English) mapped to weekday index (0 = Monday)
DAY_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

# Shift start and end times for weekdays vs weekends
SHIFT_TIMES = {
    "AM": {
        "weekday": ("07:00", "13:00"),
        "weekend": ("07:00", "14:00")
    },
    "PM": {
        "weekday": ("13:00", "18:00"),
        "weekend": ("14:00", "18:00")
    }
}
