"""Production Qdrant indexing for MetricGuard AI."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from qdrant_client import models

from metricguard.lineage.enrichment_pipeline import (
    run_full_knowledge_enrichment,
)
from metricguard.retrieval.config import (
    load_retrieval_config,
)
from metricguard.retrieval.factories import (
    load_embedding_model,
)


@dataclass(
    slots=True,
    frozen=True,
)
class IndexingResult:
    """Summary of one completed MetricGuard indexing run."""

    collection_name: str
    chunk_count: int
    vector_size: int


def point_id_for_chunk(
    chunk_id: str,
) -> str:
    """Create a deterministic Qdrant-safe UUID from a chunk ID."""

    normalized_chunk_id = (
        str(chunk_id)
        .strip()
    )

    if not normalized_chunk_id:

        raise ValueError(
            "chunk_id cannot be empty."
        )

    return str(
        uuid5(
            NAMESPACE_URL,
            (
                "metricguard:"
                + normalized_chunk_id
            ),
        )
    )


def load_fully_enriched_chunks(
    repo_root: Path,
) -> list[dict[str, Any]]:
    """Load and validate embedding-ready MetricGuard chunks."""

    repo_root = Path(
        repo_root
    ).resolve()

    chunks_path = (
        repo_root
        / "data"
        / "processed"
        / "fully_enriched_chunks.jsonl"
    )

    if not chunks_path.exists():

        raise FileNotFoundError(
            "Embedding-ready chunks were not found: "
            f"{chunks_path}"
        )

    chunks: list[
        dict[str, Any]
    ] = []


    with chunks_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1,
        ):

            if not line.strip():

                continue


            try:

                chunk = json.loads(
                    line
                )

            except json.JSONDecodeError as exc:

                raise ValueError(
                    "Invalid JSON in fully enriched "
                    f"chunks at line {line_number}."
                ) from exc


            chunk_id = str(
                chunk.get(
                    "chunk_id",
                    "",
                )
            ).strip()

            content = str(
                chunk.get(
                    "content",
                    "",
                )
            ).strip()

            metadata = (
                chunk.get(
                    "metadata"
                )
                or {}
            )


            if not chunk_id:

                raise ValueError(
                    "Missing chunk_id at "
                    f"line {line_number}."
                )


            if not content:

                raise ValueError(
                    "Missing chunk content at "
                    f"line {line_number}."
                )


            if not isinstance(
                metadata,
                dict,
            ):

                raise ValueError(
                    "Chunk metadata must be a "
                    f"mapping at line {line_number}."
                )


            chunks.append(
                {
                    "chunk_id":
                        chunk_id,

                    "content":
                        content,

                    "metadata":
                        dict(
                            metadata
                        ),
                }
            )


    if not chunks:

        raise ValueError(
            "No fully enriched chunks "
            "were available for indexing."
        )


    chunk_ids = [
        chunk[
            "chunk_id"
        ]
        for chunk in chunks
    ]


    if len(
        chunk_ids
    ) != len(
        set(
            chunk_ids
        )
    ):

        raise ValueError(
            "Duplicate chunk IDs detected "
            "before Qdrant indexing."
        )


    return chunks


def build_qdrant_payload(
    chunk: dict[str, Any],
) -> dict[str, Any]:
    """
    Build retrieval-compatible Qdrant payload.

    Governance and lineage metadata remain available
    both as top-level fields and under metadata.
    """

    metadata = dict(
        chunk[
            "metadata"
        ]
    )

    payload = dict(
        metadata
    )

    payload[
        "chunk_id"
    ] = chunk[
        "chunk_id"
    ]

    payload[
        "content"
    ] = chunk[
        "content"
    ]

    payload[
        "metadata"
    ] = metadata

    return payload


def encode_chunks(
    *,
    chunks: list[
        dict[str, Any]
    ],
    embedding_model: Any,
    normalize_embeddings: bool,
    batch_size: int,
) -> list[list[float]]:
    """Embed chunk content using the production embedding model."""

    if batch_size <= 0:

        raise ValueError(
            "batch_size must be positive."
        )


    contents = [
        chunk[
            "content"
        ]
        for chunk in chunks
    ]


    vectors = (
        embedding_model.encode(
            contents,
            normalize_embeddings=
                normalize_embeddings,
            convert_to_numpy=True,
            show_progress_bar=False,
            batch_size=batch_size,
        )
    )


    if hasattr(
        vectors,
        "tolist",
    ):

        vectors = (
            vectors.tolist()
        )


    normalized_vectors = [
        [
            float(
                value
            )
            for value in vector
        ]
        for vector in vectors
    ]


    if len(
        normalized_vectors
    ) != len(
        chunks
    ):

        raise RuntimeError(
            "Embedding output count does "
            "not match chunk count."
        )


    if not normalized_vectors:

        raise RuntimeError(
            "Embedding model returned "
            "no vectors."
        )


    vector_size = len(
        normalized_vectors[
            0
        ]
    )


    if vector_size <= 0:

        raise RuntimeError(
            "Embedding vectors cannot "
            "be empty."
        )


    if any(
        len(
            vector
        )
        != vector_size
        for vector
        in normalized_vectors
    ):

        raise RuntimeError(
            "Embedding vectors have "
            "inconsistent dimensions."
        )


    return normalized_vectors


def replace_qdrant_collection(
    *,
    qdrant_client: Any,
    collection_name: str,
    vector_size: int,
) -> None:
    """Replace the production dense-vector collection."""

    if vector_size <= 0:

        raise ValueError(
            "vector_size must be positive."
        )


    if qdrant_client.collection_exists(
        collection_name=
            collection_name,
    ):

        qdrant_client.delete_collection(
            collection_name=
                collection_name,
        )


    qdrant_client.create_collection(
        collection_name=
            collection_name,

        vectors_config=
            models.VectorParams(
                size=vector_size,
                distance=
                    models.Distance.COSINE,
            ),
    )


def upsert_chunks(
    *,
    qdrant_client: Any,
    collection_name: str,
    chunks: list[
        dict[str, Any]
    ],
    vectors: list[
        list[float]
    ],
    batch_size: int,
) -> None:
    """Upsert embedded MetricGuard chunks into Qdrant."""

    if batch_size <= 0:

        raise ValueError(
            "batch_size must be positive."
        )


    if len(
        chunks
    ) != len(
        vectors
    ):

        raise ValueError(
            "Chunk and vector counts "
            "must match."
        )


    points = [
        models.PointStruct(
            id=
                point_id_for_chunk(
                    chunk[
                        "chunk_id"
                    ]
                ),

            vector=
                vector,

            payload=
                build_qdrant_payload(
                    chunk
                ),
        )

        for chunk, vector
        in zip(
            chunks,
            vectors,
        )
    ]


    for start in range(
        0,
        len(
            points
        ),
        batch_size,
    ):

        batch = points[
            start:
            start
            + batch_size
        ]

        qdrant_client.upsert(
            collection_name=
                collection_name,

            points=batch,

            wait=True,
        )


def validate_qdrant_index(
    *,
    qdrant_client: Any,
    collection_name: str,
    expected_count: int,
) -> None:
    """Confirm the final Qdrant point count."""

    result = (
        qdrant_client.count(
            collection_name=
                collection_name,
            exact=True,
        )
    )

    actual_count = int(
        result.count
    )


    if actual_count != expected_count:

        raise RuntimeError(
            "Qdrant index validation failed: "
            f"expected {expected_count} points, "
            f"found {actual_count}."
        )


def index_fully_enriched_chunks(
    *,
    repo_root: Path,
    qdrant_client: Any,
    embedding_model: Any | None = None,
    batch_size: int = 64,
) -> IndexingResult:
    """Embed fully enriched chunks and replace the Qdrant index."""

    repo_root = Path(
        repo_root
    ).resolve()

    config = (
        load_retrieval_config(
            repo_root
        )
    )

    chunks = (
        load_fully_enriched_chunks(
            repo_root
        )
    )


    if embedding_model is None:

        embedding_model = (
            load_embedding_model(
                config.embedding_model
            )
        )


    vectors = encode_chunks(
        chunks=chunks,
        embedding_model=
            embedding_model,
        normalize_embeddings=
            config
            .normalize_embeddings,
        batch_size=
            batch_size,
    )


    vector_size = len(
        vectors[
            0
        ]
    )


    replace_qdrant_collection(
        qdrant_client=
            qdrant_client,
        collection_name=
            config.collection_name,
        vector_size=
            vector_size,
    )


    upsert_chunks(
        qdrant_client=
            qdrant_client,
        collection_name=
            config.collection_name,
        chunks=
            chunks,
        vectors=
            vectors,
        batch_size=
            batch_size,
    )


    validate_qdrant_index(
        qdrant_client=
            qdrant_client,
        collection_name=
            config.collection_name,
        expected_count=
            len(
                chunks
            ),
    )


    return IndexingResult(
        collection_name=
            config.collection_name,
        chunk_count=
            len(
                chunks
            ),
        vector_size=
            vector_size,
    )


def rebuild_knowledge_base_index(
    *,
    repo_root: Path,
    qdrant_client: Any,
    as_of_date: date | None = None,
    embedding_model: Any | None = None,
    batch_size: int = 64,
) -> IndexingResult:
    """
    Rebuild the complete MetricGuard knowledge base
    and replace the production Qdrant index.
    """

    resolved_date = (
        as_of_date
        or date.today()
    )


    run_full_knowledge_enrichment(
        repo_root,
        as_of_date=
            resolved_date,
    )


    return (
        index_fully_enriched_chunks(
            repo_root=
                repo_root,
            qdrant_client=
                qdrant_client,
            embedding_model=
                embedding_model,
            batch_size=
                batch_size,
        )
    )
