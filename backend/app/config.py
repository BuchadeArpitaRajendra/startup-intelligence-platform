import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://app_user:app123@localhost:5432/startup_intelligence"
    )
    
    # JWT settings (for authentication later)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()