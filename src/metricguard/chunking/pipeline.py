import csv
import json
from pathlib import Path

import yaml

from metricguard.ingestion import (
    parse_knowledge_base,
)
from metricguard.ingestion.models import ParsedDocument
from metricguard.metadata import (
    build_document_metadata,
)

from .models import (
    ChunkError,
    KnowledgeChunk,
)
from .splitters import chunk_document


def build_chunks(
    document: ParsedDocument,
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[KnowledgeChunk]:
    """Convert one parsed document into retrieval-ready chunks."""

    raw_chunks = chunk_document(
        document,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    base_metadata = build_document_metadata(
        document
    )

    chunks: list[KnowledgeChunk] = []

    total_chunks = len(raw_chunks)

    for index, raw_chunk in enumerate(
        raw_chunks
    ):

        chunk_id = (
            f"{document.document_id}"
            f"-chunk-{index:04d}"
        )

        metadata = {
            **base_metadata,
            **raw_chunk["section_metadata"],
            "chunk_index": index,
            "chunk_count": total_chunks,
        }

        chunks.append(
            KnowledgeChunk(
                chunk_id=chunk_id,
                content=raw_chunk["content"],
                metadata=metadata,
            )
        )

    return chunks


def chunk_knowledge_base(
    documents: list[ParsedDocument],
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> tuple[
    list[KnowledgeChunk],
    list[ChunkError],
]:
    """Chunk all parsed documents while collecting failures."""

    chunks: list[KnowledgeChunk] = []
    errors: list[ChunkError] = []

    for document in documents:

        try:

            chunks.extend(
                build_chunks(
                    document,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            )

        except Exception as exc:

            errors.append(
                ChunkError(
                    source_path=document.source_path,
                    error=str(exc),
                )
            )

    return chunks, errors


def validate_chunks(
    chunks: list[KnowledgeChunk],
) -> None:
    """Validate critical chunking invariants."""

    if not chunks:
        raise ValueError(
            "No chunks were generated."
        )

    if any(
        not chunk.content.strip()
        for chunk in chunks
    ):
        raise ValueError(
            "Empty chunk detected."
        )

    chunk_ids = [
        chunk.chunk_id
        for chunk in chunks
    ]

    if len(chunk_ids) != len(
        set(chunk_ids)
    ):
        raise ValueError(
            "Duplicate chunk IDs detected."
        )

    required_metadata = {
        "document_id",
        "source_path",
        "file_name",
        "source_type",
        "asset_type",
        "content_hash",
        "chunk_index",
        "chunk_count",
    }

    for chunk in chunks:

        missing = (
            required_metadata
            - set(chunk.metadata)
        )

        if missing:

            raise ValueError(
                f"Chunk {chunk.chunk_id} "
                f"is missing metadata: "
                f"{sorted(missing)}"
            )

        if (
            "ground_truth"
            in chunk.metadata[
                "source_path"
            ]
        ):

            raise ValueError(
                "Ground-truth leakage "
                "detected."
            )


def write_chunks_jsonl(
    chunks: list[KnowledgeChunk],
    output_path: Path,
) -> None:
    """Write retrieval-ready chunks to JSONL."""

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


def write_chunk_manifest(
    chunks: list[KnowledgeChunk],
    output_path: Path,
) -> None:
    """Write a compact chunk manifest for inspection."""

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
                "chunk_id",
                "source_type",
                "asset_type",
                "file_name",
                "metric_name",
                "version",
                "content_length",
            ],
        )

        writer.writeheader()

        for chunk in chunks:

            writer.writerow(
                {
                    "chunk_id":
                        chunk.chunk_id,

                    "source_type":
                        chunk.metadata[
                            "source_type"
                        ],

                    "asset_type":
                        chunk.metadata[
                            "asset_type"
                        ],

                    "file_name":
                        chunk.metadata[
                            "file_name"
                        ],

                    "metric_name":
                        chunk.metadata.get(
                            "metric_name"
                        ),

                    "version":
                        chunk.metadata.get(
                            "version"
                        ),

                    "content_length":
                        len(chunk.content),
                }
            )


def load_chunking_settings(
    repo_root: Path,
) -> tuple[int, int]:
    """Read chunking parameters from settings.yaml."""

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

    chunking_config = config[
        "chunking"
    ]

    return (
        int(
            chunking_config[
                "chunk_size"
            ]
        ),
        int(
            chunking_config[
                "chunk_overlap"
            ]
        ),
    )


def run_chunking(
    repo_root: Path,
) -> None:
    """Run parsing and chunking as one local pipeline."""

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
    ) = load_chunking_settings(
        repo_root
    )

    documents, parse_errors = (
        parse_knowledge_base(
            source_root=raw_dir,
            repo_root=repo_root,
        )
    )

    if parse_errors:

        raise RuntimeError(
            "Parsing failed before "
            "chunking."
        )

    chunks, chunk_errors = (
        chunk_knowledge_base(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    )

    validate_chunks(chunks)

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

    write_chunks_jsonl(
        chunks,
        processed_dir / "chunks.jsonl",
    )

    write_chunk_manifest(
        chunks,
        processed_dir
        / "chunk_manifest.csv",
    )

    print("=" * 60)
    print(
        "METRICGUARD CHUNKING REPORT"
    )
    print("=" * 60)

    print(
        f"Documents processed : "
        f"{len(documents)}"
    )

    print(
        f"Chunks generated    : "
        f"{len(chunks)}"
    )

    print(
        f"Chunking errors     : "
        f"{len(chunk_errors)}"
    )

    print(
        f"Chunk size target   : "
        f"{chunk_size}"
    )

    print(
        f"Chunk overlap       : "
        f"{chunk_overlap}"
    )

    print(
        "Ground truth        : excluded"
    )

    print(
        "Metadata            : attached"
    )


if __name__ == "__main__":

    repository_root = Path.cwd()

    run_chunking(
        repository_root
    )