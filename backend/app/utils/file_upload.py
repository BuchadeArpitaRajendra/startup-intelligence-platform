import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from datetime import datetime
from ..config import settings

def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """Validate if file extension is allowed"""
    extension = Path(filename).suffix.lower()
    return extension in allowed_extensions

def get_file_size(file: UploadFile) -> int:
    """Get file size in bytes"""
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    return size

async def save_upload_file(
    upload_file: UploadFile,
    subfolder: str,
    allowed_extensions: set
) -> str:
    """
    Save an uploaded file to the server
    
    Args:
        upload_file: The uploaded file
        subfolder: Subfolder under uploads/ (e.g., 'pitch_decks')
        allowed_extensions: Set of allowed extensions
    
    Returns:
        str: The saved file path
    """
    # Validate file type
    if not validate_file_extension(upload_file.filename, allowed_extensions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Check file size
    size = get_file_size(upload_file)
    if size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024} MB"
        )
    
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIR) / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = Path(upload_file.filename).stem
    extension = Path(upload_file.filename).suffix
    safe_filename = f"{original_name}_{timestamp}{extension}"
    file_path = upload_dir / safe_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return str(file_path)

async def save_pitch_deck(upload_file: UploadFile) -> str:
    """Save a pitch deck PDF file"""
    return await save_upload_file(
        upload_file,
        "pitch_decks",
        settings.ALLOWED_PDF_EXTENSIONS
    )

async def save_pitch_video(upload_file: UploadFile) -> str:
    """Save a pitch video file"""
    return await save_upload_file(
        upload_file,
        "pitch_videos",
        settings.ALLOWED_VIDEO_EXTENSIONS
    )