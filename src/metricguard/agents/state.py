from typing import Any

from typing_extensions import (
    TypedDict,
)


class MetricGuardAgentState(
    TypedDict,
    total=False,
):
    """Shared state across the MetricGuard agent graph."""

    question: str

    evidence: list[
        dict[str, Any]
    ]

    investigation: dict[
        str,
        Any,
    ]

    final_report: dict[
        str,
        Any,
    ]

    retrieval_complete: bool

    retrieval_relevant: bool

    retrieval_top1_score: (
        float | None
    )

    retrieval_relevance_reason: (
        str | None
    )

    investigation_complete: bool

    verification_complete: bool

    verification_decision: str

    verification_feedback: (
        str | None
    )

    revision_count: int

    max_revisions: int

    trace: list[str]

    error: str | None