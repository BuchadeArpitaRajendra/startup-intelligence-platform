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

class CoFounderInvitation(Base):
    __tablename__ = "cofounder_invitations"
    
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    inviter_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    invitee_email = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # Remove timezone=True
    created_at = Column(DateTime, server_default=func.now())  # Remove timezone=True
    
class PitchDeckComment(Base):
    __tablename__ = "pitch_deck_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    slide_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    startup = relationship("Startup")
    founder = relationship("Founder")

class PitchVideoComment(Base):
    __tablename__ = "pitch_video_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    timestamp = Column(Float, nullable=False)  # seconds in video
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    startup = relationship("Startup")
    founder = relationship("Founder")

class CoFounderRating(Base):
    __tablename__ = "cofounder_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    dimension = Column(String(100), nullable=False)  # founder_vision, business_model, etc.
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    startup = relationship("Startup")
    founder = relationship("Founder")

class DiscussionPost(Base):
    __tablename__ = "discussion_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("discussion_posts.id"), nullable=True)  # For replies
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    startup = relationship("Startup")
    founder = relationship("Founder")
    replies = relationship("DiscussionPost", backref="parent", remote_side=[id])

class FinalDecision(Base):
    __tablename__ = "final_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    decision = Column(String(50), nullable=False)  # approve, needs_changes, reject
    rationale = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    startup = relationship("Startup")
    founder = relationship("Founder")