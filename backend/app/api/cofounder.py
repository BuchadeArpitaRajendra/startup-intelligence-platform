from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import (
    Startup, Founder, PitchDeckComment, PitchVideoComment,
    CoFounderRating, DiscussionPost, FinalDecision,CoFounderInvitation
)
from ..schemas import (
    PitchDeckCommentCreate, PitchDeckCommentResponse,
    PitchVideoCommentCreate, PitchVideoCommentResponse,
    RatingCreate, RatingResponse,
    DiscussionPostCreate, DiscussionPostResponse,
    FinalDecisionCreate, FinalDecisionResponse,
    StartupDetailResponse, FounderResponse
)
from ..auth import get_current_active_founder

router = APIRouter(prefix="/api/cofounder", tags=["cofounder"])

# Helper function to check if founder is authorized for a startup
def is_authorized_for_startup(startup_id: int, founder_id: int, db: Session) -> bool:
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        return False
    
    # Check if user is the founder
    if startup.founder_id == founder_id:
        return True
    
    # Check if user is an accepted co-founder
    invitation = db.query(CoFounderInvitation).filter(
        CoFounderInvitation.startup_id == startup_id,
        CoFounderInvitation.invitee_email == db.query(Founder).filter(Founder.id == founder_id).first().email,
        CoFounderInvitation.status == "accepted"
    ).first()
    
    if invitation:
        return True
    
    return False

