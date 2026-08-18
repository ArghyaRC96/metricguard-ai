import json
from datetime import date
from typing import Any

from metricguard.chunking.models import KnowledgeChunk

from .freshness import assess_freshness
from .versions import assess_metric_version


def extract_metric_context(
    chunk: KnowledgeChunk,
) -> tuple[str | None, str | None]:
    """
    Identify the metric and observed version represented by a chunk.

    First use existing filename-derived metadata.
    If unavailable, inspect structure-aware JSON/YAML chunks.
    """

    metric_name = chunk.metadata.get(
        "metric_name"
    )

    observed_version = chunk.metadata.get(
        "version"
    )

    if metric_name:
        return (
            str(metric_name),
            (
                str(observed_version)
                if observed_version
                else None
            ),
        )

    try:
        data = json.loads(
            chunk.content
        )
    except (
        json.JSONDecodeError,
        TypeError,
    ):
        return None, None

    if not isinstance(data, dict):
        return None, None

    for value in data.values():

        if not isinstance(value, dict):
            continue

        discovered_metric = (
            value.get("metric_name")
            or value.get("name")
        )

        discovered_version = (
            value.get("metric_version")
            or value.get("current_version")
            or value.get("version")
        )

        if discovered_metric:

            return (
                str(discovered_metric),
                (
                    str(discovered_version)
                    if discovered_version
                    else None
                ),
            )

    return None, None


def enrich_chunk_with_governance(
    chunk: KnowledgeChunk,
    *,
    registry: dict[str, dict[str, Any]],
    as_of_date: date,
    warning_after_days: int,
    stale_after_days: int,
) -> KnowledgeChunk:
    """
    Attach version authority and freshness intelligence to one chunk.
    """

    metadata = dict(
        chunk.metadata
    )

    (
        metric_name,
        observed_version,
    ) = extract_metric_context(
        chunk
    )

    if metric_name:

        version_assessment = (
            assess_metric_version(
                metric_name=metric_name,
                observed_version=
                    observed_version,
                registry=registry,
            )
        )

        metadata[
            "metric_name"
        ] = metric_name

        metadata[
            "observed_version"
        ] = observed_version

        metadata[
            "authoritative_version"
        ] = (
            version_assessment
            .authoritative_version
        )

        metadata[
            "version_relation"
        ] = version_assessment.relation

        metadata[
            "authoritative_owner"
        ] = version_assessment.owner

        metadata[
            "authoritative_effective_from"
        ] = (
            version_assessment
            .effective_from
        )

    freshness = assess_freshness(
        metadata.get(
            "last_reviewed"
        ),
        as_of_date=as_of_date,
        warning_after_days=
            warning_after_days,
        stale_after_days=
            stale_after_days,
    )

    metadata[
        "freshness_status"
    ] = freshness.status

    metadata[
        "days_since_review"
    ] = freshness.days_since_review

    metadata[
        "freshness_as_of_date"
    ] = freshness.as_of_date

    return KnowledgeChunk(
        chunk_id=chunk.chunk_id,
        content=chunk.content,
        metadata=metadata,
    )


def enrich_chunks_with_governance(
    chunks: list[KnowledgeChunk],
    *,
    registry: dict[str, dict[str, Any]],
    as_of_date: date,
    warning_after_days: int,
    stale_after_days: int,
) -> list[KnowledgeChunk]:
    """Apply governance enrichment to all retrieval chunks."""

    return [
        enrich_chunk_with_governance(
            chunk,
            registry=registry,
            as_of_date=as_of_date,
            warning_after_days=
                warning_after_days,
            stale_after_days=
                stale_after_days,
        )
        for chunk in chunks
    ]


def validate_governance_enrichment(
    chunks: list[KnowledgeChunk],
) -> None:
    """Validate governance metadata before embedding."""

    if not chunks:
        raise ValueError(
            "No enriched chunks found."
        )

    for chunk in chunks:

        metadata = chunk.metadata

        if (
            "freshness_status"
            not in metadata
        ):
            raise ValueError(
                f"{chunk.chunk_id} "
                "has no freshness status."
            )

        if (
            "freshness_as_of_date"
            not in metadata
        ):
            raise ValueError(
                f"{chunk.chunk_id} "
                "has no freshness reference date."
            )

        if metadata.get(
            "metric_name"
        ):

            if (
                "version_relation"
                not in metadata
            ):
                raise ValueError(
                    f"{chunk.chunk_id} "
                    "has no version relation."
                )

        if (
            "ground_truth"
            in metadata.get(
                "source_path",
                "",
            )
        ):
            raise ValueError(
                "Ground-truth leakage detected."
            )