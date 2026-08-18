from typing import Literal

from pydantic import (
    BaseModel,
    Field,
)


Diagnosis = Literal[
    "version_mismatch",
    "stale_definition",
    "intentional_semantic_difference",
    "metric_migration",
    "data_pipeline_issue",
    "insufficient_evidence",
    "other",
]


class InvestigationResult(
    BaseModel
):

    diagnosis: Diagnosis

    metric_name: (
        str | None
    ) = None

    hypothesis: str

    findings: list[str]

    contradictions: list[str]

    tool_observations: list[str]

    evidence_ids: list[str]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    revision_summary: (
        str | None
    ) = None


class VerificationResult(
    BaseModel
):

    decision: Literal[
        "approved",
        "revise",
        "insufficient_evidence",
    ]

    diagnosis: Diagnosis

    answer: str

    key_findings: list[str]

    evidence_ids: list[str]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    feedback: str

    unsupported_claims: list[str]

    missing_evidence: list[str]