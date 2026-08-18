from typing import Any

from metricguard.retrieval import (
    format_final_evidence,
)

from .state import (
    MetricGuardAgentState,
)


class EvidenceRetrievalAgent:
    """
    Agent 1 - retrieve, rerank and relevance-check
    evidence before LLM investigation.
    """

    def __init__(
        self,
        *,
        retrieval_pipeline: Any,
        relevance_gate: Any | None = None,
    ) -> None:

        self.retrieval_pipeline = (
            retrieval_pipeline
        )

        self.relevance_gate = (
            relevance_gate
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

        trace = list(
            state.get(
                "trace",
                [],
            )
        )

        trace.append(
            "evidence_retrieval_agent"
        )

        if (
            self.relevance_gate
            is not None
        ):

            relevance = (
                self.relevance_gate
                .assess(
                    retrieval_results
                )
            )

            if not relevance.is_relevant:

                trace.append(
                    "relevance_gate_rejected"
                )

                return {
                    "evidence": [],

                    "retrieval_complete":
                        True,

                    "retrieval_relevant":
                        False,

                    "retrieval_top1_score":
                        relevance
                        .top1_rerank_score,

                    "retrieval_relevance_reason":
                        relevance.reason,

                    "trace":
                        trace,
                }

            relevance_score = (
                relevance
                .top1_rerank_score
            )

            relevance_reason = (
                relevance.reason
            )

        else:

            relevance_score = None

            relevance_reason = (
                "No relevance gate configured."
            )

        evidence = (
            format_final_evidence(
                retrieval_results
            )
        )

        return {
            "evidence":
                evidence,

            "retrieval_complete":
                True,

            "retrieval_relevant":
                True,

            "retrieval_top1_score":
                relevance_score,

            "retrieval_relevance_reason":
                relevance_reason,

            "trace":
                trace,
        }