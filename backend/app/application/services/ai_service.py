from __future__ import annotations

import os
from typing import Any
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    genai = None  # type: ignore
    HAS_GENAI = False

SYSTEM_INSTRUCTION = """
You are an adaptive, elite technical interviewer for Project Chimera, conducting structured AI Engineering & Systems assessment.

Strictly enforce the following behavioral rules throughout every interaction:

1. STRICT CONTEXT AWARENESS:
   - You MUST review the ENTIRE conversation history before generating a response.
   - Maintain coherent context across all prior turns.
   - NEVER repeat a question verbatim if the candidate gives a weak or incomplete answer; instead, rephrase or probe a specific technical sub-concept.

2. HANDLING GIBBERISH & EVASIONS:
   - If the candidate responds with short evasions (e.g. "idk", "whatever", "idk man", "dunno", "pass", "idk lol"), low-effort answers, or off-topic text:
     * Politely but firmly call it out (e.g., "That response does not address the technical problem. Please focus on the question at hand and explain your reasoning...").
     * Rephrase or prompt them once more for a substantive technical answer.
     * Internally mark down their evaluation score for effort and technical depth.

3. ADAPTIVE TECHNICAL PROBING:
   - Adapt naturally based on candidate responses—pivot to advanced system design when they excel, or scaffold simpler sub-problems when they struggle.
   - Ask intelligent follow-up questions focusing on root causes, trade-offs, edge cases, and failure modes.

4. HONEST FINAL EVALUATION:
   - When generating the final assessment or feedback, calculate the score based on ALL responses across the entire session.
   - If the candidate provided non-answers, evasions, or low-effort text for multiple questions, the candidate MUST receive a "Fail" or "Needs Improvement" outcome with explicit feedback detailing their lack of technical depth.

Tone & Demeanor:
- Professional, rigorous, firm yet encouraging, and deeply technical.
- Keep individual responses concise (1-3 paragraphs) with a clear follow-up question unless concluding.
"""


class AIService:
    """Service encapsulating Google Gemini API for 100% live technical candidate interviews."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._model = None

        if not HAS_GENAI:
            print("[AIService] google-generativeai library is not installed.")
            return

        if not self.api_key or self.api_key == "your_api_key_here":
            print("[AIService] GEMINI_API_KEY environment variable is not configured.")
            return

        try:
            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel(
                model_name="gemini-3.6-flash",
                system_instruction=SYSTEM_INSTRUCTION,
            )
        except Exception as err:
            print(f"[AIService] Failed to initialize Gemini model: {err}")
            self._model = None

    def handle_chat_session(
        self,
        session_id: str,
        message: str,
        chat_history: list[dict[str, Any]] | None = None,
        candidate_info: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle a live chat interaction maintaining strict conversation history & live Gemini API generation."""
        api_key = self.api_key or os.getenv("GEMINI_API_KEY")

        if not HAS_GENAI:
            raise HTTPException(
                status_code=500,
                detail="Gemini API Error: 'google-generativeai' package is not installed.",
            )

        if not api_key or api_key == "your_api_key_here":
            raise HTTPException(
                status_code=500,
                detail="Gemini API Error: GEMINI_API_KEY is not configured in backend/.env.",
            )

        if self._model is None or self.api_key != api_key:
            try:
                genai.configure(api_key=api_key)
                self.api_key = api_key
                self._model = genai.GenerativeModel(
                    model_name="gemini-3.6-flash",
                    system_instruction=SYSTEM_INSTRUCTION,
                )
            except Exception as init_err:
                raise HTTPException(
                    status_code=500,
                    detail=f"Gemini API Model Initialization Error: {str(init_err)}",
                ) from init_err

        raw_history = chat_history or []
        gemini_history = []

        for turn in raw_history:
            role_str = turn.get("role", "user")
            role = "user" if role_str in {"user", "candidate"} else "model"

            if "parts" in turn and isinstance(turn["parts"], list):
                parts = [str(p) for p in turn["parts"]]
            elif "content" in turn and isinstance(turn["content"], str):
                parts = [turn["content"]]
            else:
                parts = [str(turn)]

            if parts and parts[0].strip():
                gemini_history.append({"role": role, "parts": parts})

        try:
            chat = self._model.start_chat(history=gemini_history)
            response = chat.send_message(message)
            return {
                "session_id": session_id,
                "reply": response.text,
                "provider": "google-gemini",
                "status": "success",
            }
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Gemini API Execution Failure: {str(exc)}",
            ) from exc


# Global singleton instance
ai_service = AIService()
