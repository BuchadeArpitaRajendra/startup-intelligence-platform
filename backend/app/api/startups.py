from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Startup, Founder
from ..schemas import StartupCreate, StartupUpdate, StartupResponse

router = APIRouter(prefix="/api/startups", tags=["startups"])

@router.post("/", response_model=StartupResponse)
def create_startup(startup: StartupCreate, db: Session = Depends(get_db)):
    """Create a new startup"""
    # Check if founder exists
    founder = db.query(Founder).filter(Founder.id == startup.founder_id).first()
    if not founder:
        raise HTTPException(status_code=404, detail="Founder not found")
    
    # Create startup
    db_startup = Startup(**startup.dict())
    db.add(db_startup)
    db.commit()
    db.refresh(db_startup)
    return db_startup

@router.get("/", response_model=List[StartupResponse])
def get_startups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all startups"""
    startups = db.query(Startup).offset(skip).limit(limit).all()
    return startups

@router.get("/{startup_id}", response_model=StartupResponse)
def get_startup(startup_id: int, db: Session = Depends(get_db)):
    """Get a specific startup by ID"""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup

@router.put("/{startup_id}", response_model=StartupResponse)
def update_startup(startup_id: int, startup_update: StartupUpdate, db: Session = Depends(get_db)):
    """Update a startup"""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Update fields
    for key, value in startup_update.dict(exclude_unset=True).items():
        setattr(startup, key, value)
    
    db.commit()
    db.refresh(startup)
    return startup

@router.delete("/{startup_id}")
def delete_startup(startup_id: int, db: Session = Depends(get_db)):
    """Delete a startup"""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    db.delete(startup)
    db.commit()
    return {"message": f"Startup {startup_id} deleted successfully"}