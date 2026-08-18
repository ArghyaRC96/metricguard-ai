from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class VersionAssessment:
    """Result of comparing an observed metric version with the authority."""

    metric_name: str
    observed_version: str | None
    authoritative_version: str | None
    relation: str
    owner: str | None = None
    effective_from: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class FreshnessAssessment:
    """Result of evaluating how recently an asset was reviewed."""

    last_reviewed: str | None
    as_of_date: str
    days_since_review: int | None
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)