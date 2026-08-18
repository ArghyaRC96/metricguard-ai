from pathlib import Path

from metricguard.chunking import (
    build_chunks,
)
from metricguard.ingestion import (
    build_parsed_document,
    parse_knowledge_base,
)
from metricguard.lineage import (
    build_lineage_edges,
    build_lineage_graph,
    enrich_chunk_with_lineage,
)


REPO_ROOT = Path(
    __file__
).resolve().parents[1]

RAW_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
)

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def _graph():

    documents, errors = (
        parse_knowledge_base(
            source_root=RAW_DIR,
            repo_root=REPO_ROOT,
        )
    )

    assert errors == []

    edges = build_lineage_edges(
        documents
    )

    return build_lineage_graph(
        edges
    )


def test_finance_mart_lineage():

    path = (
        RAW_DIR
        / "sql"
        / "marts"
        / "mart_finance_daily.sql"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    chunk = build_chunks(
        document,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )[0]

    enriched = (
        enrich_chunk_with_lineage(
            chunk,
            _graph(),
        )
    )

    assert (
        enriched.metadata[
            "lineage_node"
        ]
        == "mart_finance_daily"
    )

    assert (
        enriched.metadata[
            "lineage_available"
        ]
        is True
    )

    assert (
        "fct_orders"
        in enriched.metadata[
            "all_upstream"
        ]
    )

    assert (
        "Finance Revenue Dashboard"
        in enriched.metadata[
            "all_downstream"
        ]
    )


def test_finance_dashboard_lineage():

    path = (
        RAW_DIR
        / "dashboards"
        / "finance_revenue_dashboard.json"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    chunk = build_chunks(
        document,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )[0]

    enriched = (
        enrich_chunk_with_lineage(
            chunk,
            _graph(),
        )
    )

    assert (
        enriched.metadata[
            "lineage_node"
        ]
        == "Finance Revenue Dashboard"
    )

    assert (
        "mart_finance_daily"
        in enriched.metadata[
            "all_upstream"
        ]
    )

    assert (
        "fct_orders"
        in enriched.metadata[
            "all_upstream"
        ]
    )


def test_raw_payments_downstream_impact():

    path = (
        RAW_DIR
        / "tabular"
        / "raw_payments.csv"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    chunk = build_chunks(
        document,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )[0]

    enriched = (
        enrich_chunk_with_lineage(
            chunk,
            _graph(),
        )
    )

    assert (
        enriched.metadata[
            "lineage_available"
        ]
        is True
    )

    assert (
        "fct_orders"
        in enriched.metadata[
            "all_downstream"
        ]
    )

    assert (
        "Finance Revenue Dashboard"
        in enriched.metadata[
            "all_downstream"
        ]
    )


def test_analyst_note_has_no_graph_node():

    path = (
        RAW_DIR
        / "analyst_notes"
        / "active_customer_review.md"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    chunk = build_chunks(
        document,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )[0]

    enriched = (
        enrich_chunk_with_lineage(
            chunk,
            _graph(),
        )
    )

    assert (
        enriched.metadata[
            "lineage_available"
        ]
        is False
    )

    assert (
        enriched.metadata[
            "lineage_node"
        ]
        is None
    )