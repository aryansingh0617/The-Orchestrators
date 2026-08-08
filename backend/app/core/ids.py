from typing import Protocol
from uuid import uuid4


class IdGenerator(Protocol):
    def new_id(self) -> str:
        """Return a new stable string identifier."""


class UuidGenerator:
    def new_id(self) -> str:
        return str(uuid4())
