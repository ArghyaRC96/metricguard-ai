from typing import Any, Literal

from pydantic import (
    BaseModel,
    Field,
)


class EvidenceUse(BaseModel):
    evidence_id: str
    supports: str


class BaselineRAGAnswer(BaseModel):

    status: Literal[
        "answered",
        "insufficient_evidence",
    ]

    diagnosis: Literal[
        "version_mismatch",
        "stale_definition",
        "intentional_semantic_difference",
        "metric_migration",
        "data_pipeline_issue",
        "insufficient_evidence",
        "other",
    ]

    metric_name: str | None = None

    answer: str

    key_findings: list[str]

    evidence_used: list[
        EvidenceUse
    ]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    confidence_reason: str

    missing_evidence: list[str]


class ResolvedSource(BaseModel):

    evidence_id: str

    source_path: str

    file_name: str | None = None

    supports: str


class RAGResult(BaseModel):

    question: str

    answer: BaselineRAGAnswer

    sources: list[
        ResolvedSource
    ]

    evidence: list[
        dict[str, Any]
    ]

    fallback_triggered: bool

    display_answer: str

    cache_hit: bool = False