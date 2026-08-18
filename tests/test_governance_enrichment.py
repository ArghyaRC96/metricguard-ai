from datetime import date
from pathlib import Path

from metricguard.chunking import (
    build_chunks,
)
from metricguard.governance import (
    enrich_chunk_with_governance,
    load_authoritative_metric_registry,
)
from metricguard.ingestion import (
    build_parsed_document,
)


REPO_ROOT = Path(
    __file__
).resolve().parents[1]

RAW_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
)

AS_OF_DATE = date(
    2026,
    8,
    18,
)

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def _dashboard_chunks(
    file_name: str,
):

    path = (
        RAW_DIR
        / "dashboards"
        / file_name
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    return build_chunks(
        document,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )


def test_executive_net_revenue_enrichment():

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    chunks = _dashboard_chunks(
        "executive_kpi_dashboard.json"
    )

    target = next(
        chunk
        for chunk in chunks
        if (
            chunk.metadata.get(
                "structure_key"
            )
            == "metrics"
            and '"net_revenue"'
            in chunk.content
        )
    )

    enriched = (
        enrich_chunk_with_governance(
            target,
            registry=registry,
            as_of_date=AS_OF_DATE,
            warning_after_days=120,
            stale_after_days=180,
        )
    )

    assert (
        enriched.metadata[
            "metric_name"
        ]
        == "net_revenue"
    )

    assert (
        enriched.metadata[
            "observed_version"
        ]
        == "v2"
    )

    assert (
        enriched.metadata[
            "authoritative_version"
        ]
        == "v3"
    )

    assert (
        enriched.metadata[
            "version_relation"
        ]
        == "non_current"
    )

    assert (
        enriched.metadata[
            "freshness_status"
        ]
        == "stale"
    )


def test_finance_net_revenue_is_current():

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    chunks = _dashboard_chunks(
        "finance_revenue_dashboard.json"
    )

    target = next(
        chunk
        for chunk in chunks
        if (
            chunk.metadata.get(
                "structure_key"
            )
            == "metrics"
            and '"net_revenue"'
            in chunk.content
        )
    )

    enriched = (
        enrich_chunk_with_governance(
            target,
            registry=registry,
            as_of_date=AS_OF_DATE,
            warning_after_days=120,
            stale_after_days=180,
        )
    )

    assert (
        enriched.metadata[
            "observed_version"
        ]
        == "v3"
    )

    assert (
        enriched.metadata[
            "authoritative_version"
        ]
        == "v3"
    )

    assert (
        enriched.metadata[
            "version_relation"
        ]
        == "current"
    )

    assert (
        enriched.metadata[
            "freshness_status"
        ]
        == "warning"
    )


def test_growth_active_customers_non_current():

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    chunks = _dashboard_chunks(
        "growth_marketing_dashboard.json"
    )

    target = next(
        chunk
        for chunk in chunks
        if (
            chunk.metadata.get(
                "structure_key"
            )
            == "metrics"
            and '"active_customers"'
            in chunk.content
        )
    )

    enriched = (
        enrich_chunk_with_governance(
            target,
            registry=registry,
            as_of_date=AS_OF_DATE,
            warning_after_days=120,
            stale_after_days=180,
        )
    )

    assert (
        enriched.metadata[
            "observed_version"
        ]
        == "v1"
    )

    assert (
        enriched.metadata[
            "authoritative_version"
        ]
        == "v2"
    )

    assert (
        enriched.metadata[
            "version_relation"
        ]
        == "non_current"
    )

    assert (
        enriched.metadata[
            "freshness_status"
        ]
        == "fresh"
    )


def test_business_rule_version_enrichment():

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

    chunks = build_chunks(
        document,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    registry = (
        load_authoritative_metric_registry(
            REPO_ROOT
        )
    )

    enriched = (
        enrich_chunk_with_governance(
            chunks[0],
            registry=registry,
            as_of_date=AS_OF_DATE,
            warning_after_days=120,
            stale_after_days=180,
        )
    )

    assert (
        enriched.metadata[
            "metric_name"
        ]
        == "net_revenue"
    )

    assert (
        enriched.metadata[
            "authoritative_version"
        ]
        == "v3"
    )

    assert (
        enriched.metadata[
            "version_relation"
        ]
        == "current"
    )