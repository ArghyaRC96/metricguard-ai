from metricguard.agents import (
    InvestigationResult,
    MetricInvestigator,
    VerificationReporter,
    VerificationResult,
)


EVIDENCE = [
    {
        "source_path":
            "data/raw/dashboard.json",
        "file_name":
            "dashboard.json",
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
            ["mart_executive_daily"],
        "direct_downstream":
            [],
        "content":
            "Executive uses Net Revenue v2.",
    }
]


class FakeStructuredLLM:

    def __init__(
        self,
    ):
        self.last_prompt = None

    def generate(
        self,
        *,
        prompt,
        response_schema,
    ):

        self.last_prompt = prompt

        if (
            response_schema
            is InvestigationResult
        ):

            return InvestigationResult(
                diagnosis=
                    "version_mismatch",
                metric_name=
                    "net_revenue",
                hypothesis=
                    "Executive uses v2.",
                findings=[
                    "Observed v2 differs from v3."
                ],
                contradictions=[],
                tool_observations=[
                    "Version relation is non_current."
                ],
                evidence_ids=[
                    "E1"
                ],
                confidence=0.90,
            )

        if (
            response_schema
            is VerificationResult
        ):

            return VerificationResult(
                decision=
                    "approved",
                diagnosis=
                    "version_mismatch",
                answer=
                    (
                        "The dashboard uses "
                        "an older metric version."
                    ),
                key_findings=[
                    "v2 differs from v3."
                ],
                evidence_ids=[
                    "E1"
                ],
                confidence=0.95,
                feedback=
                    "Evidence supports the conclusion.",
                unsupported_claims=[],
                missing_evidence=[],
            )

        raise AssertionError(
            "Unexpected schema."
        )


def test_metric_investigator():

    llm = FakeStructuredLLM()

    investigator = (
        MetricInvestigator(
            llm=llm
        )
    )

    result = investigator.investigate(
        question=
            "Why does revenue differ?",
        evidence=EVIDENCE,
    )

    assert (
        result.diagnosis
        == "version_mismatch"
    )

    assert (
        result.evidence_ids
        == ["E1"]
    )

    assert (
        "DETERMINISTIC TOOL OBSERVATIONS"
        in llm.last_prompt
    )


def test_verification_reporter():

    llm = FakeStructuredLLM()

    verifier = (
        VerificationReporter(
            llm=llm
        )
    )

    investigation = {
        "diagnosis":
            "version_mismatch",
        "metric_name":
            "net_revenue",
        "hypothesis":
            "Executive uses v2.",
        "findings": [
            "v2 differs from v3."
        ],
        "evidence_ids": [
            "E1"
        ],
    }

    result = verifier.verify(
        question=
            "Why does revenue differ?",
        evidence=EVIDENCE,
        investigation=
            investigation,
    )

    assert (
        result.decision
        == "approved"
    )

    assert (
        result.evidence_ids
        == ["E1"]
    )