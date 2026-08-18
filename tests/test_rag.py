from metricguard.rag import (
    BaselineRAGAnswer,
    EvidenceUse,
    MetricGuardRAG,
)
from metricguard.retrieval import (
    RerankedEvidence,
)


class FakeRetrievalPipeline:

    def __init__(
        self,
        *,
        empty=False,
    ):

        self.empty = empty
        self.calls = 0

    def retrieve(
        self,
        query,
    ):

        self.calls += 1

        if self.empty:
            return []

        return [
            RerankedEvidence(
                point_id="point-1",
                dense_score=0.80,
                rerank_score=0.98,
                payload={
                    "source_path":
                        (
                            "data/raw/"
                            "dashboards/"
                            "executive_kpi_dashboard.json"
                        ),
                    "file_name":
                        "executive_kpi_dashboard.json",
                    "asset_type":
                        "dashboard",
                    "metric_name":
                        "net_revenue",
                    "observed_version":
                        "v2",
                    "authoritative_version":
                        "v3",
                    "version_relation":
                        "non_current",
                    "freshness_status":
                        "stale",
                    "lineage_node":
                        "Executive KPI Dashboard",
                    "direct_upstream":
                        [
                            "mart_executive_daily"
                        ],
                    "all_upstream":
                        [
                            "fct_orders"
                        ],
                    "direct_downstream":
                        [],
                    "all_downstream":
                        [],
                    "content":
                        (
                            "Executive dashboard "
                            "uses Net Revenue v2."
                        ),
                },
                dense_rank=2,
                rerank_rank=1,
            )
        ]


class FakeLLM:

    def __init__(
        self,
        *,
        confidence=0.90,
        evidence_id="E1",
    ):

        self.confidence = (
            confidence
        )

        self.evidence_id = (
            evidence_id
        )

        self.calls = 0

    def generate(
        self,
        *,
        prompt,
        response_schema,
    ):

        self.calls += 1

        return BaselineRAGAnswer(
            status="answered",
            diagnosis=
                "version_mismatch",
            metric_name=
                "net_revenue",
            answer=(
                "The Executive dashboard "
                "uses an older definition."
            ),
            key_findings=[
                (
                    "Executive uses "
                    "Net Revenue v2."
                )
            ],
            evidence_used=[
                EvidenceUse(
                    evidence_id=
                        self.evidence_id,
                    supports=(
                        "Shows the older "
                        "dashboard version."
                    ),
                )
            ],
            confidence=
                self.confidence,
            confidence_reason=
                "Evidence is consistent.",
            missing_evidence=[],
        )


def test_rag_answered():

    retrieval = (
        FakeRetrievalPipeline()
    )

    llm = FakeLLM()

    rag = MetricGuardRAG(
        retrieval_pipeline=
            retrieval,
        llm=llm,
        minimum_confidence=0.60,
    )

    result = rag.ask(
        "Why does revenue differ?"
    )

    assert (
        result.answer.status
        == "answered"
    )

    assert (
        result.fallback_triggered
        is False
    )

    assert (
        result.sources[0]
        .evidence_id
        == "E1"
    )


def test_low_confidence_fallback():

    rag = MetricGuardRAG(
        retrieval_pipeline=
            FakeRetrievalPipeline(),
        llm=FakeLLM(
            confidence=0.40
        ),
        minimum_confidence=0.60,
    )

    result = rag.ask(
        "Why does revenue differ?"
    )

    assert (
        result.fallback_triggered
        is True
    )


def test_invalid_evidence_id_rejected():

    rag = MetricGuardRAG(
        retrieval_pipeline=
            FakeRetrievalPipeline(),
        llm=FakeLLM(
            evidence_id="E99"
        ),
    )

    try:

        rag.ask(
            "Why does revenue differ?"
        )

    except ValueError:
        return

    raise AssertionError(
        "Invalid evidence ID "
        "should be rejected."
    )


def test_empty_retrieval_skips_llm():

    retrieval = (
        FakeRetrievalPipeline(
            empty=True
        )
    )

    llm = FakeLLM()

    rag = MetricGuardRAG(
        retrieval_pipeline=
            retrieval,
        llm=llm,
    )

    result = rag.ask(
        "Unsupported question"
    )

    assert (
        result.answer.status
        == "insufficient_evidence"
    )

    assert (
        result.fallback_triggered
        is True
    )

    assert llm.calls == 0


def test_cache_avoids_second_llm_call():

    retrieval = (
        FakeRetrievalPipeline()
    )

    llm = FakeLLM()

    rag = MetricGuardRAG(
        retrieval_pipeline=
            retrieval,
        llm=llm,
        cache_enabled=True,
    )

    first = rag.ask(
        "Why does revenue differ?"
    )

    second = rag.ask(
        "Why does revenue differ?"
    )

    assert (
        first.cache_hit
        is False
    )

    assert (
        second.cache_hit
        is True
    )

    assert llm.calls == 1

    assert retrieval.calls == 1