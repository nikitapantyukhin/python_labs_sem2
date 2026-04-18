from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Task:
    id: int
    payload: Any