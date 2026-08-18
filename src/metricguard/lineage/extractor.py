from pathlib import Path

from sqlglot import exp, parse_one

from metricguard.ingestion.models import (
    ParsedDocument,
)
from metricguard.metadata import (
    build_document_metadata,
)

from .models import LineageEdge


def _table_identifier(
    table: exp.Table,
) -> str:
    """Return a normalized table identifier."""

    parts = [
        table.catalog,
        table.db,
        table.name,
    ]

    return ".".join(
        str(part)
        for part in parts
        if part
    )


def extract_sql_dependencies(
    document: ParsedDocument,
) -> set[str]:
    """
    Extract real upstream SQL relations while excluding CTE aliases.
    """

    if document.source_type != "sql":
        raise ValueError(
            "SQL dependency extraction requires a SQL document."
        )

    expression = parse_one(
        document.content
    )

    cte_names = {
        cte.alias_or_name
        for cte in expression.find_all(
            exp.CTE
        )
        if cte.alias_or_name
    }

    upstream_relations: set[str] = set()

    for table in expression.find_all(
        exp.Table
    ):

        identifier = _table_identifier(
            table
        )

        if not identifier:
            continue

        # A CTE behaves like a temporary relation inside
        # the query and should not become an external
        # lineage node.
        if table.name in cte_names:
            continue

        upstream_relations.add(
            identifier
        )

    return upstream_relations


def build_sql_lineage_edges(
    documents: list[ParsedDocument],
) -> list[LineageEdge]:
    """Convert SQL source dependencies into directed lineage edges."""

    edges: list[LineageEdge] = []

    for document in documents:

        if document.source_type != "sql":
            continue

        target_model = Path(
            document.file_name
        ).stem

        dependencies = (
            extract_sql_dependencies(
                document
            )
        )

        for upstream in dependencies:

            edges.append(
                LineageEdge(
                    upstream=upstream,
                    downstream=target_model,
                    relationship="sql_dependency",
                    source_path=document.source_path,
                )
            )

    return edges


def build_dashboard_lineage_edges(
    documents: list[ParsedDocument],
) -> list[LineageEdge]:
    """
    Link downstream dashboards to the marts declared in dashboard JSON.
    """

    edges: list[LineageEdge] = []

    for document in documents:

        metadata = build_document_metadata(
            document
        )

        if (
            metadata.get("asset_type")
            != "dashboard"
        ):
            continue

        source_mart = metadata.get(
            "source_mart"
        )

        dashboard_name = metadata.get(
            "dashboard_name"
        )

        if (
            not source_mart
            or not dashboard_name
        ):
            continue

        edges.append(
            LineageEdge(
                upstream=str(source_mart),
                downstream=str(
                    dashboard_name
                ),
                relationship=
                    "dashboard_consumption",
                source_path=
                    document.source_path,
            )
        )

    return edges


def build_lineage_edges(
    documents: list[ParsedDocument],
) -> list[LineageEdge]:
    """
    Combine SQL-model lineage and dashboard consumption lineage.
    """

    edges = (
        build_sql_lineage_edges(
            documents
        )
        + build_dashboard_lineage_edges(
            documents
        )
    )

    unique_edges = {
        (
            edge.upstream,
            edge.downstream,
            edge.relationship,
            edge.source_path,
        ): edge
        for edge in edges
    }

    return sorted(
        unique_edges.values(),
        key=lambda edge: (
            edge.upstream,
            edge.downstream,
            edge.relationship,
        ),
    )