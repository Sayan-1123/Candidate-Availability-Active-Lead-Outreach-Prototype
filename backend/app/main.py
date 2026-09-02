from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import candidates
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Candidate Outreach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates.router, prefix="/api")
