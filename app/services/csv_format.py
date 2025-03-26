import pandas as pd
from dotenv import load_dotenv
import os


#loading environment variables from .env file
load_dotenv()



# Replace with your Google Sheets link
SHEET_URL = os.getenv("SHEET_URL")
print("SHEET_URL:", SHEET_URL)


# Read the spreadsheet into a pandas DataFrame
try:
        df = pd.read_csv(SHEET_URL)
        # Filter the DataFrame based on the condition
        df_filtered = df[df['shift'].isin(['AM', 'PM'])]
        print(df_filtered)
        print(df_filtered.head())
        # Convert the filtered DataFrame to JSON
        json_data = df_filtered.to_json(orient='records')
except Exception as e:
        print("Error reading the spreadsheet:", e)



