import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Get connection settings with default values
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "scheduler_db")

# Print connection info for debugging
print(f"MONGO_URI: {MONGO_URI}")
print(f"DB_NAME: {DB_NAME}")

# MongoDB connection with error handling
try:
    # Validate settings
    if not isinstance(DB_NAME, str):
        raise TypeError("DB_NAME must be a string")
    
    # Attempt connection
    client = MongoClient(MONGO_URI)
    
    # Verify connection is working
    client.admin.command('ping')
    print("MongoDB connection established successfully.")
    
    # Connect to the database
    db = client[DB_NAME]
    
except (ConnectionFailure, ConfigurationError) as e:
    print(f"MongoDB connection error: {e}", file=sys.stderr)
    # Fallback to a minimal client that won't crash the app
    # but functions requiring DB access will fail gracefully
    client = None
    db = None
except TypeError as e:
    print(f"MongoDB configuration error: {e}", file=sys.stderr)
    client = None
    db = None
except Exception as e:
    print(f"Unexpected error when connecting to MongoDB: {e}", file=sys.stderr)
    client = None
    db = None
def get_workers_from_db(): # fake function to simulate fetching workers from a database
    # Check if database connection is available
    if db is None:
        print("Warning: Database connection not available, returning default workers list")
    
    workers = ["nazik", "nabor", "maher", "maria", "valeria", "charlie", "eduardo", "rafa"]
    return workers    # Return the list of workers as a response

def is_db_connected():
    """Check if the database connection is available"""
    return client is not None and db is not None
