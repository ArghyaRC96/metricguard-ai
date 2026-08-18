from copy import deepcopy
from typing import Any


def normalize_verification_report(
    report: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize verification semantics before
    LangGraph routing consumes the decision.

    The verifier may semantically "approve"
    an Agent 2 conclusion that evidence is
    insufficient. At application level, that
    must become an insufficient-evidence exit.
    """

    normalized = deepcopy(
        report
    )

    decision = str(
        normalized.get(
            "decision",
            "",
        )
    )

    diagnosis = str(
        normalized.get(
            "diagnosis",
            "",
        )
    )

    if (
        decision == "insufficient_evidence"
        or diagnosis == "insufficient_evidence"
    ):
        normalized[
            "decision"
        ] = "insufficient_evidence"

        normalized[
            "diagnosis"
        ] = "insufficient_evidence"

    return normalized