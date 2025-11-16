import motor.motor_asyncio
from dotenv import load_dotenv  # <-- Import karo
import os                     # <-- Import karo

# Yeh .env file se saare variables load kar dega
load_dotenv() 

# Ab code ke baahar (environment) se variables lo
MONGO_URI = os.getenv("MONGO_URI") 
DB_NAME = os.getenv("DB_NAME", "todo_db") # Default de sakte hain
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "todos")

# Check karo ki variable mila ya nahi
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables. Did you create a .env file?")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("Connected to MongoDB!")