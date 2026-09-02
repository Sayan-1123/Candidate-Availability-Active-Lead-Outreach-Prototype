import os
import uvicorn
from app.main import app
from app.database import engine, Base, SessionLocal
from app.models import Candidate

def seed_db():
    db = SessionLocal()
    if db.query(Candidate).count() == 0:
        candidates = [
            Candidate(name="Sayan Sharma", email="sayan@example.com", phone="1234567890", role="Backend Engineer", skills="Python, Django, PostgreSQL", resume_score=91, current_company="ABC Tech", status="READY_FOR_OUTREACH"),
            Candidate(name="Alice Smith", email="alice@example.com", phone="1234567891", role="Frontend Developer", skills="React, TypeScript, CSS", resume_score=88, current_company="TechCorp", status="READY_FOR_OUTREACH"),
            Candidate(name="Bob Johnson", email="bob@example.com", phone="1234567892", role="Full Stack Engineer", skills="Node.js, React, MongoDB", resume_score=95, current_company="Startup Inc", status="READY_FOR_OUTREACH"),
            Candidate(name="Charlie Brown", email="charlie@example.com", phone="1234567893", role="DevOps Engineer", skills="AWS, Docker, Kubernetes", resume_score=85, current_company="CloudNet", status="READY_FOR_OUTREACH"),
            Candidate(name="Diana Prince", email="diana@example.com", phone="1234567894", role="Data Scientist", skills="Python, Machine Learning, SQL", resume_score=92, current_company="DataWorks", status="READY_FOR_OUTREACH"),
        ]
        db.add_all(candidates)
        db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_db()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
