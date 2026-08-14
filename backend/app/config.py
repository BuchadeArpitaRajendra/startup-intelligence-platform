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
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_PDF_EXTENSIONS: set = {".pdf"}
    ALLOWED_VIDEO_EXTENSIONS: set = {".mp4", ".mov", ".avi", ".webm"}
    UPLOAD_DIR: str = "uploads"

settings = Settings()