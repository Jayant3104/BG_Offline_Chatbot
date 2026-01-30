from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from services.alarm_service import (
    handle_alarm_code,
    handle_alarm_description
)
from core.llm import generate_llm
from utils.text_utils import clean_llm_output

router = APIRouter(prefix="/chat", tags=["Chat"])


# ===============================
# REQUEST MODEL
# ===============================
class ChatRequest(BaseModel):
    query: Optional[str] = None          # Alarm description / normal question
    alarm_code: Optional[str] = None     # AL123, ST456


# ===============================
# CHAT ROUTE
# ===============================
@router.post("")
def chat(req: ChatRequest):

    query = (req.query or "").strip()
    alarm_code = (req.alarm_code or "").strip().upper()

    # 1️⃣ Alarm Code (HIGHEST PRIORITY)
    if alarm_code:
        return handle_alarm_code(alarm_code)

    # 2️⃣ Alarm Description
    if query:
        result = handle_alarm_description(query)
        if result:
            return result

    # 3️⃣ Normal Question (Fallback)
    if query:
        prompt = f"""
You are a helpful assistant.
Answer clearly.

Question:
{query}

Answer:
"""
        return {"reply": clean_llm_output(generate_llm(prompt))}

    # 4️⃣ Nothing entered
    return {"reply": "Please enter an alarm code or description."}
