from __future__ import annotations

import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior|system)\s+",
    r"system\s*prompt",
    r"you\s+are\s+now\s+",
    r"<\s*/?\s*system\s*>",
    r"jailbreak",
    r"reveal\s+(hidden|secret|evaluation)\s+",
]


def sanitize_candidate_text(text: str, *, max_length: int = 8000) -> str:
    """Treat candidate text as untrusted data and bound its size."""
    cleaned = (text or "").strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    # Neutralize common control tokens without altering technical content meaning.
    cleaned = cleaned.replace("```", "'''")
    return cleaned


def detect_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pat, lowered) for pat in INJECTION_PATTERNS)


def wrap_untrusted_candidate_content(text: str) -> str:
    sanitized = sanitize_candidate_text(text)
    return (
        "BEGIN_UNTRUSTED_CANDIDATE_ANSWER\n"
        f"{sanitized}\n"
        "END_UNTRUSTED_CANDIDATE_ANSWER"
    )
