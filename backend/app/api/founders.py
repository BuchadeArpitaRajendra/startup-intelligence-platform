from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import get_db
from ..models import Founder
from ..schemas import FounderCreate, FounderResponse

router = APIRouter(prefix="/api/founders", tags=["founders"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=FounderResponse)
def create_founder(founder: FounderCreate, db: Session = Depends(get_db)):
    """Register a new founder"""
    # Check if email exists
    existing = db.query(Founder).filter(Founder.email == founder.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed = pwd_context.hash(founder.password)
    
    # Create founder
    db_founder = Founder(
        email=founder.email,
        full_name=founder.full_name,
        hashed_password=hashed,
        expertise=founder.expertise,
        experience_years=founder.experience_years
    )
    db.add(db_founder)
    db.commit()
    db.refresh(db_founder)
    return db_founder

@router.get("/{founder_id}", response_model=FounderResponse)
def get_founder(founder_id: int, db: Session = Depends(get_db)):
    """Get founder by ID"""
    founder = db.query(Founder).filter(Founder.id == founder_id).first()
    if not founder:
        raise HTTPException(status_code=404, detail="Founder not found")
    return founder

@router.get("/{founder_id}/startups")
def get_founder_startups(founder_id: int, db: Session = Depends(get_db)):
    """Get all startups created by a founder"""
    founder = db.query(Founder).filter(Founder.id == founder_id).first()
    if not founder:
        raise HTTPException(status_code=404, detail="Founder not found")
    return founder.startups