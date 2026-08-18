from pathlib import Path
from typing import Any

import yaml

from metricguard.ingestion.models import ParsedDocument
from metricguard.metadata import build_document_metadata

from .models import VersionAssessment


def _stringify(value: Any) -> str | None:
    """Convert YAML values such as dates into stable strings."""

    if value is None:
        return None

    return str(value)


def load_authoritative_metric_registry(
    repo_root: Path,
) -> dict[str, dict[str, Any]]:
    """
    Load currently approved metric definitions from dbt-style metrics.yml.
    """

    metrics_path = (
        repo_root
        / "data"
        / "raw"
        / "dbt"
        / "metrics.yml"
    )

    with metrics_path.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        data = yaml.safe_load(file)

    metric_items = data.get("metrics", [])

    registry: dict[str, dict[str, Any]] = {}

    for item in metric_items:

        if not isinstance(item, dict):
            continue

        metric_name = (
            item.get("metric_name")
            or item.get("name")
        )

        current_version = (
            item.get("current_version")
            or item.get("metric_version")
            or item.get("version")
        )

        if not metric_name or not current_version:
            continue

        registry[str(metric_name)] = {
            "authoritative_version": str(current_version),
            "status": item.get("status"),
            "owner": item.get("owner"),
            "effective_from": _stringify(
                item.get("effective_from")
            ),
            "definition": item.get("definition"),
            "source_path": str(
                metrics_path.relative_to(repo_root)
            ),
        }

    if not registry:
        raise ValueError(
            "No authoritative metrics found in metrics.yml."
        )

    return registry


def assess_metric_version(
    metric_name: str,
    observed_version: str | None,
    registry: dict[str, dict[str, Any]],
) -> VersionAssessment:
    """
    Compare an observed version with the approved enterprise version.

    This only identifies whether versions differ.
    It does NOT decide whether that difference is a business defect.
    """

    authority = registry.get(metric_name)

    if authority is None:
        return VersionAssessment(
            metric_name=metric_name,
            observed_version=observed_version,
            authoritative_version=None,
            relation="unknown_metric",
        )

    authoritative_version = authority[
        "authoritative_version"
    ]

    if observed_version is None:

        relation = "unknown_observed_version"

    elif observed_version == authoritative_version:

        relation = "current"

    else:

        relation = "non_current"

    return VersionAssessment(
        metric_name=metric_name,
        observed_version=observed_version,
        authoritative_version=authoritative_version,
        relation=relation,
        owner=authority.get("owner"),
        effective_from=authority.get(
            "effective_from"
        ),
    )


def build_version_history(
    documents: list[ParsedDocument],
) -> list[dict[str, Any]]:
    """
    Build historical metric-version records from business-rule documents.
    """

    history: list[dict[str, Any]] = []

    for document in documents:

        metadata = build_document_metadata(
            document
        )

        if (
            metadata.get("asset_type")
            != "business_rule"
        ):
            continue

        metric_name = metadata.get(
            "metric_name"
        )

        version = metadata.get(
            "version"
        )

        if not metric_name or not version:
            continue

        history.append(
            {
                "metric_name": metric_name,
                "version": version,
                "status": metadata.get(
                    "status"
                ),
                "owner": metadata.get(
                    "owner"
                ),
                "effective_from":
                    metadata.get(
                        "effective_from"
                    ),
                "effective_to":
                    metadata.get(
                        "effective_to"
                    ),
                "source_path":
                    document.source_path,
            }
        )

    return history


def build_dashboard_version_report(
    documents: list[ParsedDocument],
    registry: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Compare every dashboard's declared metric versions with the registry.
    """

    report: list[dict[str, Any]] = []

    for document in documents:

        metadata = build_document_metadata(
            document
        )

        if (
            metadata.get("asset_type")
            != "dashboard"
        ):
            continue

        metric_versions = metadata.get(
            "metric_versions",
            {},
        )

        if not isinstance(
            metric_versions,
            dict,
        ):
            continue

        for (
            metric_name,
            observed_version,
        ) in metric_versions.items():

            # Only evaluate metrics that belong
            # to the authoritative registry.
            if metric_name not in registry:
                continue

            assessment = assess_metric_version(
                metric_name=metric_name,
                observed_version=observed_version,
                registry=registry,
            )

            report.append(
                {
                    "dashboard_name":
                        metadata.get(
                            "dashboard_name"
                        ),
                    "source_mart":
                        metadata.get(
                            "source_mart"
                        ),
                    **assessment.to_dict(),
                }
            )

    return report