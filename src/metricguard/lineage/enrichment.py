from pathlib import Path

import networkx as nx

from metricguard.chunking.models import KnowledgeChunk

from .graph import (
    get_all_downstream,
    get_all_upstream,
    get_direct_downstream,
    get_direct_upstream,
)


def infer_lineage_node(
    chunk: KnowledgeChunk,
) -> str | None:
    """
    Map a retrieval chunk to the asset name used in the lineage graph.
    """

    metadata = chunk.metadata

    asset_type = metadata.get(
        "asset_type"
    )

    file_name = metadata.get(
        "file_name"
    )

    if asset_type == "dashboard":

        dashboard_name = metadata.get(
            "dashboard_name"
        )

        return (
            str(dashboard_name)
            if dashboard_name
            else None
        )

    if asset_type in {
        "raw_dataset",
        "staging_model",
        "fact_model",
        "mart",
        "metric_sql",
    }:

        if not file_name:
            return None

        return Path(
            str(file_name)
        ).stem

    return None


def enrich_chunk_with_lineage(
    chunk: KnowledgeChunk,
    graph: nx.DiGraph,
) -> KnowledgeChunk:
    """
    Attach deterministic upstream lineage and downstream impact metadata.
    """

    metadata = dict(
        chunk.metadata
    )

    lineage_node = infer_lineage_node(
        chunk
    )

    metadata[
        "lineage_node"
    ] = lineage_node

    if (
        lineage_node is None
        or lineage_node not in graph
    ):

        metadata[
            "lineage_available"
        ] = False

        metadata[
            "direct_upstream"
        ] = []

        metadata[
            "all_upstream"
        ] = []

        metadata[
            "direct_downstream"
        ] = []

        metadata[
            "all_downstream"
        ] = []

        metadata[
            "upstream_count"
        ] = 0

        metadata[
            "downstream_count"
        ] = 0

        return KnowledgeChunk(
            chunk_id=chunk.chunk_id,
            content=chunk.content,
            metadata=metadata,
        )

    direct_upstream = (
        get_direct_upstream(
            graph,
            lineage_node,
        )
    )

    all_upstream = (
        get_all_upstream(
            graph,
            lineage_node,
        )
    )

    direct_downstream = (
        get_direct_downstream(
            graph,
            lineage_node,
        )
    )

    all_downstream = (
        get_all_downstream(
            graph,
            lineage_node,
        )
    )

    metadata[
        "lineage_available"
    ] = True

    metadata[
        "direct_upstream"
    ] = direct_upstream

    metadata[
        "all_upstream"
    ] = all_upstream

    metadata[
        "direct_downstream"
    ] = direct_downstream

    metadata[
        "all_downstream"
    ] = all_downstream

    metadata[
        "upstream_count"
    ] = len(
        all_upstream
    )

    metadata[
        "downstream_count"
    ] = len(
        all_downstream
    )

    return KnowledgeChunk(
        chunk_id=chunk.chunk_id,
        content=chunk.content,
        metadata=metadata,
    )


def enrich_chunks_with_lineage(
    chunks: list[KnowledgeChunk],
    graph: nx.DiGraph,
) -> list[KnowledgeChunk]:
    """Apply lineage enrichment to all retrieval chunks."""

    return [
        enrich_chunk_with_lineage(
            chunk,
            graph,
        )
        for chunk in chunks
    ]


def validate_lineage_enrichment(
    chunks: list[KnowledgeChunk],
) -> None:
    """Validate lineage metadata before embeddings."""

    if not chunks:
        raise ValueError(
            "No lineage-enriched chunks found."
        )

    required_fields = {
        "lineage_available",
        "direct_upstream",
        "all_upstream",
        "direct_downstream",
        "all_downstream",
        "upstream_count",
        "downstream_count",
    }

    for chunk in chunks:

        metadata = chunk.metadata

        missing = (
            required_fields
            - set(metadata)
        )

        if missing:

            raise ValueError(
                f"{chunk.chunk_id} "
                f"is missing lineage metadata: "
                f"{sorted(missing)}"
            )

        if (
            "ground_truth"
            in metadata.get(
                "source_path",
                "",
            )
        ):

            raise ValueError(
                "Ground-truth leakage detected."
            )