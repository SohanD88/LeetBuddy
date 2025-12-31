from dotenv import load_dotenv
import os

load_dotenv()  # looks for .env in project root

DATABASE_URL = os.getenv("DATABASE_URL")