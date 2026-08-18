from .state import (
    MetricGuardAgentState,
)


def no_evidence_fallback(
    state: MetricGuardAgentState,
) -> dict:

    trace = list(
        state.get(
            "trace",
            [],
        )
    )

    trace.append(
        "no_evidence_fallback"
    )

    return {
        "final_report": {
            "decision":
                "insufficient_evidence",

            "diagnosis":
                "insufficient_evidence",

            "answer":
                (
                    "MetricGuard could not "
                    "retrieve sufficient "
                    "evidence to investigate "
                    "this question reliably."
                ),

            "key_findings": [],

            "evidence_ids": [],

            "confidence": 0.0,

            "feedback":
                "No retrieval evidence.",

            "unsupported_claims": [],

            "missing_evidence": [
                "Relevant source evidence"
            ],
        },

        "verification_decision":
            "insufficient_evidence",

        "verification_complete":
            True,

        "trace":
            trace,
    }


def revision_limit_fallback(
    state: MetricGuardAgentState,
) -> dict:

    trace = list(
        state.get(
            "trace",
            [],
        )
    )

    trace.append(
        "revision_limit_fallback"
    )

    previous_report = (
        state.get(
            "final_report",
            {}
        )
    )

    return {
        "final_report": {
            "decision":
                "insufficient_evidence",

            "diagnosis":
                "insufficient_evidence",

            "answer":
                (
                    "MetricGuard could not "
                    "produce a sufficiently "
                    "verified conclusion "
                    "within the allowed "
                    "revision limit."
                ),

            "key_findings":
                previous_report.get(
                    "key_findings",
                    [],
                ),

            "evidence_ids":
                previous_report.get(
                    "evidence_ids",
                    [],
                ),

            "confidence":
                min(
                    float(
                        previous_report.get(
                            "confidence",
                            0.0,
                        )
                    ),
                    0.49,
                ),

            "feedback":
                (
                    "Verification continued "
                    "to require revision "
                    "after the configured "
                    "revision limit."
                ),

            "unsupported_claims":
                previous_report.get(
                    "unsupported_claims",
                    [],
                ),

            "missing_evidence":
                previous_report.get(
                    "missing_evidence",
                    [],
                ),
        },

        "verification_decision":
            "insufficient_evidence",

        "verification_complete":
            True,

        "trace":
            trace,
    }