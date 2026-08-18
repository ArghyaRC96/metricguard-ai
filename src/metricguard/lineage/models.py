from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class LineageEdge:
    """One directed upstream-to-downstream dependency."""

    upstream: str
    downstream: str
    relationship: str
    source_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)