import csv
import hashlib
import json
from pathlib import Path

from .models import ParseError, ParsedDocument
from .parsers import SOURCE_TYPE_MAP, get_source_type, parse_file


SUPPORTED_EXTENSIONS = set(SOURCE_TYPE_MAP)


def calculate_file_hash(path: Path) -> str:
    """Calculate a deterministic SHA-256 hash for a source file."""

    hasher = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def discover_source_files(source_root: Path) -> list[Path]:
    """Discover supported knowledge files below a source directory."""

    return sorted(
        path
        for path in source_root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def build_parsed_document(
    path: Path,
    repo_root: Path,
) -> ParsedDocument:
    """Parse one file into MetricGuard's canonical document model."""

    content, structured_data = parse_file(path)

    content_hash = calculate_file_hash(path)

    document_id = (
        f"{path.stem}-"
        f"{content_hash[:12]}"
    )

    return ParsedDocument(
        document_id=document_id,
        source_path=str(path.relative_to(repo_root)),
        file_name=path.name,
        source_type=get_source_type(path),
        content_hash=content_hash,
        content=content,
        structured_data=structured_data,
    )


def parse_knowledge_base(
    source_root: Path,
    repo_root: Path,
) -> tuple[list[ParsedDocument], list[ParseError]]:
    """Parse every supported source while collecting file-level errors."""

    documents: list[ParsedDocument] = []
    errors: list[ParseError] = []

    for path in discover_source_files(source_root):
        try:
            documents.append(
                build_parsed_document(
                    path=path,
                    repo_root=repo_root,
                )
            )

        except Exception as exc:
            errors.append(
                ParseError(
                    source_path=str(path.relative_to(repo_root)),
                    error=str(exc),
                )
            )

    return documents, errors


def validate_documents(
    documents: list[ParsedDocument],
) -> None:
    """Validate basic ingestion invariants."""

    if not documents:
        raise ValueError("No documents were parsed.")

    if any(
        not document.content.strip()
        for document in documents
    ):
        raise ValueError("Empty parsed document detected.")

    document_ids = [
        document.document_id
        for document in documents
    ]

    if len(document_ids) != len(set(document_ids)):
        raise ValueError("Duplicate document IDs detected.")

    if any(
        "ground_truth" in document.source_path
        for document in documents
    ):
        raise ValueError(
            "Ground-truth evaluation leakage detected."
        )


def write_jsonl(
    documents: list[ParsedDocument],
    output_path: Path,
) -> None:
    """Write canonical documents as JSON Lines."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for document in documents:
            file.write(
                json.dumps(
                    document.to_dict(),
                    ensure_ascii=False,
                    default=str,
                )
                + "\n"
            )


def write_manifest(
    documents: list[ParsedDocument],
    output_path: Path,
) -> None:
    """Write a compact parsing manifest for inspection."""

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
                "document_id",
                "source_path",
                "source_type",
                "content_length",
            ],
        )

        writer.writeheader()

        for document in documents:
            writer.writerow(
                {
                    "document_id": document.document_id,
                    "source_path": document.source_path,
                    "source_type": document.source_type,
                    "content_length": len(document.content),
                }
            )


def run_ingestion(repo_root: Path) -> None:
    """Run the MetricGuard source parsing pipeline."""

    raw_dir = repo_root / "data" / "raw"
    processed_dir = repo_root / "data" / "processed"

    documents, errors = parse_knowledge_base(
        source_root=raw_dir,
        repo_root=repo_root,
    )

    validate_documents(documents)

    if errors:
        error_messages = "\n".join(
            f"{error.source_path}: {error.error}"
            for error in errors
        )

        raise RuntimeError(
            "Parsing errors detected:\n"
            f"{error_messages}"
        )

    write_jsonl(
        documents,
        processed_dir / "parsed_documents.jsonl",
    )

    write_manifest(
        documents,
        processed_dir / "parse_manifest.csv",
    )

    print("=" * 60)
    print("METRICGUARD INGESTION REPORT")
    print("=" * 60)
    print(f"Documents parsed : {len(documents)}")
    print(f"Parse errors     : {len(errors)}")
    print("Ground truth     : excluded")
    print(
        "Output           : "
        "data/processed/parsed_documents.jsonl"
    )


if __name__ == "__main__":
    repository_root = Path.cwd()

    run_ingestion(repository_root)
