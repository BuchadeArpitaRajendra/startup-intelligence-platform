from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models import Founder
from ..schemas import FounderRegister, FounderResponse, Token, LoginRequest
from ..auth import (
    authenticate_founder,
    create_access_token,
    get_password_hash,
    get_current_active_founder
)
from ..config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register", response_model=FounderResponse)
def register_founder(founder: FounderRegister, db: Session = Depends(get_db)):
    """Register a new founder"""
    # Check if email already exists
    existing = db.query(Founder).filter(Founder.email == founder.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(founder.password)
    
    # Create new founder
    db_founder = Founder(
        email=founder.email,
        full_name=founder.full_name,
        hashed_password=hashed_password,
        expertise=founder.expertise,
        experience_years=founder.experience_years
    )
    
    db.add(db_founder)
    db.commit()
    db.refresh(db_founder)
    
    return db_founder

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token"""
    founder = authenticate_founder(db, login_data.email, login_data.password)
    if not founder:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(founder.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Alternative login using OAuth2 form (for Swagger UI)
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login using OAuth2 form (for Swagger UI)"""
    founder = authenticate_founder(db, form_data.username, form_data.password)
    if not founder:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": founder.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=FounderResponse)
def get_current_user(current_founder: Founder = Depends(get_current_active_founder)):
    """Get the current authenticated founder's information"""
    return current_founder

@router.get("/test-auth")
def test_auth(current_founder: Founder = Depends(get_current_active_founder)):
    """Test endpoint to verify authentication works"""
    return {
        "message": "Authentication successful!",
        "founder_id": current_founder.id,
        "email": current_founder.email
    }