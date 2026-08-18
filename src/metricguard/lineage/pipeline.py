import csv
import json
from pathlib import Path

from metricguard.ingestion import (
    parse_knowledge_base,
)

from .extractor import (
    build_lineage_edges,
)
from .graph import (
    build_lineage_graph,
    get_all_downstream,
    get_direct_downstream,
    validate_lineage_graph,
)


def write_lineage_edges(
    edges,
    output_path: Path,
) -> None:
    """Write direct lineage edges to CSV."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "upstream",
                "downstream",
                "relationship",
                "source_path",
            ],
        )

        writer.writeheader()

        for edge in edges:
            writer.writerow(
                edge.to_dict()
            )


def write_graph_json(
    graph,
    edges,
    output_path: Path,
) -> None:
    """Write a simple portable JSON representation of the graph."""

    payload = {
        "nodes": sorted(
            graph.nodes
        ),
        "edges": [
            edge.to_dict()
            for edge in edges
        ],
    }

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            payload,
            file,
            indent=2,
            ensure_ascii=False,
        )


def write_impact_report(
    graph,
    output_path: Path,
) -> None:
    """Write downstream impact information for every lineage node."""

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "asset",
                "direct_downstream_count",
                "total_downstream_count",
                "direct_downstream",
                "all_downstream",
            ],
        )

        writer.writeheader()

        for node in sorted(
            graph.nodes
        ):

            direct = (
                get_direct_downstream(
                    graph,
                    node,
                )
            )

            all_downstream = (
                get_all_downstream(
                    graph,
                    node,
                )
            )

            writer.writerow(
                {
                    "asset": node,
                    "direct_downstream_count":
                        len(direct),
                    "total_downstream_count":
                        len(all_downstream),
                    "direct_downstream":
                        " | ".join(
                            direct
                        ),
                    "all_downstream":
                        " | ".join(
                            all_downstream
                        ),
                }
            )


def run_lineage_analysis(
    repo_root: Path,
) -> None:
    """Build the complete MetricGuard lineage and impact graph."""

    raw_dir = (
        repo_root
        / "data"
        / "raw"
    )

    processed_dir = (
        repo_root
        / "data"
        / "processed"
    )

    processed_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    documents, parse_errors = (
        parse_knowledge_base(
            source_root=raw_dir,
            repo_root=repo_root,
        )
    )

    if parse_errors:

        messages = "\n".join(
            f"{error.source_path}: "
            f"{error.error}"
            for error in parse_errors
        )

        raise RuntimeError(
            "Parsing errors detected:\n"
            f"{messages}"
        )

    edges = build_lineage_edges(
        documents
    )

    graph = build_lineage_graph(
        edges
    )

    validate_lineage_graph(
        graph
    )

    write_lineage_edges(
        edges,
        processed_dir
        / "lineage_edges.csv",
    )

    write_graph_json(
        graph,
        edges,
        processed_dir
        / "lineage_graph.json",
    )

    write_impact_report(
        graph,
        processed_dir
        / "impact_report.csv",
    )

    print("=" * 65)
    print(
        "METRICGUARD LINEAGE & IMPACT REPORT"
    )
    print("=" * 65)

    print(
        f"Parsed documents : "
        f"{len(documents)}"
    )

    print(
        f"Lineage nodes    : "
        f"{graph.number_of_nodes()}"
    )

    print(
        f"Lineage edges    : "
        f"{graph.number_of_edges()}"
    )

    print(
        "Graph type       : directed"
    )

    print(
        "Cycle check      : passed"
    )

    print(
        "Ground truth     : excluded"
    )


if __name__ == "__main__":

    repository_root = Path.cwd()

    run_lineage_analysis(
        repository_root
    )