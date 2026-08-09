from __future__ import annotations

import os
import re
from typing import Any
from dotenv import load_dotenv

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
    """Service encapsulating Google Gemini API for technical candidate interviews with strict history & grading."""

    EVASION_PATTERN = re.compile(
        r"\b(idk|dunno|whatever|idk man|idk lol|pass|idk bro|not sure man|skip|who cares|no idea)\b",
        re.IGNORECASE,
    )

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._model = None

        if HAS_GENAI and self.api_key and self.api_key != "your_api_key_here":
            try:
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
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
        """Handle a chat interaction maintaining strict conversation history & context."""
        raw_history = chat_history or []

        # If Gemini client is active, execute live inference
        if self._model is not None:
            try:
                gemini_history = []
                for turn in raw_history:
                    role_str = turn.get("role", "user")
                    role = "user" if role_str in {"user", "candidate"} else "model"
                    
                    # Normalize parts / content
                    if "parts" in turn and isinstance(turn["parts"], list):
                        parts = [str(p) for p in turn["parts"]]
                    elif "content" in turn and isinstance(turn["content"], str):
                        parts = [turn["content"]]
                    else:
                        parts = [str(turn)]

                    if parts and parts[0].strip():
                        gemini_history.append({"role": role, "parts": parts})

                chat = self._model.start_chat(history=gemini_history)
                response = chat.send_message(message)
                return {
                    "session_id": session_id,
                    "reply": response.text,
                    "provider": "google-gemini",
                    "status": "success",
                }
            except Exception as exc:
                print(f"[AIService] Gemini API error, falling back to adaptive response: {exc}")

        # Fallback adaptive response engine for offline / test mode
        return self._fallback_adaptive_response(session_id, message, raw_history, candidate_info)

    def _fallback_adaptive_response(
        self,
        session_id: str,
        message: str,
        history: list[dict[str, Any]],
        candidate_info: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Adaptive fallback engine enforcing strict evasion detection & honest grading."""
        msg_l = message.lower().strip()
        cand_name = candidate_info.get("name", "Candidate") if candidate_info else "Candidate"

        # Check if current message is evasive or low-effort
        is_evasive = bool(self.EVASION_PATTERN.search(msg_l)) or len(msg_l) < 4

        # Check entire history for evasions
        has_history_evasions = any(
            bool(self.EVASION_PATTERN.search(str(turn.get("content", turn.get("parts", ""))).lower()))
            for turn in history
        )

        if "feedback" in msg_l or "conclude" in msg_l or "end" in msg_l:
            if is_evasive or has_history_evasions:
                reply = (
                    f"### Final Interview Assessment & Feedback for {cand_name}\n\n"
                    "**Overall Assessment: NEEDS IMPROVEMENT / FAIL**\n\n"
                    "**Critical Feedback & Technical Gaps:**\n"
                    "- The candidate provided evasive, non-technical, or low-effort responses during the evaluation session.\n"
                    "- Failed to demonstrate technical depth in RAG optimization, vector indexing, or system failure recovery.\n\n"
                    "**Actionable Next Steps:**\n"
                    "- Review core AI systems architecture, hybrid retrieval (BM25 + Dense), and exponential backoff retry patterns before re-interviewing."
                )
            else:
                reply = (
                    f"### Final Interview Assessment & Feedback for {cand_name}\n\n"
                    "**Overall Assessment: PASS (Strong Technical Reasoning)**\n\n"
                    "**Technical Strengths:**\n"
                    "- Clear understanding of RAG production incident recovery and hybrid vector search.\n"
                    "- Good awareness of exponential backoff retry logic and fallback mechanisms.\n\n"
                    "**Areas for Growth:**\n"
                    "- Deepen quantitative analysis of cache hit rate trade-offs vs false positive rates."
                )
        elif is_evasive:
            reply = (
                "That response does not answer the technical problem. Please focus on the question at hand and explain your reasoning.\n\n"
                "To restate: how would you optimize query recall and error handling when a vector database experiences latency spikes?"
            )
        elif "hybrid" in msg_l or "bm25" in msg_l:
            reply = (
                "Combining BM25 keyword matching with dense embeddings effectively resolves vocabulary mismatch. "
                "How do you configure reciprocity rank fusion (RRF) weights to balance exact keyword matches against semantic similarity?"
            )
        elif "cache" in msg_l or "threshold" in msg_l:
            reply = (
                "Lowering the semantic cache similarity threshold improves hit rate, but risks serving false positives. "
                "What validation strategy would you implement to detect invalid cache hits in real-time?"
            )
        else:
            reply = (
                f"Thank you for that explanation. To probe deeper: how would you monitor latency and error cascades "
                "when downstream vector database calls timeout during peak traffic loads?"
            )

        return {
            "session_id": session_id,
            "reply": reply,
            "provider": "adaptive-interviewer-fallback",
            "status": "success",
        }


# Global singleton instance
ai_service = AIService()
