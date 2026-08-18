import csv
import json
from datetime import date
from pathlib import Path

from metricguard.chunking import (
    chunk_knowledge_base,
    validate_chunks,
)
from metricguard.governance import (
    enrich_chunks_with_governance,
    load_authoritative_metric_registry,
    validate_governance_enrichment,
)
from metricguard.governance.enrichment_pipeline import (
    load_pipeline_settings,
)
from metricguard.ingestion import (
    parse_knowledge_base,
)

from .enrichment import (
    enrich_chunks_with_lineage,
    validate_lineage_enrichment,
)
from .extractor import (
    build_lineage_edges,
)
from .graph import (
    build_lineage_graph,
    validate_lineage_graph,
)


def write_fully_enriched_chunks(
    chunks,
    output_path: Path,
) -> None:
    """Write embedding-ready chunks as JSON Lines."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        for chunk in chunks:

            file.write(
                json.dumps(
                    chunk.to_dict(),
                    ensure_ascii=False,
                    default=str,
                )
                + "\n"
            )


def write_fully_enriched_manifest(
    chunks,
    output_path: Path,
) -> None:
    """Write a compact inspection manifest."""

    fields = [
        "chunk_id",
        "file_name",
        "asset_type",
        "metric_name",
        "observed_version",
        "authoritative_version",
        "version_relation",
        "freshness_status",
        "lineage_node",
        "lineage_available",
        "upstream_count",
        "downstream_count",
    ]

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()

        for chunk in chunks:

            metadata = chunk.metadata

            writer.writerow(
                {
                    field:
                        (
                            chunk.chunk_id
                            if field == "chunk_id"
                            else metadata.get(
                                field
                            )
                        )
                    for field in fields
                }
            )


def run_full_knowledge_enrichment(
    repo_root: Path,
    *,
    as_of_date: date,
) -> None:
    """
    Build retrieval chunks enriched with governance, lineage and impact.
    """

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

    (
        chunk_size,
        chunk_overlap,
        warning_after_days,
        stale_after_days,
    ) = load_pipeline_settings(
        repo_root
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

    chunks, chunk_errors = (
        chunk_knowledge_base(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    )

    if chunk_errors:

        messages = "\n".join(
            f"{error.source_path}: "
            f"{error.error}"
            for error in chunk_errors
        )

        raise RuntimeError(
            "Chunking errors detected:\n"
            f"{messages}"
        )

    validate_chunks(
        chunks
    )

    registry = (
        load_authoritative_metric_registry(
            repo_root
        )
    )

    governance_chunks = (
        enrich_chunks_with_governance(
            chunks,
            registry=registry,
            as_of_date=as_of_date,
            warning_after_days=
                warning_after_days,
            stale_after_days=
                stale_after_days,
        )
    )

    validate_governance_enrichment(
        governance_chunks
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

    final_chunks = (
        enrich_chunks_with_lineage(
            governance_chunks,
            graph,
        )
    )

    validate_lineage_enrichment(
        final_chunks
    )

    write_fully_enriched_chunks(
        final_chunks,
        processed_dir
        / "fully_enriched_chunks.jsonl",
    )

    write_fully_enriched_manifest(
        final_chunks,
        processed_dir
        / "fully_enriched_chunk_manifest.csv",
    )

    lineage_aware = [
        chunk
        for chunk in final_chunks
        if chunk.metadata.get(
            "lineage_available"
        )
    ]

    metric_aware = [
        chunk
        for chunk in final_chunks
        if chunk.metadata.get(
            "metric_name"
        )
    ]

    print("=" * 72)
    print(
        "METRICGUARD FULL KNOWLEDGE ENRICHMENT REPORT"
    )
    print("=" * 72)

    print(
        f"Parsed documents      : "
        f"{len(documents)}"
    )

    print(
        f"Final chunks          : "
        f"{len(final_chunks)}"
    )

    print(
        f"Metric-aware chunks   : "
        f"{len(metric_aware)}"
    )

    print(
        f"Lineage-aware chunks  : "
        f"{len(lineage_aware)}"
    )

    print(
        f"Lineage graph nodes   : "
        f"{graph.number_of_nodes()}"
    )

    print(
        f"Lineage graph edges   : "
        f"{graph.number_of_edges()}"
    )

    print(
        f"Freshness as-of       : "
        f"{as_of_date}"
    )

    print(
        "Ground truth          : excluded"
    )

    print(
        "Embedding readiness   : YES"
    )


if __name__ == "__main__":

    repository_root = Path.cwd()

    run_full_knowledge_enrichment(
        repository_root,
        as_of_date=date.today(),
    )