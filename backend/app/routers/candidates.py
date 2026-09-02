from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from ..services.llm import analyze_candidate_reply
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/candidates", response_model=list[schemas.CandidateResponse])
def read_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_candidates(db, skip=skip, limit=limit)

@router.get("/candidates/{candidate_id}", response_model=schemas.CandidateResponse)
def read_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

@router.get("/candidates/{candidate_id}/timeline", response_model=list[schemas.TimelineEventResponse])
def get_timeline(candidate_id: int, db: Session = Depends(get_db)):
    return crud.get_timeline(db, candidate_id=candidate_id)

@router.post("/candidates/{candidate_id}/outreach")
def start_outreach(candidate_id: int, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    msg = f"Hi {candidate.name}, I'm reaching out regarding a {candidate.role} opportunity that seems aligned with your experience in {candidate.skills}. Are you currently open to new opportunities? If yes, could you also let me know your notice period and general availability for an interview? Thanks!"
    
    crud.update_candidate_status(db, candidate_id, "NUDGE_SENT")
    crud.log_timeline(db, candidate_id, "Outreach Generated", f"Generated outreach message for {candidate.name}")
    crud.log_timeline(db, candidate_id, "Nudge Sent", f"Simulated sending email to {candidate.email}")
    
    return {"message": msg, "status": "NUDGE_SENT"}

@router.post("/candidates/{candidate_id}/reply")
def handle_reply(candidate_id: int, reply: schemas.CandidateReply, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    crud.update_candidate_status(db, candidate_id, "REPLY_RECEIVED")
    crud.log_timeline(db, candidate_id, "Reply Received", f"Candidate replied: '{reply.message}'")
    
    # Process with AI
    crud.log_timeline(db, candidate_id, "AI Analysis Started", "Analyzing candidate reply with LLM")
    analysis = analyze_candidate_reply(reply.message, candidate.role)
    
    crud.save_ai_analysis(db, candidate_id, analysis)
    
    intent = analysis.get("intent")
    crud.log_timeline(db, candidate_id, "AI Analysis Completed", f"Extracted Intent: {intent}")
    
    if intent == "INTERESTED":
        crud.update_candidate_status(db, candidate_id, "READY_TO_SCHEDULE")
        crud.log_timeline(db, candidate_id, "Status Updated", "Candidate marked as READY_TO_SCHEDULE")
    elif intent == "NOT_INTERESTED":
        crud.update_candidate_status(db, candidate_id, "CLOSED")
        crud.log_timeline(db, candidate_id, "Status Updated", "Candidate marked as CLOSED")
    elif intent == "NEEDS_INFORMATION":
        crud.update_candidate_status(db, candidate_id, "FOLLOW_UP_REQUIRED")
        crud.log_timeline(db, candidate_id, "Status Updated", "Candidate marked as FOLLOW_UP_REQUIRED")
    else:
        crud.update_candidate_status(db, candidate_id, "HUMAN_REVIEW_REQUIRED")
        crud.log_timeline(db, candidate_id, "Status Updated", "Candidate marked as HUMAN_REVIEW_REQUIRED")
        
    return {"analysis": analysis, "status": candidate.status}

@router.post("/candidates/{candidate_id}/schedule")
def schedule_interview(candidate_id: int, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    crud.log_timeline(db, candidate_id, "Calendar Check", "Checked recruiter calendar for available slots matching candidate availability")
    crud.log_timeline(db, candidate_id, "Slot Matched", "Found matching slot: Sept 8, 2026, 14:00")
    
    event_data = {
        "recruiter_email": "recruiter@example.com",
        "start_time": datetime.strptime("2026-09-08T14:00:00", "%Y-%m-%dT%H:%M:%S"),
        "end_time": datetime.strptime("2026-09-08T14:45:00", "%Y-%m-%dT%H:%M:%S"),
        "meeting_link": "https://meet.google.com/fake-demo-link"
    }
    
    crud.schedule_interview(db, candidate_id, event_data)
    crud.update_candidate_status(db, candidate_id, "INTERVIEW_SCHEDULED")
    crud.log_timeline(db, candidate_id, "Interview Scheduled", "Automatically scheduled interview and generated meeting link")
    
    confirm_msg = f"Hi {candidate.name},\nThanks for confirming your availability.\nYour {candidate.role} interview has been scheduled for:\nSeptember 8, 2026\n2:00 PM - 2:45 PM\nMeeting Link: {event_data['meeting_link']}\nLooking forward to speaking with you."
    crud.log_timeline(db, candidate_id, "Confirmation Sent", "Simulated sending confirmation email to candidate")
    
    return {"message": "Interview Scheduled", "event": event_data, "confirmation_email": confirm_msg}

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    candidates = crud.get_candidates(db)
    
    stats = {
        "total": len(candidates),
        "nudges_sent": len([c for c in candidates if c.status in ["NUDGE_SENT", "REPLY_RECEIVED", "READY_TO_SCHEDULE", "INTERVIEW_SCHEDULED", "CLOSED", "FOLLOW_UP_REQUIRED"]]),
        "replies_received": len([c for c in candidates if c.status in ["REPLY_RECEIVED", "READY_TO_SCHEDULE", "INTERVIEW_SCHEDULED", "CLOSED", "FOLLOW_UP_REQUIRED"]]),
        "interested": len([c for c in candidates if c.status in ["READY_TO_SCHEDULE", "INTERVIEW_SCHEDULED"]]),
        "follow_up_required": len([c for c in candidates if c.status == "FOLLOW_UP_REQUIRED"]),
        "interviews_scheduled": len([c for c in candidates if c.status == "INTERVIEW_SCHEDULED"])
    }
    return stats
