from .models import RetrievedCandidate


def build_reranker_text(
    candidate: RetrievedCandidate,
) -> str:
    """Build compact evidence text for Cross-Encoder scoring."""

    payload = candidate.payload

    parts: list[str] = []

    fields = [
        ("Source file", "file_name"),
        ("Asset type", "asset_type"),
        ("Metric", "metric_name"),
        (
            "Observed version",
            "observed_version",
        ),
        (
            "Authoritative version",
            "authoritative_version",
        ),
        (
            "Version relation",
            "version_relation",
        ),
        (
            "Freshness status",
            "freshness_status",
        ),
    ]

    for label, field in fields:

        value = payload.get(field)

        if value is not None:
            parts.append(
                f"{label}: {value}."
            )

    content = str(
        payload.get(
            "content",
            "",
        )
    ).strip()

    if content:
        parts.append(content)

    return "\n".join(parts)