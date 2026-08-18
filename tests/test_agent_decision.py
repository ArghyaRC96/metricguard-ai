from metricguard.agents import (
    normalize_verification_report,
)


def test_approved_insufficient_evidence_is_normalized():

    report = {
        "decision":
            "approved",

        "diagnosis":
            "insufficient_evidence",

        "answer":
            "There is insufficient evidence.",

        "confidence":
            1.0,
    }

    normalized = (
        normalize_verification_report(
            report
        )
    )

    assert (
        normalized["decision"]
        == "insufficient_evidence"
    )

    assert (
        normalized["diagnosis"]
        == "insufficient_evidence"
    )


def test_normal_approved_answer_remains_approved():

    report = {
        "decision":
            "approved",

        "diagnosis":
            "version_mismatch",

        "answer":
            "The definitions differ.",

        "confidence":
            0.95,
    }

    normalized = (
        normalize_verification_report(
            report
        )
    )

    assert (
        normalized["decision"]
        == "approved"
    )

    assert (
        normalized["diagnosis"]
        == "version_mismatch"
    )


def test_explicit_insufficient_evidence_remains_insufficient():

    report = {
        "decision":
            "insufficient_evidence",

        "diagnosis":
            "insufficient_evidence",

        "answer":
            "Evidence is insufficient.",

        "confidence":
            0.20,
    }

    normalized = (
        normalize_verification_report(
            report
        )
    )

    assert (
        normalized["decision"]
        == "insufficient_evidence"
    )