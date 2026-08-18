from metricguard.rag.agentic_result import (
    build_agentic_rag_result,
)


def test_approved_result_resolves_sources():

    state = {
        "verification_decision":
            "approved",

        "retrieval_relevant":
            True,

        "retrieval_top1_score":
            0.75,

        "revision_count":
            0,

        "trace": [
            "evidence_retrieval_agent",
            "metric_investigation_agent",
            "verification_reporting_agent",
        ],

        "evidence": [
            {
                "source_path":
                    "data/raw/rules/net_revenue.md",

                "file_name":
                    "net_revenue.md",

                "metric_name":
                    "net_revenue",
            }
        ],

        "final_report": {
            "decision":
                "approved",

            "diagnosis":
                "metric_migration",

            "answer":
                "Finance migrated to v3.",

            "key_findings": [
                "Finance uses v3."
            ],

            "evidence_ids": [
                "E1"
            ],

            "confidence":
                0.95,
        },
    }


    result = build_agentic_rag_result(
        question=
            "Why do revenues differ?",

        state=
            state,

        minimum_confidence=
            0.60,
    )


    assert result.status == "answered"
    assert result.decision == "approved"

    assert (
        result.sources[0]
        .evidence_id
        == "E1"
    )

    assert (
        result.sources[0]
        .source_path
        == "data/raw/rules/net_revenue.md"
    )


def test_low_confidence_forces_fallback():

    state = {
        "verification_decision":
            "approved",

        "retrieval_relevant":
            True,

        "evidence": [],

        "final_report": {
            "decision":
                "approved",

            "diagnosis":
                "version_mismatch",

            "answer":
                "Possible mismatch.",

            "evidence_ids": [],

            "confidence":
                0.40,
        },
    }


    result = build_agentic_rag_result(
        question=
            "Why do they differ?",

        state=
            state,

        minimum_confidence=
            0.60,
    )


    assert (
        result.status
        == "insufficient_evidence"
    )

    assert (
        result.decision
        == "insufficient_evidence"
    )

    assert (
        result.diagnosis
        == "insufficient_evidence"
    )

    assert (
        result.fallback_reason
        is not None
    )


def test_irrelevant_retrieval_forces_fallback():

    state = {
        "verification_decision":
            "insufficient_evidence",

        "retrieval_relevant":
            False,

        "retrieval_top1_score":
            0.01,

        "evidence": [],

        "final_report": {
            "decision":
                "insufficient_evidence",

            "diagnosis":
                "insufficient_evidence",

            "answer":
                "No relevant evidence.",

            "evidence_ids": [],

            "confidence":
                0.0,
        },
    }


    result = build_agentic_rag_result(
        question=
            "How much electricity?",

        state=
            state,

        minimum_confidence=
            0.60,
    )


    assert (
        result.status
        == "insufficient_evidence"
    )

    assert (
        result.retrieval_relevant
        is False
    )