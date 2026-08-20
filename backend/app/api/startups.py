from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Startup, Founder
from ..schemas import StartupCreate, StartupUpdate, StartupResponse
from ..utils.file_upload import save_pitch_deck, save_pitch_video
from ..auth import get_current_active_founder

router = APIRouter(prefix="/api/startups", tags=["startups"])

@router.post("/", response_model=StartupResponse)
def create_startup(
    startup: StartupCreate, 
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder) 
):
    # Convert to dict and EXCLUDE 'founder_id' to avoid duplicate key errors
    startup_data = startup.dict(exclude={'founder_id'}) 
    
    # Create the startup with the authenticated user's ID
    db_startup = Startup(
        **startup_data, 
        founder_id=current_founder.id
    )
    
    db.add(db_startup)
    db.commit()
    db.refresh(db_startup)
    return db_startup

@router.get("/", response_model=List[StartupResponse])
def get_startups(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)  # 👈 ADD THIS
):
    """Get all startups created by the logged-in founder"""
    startups = db.query(Startup).filter(
        Startup.founder_id == current_founder.id  # 👈 Filter by logged-in user
    ).offset(skip).limit(limit).all()
    return startups

@router.get("/{startup_id}", response_model=StartupResponse)
def get_startup(startup_id: int, db: Session = Depends(get_db)):
    """Get a specific startup by ID"""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup

@router.put("/{startup_id}", response_model=StartupResponse)
def update_startup(
    startup_id: int, 
    startup_update: StartupUpdate, 
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)  # Add this
):
    """Update a startup (requires authentication and ownership)"""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Check if founder owns this startup
    if startup.founder_id != current_founder.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this startup")
    
    # Update fields
    for key, value in startup_update.dict(exclude_unset=True).items():
        setattr(startup, key, value)
    
    db.commit()
    db.refresh(startup)
    return startup

@router.delete("/{startup_id}")
def delete_startup(
    startup_id: int, 
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)  # Add this
):
    """Delete a startup (requires authentication and ownership)"""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Check if founder owns this startup
    if startup.founder_id != current_founder.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this startup")
    
    db.delete(startup)
    db.commit()
    return {"message": f"Startup {startup_id} deleted successfully"}

@router.post("/{startup_id}/upload-pitch-deck")
async def upload_pitch_deck(
    startup_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)  # Protect with auth
):
    """Upload a pitch deck (PDF) for a startup"""
    # Check if startup exists
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Check if founder owns this startup
    if startup.founder_id != current_founder.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this startup")
    
    try:
        # Save the file
        file_path = await save_pitch_deck(file)
        
        # Update startup with file path
        startup.pitch_deck_url = file_path
        db.commit()
        db.refresh(startup)
        
        return {
            "message": "Pitch deck uploaded successfully",
            "file_path": file_path,
            "startup_id": startup_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{startup_id}/upload-pitch-video")
async def upload_pitch_video(
    startup_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)  # Protect with auth
):
    """Upload a pitch video for a startup"""
    # Check if startup exists
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Check if founder owns this startup
    if startup.founder_id != current_founder.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this startup")
    
    try:
        # Save the file
        file_path = await save_pitch_video(file)
        
        # Update startup with file path
        startup.pitch_video_url = file_path
        db.commit()
        db.refresh(startup)
        
        return {
            "message": "Pitch video uploaded successfully",
            "file_path": file_path,
            "startup_id": startup_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=StartupResponse)
def create_startup(
    startup: StartupCreate,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Create a new startup (requires authentication)"""
    # Use authenticated user's ID if founder_id is not provided
    founder_id = startup.founder_id or current_founder.id
    
    # Check if the founder exists (if provided)
    founder = db.query(Founder).filter(Founder.id == founder_id).first()
    if not founder:
        raise HTTPException(status_code=404, detail="Founder not found")
    
    # Create startup with the determined founder_id
    db_startup = Startup(
        name=startup.name,
        industry=startup.industry,
        problem_statement=startup.problem_statement,
        solution=startup.solution,
        target_customers=startup.target_customers,
        business_model=startup.business_model,
        funding_requirement=startup.funding_requirement,
        market_size=startup.market_size,
        competition=startup.competition,
        founder_id=founder_id  # Use the determined ID
    )
    db.add(db_startup)
    db.commit()
    db.refresh(db_startup)
    return db_startup