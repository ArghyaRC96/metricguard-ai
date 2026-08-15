from pathlib import Path

from metricguard.ingestion import (
    build_parsed_document,
)
from metricguard.metadata import (
    build_document_metadata,
    infer_asset_type,
    infer_metric_version,
)


REPO_ROOT = Path(
    __file__
).resolve().parents[1]

RAW_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
)


def test_versioned_metric_inference():

    result = infer_metric_version(
        "net_revenue_v3.md"
    )

    assert (
        result["metric_name"]
        == "net_revenue"
    )

    assert (
        result["version"]
        == "v3"
    )


def test_non_versioned_file():

    result = infer_metric_version(
        "mart_finance_daily.sql"
    )

    assert result["metric_name"] is None
    assert result["version"] is None


def test_asset_type_inference():

    path = (
        "data/raw/sql/marts/"
        "mart_finance_daily.sql"
    )

    assert (
        infer_asset_type(path)
        == "mart"
    )


def test_business_rule_metadata():

    path = (
        RAW_DIR
        / "business_rules"
        / "net_revenue"
        / "net_revenue_v3.md"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    metadata = build_document_metadata(
        document
    )

    assert (
        metadata["asset_type"]
        == "business_rule"
    )

    assert (
        metadata["metric_name"]
        == "net_revenue"
    )

    assert metadata["version"] == "v3"


def test_dashboard_metadata():

    path = (
        RAW_DIR
        / "dashboards"
        / "finance_revenue_dashboard.json"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    metadata = build_document_metadata(
        document
    )

    assert (
        metadata["dashboard_name"]
        == "Finance Revenue Dashboard"
    )

    assert (
        metadata["source_mart"]
        == "mart_finance_daily"
    )

    assert (
        metadata[
            "metric_versions"
        ]["net_revenue"]
        == "v3"
    )