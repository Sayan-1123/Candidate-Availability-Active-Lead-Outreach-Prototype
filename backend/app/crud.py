from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def get_candidates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Candidate).offset(skip).limit(limit).all()

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = models.Candidate(**candidate.model_dump())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def update_candidate_status(db: Session, candidate_id: int, status: str):
    db_candidate = get_candidate(db, candidate_id)
    if db_candidate:
        db_candidate.status = status
        db.commit()
        db.refresh(db_candidate)
    return db_candidate

def log_timeline(db: Session, candidate_id: int, action: str, description: str):
    event = models.TimelineEvent(candidate_id=candidate_id, action=action, description=description)
    db.add(event)
    db.commit()

def save_ai_analysis(db: Session, candidate_id: int, analysis_data: dict):
    analysis = models.AIAnalysis(
        candidate_id=candidate_id,
        intent=analysis_data.get("intent"),
        active_job_search=analysis_data.get("active_job_search", False),
        notice_period_days=analysis_data.get("notice_period_days"),
        availability=str(analysis_data.get("availability")),
        confidence=analysis_data.get("confidence", 0.0),
        missing_information=str(analysis_data.get("missing_information", []))
    )
    db.add(analysis)
    db.commit()
    
def schedule_interview(db: Session, candidate_id: int, event_data: dict):
    interview = models.Interview(
        candidate_id=candidate_id,
        recruiter_email=event_data["recruiter_email"],
        start_time=event_data["start_time"],
        end_time=event_data["end_time"],
        meeting_link=event_data["meeting_link"]
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview

def get_timeline(db: Session, candidate_id: int):
    return db.query(models.TimelineEvent).filter(models.TimelineEvent.candidate_id == candidate_id).order_by(models.TimelineEvent.created_at.desc()).all()
