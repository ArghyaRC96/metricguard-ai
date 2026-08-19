import json
from types import SimpleNamespace

import pytest

from metricguard.indexing import (
    build_qdrant_payload,
    index_fully_enriched_chunks,
    point_id_for_chunk,
)


class FakeEmbeddingModel:

    def encode(
        self,
        texts,
        **kwargs,
    ):

        return [
            [
                float(index + 1),
                0.5,
                0.25,
            ]
            for index, _
            in enumerate(texts)
        ]


class FakeQdrantClient:

    def __init__(
        self,
        *,
        existing: bool = False,
    ):

        self.existing = existing
        self.deleted = False
        self.created = None
        self.points = []


    def collection_exists(
        self,
        *,
        collection_name,
    ):

        return self.existing


    def delete_collection(
        self,
        *,
        collection_name,
    ):

        self.deleted = True
        self.existing = False

        return True


    def create_collection(
        self,
        *,
        collection_name,
        vectors_config,
    ):

        self.created = {
            "collection_name":
                collection_name,

            "vectors_config":
                vectors_config,
        }

        self.existing = True

        return True


    def upsert(
        self,
        *,
        collection_name,
        points,
        wait,
    ):

        self.points.extend(
            points
        )

        return SimpleNamespace(
            status="completed"
        )


    def count(
        self,
        *,
        collection_name,
        exact,
    ):

        return SimpleNamespace(
            count=
                len(
                    self.points
                )
        )


def write_test_repository(
    repo_root,
):

    config_dir = (
        repo_root
        / "configs"
    )

    processed_dir = (
        repo_root
        / "data"
        / "processed"
    )

    config_dir.mkdir(
        parents=True
    )

    processed_dir.mkdir(
        parents=True
    )


    (
        config_dir
        / "settings.yaml"
    ).write_text(
        """
retrieval:
  candidate_top_k: 20
  final_top_k: 5
  rerank_enabled: true
  reranker_model: fake-reranker

embeddings:
  model: fake-embedding
  normalize: true

vector_database:
  collection_name: metricguard_dense_v1
""".strip()
        + "\n",
        encoding="utf-8",
    )


    chunks = [
        {
            "chunk_id":
                "revenue-chunk-0001",

            "content":
                "Net Revenue uses version 2.",

            "metadata": {
                "metric_name":
                    "Net Revenue",

                "version_relation":
                    "current",
            },
        },
        {
            "chunk_id":
                "revenue-chunk-0002",

            "content":
                "Legacy dashboard uses version 1.",

            "metadata": {
                "metric_name":
                    "Net Revenue",

                "version_relation":
                    "non_current",
            },
        },
    ]


    chunks_path = (
        processed_dir
        / "fully_enriched_chunks.jsonl"
    )


    chunks_path.write_text(
        "\n".join(
            json.dumps(
                chunk
            )
            for chunk
            in chunks
        )
        + "\n",
        encoding="utf-8",
    )


def test_point_id_is_deterministic():

    first = (
        point_id_for_chunk(
            "chunk-123"
        )
    )

    second = (
        point_id_for_chunk(
            "chunk-123"
        )
    )

    assert first == second


def test_payload_preserves_governance_metadata():

    payload = (
        build_qdrant_payload(
            {
                "chunk_id":
                    "chunk-1",

                "content":
                    "Metric definition.",

                "metadata": {
                    "metric_name":
                        "Net Revenue",

                    "freshness_status":
                        "fresh",
                },
            }
        )
    )

    assert (
        payload[
            "metric_name"
        ]
        == "Net Revenue"
    )

    assert (
        payload[
            "freshness_status"
        ]
        == "fresh"
    )

    assert (
        payload[
            "metadata"
        ][
            "metric_name"
        ]
        == "Net Revenue"
    )


def test_index_builds_collection_and_upserts_chunks(
    tmp_path,
):

    write_test_repository(
        tmp_path
    )

    client = (
        FakeQdrantClient()
    )


    result = (
        index_fully_enriched_chunks(
            repo_root=
                tmp_path,

            qdrant_client=
                client,

            embedding_model=
                FakeEmbeddingModel(),

            batch_size=1,
        )
    )


    assert (
        result.collection_name
        == "metricguard_dense_v1"
    )

    assert (
        result.chunk_count
        == 2
    )

    assert (
        result.vector_size
        == 3
    )

    assert (
        client.created[
            "collection_name"
        ]
        == "metricguard_dense_v1"
    )

    assert len(
        client.points
    ) == 2

    assert (
        client.points[
            0
        ].payload[
            "content"
        ]
        == "Net Revenue uses version 2."
    )


def test_existing_collection_is_replaced(
    tmp_path,
):

    write_test_repository(
        tmp_path
    )

    client = (
        FakeQdrantClient(
            existing=True
        )
    )


    index_fully_enriched_chunks(
        repo_root=
            tmp_path,

        qdrant_client=
            client,

        embedding_model=
            FakeEmbeddingModel(),
    )


    assert (
        client.deleted
        is True
    )

    assert (
        client.created
        is not None
    )
