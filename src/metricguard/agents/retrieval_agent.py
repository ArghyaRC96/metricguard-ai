from typing import Any

from metricguard.retrieval import (
    format_final_evidence,
)

from .state import (
    MetricGuardAgentState,
)


class EvidenceRetrievalAgent:
    """Agent 1 — retrieve and prepare grounded evidence."""

    def __init__(
        self,
        *,
        retrieval_pipeline: Any,
    ) -> None:

        self.retrieval_pipeline = (
            retrieval_pipeline
        )

    def __call__(
        self,
        state: MetricGuardAgentState,
    ) -> dict:

        question = (
            state["question"]
        )

        retrieval_results = (
            self.retrieval_pipeline
            .retrieve(
                question
            )
        )

        evidence = (
            format_final_evidence(
                retrieval_results
            )
        )

        trace = list(
            state.get(
                "trace",
                [],
            )
        )

        trace.append(
            "evidence_retrieval_agent"
        )

        return {
            "evidence":
                evidence,
            "retrieval_complete":
                True,
            "trace":
                trace,
        }