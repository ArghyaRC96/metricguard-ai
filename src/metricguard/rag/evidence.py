from .schemas import (
    BaselineRAGAnswer,
    ResolvedSource,
)


def build_evidence_context(
    evidence: list[dict],
) -> str:
    """Convert final retrieval evidence into grounded prompt context."""

    blocks: list[str] = []

    for index, item in enumerate(
        evidence,
        start=1,
    ):

        evidence_id = (
            f"E{index}"
        )

        block = f"""
[{evidence_id}]

Source: {item.get('source_path')}
File: {item.get('file_name')}
Asset type: {item.get('asset_type')}
Metric: {item.get('metric_name')}
Observed version: {item.get('observed_version')}
Authoritative version: {item.get('authoritative_version')}
Version relation: {item.get('version_relation')}
Freshness: {item.get('freshness_status')}
Lineage node: {item.get('lineage_node')}

Direct upstream:
{item.get('direct_upstream', [])}

Direct downstream:
{item.get('direct_downstream', [])}

CONTENT:
{item.get('content', '')}
"""

        blocks.append(
            block.strip()
        )

    return "\n\n".join(
        blocks
    )


def validate_evidence_ids(
    answer: BaselineRAGAnswer,
    evidence: list[dict],
) -> None:
    """Ensure the LLM only references retrieved evidence."""

    allowed = {
        f"E{index}"
        for index in range(
            1,
            len(evidence) + 1,
        )
    }

    used = {
        item.evidence_id
        for item
        in answer.evidence_used
    }

    invalid = (
        used - allowed
    )

    if invalid:
        raise ValueError(
            "LLM returned invalid "
            f"evidence IDs: "
            f"{sorted(invalid)}"
        )

    if (
        answer.status == "answered"
        and not used
    ):
        raise ValueError(
            "An answered response must "
            "cite at least one evidence item."
        )


def resolve_sources(
    answer: BaselineRAGAnswer,
    evidence: list[dict],
) -> list[ResolvedSource]:
    """Resolve LLM-selected evidence IDs to real source metadata."""

    source_map = {
        f"E{index}": item
        for index, item
        in enumerate(
            evidence,
            start=1,
        )
    }

    resolved: list[
        ResolvedSource
    ] = []

    for use in (
        answer.evidence_used
    ):

        source = (
            source_map[
                use.evidence_id
            ]
        )

        source_path = source.get(
            "source_path"
        )

        if not source_path:
            raise ValueError(
                "Retrieved evidence "
                "has no source_path."
            )

        if (
            "ground_truth"
            in str(source_path)
        ):
            raise ValueError(
                "Ground-truth leakage "
                "detected during citation "
                "resolution."
            )

        resolved.append(
            ResolvedSource(
                evidence_id=
                    use.evidence_id,
                source_path=
                    str(source_path),
                file_name=
                    source.get(
                        "file_name"
                    ),
                supports=
                    use.supports,
            )
        )

    return resolved