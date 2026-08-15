from pathlib import Path

from metricguard.chunking import (
    build_chunks,
    chunk_knowledge_base,
    validate_chunks,
)
from metricguard.ingestion import (
    build_parsed_document,
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

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def test_markdown_chunking():

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

    assert chunks

    assert all(
        chunk.content.strip()
        for chunk in chunks
    )


def test_chunk_metadata_provenance():

    path = (
        RAW_DIR
        / "sql"
        / "metrics"
        / "net_revenue_v3.sql"
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

    first_chunk = chunks[0]

    assert (
        first_chunk.metadata[
            "metric_name"
        ]
        == "net_revenue"
    )

    assert (
        first_chunk.metadata[
            "version"
        ]
        == "v3"
    )

    assert (
        first_chunk.metadata[
            "asset_type"
        ]
        == "metric_sql"
    )


def test_chunk_ids_are_unique():

    documents, errors = (
        parse_knowledge_base(
            source_root=RAW_DIR,
            repo_root=REPO_ROOT,
        )
    )

    assert errors == []

    chunks, chunk_errors = (
        chunk_knowledge_base(
            documents,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
    )

    assert chunk_errors == []

    chunk_ids = [
        chunk.chunk_id
        for chunk in chunks
    ]

    assert len(chunk_ids) == len(
        set(chunk_ids)
    )


def test_no_ground_truth_leakage():

    documents, errors = (
        parse_knowledge_base(
            source_root=RAW_DIR,
            repo_root=REPO_ROOT,
        )
    )

    assert errors == []

    chunks, chunk_errors = (
        chunk_knowledge_base(
            documents,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
    )

    assert chunk_errors == []

    assert all(
        "ground_truth"
        not in chunk.metadata[
            "source_path"
        ]
        for chunk in chunks
    )


def test_complete_chunk_validation():

    documents, errors = (
        parse_knowledge_base(
            source_root=RAW_DIR,
            repo_root=REPO_ROOT,
        )
    )

    assert errors == []

    chunks, chunk_errors = (
        chunk_knowledge_base(
            documents,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
    )

    assert chunk_errors == []

    validate_chunks(chunks)