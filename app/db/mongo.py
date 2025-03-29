import os
from pymongo import MongoClient
from dotenv import load_dotenv

#loading environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
print("MONGO_URI:", MONGO_URI)
print("DB_NAME:", DB_NAME)
# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
def get_workers_from_db(): # fake function to simulate fetching workers from a database
    workers = ["nazik", "nabor", "maher", "maria", "valeria", "charlie","eduardo", "rafa"]
    return workers    # Return the list of workers as a response
