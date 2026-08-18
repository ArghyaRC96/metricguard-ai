from typing import Any

from .models import (
    RerankedEvidence,
    RetrievedCandidate,
)
from .text import (
    build_reranker_text,
)


class CrossEncoderReranker:
    """Mandatory second-stage evidence reranker."""

    def __init__(
        self,
        *,
        model: Any,
        batch_size: int = 16,
    ) -> None:

        self.model = model
        self.batch_size = batch_size

    def rerank(
        self,
        query: str,
        candidates: list[
            RetrievedCandidate
        ],
        *,
        top_k: int,
    ) -> list[RerankedEvidence]:

        if not candidates:
            return []

        if top_k <= 0:
            raise ValueError(
                "top_k must be positive."
            )

        pairs = [
            (
                query,
                build_reranker_text(
                    candidate
                ),
            )
            for candidate
            in candidates
        ]

        scores = self.model.predict(
            pairs,
            batch_size=self.batch_size,
            show_progress_bar=False,
        )

        reranked: list[
            RerankedEvidence
        ] = []

        for candidate, score in zip(
            candidates,
            scores,
        ):

            if hasattr(
                score,
                "item",
            ):
                score_value = float(
                    score.item()
                )
            else:
                score_value = float(
                    score
                )

            reranked.append(
                RerankedEvidence(
                    point_id=
                        candidate.point_id,
                    dense_score=
                        candidate.dense_score,
                    rerank_score=
                        score_value,
                    payload=
                        candidate.payload,
                    dense_rank=
                        candidate.dense_rank,
                    rerank_rank=0,
                )
            )

        reranked.sort(
            key=lambda evidence:
                evidence.rerank_score,
            reverse=True,
        )

        final = reranked[:top_k]

        for rank, evidence in enumerate(
            final,
            start=1,
        ):
            evidence.rerank_rank = (
                rank
            )

        return final