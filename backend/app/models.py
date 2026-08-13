from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Founder(Base):
    __tablename__ = "founders"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    expertise = Column(Text)  # JSON string of expertise areas
    experience_years = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with startups (one founder can have many startups)
    startups = relationship("Startup", back_populates="founder")

class Startup(Base):
    __tablename__ = "startups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(100))
    problem_statement = Column(Text)
    solution = Column(Text)
    target_customers = Column(Text)
    business_model = Column(String(100))
    funding_requirement = Column(Float, default=0.0)
    market_size = Column(Float, default=0.0)
    competition = Column(Text)
    
    # Foreign key to founder
    founder_id = Column(Integer, ForeignKey("founders.id"))
    
    # File URLs
    pitch_deck_url = Column(String(500))
    pitch_video_url = Column(String(500))
    
    # Status
    status = Column(String(50), default="draft")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with founder
    founder = relationship("Founder", back_populates="startups")