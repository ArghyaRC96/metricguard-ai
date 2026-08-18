from typing import Any, Literal

from pydantic import (
    BaseModel,
    Field,
)


class AgenticSource(
    BaseModel,
):
    evidence_id: str

    source_path: str | None = None

    file_name: str | None = None

    document_type: str | None = None

    metric_name: str | None = None


class AgenticRAGResult(
    BaseModel,
):
    question: str

    status: Literal[
        "answered",
        "insufficient_evidence",
    ]

    decision: Literal[
        "approved",
        "insufficient_evidence",
    ]

    diagnosis: str

    answer: str

    key_findings: list[str] = (
        Field(
            default_factory=list
        )
    )

    sources: list[
        AgenticSource
    ] = Field(
        default_factory=list
    )

    confidence: float = 0.0

    fallback_reason: (
        str | None
    ) = None

    revision_count: int = 0

    retrieval_relevant: (
        bool | None
    ) = None

    retrieval_top1_score: (
        float | None
    ) = None

    trace: list[str] = Field(
        default_factory=list
    )

    cached: bool = False


def _source_value(
    evidence: dict[str, Any],
    key: str,
) -> Any:
    """
    Read common source metadata whether it is
    stored directly, under metadata, or payload.
    """

    if key in evidence:
        return evidence.get(key)

    metadata = (
        evidence.get("metadata")
        or {}
    )

    if key in metadata:
        return metadata.get(key)

    payload = (
        evidence.get("payload")
        or {}
    )

    return payload.get(key)


def resolve_agent_sources(
    evidence_ids: list[str],
    evidence: list[dict[str, Any]],
) -> list[AgenticSource]:
    """
    Deterministically resolve model-selected
    evidence IDs back to retrieved documents.
    """

    source_map = {
        f"E{index}": item
        for index, item
        in enumerate(
            evidence,
            start=1,
        )
    }

    invalid = (
        set(evidence_ids)
        - set(source_map)
    )

    if invalid:
        raise ValueError(
            "Invalid agent evidence IDs: "
            f"{sorted(invalid)}"
        )

    resolved = []

    for evidence_id in evidence_ids:

        item = source_map[
            evidence_id
        ]

        source_path = (
            _source_value(
                item,
                "source_path",
            )
        )

        if (
            source_path
            and "ground_truth"
            in str(source_path)
        ):
            raise ValueError(
                "Ground-truth data cannot "
                "be exposed as runtime evidence."
            )

        resolved.append(
            AgenticSource(
                evidence_id=
                    evidence_id,

                source_path=
                    source_path,

                file_name=
                    _source_value(
                        item,
                        "file_name",
                    ),

                document_type=
                    _source_value(
                        item,
                        "document_type",
                    ),

                metric_name=
                    (
                        _source_value(
                            item,
                            "metric_name",
                        )
                        or
                        _source_value(
                            item,
                            "related_metric",
                        )
                    ),
            )
        )

    return resolved


def build_agentic_rag_result(
    *,
    question: str,
    state: dict[str, Any],
    minimum_confidence: float,
) -> AgenticRAGResult:
    """
    Convert raw LangGraph state into the final
    application-facing MetricGuard result.
    """

    report = (
        state.get("final_report")
        or {}
    )

    if hasattr(
        report,
        "model_dump",
    ):
        report = report.model_dump()

    evidence = list(
        state.get(
            "evidence",
            [],
        )
    )

    decision = str(
        state.get(
            "verification_decision",
        )
        or
        report.get(
            "decision",
            "insufficient_evidence",
        )
    )

    diagnosis = str(
        report.get(
            "diagnosis",
            "insufficient_evidence",
        )
    )

    confidence = float(
        report.get(
            "confidence",
            0.0,
        )
        or 0.0
    )

    answer = str(
        report.get(
            "answer",
            "",
        )
        or ""
    )

    key_findings = list(
        report.get(
            "key_findings",
            [],
        )
        or []
    )

    evidence_ids = list(
        report.get(
            "evidence_ids",
            [],
        )
        or []
    )

    retrieval_relevant = (
        state.get(
            "retrieval_relevant"
        )
    )

    fallback_reason = None


    # -----------------------------------------------------
    # RELEVANCE SAFEGUARD
    # -----------------------------------------------------

    if retrieval_relevant is False:

        decision = (
            "insufficient_evidence"
        )

        diagnosis = (
            "insufficient_evidence"
        )

        fallback_reason = (
            "Retrieved evidence did not meet "
            "the calibrated relevance threshold."
        )


    # -----------------------------------------------------
    # DECISION SAFEGUARD
    # -----------------------------------------------------

    elif (
        decision
        == "insufficient_evidence"
        or diagnosis
        == "insufficient_evidence"
    ):

        decision = (
            "insufficient_evidence"
        )

        diagnosis = (
            "insufficient_evidence"
        )

        fallback_reason = (
            "Verification concluded that the "
            "available evidence is insufficient."
        )


    # -----------------------------------------------------
    # CONFIDENCE SAFEGUARD
    # -----------------------------------------------------

    elif (
        decision == "approved"
        and confidence
        < minimum_confidence
    ):

        decision = (
            "insufficient_evidence"
        )

        diagnosis = (
            "insufficient_evidence"
        )

        fallback_reason = (
            "Verification confidence was below "
            "the configured minimum threshold."
        )


    if (
        decision
        == "insufficient_evidence"
    ):

        status = (
            "insufficient_evidence"
        )

        if not answer:

            answer = (
                "MetricGuard could not produce "
                "a sufficiently supported answer "
                "from the available evidence."
            )

    else:

        status = "answered"


    sources = (
        resolve_agent_sources(
            evidence_ids,
            evidence,
        )
        if evidence_ids
        else []
    )


    return AgenticRAGResult(
        question=
            question,

        status=
            status,

        decision=
            decision,

        diagnosis=
            diagnosis,

        answer=
            answer,

        key_findings=
            key_findings,

        sources=
            sources,

        confidence=
            confidence,

        fallback_reason=
            fallback_reason,

        revision_count=int(
            state.get(
                "revision_count",
                0,
            )
        ),

        retrieval_relevant=
            retrieval_relevant,

        retrieval_top1_score=
            state.get(
                "retrieval_top1_score"
            ),

        trace=list(
            state.get(
                "trace",
                [],
            )
        ),

        cached=False,
    )