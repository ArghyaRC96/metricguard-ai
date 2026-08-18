from typing import Any

from metricguard.retrieval import (
    format_final_evidence,
)

from .cache import (
    InMemoryRAGCache,
)
from .evidence import (
    resolve_sources,
    validate_evidence_ids,
)
from .prompt import (
    build_rag_prompt,
)
from .schemas import (
    BaselineRAGAnswer,
    RAGResult,
)


class MetricGuardRAG:
    """Production baseline MetricGuard RAG orchestration."""

    def __init__(
        self,
        *,
        retrieval_pipeline: Any,
        llm: Any,
        minimum_confidence: float = 0.60,
        cache_enabled: bool = True,
    ) -> None:

        if not (
            0.0
            <= minimum_confidence
            <= 1.0
        ):
            raise ValueError(
                "minimum_confidence "
                "must be between 0 and 1."
            )

        self.retrieval_pipeline = (
            retrieval_pipeline
        )

        self.llm = llm

        self.minimum_confidence = (
            minimum_confidence
        )

        self.cache = (
            InMemoryRAGCache()
            if cache_enabled
            else None
        )

    def _insufficient_evidence_result(
        self,
        *,
        question: str,
        reason: str,
    ) -> RAGResult:

        answer = BaselineRAGAnswer(
            status=
                "insufficient_evidence",
            diagnosis=
                "insufficient_evidence",
            metric_name=None,
            answer=(
                "MetricGuard does not "
                "have sufficient evidence "
                "to answer this question."
            ),
            key_findings=[],
            evidence_used=[],
            confidence=0.0,
            confidence_reason=
                reason,
            missing_evidence=[
                reason
            ],
        )

        return RAGResult(
            question=question,
            answer=answer,
            sources=[],
            evidence=[],
            fallback_triggered=True,
            display_answer=(
                "MetricGuard does not "
                "have enough reliable "
                "evidence to answer this "
                "question with the required "
                "confidence."
            ),
            cache_hit=False,
        )

    def ask(
        self,
        question: str,
    ) -> RAGResult:

        question = (
            question.strip()
        )

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        if self.cache is not None:

            cached = (
                self.cache.get(
                    question
                )
            )

            if cached is not None:

                return cached.model_copy(
                    update={
                        "cache_hit": True
                    }
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

        if not evidence:

            result = (
                self
                ._insufficient_evidence_result(
                    question=question,
                    reason=(
                        "No retrieval evidence "
                        "was available."
                    ),
                )
            )

            if self.cache is not None:
                self.cache.set(
                    question,
                    result,
                )

            return result

        prompt = build_rag_prompt(
            question=question,
            evidence=evidence,
        )

        answer = self.llm.generate(
            prompt=prompt,
            response_schema=
                BaselineRAGAnswer,
        )

        validate_evidence_ids(
            answer,
            evidence,
        )

        sources = resolve_sources(
            answer,
            evidence,
        )

        fallback_triggered = (
            answer.status
            == "insufficient_evidence"
            or answer.confidence
            < self.minimum_confidence
        )

        if fallback_triggered:

            display_answer = (
                "MetricGuard does not "
                "have enough reliable "
                "evidence to answer this "
                "question with the required "
                "confidence."
            )

        else:

            display_answer = (
                answer.answer
            )

        result = RAGResult(
            question=question,
            answer=answer,
            sources=sources,
            evidence=evidence,
            fallback_triggered=
                fallback_triggered,
            display_answer=
                display_answer,
            cache_hit=False,
        )

        if self.cache is not None:

            self.cache.set(
                question,
                result,
            )

        return result