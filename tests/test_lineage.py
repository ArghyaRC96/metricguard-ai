from pathlib import Path

from metricguard.ingestion import (
    build_parsed_document,
    parse_knowledge_base,
)
from metricguard.lineage import (
    build_lineage_edges,
    build_lineage_graph,
    extract_sql_dependencies,
    get_all_downstream,
    get_all_upstream,
    validate_lineage_graph,
)


REPO_ROOT = Path(
    __file__
).resolve().parents[1]

RAW_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
)


def test_staging_dependency():

    path = (
        RAW_DIR
        / "sql"
        / "staging"
        / "stg_orders.sql"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    dependencies = (
        extract_sql_dependencies(
            document
        )
    )

    assert dependencies == {
        "raw_orders"
    }


def test_fact_dependencies_exclude_ctes():

    path = (
        RAW_DIR
        / "sql"
        / "facts"
        / "fct_orders.sql"
    )

    document = build_parsed_document(
        path=path,
        repo_root=REPO_ROOT,
    )

    dependencies = (
        extract_sql_dependencies(
            document
        )
    )

    assert {
        "stg_orders",
        "stg_payments",
        "stg_refunds",
    }.issubset(
        dependencies
    )

    assert (
        "payment_summary"
        not in dependencies
    )

    assert (
        "refund_summary"
        not in dependencies
    )


def _build_graph():

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

    graph = build_lineage_graph(
        edges
    )

    validate_lineage_graph(
        graph
    )

    return graph, edges


def test_dashboard_lineage():

    graph, _ = _build_graph()

    assert graph.has_edge(
        "mart_finance_daily",
        "Finance Revenue Dashboard",
    )


def test_lineage_graph_is_valid():

    graph, edges = _build_graph()

    assert graph.number_of_nodes() > 0
    assert graph.number_of_edges() > 0
    assert len(edges) > 0


def test_finance_dashboard_upstream_lineage():

    graph, _ = _build_graph()

    upstream = set(
        get_all_upstream(
            graph,
            "Finance Revenue Dashboard",
        )
    )

    expected = {
        "mart_finance_daily",
        "fct_orders",
        "stg_orders",
        "stg_payments",
        "stg_refunds",
        "raw_orders",
        "raw_payments",
        "raw_refunds",
    }

    assert expected.issubset(
        upstream
    )


def test_fct_orders_downstream_impact():

    graph, _ = _build_graph()

    downstream = set(
        get_all_downstream(
            graph,
            "fct_orders",
        )
    )

    assert (
        "Finance Revenue Dashboard"
        in downstream
    )

    assert (
        "Executive KPI Dashboard"
        in downstream
    )

    assert (
        "mart_finance_daily"
        in downstream
    )

    assert (
        "mart_executive_daily"
        in downstream
    )