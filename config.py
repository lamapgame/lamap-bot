import os
from dotenv import load_dotenv

# Load the stored environment variables
load_dotenv()

# Get the values
token = str(os.getenv("TOKEN"))
database_url = os.getenv("DATABASE_URL")