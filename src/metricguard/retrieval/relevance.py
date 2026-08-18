from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(
    slots=True,
    frozen=True,
)
class RelevanceConfig:
    enabled: bool
    top1_rerank_threshold: float


@dataclass(
    slots=True,
    frozen=True,
)
class RelevanceDecision:
    is_relevant: bool
    top1_rerank_score: float | None
    threshold: float
    reason: str


def load_relevance_config(
    repo_root: Path,
) -> RelevanceConfig:
    """
    Load the calibrated retrieval relevance gate.
    """

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

    relevance = (
        settings.get("relevance")
        or {}
    )

    enabled = bool(
        relevance.get(
            "enabled",
            True,
        )
    )

    threshold = float(
        relevance.get(
            "top1_rerank_threshold",
            0.27,
        )
    )

    return RelevanceConfig(
        enabled=enabled,
        top1_rerank_threshold=
            threshold,
    )


class RelevanceGate:
    """
    Reject retrieval results whose best reranked
    candidate does not meet the calibrated threshold.
    """

    def __init__(
        self,
        *,
        threshold: float,
        enabled: bool = True,
    ) -> None:

        self.threshold = float(
            threshold
        )

        self.enabled = bool(
            enabled
        )

    def assess(
        self,
        candidates: list[Any],
    ) -> RelevanceDecision:

        if not candidates:

            return RelevanceDecision(
                is_relevant=False,
                top1_rerank_score=None,
                threshold=self.threshold,
                reason=(
                    "No retrieval candidates "
                    "were returned."
                ),
            )

        scores = [
            float(
                candidate.rerank_score
            )
            for candidate in candidates
        ]

        top1_score = max(
            scores
        )

        if not self.enabled:

            return RelevanceDecision(
                is_relevant=True,
                top1_rerank_score=
                    top1_score,
                threshold=
                    self.threshold,
                reason=(
                    "Relevance gate is disabled."
                ),
            )

        is_relevant = (
            top1_score
            >= self.threshold
        )

        if is_relevant:

            reason = (
                "Top reranked candidate "
                "passed the calibrated "
                "relevance threshold."
            )

        else:

            reason = (
                "Top reranked candidate "
                "did not pass the calibrated "
                "relevance threshold."
            )

        return RelevanceDecision(
            is_relevant=is_relevant,
            top1_rerank_score=
                top1_score,
            threshold=
                self.threshold,
            reason=
                reason,
        )