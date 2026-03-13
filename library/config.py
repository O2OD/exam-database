import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DB_URL")
    
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL topilmadi.")

settings = Settings()