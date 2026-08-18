from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from metricguard.rag.agentic_result import (
    AgenticRAGResult,
    build_agentic_rag_result,
)

from .cache import (
    AgenticResultCache,
)


@dataclass(
    slots=True,
    frozen=True,
)
class AgenticServiceConfig:
    minimum_confidence: float
    cache_enabled: bool
    cache_max_entries: int


def load_agentic_service_config(
    repo_root: Path,
) -> AgenticServiceConfig:

    path = (
        repo_root
        / "configs"
        / "settings.yaml"
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        settings = (
            yaml.safe_load(file)
            or {}
        )


    confidence = (
        settings.get(
            "confidence"
        )
        or {}
    )

    agentic = (
        settings.get(
            "agentic"
        )
        or {}
    )


    return AgenticServiceConfig(
        minimum_confidence=float(
            confidence.get(
                "minimum_threshold",
                0.60,
            )
        ),

        cache_enabled=bool(
            agentic.get(
                "cache_enabled",
                True,
            )
        ),

        cache_max_entries=int(
            agentic.get(
                "cache_max_entries",
                128,
            )
        ),
    )


class MetricGuardAgenticRAG:
    """
    Application-facing wrapper around the
    production LangGraph agent system.
    """

    def __init__(
        self,
        *,
        agent_system: Any,
        config: AgenticServiceConfig,
        cache: AgenticResultCache | None = None,
    ) -> None:

        self.agent_system = (
            agent_system
        )

        self.config = config

        if (
            config.cache_enabled
            and cache is None
        ):
            cache = (
                AgenticResultCache(
                    max_entries=
                        config
                        .cache_max_entries
                )
            )

        self.cache = cache


    def ask(
        self,
        question: str,
    ) -> AgenticRAGResult:

        question = (
            " ".join(
                question
                .strip()
                .split()
            )
        )

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )


        # -------------------------------------------------
        # CACHE
        # -------------------------------------------------

        if self.cache is not None:

            cached = self.cache.get(
                question
            )

            if cached is not None:
                return cached


        # -------------------------------------------------
        # AGENTIC WORKFLOW
        # -------------------------------------------------

        state = (
            self.agent_system
            .investigate(
                question
            )
        )


        # -------------------------------------------------
        # FINAL DETERMINISTIC ASSEMBLY
        # -------------------------------------------------

        result = (
            build_agentic_rag_result(
                question=
                    question,

                state=
                    state,

                minimum_confidence=
                    self.config
                    .minimum_confidence,
            )
        )


        # -------------------------------------------------
        # CACHE FINAL RESULT
        # -------------------------------------------------

        if self.cache is not None:

            self.cache.set(
                question,
                result,
            )


        return result