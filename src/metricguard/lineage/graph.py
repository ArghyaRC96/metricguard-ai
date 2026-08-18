from typing import Any

import networkx as nx

from .models import LineageEdge


def build_lineage_graph(
    edges: list[LineageEdge],
) -> nx.DiGraph:
    """Build the upstream-to-downstream lineage graph."""

    graph = nx.DiGraph()

    for edge in edges:

        graph.add_edge(
            edge.upstream,
            edge.downstream,
            relationship=edge.relationship,
            source_path=edge.source_path,
        )

    return graph


def validate_lineage_graph(
    graph: nx.DiGraph,
) -> None:
    """Validate critical graph invariants."""

    if graph.number_of_nodes() == 0:
        raise ValueError(
            "Lineage graph contains no nodes."
        )

    if graph.number_of_edges() == 0:
        raise ValueError(
            "Lineage graph contains no edges."
        )

    self_loops = list(
        nx.selfloop_edges(graph)
    )

    if self_loops:
        raise ValueError(
            f"Self-referencing lineage edges found: "
            f"{self_loops}"
        )

    if not nx.is_directed_acyclic_graph(
        graph
    ):
        raise ValueError(
            "Lineage graph contains a dependency cycle."
        )


def _require_node(
    graph: nx.DiGraph,
    node: str,
) -> None:
    """Raise a clear error if an asset is not in the graph."""

    if node not in graph:
        raise KeyError(
            f"Asset not found in lineage graph: "
            f"{node}"
        )


def get_direct_upstream(
    graph: nx.DiGraph,
    node: str,
) -> list[str]:
    """Return immediate upstream dependencies."""

    _require_node(
        graph,
        node,
    )

    return sorted(
        graph.predecessors(node)
    )


def get_all_upstream(
    graph: nx.DiGraph,
    node: str,
) -> list[str]:
    """Return all transitive upstream dependencies."""

    _require_node(
        graph,
        node,
    )

    return sorted(
        nx.ancestors(
            graph,
            node,
        )
    )


def get_direct_downstream(
    graph: nx.DiGraph,
    node: str,
) -> list[str]:
    """Return immediate downstream consumers."""

    _require_node(
        graph,
        node,
    )

    return sorted(
        graph.successors(node)
    )


def get_all_downstream(
    graph: nx.DiGraph,
    node: str,
) -> list[str]:
    """Return every transitively impacted downstream asset."""

    _require_node(
        graph,
        node,
    )

    return sorted(
        nx.descendants(
            graph,
            node,
        )
    )


def trace_asset(
    graph: nx.DiGraph,
    node: str,
) -> dict[str, Any]:
    """Return one combined lineage and impact view."""

    return {
        "asset": node,
        "direct_upstream":
            get_direct_upstream(
                graph,
                node,
            ),
        "all_upstream":
            get_all_upstream(
                graph,
                node,
            ),
        "direct_downstream":
            get_direct_downstream(
                graph,
                node,
            ),
        "all_downstream":
            get_all_downstream(
                graph,
                node,
            ),
    }