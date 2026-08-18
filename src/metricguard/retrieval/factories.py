from pathlib import Path
from typing import Any

from .config import (
    load_retrieval_config,
)
from .dense import DenseRetriever
from .pipeline import RetrievalPipeline
from .reranker import CrossEncoderReranker


def load_embedding_model(
    model_name: str,
) -> Any:
    """Heavy import is intentionally lazy."""

    from sentence_transformers import (
        SentenceTransformer,
    )

    return SentenceTransformer(
        model_name
    )


def load_reranker_model(
    model_name: str,
) -> Any:
    """Heavy Torch/SentenceTransformers import is lazy."""

    import torch
    from sentence_transformers import (
        CrossEncoder,
    )

    return CrossEncoder(
        model_name,
        activation_fn=
            torch.nn.Sigmoid(),
    )


def build_retrieval_pipeline(
    *,
    repo_root: Path,
    qdrant_client: Any,
) -> RetrievalPipeline:
    """
    Build the complete production retrieval stack.
    """

    config = (
        load_retrieval_config(
            repo_root
        )
    )

    embedding_model = (
        load_embedding_model(
            config.embedding_model
        )
    )

    reranker_model = (
        load_reranker_model(
            config.reranker_model
        )
    )

    dense_retriever = (
        DenseRetriever(
            client=qdrant_client,
            embedding_model=
                embedding_model,
            collection_name=
                config.collection_name,
            normalize_embeddings=
                config
                .normalize_embeddings,
        )
    )

    reranker = (
        CrossEncoderReranker(
            model=reranker_model
        )
    )

    return RetrievalPipeline(
        dense_retriever=
            dense_retriever,
        reranker=reranker,
        candidate_top_k=
            config.candidate_top_k,
        final_top_k=
            config.final_top_k,
    )