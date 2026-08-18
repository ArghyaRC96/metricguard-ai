from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class RetrievedCandidate:
    point_id: str
    dense_score: float
    payload: dict[str, Any]
    dense_rank: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RerankedEvidence:
    point_id: str
    dense_score: float
    rerank_score: float
    payload: dict[str, Any]
    dense_rank: int
    rerank_rank: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)