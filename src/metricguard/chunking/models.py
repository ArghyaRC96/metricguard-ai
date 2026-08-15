from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class KnowledgeChunk:
    """Canonical retrieval-ready MetricGuard chunk."""

    chunk_id: str
    content: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable dictionary representation."""

        return asdict(self)


@dataclass(slots=True)
class ChunkError:
    """Represents one document that failed during chunking."""

    source_path: str
    error: str