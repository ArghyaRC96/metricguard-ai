from pathlib import Path
from types import SimpleNamespace

import pytest

from metricguard.retrieval import (
    CrossEncoderReranker,
    DenseRetriever,
    RetrievalPipeline,
    RerankedEvidence,
    format_final_evidence,
    load_retrieval_config,
    validate_final_evidence,
)


REPO_ROOT = Path(
    __file__
).resolve().parents[1]


class FakeEmbeddingModel:

    def encode(
        self,
        text,
        **kwargs,
    ):
        return [
            0.1,
            0.2,
            0.3,
        ]


class FakeQdrantClient:

    def __init__(self):
        self.last_filter = None

    def query_points(
        self,
        *,
        collection_name,
        query,
        query_filter,
        limit,
        with_payload,
    ):
        self.last_filter = (
            query_filter
        )

        points = [
            SimpleNamespace(
                id="point-1",
                score=0.95,
                payload={
                    "file_name":
                        "weak.sql",
                    "source_path":
                        "data/raw/sql/weak.sql",
                    "content":
                        "General revenue note.",
                },
            ),
            SimpleNamespace(
                id="point-2",
                score=0.80,
                payload={
                    "file_name":
                        "strong.sql",
                    "source_path":
                        "data/raw/sql/strong.sql",
                    "content":
                        "Authoritative revenue "
                        "definition includes "
                        "chargebacks.",
                },
            ),
        ]

        return SimpleNamespace(
            points=points[:limit]
        )


class FakeCrossEncoder:

    def predict(
        self,
        pairs,
        **kwargs,
    ):
        scores = []

        for _, text in pairs:

            if (
                "Authoritative revenue"
                in text
            ):
                scores.append(0.99)
            else:
                scores.append(0.10)

        return scores


def test_retrieval_config():

    config = (
        load_retrieval_config(
            REPO_ROOT
        )
    )

    assert (
        config.candidate_top_k
        == 20
    )

    assert (
        config.final_top_k
        == 5
    )

    assert (
        config.reranker_model
        == (
            "cross-encoder/"
            "ms-marco-MiniLM-L6-v2"
        )
    )


def test_dense_retrieval():

    client = FakeQdrantClient()

    retriever = DenseRetriever(
        client=client,
        embedding_model=
            FakeEmbeddingModel(),
        collection_name="test",
    )

    candidates = retriever.retrieve(
        "revenue mismatch",
        top_k=2,
    )

    assert len(candidates) == 2
    assert candidates[0].dense_rank == 1
    assert candidates[1].dense_rank == 2
    assert candidates[0].dense_score == 0.95


def test_cross_encoder_changes_ranking():

    retriever = DenseRetriever(
        client=FakeQdrantClient(),
        embedding_model=
            FakeEmbeddingModel(),
        collection_name="test",
    )

    candidates = retriever.retrieve(
        "revenue mismatch",
        top_k=2,
    )

    reranker = (
        CrossEncoderReranker(
            model=FakeCrossEncoder()
        )
    )

    evidence = reranker.rerank(
        "revenue mismatch",
        candidates,
        top_k=2,
    )

    assert (
        evidence[0]
        .payload["file_name"]
        == "strong.sql"
    )

    assert (
        evidence[0].dense_rank
        == 2
    )

    assert (
        evidence[0].rerank_rank
        == 1
    )


def test_full_pipeline():

    dense = DenseRetriever(
        client=FakeQdrantClient(),
        embedding_model=
            FakeEmbeddingModel(),
        collection_name="test",
    )

    reranker = (
        CrossEncoderReranker(
            model=FakeCrossEncoder()
        )
    )

    pipeline = RetrievalPipeline(
        dense_retriever=dense,
        reranker=reranker,
        candidate_top_k=2,
        final_top_k=1,
    )

    evidence = pipeline.retrieve(
        "why revenue differs"
    )

    assert len(evidence) == 1

    assert (
        evidence[0]
        .payload["file_name"]
        == "strong.sql"
    )


def test_ground_truth_is_rejected():

    evidence = [
        RerankedEvidence(
            point_id="x",
            dense_score=0.8,
            rerank_score=0.9,
            payload={
                "source_path":
                    (
                        "data/ground_truth/"
                        "answers.json"
                    )
            },
            dense_rank=1,
            rerank_rank=1,
        )
    ]

    with pytest.raises(
        ValueError
    ):
        validate_final_evidence(
            evidence
        )


def test_final_evidence_format():

    evidence = [
        RerankedEvidence(
            point_id="x",
            dense_score=0.8,
            rerank_score=0.9,
            payload={
                "source_path":
                    "data/raw/a.sql",
                "file_name":
                    "a.sql",
                "asset_type":
                    "metric_sql",
                "metric_name":
                    "net_revenue",
                "content":
                    "Revenue evidence.",
            },
            dense_rank=4,
            rerank_rank=1,
        )
    ]

    formatted = (
        format_final_evidence(
            evidence
        )
    )

    assert (
        formatted[0][
            "evidence_rank"
        ]
        == 1
    )

    assert (
        formatted[0][
            "dense_rank"
        ]
        == 4
    )

    assert (
        formatted[0][
            "metric_name"
        ]
        == "net_revenue"
    )