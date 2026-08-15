from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class ParsedDocument:
    """Canonical representation of one parsed knowledge source."""

    document_id: str
    source_path: str
    file_name: str
    source_type: str
    content_hash: str
    content: str
    structured_data: Any | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        return asdict(self)


@dataclass(slots=True)
class ParseError:
    """Represents one source file that failed during parsing."""

    source_path: str
    error: str
