from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# === Founder Schemas ===
class FounderBase(BaseModel):
    email: EmailStr
    full_name: str
    expertise: Optional[str] = None
    experience_years: Optional[int] = 0

class FounderCreate(FounderBase):
    password: str

class FounderRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    expertise: Optional[str] = None
    experience_years: Optional[int] = 0

class FounderResponse(FounderBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# === Startup Schemas ===
class StartupBase(BaseModel):
    name: str
    industry: Optional[str] = None
    problem_statement: Optional[str] = None
    solution: Optional[str] = None
    target_customers: Optional[str] = None
    business_model: Optional[str] = None
    funding_requirement: Optional[float] = 0.0
    market_size: Optional[float] = 0.0
    competition: Optional[str] = None

class StartupCreate(StartupBase):
    founder_id: int

class StartupUpdate(StartupBase):
    pass

class StartupResponse(StartupBase):
    id: int
    founder_id: int
    status: str
    pitch_deck_url: Optional[str] = None
    pitch_video_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

# === Token Schemas ===
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    founder_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True