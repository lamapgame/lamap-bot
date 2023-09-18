import os
from dotenv import load_dotenv

# Load the stored environment variables
load_dotenv()

# Get the values
TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
LOGGING_CHAT_ID = os.getenv("LOGGING_CHAT_ID")
