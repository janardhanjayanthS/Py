from dataclasses import dataclass
from typing import Optional


@dataclass
class RuntimeContext:
    data: list[dict[str, str]]
    description: Optional[str] = ""
