from pathlib import Path

from metricguard.ingestion import (
    build_parsed_document,
    discover_source_files,
    parse_knowledge_base,
    validate_documents,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"


def test_source_discovery_returns_files():
    files = discover_source_files(RAW_DIR)

    assert files
    assert all(path.is_file() for path in files)


def test_ground_truth_is_not_discovered():
    files = discover_source_files(RAW_DIR)

    assert all(
        "ground_truth" not in str(path)
        for path in files
    )


def test_build_parsed_sql_document():
    sql_path = (
        RAW_DIR
        / "sql"
        / "staging"
        / "stg_orders.sql"
    )

    document = build_parsed_document(
        path=sql_path,
        repo_root=REPO_ROOT,
    )

    assert document.source_type == "sql"
    assert document.file_name == "stg_orders.sql"
    assert "raw_orders" in document.content
    assert len(document.content_hash) == 64


def test_parse_entire_knowledge_base():
    documents, errors = parse_knowledge_base(
        source_root=RAW_DIR,
        repo_root=REPO_ROOT,
    )

    assert documents
    assert errors == []

    validate_documents(documents)


def test_document_ids_are_unique():
    documents, _ = parse_knowledge_base(
        source_root=RAW_DIR,
        repo_root=REPO_ROOT,
    )

    document_ids = [
        document.document_id
        for document in documents
    ]

    assert len(document_ids) == len(set(document_ids))


def test_csv_is_summary_not_row_level_documents():
    csv_path = (
        RAW_DIR
        / "tabular"
        / "raw_orders.csv"
    )

    document = build_parsed_document(
        path=csv_path,
        repo_root=REPO_ROOT,
    )

    assert document.source_type == "csv"
    assert "Dataset: raw_orders" in document.content
    assert "Rows:" in document.content
    assert document.structured_data["row_count"] > 0
