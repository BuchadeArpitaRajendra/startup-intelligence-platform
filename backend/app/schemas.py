from pydantic import BaseModel, EmailStr, ConfigDict,field_validator
from typing import Optional,List
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
    founder_id: Optional[int] = None

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
    
    class Config:
        from_attributes = True 
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

# === Invitation Schemas ===
class InvitationCreate(BaseModel):
    invitee_email: str
    role: Optional[str] = "co-founder"

class InvitationResponse(BaseModel):
    id: int
    startup_id: int
    inviter_id: int
    invitee_email: str
    status: str
    token: str
    expires_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# === Pitch Deck Comment Schemas ===
class PitchDeckCommentCreate(BaseModel):
    slide_number: int
    content: str

class PitchDeckCommentResponse(BaseModel):
    id: int
    startup_id: int
    founder_id: int
    slide_number: int
    content: str
    created_at: datetime
    founder_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# === Pitch Video Comment Schemas ===
class PitchVideoCommentCreate(BaseModel):
    timestamp: float
    content: str

class PitchVideoCommentResponse(BaseModel):
    id: int
    startup_id: int
    founder_id: int
    timestamp: float
    content: str
    created_at: datetime
    founder_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# === Rating Schemas ===
class RatingCreate(BaseModel):
    dimension: str  # founder_vision, business_model, product_readiness, market_opportunity, team_strength, investment_readiness
    rating: int  # 1-5
    comment: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    startup_id: int
    founder_id: int
    dimension: str
    rating: int
    comment: Optional[str]
    created_at: datetime
    founder_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# === Discussion Schemas ===
class DiscussionPostCreate(BaseModel):
    """Schema for creating a discussion post"""
    content: str
    parent_id: Optional[int] = None

class DiscussionPostResponse(BaseModel):
    """Schema for returning a discussion post"""
    id: int
    startup_id: int
    founder_id: int
    content: str
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    founder_name: Optional[str] = None
    replies: List['DiscussionPostResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('replies', mode='before')
    @classmethod
    def validate_replies(cls, v):
        """Ensure replies is always a list"""
        if v is None:
            return []
        return v

# Enable forward references for recursive types
DiscussionPostResponse.model_rebuild()
    
# === Final Decision Schemas ===
class FinalDecisionCreate(BaseModel):
    decision: str  # approve, needs_changes, reject
    rationale: Optional[str] = None

class FinalDecisionResponse(BaseModel):
    id: int
    startup_id: int
    founder_id: int
    decision: str
    rationale: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    founder_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# Update StartupResponse to include co-founder info
class StartupDetailResponse(StartupResponse):
    co_founders: List[FounderResponse] = []
    pitch_deck_comments: List[PitchDeckCommentResponse] = []
    pitch_video_comments: List[PitchVideoCommentResponse] = []
    ratings: List[RatingResponse] = []
    discussions: List[DiscussionPostResponse] = []
    decisions: List[FinalDecisionResponse] = []
    
    class Config:
        from_attributes = True

# === Discussion Schemas ===
class DiscussionPostCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None

class DiscussionPostResponse(BaseModel):
    id: int
    startup_id: int
    founder_id: int
    content: str
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    founder_name: Optional[str] = None
    replies: List['DiscussionPostResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('replies', mode='before')
    @classmethod
    def validate_replies(cls, v):
        """Ensure replies is always a list"""
        if v is None:
            return []
        return v

