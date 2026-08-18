from metricguard.agents import (
    EvidenceRetrievalAgent,
    MetricGuardAgentSystem,
    MetricInvestigationAgent,
    VerificationReportingAgent,
    build_metricguard_agent_graph,
)

from metricguard.retrieval import (
    RelevanceGate,
    RerankedEvidence,
)


class WeakRetrievalPipeline:

    def retrieve(
        self,
        query,
    ):

        return [
            RerankedEvidence(
                point_id="weak-1",
                dense_score=0.20,
                rerank_score=0.012,
                payload={
                    "source_path":
                        "data/raw/unrelated.json",
                    "content":
                        "Unrelated content.",
                },
                dense_rank=1,
                rerank_rank=1,
            )
        ]


class CountingInvestigator:

    def __init__(
        self,
    ):
        self.calls = 0

    def investigate(
        self,
        **kwargs,
    ):

        self.calls += 1

        raise AssertionError(
            "Investigator must not run."
        )


class CountingVerifier:

    def __init__(
        self,
    ):
        self.calls = 0

    def verify(
        self,
        **kwargs,
    ):

        self.calls += 1

        raise AssertionError(
            "Verifier must not run."
        )


def test_weak_retrieval_skips_llm_agents():

    investigator = (
        CountingInvestigator()
    )

    verifier = (
        CountingVerifier()
    )

    evidence_agent = (
        EvidenceRetrievalAgent(
            retrieval_pipeline=
                WeakRetrievalPipeline(),

            relevance_gate=
                RelevanceGate(
                    threshold=0.27
                ),
        )
    )

    investigation_agent = (
        MetricInvestigationAgent(
            investigator=
                investigator
        )
    )

    verification_agent = (
        VerificationReportingAgent(
            verifier=
                verifier
        )
    )

    graph = (
        build_metricguard_agent_graph(
            evidence_agent=
                evidence_agent,

            investigation_agent=
                investigation_agent,

            verification_agent=
                verification_agent,
        )
    )

    system = (
        MetricGuardAgentSystem(
            graph=graph,
            max_revisions=1,
        )
    )

    result = system.investigate(
        "How much electricity did "
        "the warehouse HVAC consume?"
    )

    assert (
        result[
            "verification_decision"
        ]
        == "insufficient_evidence"
    )

    assert (
        result[
            "retrieval_relevant"
        ]
        is False
    )

    assert investigator.calls == 0
    assert verifier.calls == 0

    assert result["trace"] == [
        "evidence_retrieval_agent",
        "relevance_gate_rejected",
        "no_evidence_fallback",
    ]