# System Architecture & Technical Specifications

## 1. High-Level System Architecture

The Candidate Availability & Active-Lead Prototype follows a decoupled micro-architecture separating presentation, state orchestrations, machine learning extraction, and data persistence.

```
┌─────────────────────────────────────────────────────────┐
│                    React Web UI                         │
│   (Dashboard, Candidate Cards, Timeline & Actions)       │
└────────────────────────────┬────────────────────────────┘
                             │ HTTP REST API
                             ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │               State Machine Engine                │  │
│  └─────────────────────────┬─────────────────────────┘  │
│                            │                            │
│     ┌──────────────────────┼──────────────────────┐     │
│     ▼                      ▼                      ▼     │
│ ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │
│ │ LLM Extractor │  │ Calendar Engine│  │ Email Adapter │ │
│ └───────────────┘  └───────────────┘  └───────────────┘ │
└────────────────────────────┬────────────────────────────┘
                             │ SQLAlchemy ORM
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  Relational Database                    │
│   (Candidates, TimelineEvents, AIAnalyses, Interviews)  │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Core Operational Workflow & State Transitions

The system state machine strictly governs candidate status progression:

```
[ READY_FOR_OUTREACH ]
          │
          ├─► Action: Trigger Outreach Message
          ▼
    [ NUDGE_SENT ]
          │
          ├─► Action: Candidate Replies (Natural Language)
          ▼
   [ REPLY_RECEIVED ]
          │
          ├─► Action: AI Parsing (Intent & Availability Extraction)
          ▼
     [ AI_ANALYZED ]
          │
          ├──► Intent == NOT_INTERESTED ────────► [ CLOSED ]
          ├──► Intent == NEEDS_INFORMATION ──────► [ FOLLOW_UP_REQUIRED ]
          ├──► Intent == UNCLEAR ───────────────► [ HUMAN_REVIEW_REQUIRED ]
          └──► Intent == INTERESTED ────────────► [ READY_TO_SCHEDULE ]
                                                         │
                                                         ├─► Action: Calendar Match & Schedule
                                                         ▼
                                                [ INTERVIEW_SCHEDULED ]
```

---

## 3. Separation of Concerns: LLM Extraction vs. Deterministic Control

### LLM Responsibility (Unstructured Data Understanding)
The LLM is invoked solely to convert unstructured candidate text into structured JSON output matching a predefined Pydantic schema:

- **Input**: Candidate natural language reply, current date, job role context.
- **Output Schema**:
  - `intent`: `INTERESTED` | `NOT_INTERESTED` | `NEEDS_INFORMATION` | `UNCLEAR`
  - `active_job_search`: boolean
  - `notice_period_days`: integer or null
  - `availability`: list of date/time slot objects
  - `confidence`: float [0.0 - 1.0]
  - `missing_information`: list of strings

### Deterministic Backend Responsibility (Decision Logic & Execution)
The LLM output is never allowed to directly execute database mutations or external actions. The backend decision engine handles execution based on strict deterministic rules:

1. **Safety Check**: If `confidence < 0.70` or `intent == UNCLEAR`, force transition to `HUMAN_REVIEW_REQUIRED`.
2. **Business Rule Check**: If `notice_period_days > 60`, mark candidate for human review before scheduling.
3. **Calendar Intersection Logic**: Calculate exact overlapping time windows between Candidate Availability and Recruiter Available Slots.
4. **Transaction & Scheduling**: Create the `Interview` record, generate unique meeting URI, log `TimelineEvent`, and update candidate state.

---

## 4. Database Schema Design

### Candidates Table
- `id` (PK, Integer)
- `name` (String)
- `email` (String, Unique)
- `phone` (String)
- `role` (String)
- `skills` (String)
- `resume_score` (Integer)
- `current_company` (String)
- `notice_period_days` (Integer, Nullable)
- `status` (String)

### AIAnalyses Table
- `id` (PK, Integer)
- `candidate_id` (FK -> Candidates.id)
- `intent` (String)
- `active_job_search` (Boolean)
- `notice_period_days` (Integer, Nullable)
- `availability` (Text/JSON)
- `confidence` (Float)
- `missing_information` (Text)
- `created_at` (DateTime)

### TimelineEvents Table
- `id` (PK, Integer)
- `candidate_id` (FK -> Candidates.id)
- `action` (String)
- `description` (Text)
- `created_at` (DateTime)

### Interviews Table
- `id` (PK, Integer)
- `candidate_id` (FK -> Candidates.id)
- `recruiter_email` (String)
- `start_time` (DateTime)
- `end_time` (DateTime)
- `meeting_link` (String)
- `status` (String)

---

## 5. Enterprise & Production Readiness Roadmap

1. **Event-Driven Architecture**: Transition from synchronous REST polling to WebSockets/Server-Sent Events (SSE) for live UI state updates.
2. **Inbound Webhook Handlers**: Add webhook endpoints for SendGrid/Mailgun to process candidate replies asynchronously via Celery queues.
3. **Calendar Protocol Standard**: Integrate Google Calendar API (`google-api-python-client`) and Outlook CalDAV endpoints.
4. **Security & Compliance**: Implement OAuth2 JWT authentication, encryption for PII candidate data at rest, and audit trail retention policies.
