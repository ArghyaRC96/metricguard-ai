from typing import Any

from .dense import DenseRetriever
from .models import RerankedEvidence
from .reranker import CrossEncoderReranker


class RetrievalPipeline:
    """
    MetricGuard production retrieve-and-rerank pipeline.
    """

    def __init__(
        self,
        *,
        dense_retriever:
            DenseRetriever,
        reranker:
            CrossEncoderReranker,
        candidate_top_k: int,
        final_top_k: int,
    ) -> None:

        if (
            candidate_top_k
            < final_top_k
        ):
            raise ValueError(
                "candidate_top_k must "
                "be >= final_top_k."
            )

        self.dense_retriever = (
            dense_retriever
        )

        self.reranker = reranker

        self.candidate_top_k = (
            candidate_top_k
        )

        self.final_top_k = (
            final_top_k
        )

    def retrieve(
        self,
        query: str,
        *,
        query_filter: Any = None,
    ) -> list[RerankedEvidence]:
        """
        Dense retrieval followed by mandatory reranking.
        """

        candidates = (
            self.dense_retriever
            .retrieve(
                query,
                top_k=
                    self.candidate_top_k,
                query_filter=
                    query_filter,
            )
        )

        evidence = (
            self.reranker.rerank(
                query,
                candidates,
                top_k=
                    self.final_top_k,
            )
        )

        validate_final_evidence(
            evidence
        )

        return evidence


def validate_final_evidence(
    evidence: list[
        RerankedEvidence
    ],
) -> None:
    """Protect provenance and evaluation boundaries."""

    for item in evidence:

        source_path = str(
            item.payload.get(
                "source_path",
                "",
            )
        )

        if not source_path:
            raise ValueError(
                "Retrieved evidence "
                "has no source_path."
            )

        if (
            "ground_truth"
            in source_path
        ):
            raise ValueError(
                "Ground-truth leakage "
                "detected in retrieval."
            )


def format_final_evidence(
    evidence: list[
        RerankedEvidence
    ],
) -> list[dict[str, Any]]:
    """
    Convert reranked evidence into the structure
    consumed by RAG and agents.
    """

    output: list[
        dict[str, Any]
    ] = []

    for item in evidence:

        payload = item.payload

        output.append(
            {
                "evidence_rank":
                    item.rerank_rank,
                "dense_rank":
                    item.dense_rank,
                "dense_score":
                    item.dense_score,
                "rerank_score":
                    item.rerank_score,
                "source_path":
                    payload.get(
                        "source_path"
                    ),
                "file_name":
                    payload.get(
                        "file_name"
                    ),
                "asset_type":
                    payload.get(
                        "asset_type"
                    ),
                "metric_name":
                    payload.get(
                        "metric_name"
                    ),
                "observed_version":
                    payload.get(
                        "observed_version"
                    ),
                "authoritative_version":
                    payload.get(
                        "authoritative_version"
                    ),
                "version_relation":
                    payload.get(
                        "version_relation"
                    ),
                "freshness_status":
                    payload.get(
                        "freshness_status"
                    ),
                "lineage_node":
                    payload.get(
                        "lineage_node"
                    ),
                "direct_upstream":
                    payload.get(
                        "direct_upstream",
                        [],
                    ),
                "all_upstream":
                    payload.get(
                        "all_upstream",
                        [],
                    ),
                "direct_downstream":
                    payload.get(
                        "direct_downstream",
                        [],
                    ),
                "all_downstream":
                    payload.get(
                        "all_downstream",
                        [],
                    ),
                "content":
                    payload.get(
                        "content",
                        "",
                    ),
            }
        )

    return output