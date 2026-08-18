from pathlib import Path

from metricguard.governance import (
    assess_metric_version,
    build_dashboard_version_report,
    load_authoritative_metric_registry,
)
from metricguard.ingestion import (
    parse_knowledge_base,
)


REPO_ROOT = Path(
    __file__
).resolve().parents[1]

RAW_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
)


def test_authoritative_registry():

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    assert (
        registry[
            "net_revenue"
        ]["authoritative_version"]
        == "v3"
    )

    assert (
        registry[
            "total_orders"
        ]["authoritative_version"]
        == "v2"
    )

    assert (
        registry[
            "active_customers"
        ]["authoritative_version"]
        == "v2"
    )


def test_current_version_assessment():

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    result = assess_metric_version(
        metric_name="net_revenue",
        observed_version="v3",
        registry=registry,
    )

    assert result.relation == "current"


def test_non_current_version_assessment():

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    result = assess_metric_version(
        metric_name="net_revenue",
        observed_version="v2",
        registry=registry,
    )

    assert (
        result.relation
        == "non_current"
    )

    assert (
        result.authoritative_version
        == "v3"
    )


def test_executive_dashboard_is_non_current():

    documents, errors = (
        parse_knowledge_base(
            source_root=RAW_DIR,
            repo_root=REPO_ROOT,
        )
    )

    assert errors == []

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    report = (
        build_dashboard_version_report(
            documents,
            registry,
        )
    )

    executive_revenue = next(
        row
        for row in report
        if (
            row["dashboard_name"]
            == "Executive KPI Dashboard"
            and row["metric_name"]
            == "net_revenue"
        )
    )

    assert (
        executive_revenue[
            "observed_version"
        ]
        == "v2"
    )

    assert (
        executive_revenue[
            "authoritative_version"
        ]
        == "v3"
    )

    assert (
        executive_revenue[
            "relation"
        ]
        == "non_current"
    )


def test_finance_revenue_is_current():

    documents, errors = (
        parse_knowledge_base(
            source_root=RAW_DIR,
            repo_root=REPO_ROOT,
        )
    )

    assert errors == []

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    report = (
        build_dashboard_version_report(
            documents,
            registry,
        )
    )

    finance_revenue = next(
        row
        for row in report
        if (
            row["dashboard_name"]
            == "Finance Revenue Dashboard"
            and row["metric_name"]
            == "net_revenue"
        )
    )

    assert (
        finance_revenue["relation"]
        == "current"
    )