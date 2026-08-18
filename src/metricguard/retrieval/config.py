from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True, frozen=True)
class RetrievalConfig:
    candidate_top_k: int
    final_top_k: int
    reranker_model: str
    embedding_model: str
    collection_name: str
    normalize_embeddings: bool


def load_retrieval_config(
    repo_root: Path,
) -> RetrievalConfig:
    """Load and validate production retrieval settings."""

    config_path = (
        repo_root
        / "configs"
        / "settings.yaml"
    )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        settings = (
            yaml.safe_load(file)
            or {}
        )

    retrieval = (
        settings.get("retrieval")
        or {}
    )

    embeddings = (
        settings.get("embeddings")
        or {}
    )

    vector_database = (
        settings.get(
            "vector_database"
        )
        or {}
    )

    if (
        retrieval.get(
            "rerank_enabled"
        )
        is not True
    ):
        raise ValueError(
            "Production MetricGuard "
            "requires reranking."
        )

    candidate_top_k = int(
        retrieval.get(
            "candidate_top_k",
            20,
        )
    )

    final_top_k = int(
        retrieval.get(
            "final_top_k",
            5,
        )
    )

    if candidate_top_k < final_top_k:
        raise ValueError(
            "candidate_top_k must be "
            "greater than or equal to "
            "final_top_k."
        )

    reranker_model = (
        retrieval.get(
            "reranker_model"
        )
    )

    embedding_model = (
        embeddings.get("model")
    )

    collection_name = (
        vector_database.get(
            "collection_name"
        )
    )

    if not reranker_model:
        raise ValueError(
            "reranker_model is required."
        )

    if not embedding_model:
        raise ValueError(
            "embeddings.model is required."
        )

    if not collection_name:
        raise ValueError(
            "Qdrant collection_name "
            "is required."
        )

    return RetrievalConfig(
        candidate_top_k=
            candidate_top_k,
        final_top_k=
            final_top_k,
        reranker_model=
            str(reranker_model),
        embedding_model=
            str(embedding_model),
        collection_name=
            str(collection_name),
        normalize_embeddings=bool(
            embeddings.get(
                "normalize",
                True,
            )
        ),
    )