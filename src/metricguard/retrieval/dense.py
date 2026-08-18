from typing import Any

from .models import RetrievedCandidate


class DenseRetriever:
    """First-stage dense Qdrant retriever."""

    def __init__(
        self,
        *,
        client: Any,
        embedding_model: Any,
        collection_name: str,
        normalize_embeddings: bool = True,
    ) -> None:

        self.client = client
        self.embedding_model = (
            embedding_model
        )
        self.collection_name = (
            collection_name
        )
        self.normalize_embeddings = (
            normalize_embeddings
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        vector = (
            self.embedding_model.encode(
                query,
                normalize_embeddings=
                    self.normalize_embeddings,
                convert_to_numpy=True,
            )
        )

        if hasattr(
            vector,
            "tolist",
        ):
            return vector.tolist()

        return list(vector)

    def retrieve(
        self,
        query: str,
        *,
        top_k: int,
        query_filter: Any = None,
    ) -> list[RetrievedCandidate]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be positive."
            )

        response = (
            self.client.query_points(
                collection_name=
                    self.collection_name,
                query=self.embed_query(
                    query
                ),
                query_filter=
                    query_filter,
                limit=top_k,
                with_payload=True,
            )
        )

        candidates: list[
            RetrievedCandidate
        ] = []

        for rank, point in enumerate(
            response.points,
            start=1,
        ):

            candidates.append(
                RetrievedCandidate(
                    point_id=str(
                        point.id
                    ),
                    dense_score=float(
                        point.score
                    ),
                    payload=dict(
                        point.payload
                        or {}
                    ),
                    dense_rank=rank,
                )
            )

        return candidates