# === Pitch Deck Comments ===
@router.post("/startup/{startup_id}/pitch-deck-comment", response_model=PitchDeckCommentResponse)
def add_pitch_deck_comment(
    startup_id: int,
    comment: PitchDeckCommentCreate,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Add a comment on a pitch deck slide"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to comment on this startup")
    
    db_comment = PitchDeckComment(
        startup_id=startup_id,
        founder_id=current_founder.id,
        slide_number=comment.slide_number,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # Add founder name
    response = PitchDeckCommentResponse.from_orm(db_comment)
    response.founder_name = current_founder.full_name
    return response

@router.get("/startup/{startup_id}/pitch-deck-comments", response_model=List[PitchDeckCommentResponse])
def get_pitch_deck_comments(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all pitch deck comments for a startup"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to view comments")
    
    comments = db.query(PitchDeckComment).filter(
        PitchDeckComment.startup_id == startup_id
    ).order_by(PitchDeckComment.slide_number).all()
    
    # Add founder names
    result = []
    for comment in comments:
        founder = db.query(Founder).filter(Founder.id == comment.founder_id).first()
        response = PitchDeckCommentResponse.from_orm(comment)
        response.founder_name = founder.full_name if founder else "Unknown"
        result.append(response)
    return result

# === Pitch Video Comments ===
@router.post("/startup/{startup_id}/pitch-video-comment", response_model=PitchVideoCommentResponse)
def add_pitch_video_comment(
    startup_id: int,
    comment: PitchVideoCommentCreate,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Add a timestamped comment on the pitch video"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to comment on this startup")
    
    db_comment = PitchVideoComment(
        startup_id=startup_id,
        founder_id=current_founder.id,
        timestamp=comment.timestamp,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    response = PitchVideoCommentResponse.from_orm(db_comment)
    response.founder_name = current_founder.full_name
    return response

@router.get("/startup/{startup_id}/pitch-video-comments", response_model=List[PitchVideoCommentResponse])
def get_pitch_video_comments(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all pitch video comments for a startup"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to view comments")
    
    comments = db.query(PitchVideoComment).filter(
        PitchVideoComment.startup_id == startup_id
    ).order_by(PitchVideoComment.timestamp).all()
    
    result = []
    for comment in comments:
        founder = db.query(Founder).filter(Founder.id == comment.founder_id).first()
        response = PitchVideoCommentResponse.from_orm(comment)
        response.founder_name = founder.full_name if founder else "Unknown"
        result.append(response)
    return result

# === Co-Founder Ratings ===
@router.post("/startup/{startup_id}/rate", response_model=RatingResponse)
def rate_startup(
    startup_id: int,
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Rate a startup on a specific dimension"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to rate this startup")
    
    # Check if rating already exists for this dimension
    existing = db.query(CoFounderRating).filter(
        CoFounderRating.startup_id == startup_id,
        CoFounderRating.founder_id == current_founder.id,
        CoFounderRating.dimension == rating.dimension
    ).first()
    
    if existing:
        # Update existing rating
        existing.rating = rating.rating
        existing.comment = rating.comment
        db.commit()
        db.refresh(existing)
        response = RatingResponse.from_orm(existing)
        response.founder_name = current_founder.full_name
        return response
    
    # Create new rating
    db_rating = CoFounderRating(
        startup_id=startup_id,
        founder_id=current_founder.id,
        dimension=rating.dimension,
        rating=rating.rating,
        comment=rating.comment
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    response = RatingResponse.from_orm(db_rating)
    response.founder_name = current_founder.full_name
    return response

@router.get("/startup/{startup_id}/ratings", response_model=List[RatingResponse])
def get_ratings(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all ratings for a startup"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to view ratings")
    
    ratings = db.query(CoFounderRating).filter(
        CoFounderRating.startup_id == startup_id
    ).all()
    
    result = []
    for rating in ratings:
        founder = db.query(Founder).filter(Founder.id == rating.founder_id).first()
        response = RatingResponse.from_orm(rating)
        response.founder_name = founder.full_name if founder else "Unknown"
        result.append(response)
    return result

# === Discussion Board ===
@router.post("/startup/{startup_id}/discussion", response_model=DiscussionPostResponse)
def create_discussion_post(
    startup_id: int,
    post: DiscussionPostCreate,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Create a discussion post or reply"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to post in this startup")
    
    # If it's a reply, check parent exists
    if post.parent_id:
        parent = db.query(DiscussionPost).filter(
            DiscussionPost.id == post.parent_id,
            DiscussionPost.startup_id == startup_id
        ).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent post not found")
    
    # Create the post
    db_post = DiscussionPost(
        startup_id=startup_id,
        founder_id=current_founder.id,
        content=post.content,
        parent_id=post.parent_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Get the founder name for the response
    founder = db.query(Founder).filter(Founder.id == current_founder.id).first()
    
    # Build response manually with proper fields
    return DiscussionPostResponse(
        id=db_post.id,
        startup_id=db_post.startup_id,
        founder_id=db_post.founder_id,
        content=db_post.content,
        parent_id=db_post.parent_id,
        created_at=db_post.created_at,
        updated_at=db_post.updated_at,
        founder_name=founder.full_name if founder else "Unknown",
        replies=[]  # New posts always have no replies
    )

@router.get("/startup/{startup_id}/discussion", response_model=List[DiscussionPostResponse])
def get_discussion_posts(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all discussion posts for a startup"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to view discussions")
    
    # Helper function to recursively build post tree
    def build_post_tree(post_id: int = None) -> List[DiscussionPostResponse]:
        if post_id is None:
            # Get top-level posts
            posts = db.query(DiscussionPost).filter(
                DiscussionPost.startup_id == startup_id,
                DiscussionPost.parent_id.is_(None)
            ).order_by(DiscussionPost.created_at.desc()).all()
        else:
            # Get replies to a specific post
            posts = db.query(DiscussionPost).filter(
                DiscussionPost.parent_id == post_id
            ).order_by(DiscussionPost.created_at).all()
        
        result = []
        for post in posts:
            founder = db.query(Founder).filter(Founder.id == post.founder_id).first()
            
            # Build response
            response = DiscussionPostResponse(
                id=post.id,
                startup_id=post.startup_id,
                founder_id=post.founder_id,
                content=post.content,
                parent_id=post.parent_id,
                created_at=post.created_at,
                updated_at=post.updated_at,
                founder_name=founder.full_name if founder else "Unknown",
                replies=[]  # Always initialize with empty list
            )
            
            # Recursively get replies
            replies = build_post_tree(post.id)
            if replies:
                response.replies = replies
            
            result.append(response)
        
        return result
    
    return build_post_tree()

@router.get("/startup/{startup_id}/discussion", response_model=List[DiscussionPostResponse])
def get_discussion_posts(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all discussion posts for a startup"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to view discussions")
    
    # Get top-level posts (no parent)
    posts = db.query(DiscussionPost).filter(
        DiscussionPost.startup_id == startup_id,
        DiscussionPost.parent_id.is_(None)
    ).order_by(DiscussionPost.created_at.desc()).all()
    
    result = []
    for post in posts:
        # Get founder info
        founder = db.query(Founder).filter(Founder.id == post.founder_id).first()
        
        # Get replies for this post
        replies = db.query(DiscussionPost).filter(
            DiscussionPost.parent_id == post.id
        ).order_by(DiscussionPost.created_at).all()
        
        # Build reply responses
        reply_responses = []
        for reply in replies:
            reply_founder = db.query(Founder).filter(Founder.id == reply.founder_id).first()
            reply_responses.append(
                DiscussionPostResponse(
                    id=reply.id,
                    startup_id=reply.startup_id,
                    founder_id=reply.founder_id,
                    content=reply.content,
                    parent_id=reply.parent_id,
                    created_at=reply.created_at,
                    updated_at=reply.updated_at,
                    founder_name=reply_founder.full_name if reply_founder else "Unknown",
                    replies=[]  # No nested replies for simplicity
                )
            )
        
        # Create main post response
        response = DiscussionPostResponse(
            id=post.id,
            startup_id=post.startup_id,
            founder_id=post.founder_id,
            content=post.content,
            parent_id=post.parent_id,
            created_at=post.created_at,
            updated_at=post.updated_at,
            founder_name=founder.full_name if founder else "Unknown",
            replies=reply_responses  # Add replies here
        )
        result.append(response)
    
    return result

# === Final Decision ===
@router.post("/startup/{startup_id}/decision", response_model=FinalDecisionResponse)
def make_final_decision(
    startup_id: int,
    decision: FinalDecisionCreate,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Make a final decision on a startup"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to make a decision")
    
    # Check if decision already exists
    existing = db.query(FinalDecision).filter(
        FinalDecision.startup_id == startup_id,
        FinalDecision.founder_id == current_founder.id
    ).first()
    
    if existing:
        existing.decision = decision.decision
        existing.rationale = decision.rationale
        db.commit()
        db.refresh(existing)
        response = FinalDecisionResponse.from_orm(existing)
        response.founder_name = current_founder.full_name
        return response
    
    db_decision = FinalDecision(
        startup_id=startup_id,
        founder_id=current_founder.id,
        decision=decision.decision,
        rationale=decision.rationale
    )
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    
    response = FinalDecisionResponse.from_orm(db_decision)
    response.founder_name = current_founder.full_name
    return response

@router.get("/startup/{startup_id}/decisions", response_model=List[FinalDecisionResponse])
def get_decisions(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get all final decisions for a startup"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to view decisions")
    
    decisions = db.query(FinalDecision).filter(
        FinalDecision.startup_id == startup_id
    ).all()
    
    result = []
    for decision in decisions:
        founder = db.query(Founder).filter(Founder.id == decision.founder_id).first()
        response = FinalDecisionResponse.from_orm(decision)
        response.founder_name = founder.full_name if founder else "Unknown"
        result.append(response)
    return result

# === Startup Details with All Co-Founder Data ===
@router.get("/startup/{startup_id}/full-details", response_model=StartupDetailResponse)
def get_startup_full_details(
    startup_id: int,
    db: Session = Depends(get_db),
    current_founder: Founder = Depends(get_current_active_founder)
):
    """Get full startup details with all co-founder data"""
    if not is_authorized_for_startup(startup_id, current_founder.id, db):
        raise HTTPException(status_code=403, detail="Not authorized to view this startup")
    
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    
    # Get all data
    co_founders = db.query(Founder).filter(Founder.id == startup.founder_id).all()
    
    pitch_comments = db.query(PitchDeckComment).filter(
        PitchDeckComment.startup_id == startup_id
    ).all()
    
    video_comments = db.query(PitchVideoComment).filter(
        PitchVideoComment.startup_id == startup_id
    ).all()
    
    ratings = db.query(CoFounderRating).filter(
        CoFounderRating.startup_id == startup_id
    ).all()
    
    # Fix: Build discussion responses manually
    discussions = db.query(DiscussionPost).filter(
        DiscussionPost.startup_id == startup_id,
        DiscussionPost.parent_id.is_(None)
    ).all()
    
    discussion_responses = []
    for post in discussions:
        # Get founder name
        founder = db.query(Founder).filter(Founder.id == post.founder_id).first()
        
        # Get replies
        replies = db.query(DiscussionPost).filter(
            DiscussionPost.parent_id == post.id
        ).order_by(DiscussionPost.created_at).all()
        
        # Build reply responses
        reply_responses = []
        for reply in replies:
            reply_founder = db.query(Founder).filter(Founder.id == reply.founder_id).first()
            reply_responses.append(
                DiscussionPostResponse(
                    id=reply.id,
                    startup_id=reply.startup_id,
                    founder_id=reply.founder_id,
                    content=reply.content,
                    parent_id=reply.parent_id,
                    created_at=reply.created_at,
                    updated_at=reply.updated_at,
                    founder_name=reply_founder.full_name if reply_founder else "Unknown",
                    replies=[]  # No nested replies
                )
            )
        
        discussion_responses.append(
            DiscussionPostResponse(
                id=post.id,
                startup_id=post.startup_id,
                founder_id=post.founder_id,
                content=post.content,
                parent_id=post.parent_id,
                created_at=post.created_at,
                updated_at=post.updated_at,
                founder_name=founder.full_name if founder else "Unknown",
                replies=reply_responses
            )
        )
    
    decisions = db.query(FinalDecision).filter(
        FinalDecision.startup_id == startup_id
    ).all()
    
    # Build response
    response = StartupDetailResponse(
        id=startup.id,
        name=startup.name,
        industry=startup.industry,
        problem_statement=startup.problem_statement,
        solution=startup.solution,
        target_customers=startup.target_customers,
        business_model=startup.business_model,
        funding_requirement=startup.funding_requirement,
        market_size=startup.market_size,
        competition=startup.competition,
        founder_id=startup.founder_id,
        status=startup.status,
        pitch_deck_url=startup.pitch_deck_url,
        pitch_video_url=startup.pitch_video_url,
        created_at=startup.created_at,
        updated_at=startup.updated_at,
        co_founders=[FounderResponse.model_validate(f) for f in co_founders],
        pitch_deck_comments=[PitchDeckCommentResponse.model_validate(c) for c in pitch_comments],
        pitch_video_comments=[PitchVideoCommentResponse.model_validate(c) for c in video_comments],
        ratings=[RatingResponse.model_validate(r) for r in ratings],
        discussions=discussion_responses,  # Use manually built responses
        decisions=[FinalDecisionResponse.model_validate(d) for d in decisions]
    )
    
    return response