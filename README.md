# Candidate Availability & Active-Lead Outreach Prototype

## Executive Summary
An automated AI-powered candidate outreach and interview scheduling solution designed to solve recruiter bandwidth bottlenecks. The system automates candidate intent determination, notice period/availability extraction from unstructured natural language replies, deterministic slot matching against recruiter calendars, and interview booking.

---

## Live Production Demo Links
- **Live Frontend Web Application**: [https://candidate-automation-frontend.onrender.com](https://candidate-automation-frontend.onrender.com)
- **Live Backend REST API**: [https://candidate-automation-backend.onrender.com](https://candidate-automation-backend.onrender.com)
- **Interactive Swagger Documentation**: [https://candidate-automation-backend.onrender.com/docs](https://candidate-automation-backend.onrender.com/docs)

---

## Key Value Proposition
- **Automated Outreach & Tracking**: Replaces manual candidate chasing with stateful automation.
- **Natural Language Parsing**: Uses LLMs exclusively for extraction (Intent, Notice Period, Availability).
- **Deterministic Scheduling Engine**: Separates extraction from decision-making to prevent AI hallucination and ensure scheduling reliability.
- **Human-in-the-Loop Escalation**: Automatically flags ambiguous responses or edge cases (`HUMAN_REVIEW_REQUIRED`).
- **Complete Audit Trail**: Every event is stored and timestamped in an event log.

---

## Architectural Principles: LLM vs. Deterministic Separation

```
Natural Language Candidate Reply
               │
               ▼
   [ LLM Extraction Layer ] ────► Structured JSON Output (Intent, Availability, Confidence)
               │
               ▼
[ Deterministic Decision Engine ] ─► Business Rules (Notice Period check, Slot Matching)
               │
               ▼
 [ State Machine & Scheduler ] ───► Calendar Event Creation & Email Confirmation
```

### Why LLM for Extraction Only?
- **LLM Responsibility**: Parsing unstructured human language into a strict JSON schema (`INTERESTED`, `NOT_INTERESTED`, `NEEDS_INFORMATION`, `UNCLEAR`).
- **Deterministic Code Responsibility**: Managing state transitions, verifying notice period limits, checking calendar availability, creating interview entries, and sending confirmation emails.
- **Benefit**: Zero risk of AI hallucinations directly booking calendar slots or incorrectly closing candidate profiles.

---

## Core Workflow Steps

1. **Candidate Selection & Profile**: Recruiter selects candidates from the dashboard containing resume score, skills, role, and current status.
2. **Initial Nudge Generation**: Personalized outreach message is generated and logged (`NUDGE_SENT`).
3. **Candidate Reply Processing**: Inbound natural language replies are received and sent to the parsing pipeline (`REPLY_RECEIVED`).
4. **AI Intent & Entity Extraction**: LLM returns structured JSON containing intent classification, active search status, notice period in days, candidate availability slots, and confidence score.
5. **Decision Engine Logic**:
   - `NOT_INTERESTED` ──► Update status to `CLOSED`.
   - `NEEDS_INFORMATION` ──► Update status to `FOLLOW_UP_REQUIRED`.
   - `UNCLEAR` or Low Confidence (< 0.70) ──► Update status to `HUMAN_REVIEW_REQUIRED`.
   - `INTERESTED` ──► Check notice period; if valid, update status to `READY_TO_SCHEDULE`.
6. **Calendar Matching**: Candidate availability ranges are intersected with available recruiter calendar slots to select the optimal interview time.
7. **Automated Scheduling**: Meeting link generated, interview logged, status set to `INTERVIEW_SCHEDULED`.
8. **Confirmation Dispatch**: Confirmation message containing date, time, and meeting link generated and logged (`Confirmation Sent`).

---

## State Machine Diagram

```
READY_FOR_OUTREACH ──► NUDGE_SENT ──► REPLY_RECEIVED ──► AI_ANALYZED
                                                             │
        ┌───────────────────────┬────────────────────────────┼────────────────────────┐
        ▼                       ▼                            ▼                        ▼
    INTERESTED            NOT_INTERESTED             NEEDS_INFORMATION             UNCLEAR
        │                       │                            │                        │
        ▼                       ▼                            ▼                        ▼
READY_TO_SCHEDULE            CLOSED                 FOLLOW_UP_REQUIRED      HUMAN_REVIEW_REQUIRED
        │
        ▼
CALENDAR_MATCHED
        │
        ▼
INTERVIEW_SCHEDULED
```

---

## Tech Stack & Project Structure

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, React Router
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy ORM, Pydantic v2
- **Database**: SQLite (SQLAlchemy models ready for PostgreSQL transition)
- **AI Abstraction**: OpenAI API integration with fallback Demo Mode mock provider

```
candidate-automation-prototype/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── routers/
│   │   │   └── candidates.py
│   │   ├── services/
│   │   │   └── llm.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── crud.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   └── CandidateDetail.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── ARCHITECTURE.md
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Local Setup & Quickstart

### Prerequisites
- Node.js v18+
- Python 3.10+

## API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/candidates` | List all candidates |
| `GET` | `/api/candidates/{id}` | Get candidate details |
| `POST` | `/api/candidates/{id}/outreach` | Trigger initial nudge outreach |
| `POST` | `/api/candidates/{id}/reply` | Submit simulated candidate reply & run AI pipeline |
| `POST` | `/api/candidates/{id}/schedule` | Match calendar & schedule interview |
| `GET` | `/api/candidates/{id}/timeline` | Retrieve candidate audit timeline |
| `GET` | `/api/dashboard/stats` | Fetch aggregate metric counts |

---

## Production Scalability Roadmap

1. **Asynchronous Task Processing**: Implement Celery + Redis for inbound webhook handling (e.g. SendGrid Inbound Parse or Gmail Webhooks).
2. **Database Migration**: Switch SQLite to PostgreSQL with connection pooling.
3. **Calendar Integration**: Replace mock provider with Google Calendar API / Microsoft Graph API OAuth flows.
4. **Email Services**: Integrate SendGrid SDK or AWS SES for real email dispatch.
5. **Observability**: Add Prometheus metrics and OpenTelemetry tracing for AI parsing success rates and escalation frequencies.
