from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(String)
    skills = Column(String)
    resume_score = Column(Integer)
    current_company = Column(String)
    notice_period_days = Column(Integer, nullable=True)
    status = Column(String, default="READY_FOR_OUTREACH")

    timeline = relationship("TimelineEvent", back_populates="candidate")
    analyses = relationship("AIAnalysis", back_populates="candidate")
    interviews = relationship("Interview", back_populates="candidate")

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    action = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="timeline")

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    intent = Column(String)
    active_job_search = Column(Boolean)
    notice_period_days = Column(Integer, nullable=True)
    availability = Column(String, nullable=True)
    confidence = Column(Float)
    missing_information = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="analyses")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    recruiter_email = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    meeting_link = Column(String)
    status = Column(String, default="SCHEDULED")

    candidate = relationship("Candidate", back_populates="interviews")
