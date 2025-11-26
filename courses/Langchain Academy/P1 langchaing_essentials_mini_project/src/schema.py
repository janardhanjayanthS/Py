from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RuntimeContext:
    data: list[dict[str, str]]
    description: Optional[str] = ""
    reading_list: list[dict[str, str]] = field(default_factory=list)
    favorite_authors: list[str] = field(default_factory=list)
    favorite_genres: list[str] = field(default_factory=list)
