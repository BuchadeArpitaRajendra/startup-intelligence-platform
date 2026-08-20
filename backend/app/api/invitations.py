from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import secrets
from ..database import get_db
from ..models import Startup, Founder, CoFounderInvitation
from ..schemas import InvitationCreate, InvitationResponse
from ..auth import get_current_active_founder

router = APIRouter(prefix="/api/invitations", tags=["invitations"])

@router.post("/{startup_id}", response_model=InvitationResponse)
def send_invitation(
    startup_id: int,
    invitation: InvitationCreate,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Send a co-founder invitation"""
    # Check if startup exists
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Check if current user is the founder
    if startup.founder_id != current_founder.id:
        raise HTTPException(status_code=403, detail="Only the startup founder can send invitations")
    
    # Check if email is already invited
    existing = db.query(CoFounderInvitation).filter(
        CoFounderInvitation.startup_id == startup_id,
        CoFounderInvitation.invitee_email == invitation.invitee_email,
        CoFounderInvitation.status == "pending"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Invitation already sent to this email")
    
    # Generate token
    token = secrets.token_urlsafe(32)
    
    # Create invitation (expires in 7 days)
    db_invitation = CoFounderInvitation(
        startup_id=startup_id,
        inviter_id=current_founder.id,
        invitee_email=invitation.invitee_email,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation

@router.get("/", response_model=list[InvitationResponse])
def get_invitations(
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all invitations for the current founder"""
    invitations = db.query(CoFounderInvitation).filter(
        CoFounderInvitation.invitee_email == current_founder.email
    ).all()
    return invitations

@router.get("/pending", response_model=list[InvitationResponse])
def get_pending_invitations(
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get pending invitations for the current founder"""
    now = datetime.now(timezone.utc)
    invitations = db.query(CoFounderInvitation).filter(
        CoFounderInvitation.invitee_email == current_founder.email,  # Make sure this matches the new email!
        CoFounderInvitation.status == "pending",
        CoFounderInvitation.expires_at > now
    ).all()
    return invitations

@router.post("/{token}/accept")
def accept_invitation(
    token: str,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Accept a co-founder invitation"""
    invitation = db.query(CoFounderInvitation).filter(
        CoFounderInvitation.token == token
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    if invitation.invitee_email != current_founder.email:
        raise HTTPException(status_code=403, detail="This invitation is not for you")
    
    if invitation.status != "pending":
        raise HTTPException(status_code=400, detail=f"Invitation already {invitation.status}")
    
    # FIX: Use timezone-aware comparison
    now = datetime.now(timezone.utc)
    if invitation.expires_at < now:
        invitation.status = "expired"
        db.commit()
        raise HTTPException(status_code=400, detail="Invitation has expired")
    
    # Accept invitation
    invitation.status = "accepted"
    db.commit()
    return {"message": "Invitation accepted successfully"}

@router.post("/{token}/reject")
def reject_invitation(
    token: str,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Reject a co-founder invitation"""
    invitation = db.query(CoFounderInvitation).filter(
        CoFounderInvitation.token == token
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    if invitation.invitee_email != current_founder.email:
        raise HTTPException(status_code=403, detail="This invitation is not for you")
    
    if invitation.status != "pending":
        raise HTTPException(status_code=400, detail=f"Invitation already {invitation.status}")
    
    invitation.status = "rejected"
    db.commit()
    return {"message": "Invitation rejected"}

@router.get("/startup/{startup_id}", response_model=list[InvitationResponse])
def get_startup_invitations(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all invitations for a startup"""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Check if current user is the founder or a co-founder
    if startup.founder_id != current_founder.id:
        raise HTTPException(status_code=403, detail="Not authorized to view invitations")
    
    invitations = db.query(CoFounderInvitation).filter(
        CoFounderInvitation.startup_id == startup_id
    ).all()
    return invitations