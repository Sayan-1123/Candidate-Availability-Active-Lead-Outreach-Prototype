from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    email: str
    phone: str
    role: str
    skills: str
    resume_score: int
    current_company: str
    notice_period_days: Optional[int] = None
    status: str

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int

    class Config:
        from_attributes = True

class CandidateReply(BaseModel):
    message: str

class OutreachResponse(BaseModel):
    message: str

class AIAnalysisResponse(BaseModel):
    intent: str
    active_job_search: bool
    notice_period_days: Optional[int]
    availability: Optional[str]
    confidence: float
    missing_information: Optional[str]

class InterviewBase(BaseModel):
    recruiter_email: str
    start_time: datetime
    end_time: datetime
    meeting_link: str

class TimelineEventResponse(BaseModel):
    action: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
