from datetime import UTC, datetime
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime:
        """Return the current timezone-aware datetime."""


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)
