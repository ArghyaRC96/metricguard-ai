import csv
import json
from datetime import date
from pathlib import Path

import yaml

from metricguard.chunking import (
    chunk_knowledge_base,
    validate_chunks,
)
from metricguard.ingestion import (
    parse_knowledge_base,
)

from .enrichment import (
    enrich_chunks_with_governance,
    validate_governance_enrichment,
)
from .versions import (
    load_authoritative_metric_registry,
)


def load_pipeline_settings(
    repo_root: Path,
) -> tuple[int, int, int, int]:
    """
    Load chunking and freshness settings from project configuration.
    """

    config_path = (
        repo_root
        / "configs"
        / "settings.yaml"
    )

    with config_path.open(
        "r",
        encoding="utf-8-sig",
    ) as file:

        config = yaml.safe_load(file)

    chunking = config["chunking"]
    freshness = config["freshness"]

    return (
        int(chunking["chunk_size"]),
        int(chunking["chunk_overlap"]),
        int(
            freshness[
                "warning_after_days"
            ]
        ),
        int(
            freshness[
                "stale_after_days"
            ]
        ),
    )


def write_enriched_chunks(
    chunks,
    output_path: Path,
) -> None:
    """Write governance-enriched chunks as JSON Lines."""

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


def write_enriched_manifest(
    chunks,
    output_path: Path,
) -> None:
    """Write a compact manifest for governance inspection."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "chunk_id",
        "file_name",
        "asset_type",
        "metric_name",
        "observed_version",
        "authoritative_version",
        "version_relation",
        "freshness_status",
        "days_since_review",
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
                    "chunk_id":
                        chunk.chunk_id,

                    "file_name":
                        metadata.get(
                            "file_name"
                        ),

                    "asset_type":
                        metadata.get(
                            "asset_type"
                        ),

                    "metric_name":
                        metadata.get(
                            "metric_name"
                        ),

                    "observed_version":
                        metadata.get(
                            "observed_version"
                        ),

                    "authoritative_version":
                        metadata.get(
                            "authoritative_version"
                        ),

                    "version_relation":
                        metadata.get(
                            "version_relation"
                        ),

                    "freshness_status":
                        metadata.get(
                            "freshness_status"
                        ),

                    "days_since_review":
                        metadata.get(
                            "days_since_review"
                        ),
                }
            )


def run_governance_enrichment(
    repo_root: Path,
    *,
    as_of_date: date,
) -> None:
    """
    Build retrieval-ready chunks enriched with governance intelligence.
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

    validate_chunks(chunks)

    registry = (
        load_authoritative_metric_registry(
            repo_root
        )
    )

    enriched_chunks = (
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
        enriched_chunks
    )

    write_enriched_chunks(
        enriched_chunks,
        processed_dir
        / "governance_enriched_chunks.jsonl",
    )

    write_enriched_manifest(
        enriched_chunks,
        processed_dir
        / "governance_enriched_chunk_manifest.csv",
    )

    metric_chunks = [
        chunk
        for chunk in enriched_chunks
        if chunk.metadata.get(
            "metric_name"
        )
    ]

    non_current_chunks = [
        chunk
        for chunk in metric_chunks
        if chunk.metadata.get(
            "version_relation"
        )
        == "non_current"
    ]

    stale_chunks = [
        chunk
        for chunk in enriched_chunks
        if chunk.metadata.get(
            "freshness_status"
        )
        == "stale"
    ]

    print("=" * 70)
    print(
        "METRICGUARD GOVERNANCE ENRICHMENT REPORT"
    )
    print("=" * 70)

    print(
        f"Parsed documents      : "
        f"{len(documents)}"
    )

    print(
        f"Base chunks           : "
        f"{len(chunks)}"
    )

    print(
        f"Enriched chunks       : "
        f"{len(enriched_chunks)}"
    )

    print(
        f"Metric-aware chunks   : "
        f"{len(metric_chunks)}"
    )

    print(
        f"Non-current chunks    : "
        f"{len(non_current_chunks)}"
    )

    print(
        f"Stale chunks          : "
        f"{len(stale_chunks)}"
    )

    print(
        f"Freshness as-of       : "
        f"{as_of_date}"
    )

    print(
        "Ground truth          : excluded"
    )


if __name__ == "__main__":

    repository_root = Path.cwd()

    run_governance_enrichment(
        repository_root,
        as_of_date=date.today(),
    )