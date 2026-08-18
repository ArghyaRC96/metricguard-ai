from metricguard.agents import (
    EvidenceRetrievalAgent,
    MetricGuardAgentSystem,
    MetricInvestigationAgent,
    VerificationReportingAgent,
    build_metricguard_agent_graph,
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

    def retrieve(
        self,
        query,
    ):

        if self.empty:
            return []

        return [
            RerankedEvidence(
                point_id="1",
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


class FakeInvestigator:

    def __init__(
        self,
    ):
        self.calls = 0

    def investigate(
        self,
        **kwargs,
    ):

        self.calls += 1

        return {
            "diagnosis":
                "version_mismatch",

            "metric_name":
                "net_revenue",

            "hypothesis":
                (
                    "Executive uses "
                    "an older version."
                ),

            "findings": [
                "Observed v2 vs authoritative v3."
            ],

            "contradictions": [],

            "tool_observations": [
                "Version relation is non_current."
            ],

            "evidence_ids": [
                "E1"
            ],

            "confidence": 0.90,

            "revision_summary":
                (
                    "Revised using verifier feedback."
                    if kwargs.get(
                        "verification_feedback"
                    )
                    else None
                ),
        }


class FakeVerifier:

    def __init__(
        self,
        decisions,
    ):

        self.decisions = (
            list(decisions)
        )

        self.calls = 0

    def verify(
        self,
        **kwargs,
    ):

        index = min(
            self.calls,
            len(self.decisions) - 1,
        )

        decision = (
            self.decisions[index]
        )

        self.calls += 1

        return {
            "decision":
                decision,

            "diagnosis":
                "version_mismatch",

            "answer":
                (
                    "Executive uses an "
                    "older Net Revenue version."
                ),

            "key_findings": [
                "v2 differs from authoritative v3."
            ],

            "evidence_ids": [
                "E1"
            ],

            "confidence":
                (
                    0.95
                    if decision == "approved"
                    else 0.50
                ),

            "feedback":
                (
                    "Approved."
                    if decision == "approved"
                    else (
                        "Explain why the version "
                        "difference matters without "
                        "calling it a pipeline defect."
                    )
                ),

            "unsupported_claims": [],

            "missing_evidence": [],
        }


def build_system(
    *,
    decisions,
    empty=False,
    max_revisions=1,
):

    investigator = (
        FakeInvestigator()
    )

    verifier = (
        FakeVerifier(
            decisions
        )
    )

    evidence_agent = (
        EvidenceRetrievalAgent(
            retrieval_pipeline=
                FakeRetrievalPipeline(
                    empty=empty
                )
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
            verifier=verifier
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
            max_revisions=
                max_revisions,
        )
    )

    return (
        system,
        investigator,
        verifier,
    )


def test_approved_first_pass():

    system, investigator, verifier = (
        build_system(
            decisions=[
                "approved"
            ]
        )
    )

    result = system.investigate(
        "Why does revenue differ?"
    )

    assert (
        result[
            "verification_decision"
        ]
        == "approved"
    )

    assert (
        result[
            "revision_count"
        ]
        == 0
    )

    assert investigator.calls == 1
    assert verifier.calls == 1

    assert result["trace"] == [
        "evidence_retrieval_agent",
        "metric_investigation_agent",
        "verification_reporting_agent",
    ]


def test_revision_then_approval():

    system, investigator, verifier = (
        build_system(
            decisions=[
                "revise",
                "approved",
            ],
            max_revisions=1,
        )
    )

    result = system.investigate(
        "Why does revenue differ?"
    )

    assert (
        result[
            "verification_decision"
        ]
        == "approved"
    )

    assert (
        result[
            "revision_count"
        ]
        == 1
    )

    assert investigator.calls == 2
    assert verifier.calls == 2

    assert result["trace"] == [
        "evidence_retrieval_agent",
        "metric_investigation_agent",
        "verification_reporting_agent",
        "metric_investigation_agent",
        "verification_reporting_agent",
    ]


def test_revision_limit_fallback():

    system, investigator, verifier = (
        build_system(
            decisions=[
                "revise",
                "revise",
            ],
            max_revisions=1,
        )
    )

    result = system.investigate(
        "Why does revenue differ?"
    )

    assert (
        result[
            "verification_decision"
        ]
        == "insufficient_evidence"
    )

    assert (
        result[
            "revision_count"
        ]
        == 1
    )

    assert (
        result["trace"][-1]
        == "revision_limit_fallback"
    )


def test_no_evidence_skips_llm_agents():

    system, investigator, verifier = (
        build_system(
            decisions=[
                "approved"
            ],
            empty=True,
        )
    )

    result = system.investigate(
        "Unknown question"
    )

    assert (
        result[
            "verification_decision"
        ]
        == "insufficient_evidence"
    )

    assert investigator.calls == 0
    assert verifier.calls == 0

    assert result["trace"] == [
        "evidence_retrieval_agent",
        "no_evidence_fallback",
    ]