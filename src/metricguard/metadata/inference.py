import re
from pathlib import Path
from typing import Any


VERSIONED_METRIC_PATTERN = re.compile(
    r"^(?P<metric_name>.+)_(?P<version>v\d+)$"
)


def infer_asset_type(source_path: str) -> str:
    """Infer the type of analytics asset from its repository path."""

    path = source_path.replace("\\", "/").lower()

    if "/business_rules/" in path:
        return "business_rule"

    if "/sql/staging/" in path:
        return "staging_model"

    if "/sql/facts/" in path:
        return "fact_model"

    if "/sql/marts/" in path:
        return "mart"

    if "/sql/metrics/" in path:
        return "metric_sql"

    if "/dashboards/" in path:
        return "dashboard"

    if "/dbt/" in path:
        return "dbt_documentation"

    if "/incidents/" in path:
        return "incident"

    if "/analyst_notes/" in path:
        return "analyst_note"

    if "/tabular/" in path:
        return "raw_dataset"

    return "unknown"


def infer_metric_version(
    file_name: str,
) -> dict[str, Any]:
    """Infer metric name and version from versioned filenames."""

    stem = Path(file_name).stem

    match = VERSIONED_METRIC_PATTERN.match(stem)

    if not match:
        return {
            "metric_name": None,
            "version": None,
        }

    return {
        "metric_name": match.group("metric_name"),
        "version": match.group("version"),
    }