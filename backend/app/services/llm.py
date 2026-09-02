import json
import os
from datetime import datetime

def analyze_candidate_reply(reply: str, job_role: str):
    # DEMO_MODE logic - simulate LLM analysis
    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
    
    if demo_mode:
        reply_lower = reply.lower()
        if "not looking" in reply_lower or "not interested" in reply_lower:
            return {
                "intent": "NOT_INTERESTED",
                "active_job_search": False,
                "notice_period_days": None,
                "availability": None,
                "confidence": 0.95,
                "missing_information": []
            }
        elif "more information" in reply_lower or "tell me more" in reply_lower:
            return {
                "intent": "NEEDS_INFORMATION",
                "active_job_search": True,
                "notice_period_days": None,
                "availability": None,
                "confidence": 0.88,
                "missing_information": ["role_details"]
            }
        elif "ambiguous" in reply_lower or "maybe" in reply_lower or "unclear" in reply_lower:
             return {
                "intent": "UNCLEAR",
                "active_job_search": True,
                "notice_period_days": None,
                "availability": None,
                "confidence": 0.40,
                "missing_information": ["availability", "notice_period"]
            }
        else:
            # Assume interested for demo
            return {
                "intent": "INTERESTED",
                "active_job_search": True,
                "notice_period_days": 15 if "15" in reply_lower else (0 if "immediate" in reply_lower else 30),
                "availability": [
                    {
                        "date": "2026-09-08",
                        "start_time": "14:00",
                        "end_time": "17:00"
                    }
                ],
                "confidence": 0.92,
                "missing_information": []
            }
    
    # In production, use OpenAI API here with structured outputs
    # Example (psuedocode):
    # response = openai.ChatCompletion.create(
    #    model="gpt-4o",
    #    messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": reply}],
    #    response_format={"type": "json_object"}
    # )
    # return json.loads(response.choices[0].message.content)
    return {}
