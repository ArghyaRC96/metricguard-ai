from typing import Any

from metricguard.ingestion.models import ParsedDocument

from .inference import (
    infer_asset_type,
    infer_metric_version,
)


MARKDOWN_METADATA_FIELDS = {
    "incident_id",
    "status",
    "severity",
    "opened_date",
    "closed_date",
    "owner",
    "author",
    "team",
    "date",
    "related_metric",
    "affected_metric",
}


def extract_dashboard_metadata(
    document: ParsedDocument,
) -> dict[str, Any]:
    """Extract useful governance metadata from dashboard JSON."""

    if document.source_type != "json":
        return {}

    data = document.structured_data

    if not isinstance(data, dict):
        return {}

    metadata: dict[str, Any] = {}

    fields = [
        "dashboard_id",
        "dashboard_name",
        "owner_team",
        "business_domain",
        "status",
        "last_reviewed",
        "refresh_frequency",
        "source_mart",
    ]

    for key in fields:

        if key in data:
            metadata[key] = data[key]

    metrics = data.get("metrics")

    if isinstance(metrics, list):

        metadata["metric_names"] = [
            metric.get("metric_name")
            for metric in metrics
            if isinstance(metric, dict)
            and metric.get("metric_name")
        ]

        metadata["metric_versions"] = {
            metric["metric_name"]: metric.get(
                "metric_version"
            )
            for metric in metrics
            if isinstance(metric, dict)
            and metric.get("metric_name")
        }

    return metadata


def extract_markdown_metadata(
    content: str,
) -> dict[str, Any]:
    """Extract known key-value governance fields from Markdown."""

    metadata: dict[str, Any] = {}

    for line in content.splitlines():

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if (
            key in MARKDOWN_METADATA_FIELDS
            and value
        ):
            metadata[key] = value

    return metadata


def build_document_metadata(
    document: ParsedDocument,
) -> dict[str, Any]:
    """Build shared metadata inherited by every chunk."""

    metadata: dict[str, Any] = {
        "document_id": document.document_id,
        "source_path": document.source_path,
        "file_name": document.file_name,
        "source_type": document.source_type,
        "asset_type": infer_asset_type(
            document.source_path
        ),
        "content_hash": document.content_hash,
    }

    metadata.update(
        infer_metric_version(
            document.file_name
        )
    )

    if document.source_type == "json":

        metadata.update(
            extract_dashboard_metadata(
                document
            )
        )

    if document.source_type == "markdown":

        metadata.update(
            extract_markdown_metadata(
                document.content
            )
        )

    return metadata