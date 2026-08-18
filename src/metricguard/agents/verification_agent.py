from typing import Any

from .decision import (
    normalize_verification_report,
)
from .state import (
    MetricGuardAgentState,
)


class VerificationReportingAgent:
    """
    Agent 3 - independently verify Agent 2
    and produce the final report.
    """

    def __init__(
        self,
        *,
        verifier: Any,
    ) -> None:

        self.verifier = verifier

    def __call__(
        self,
        state: MetricGuardAgentState,
    ) -> dict:

        result = (
            self.verifier
            .verify(
                question=
                    state["question"],
                evidence=
                    state.get(
                        "evidence",
                        [],
                    ),
                investigation=
                    state.get(
                        "investigation",
                        {},
                    ),
            )
        )

        if hasattr(
            result,
            "model_dump",
        ):
            final_report = (
                result.model_dump()
            )

        else:
            final_report = dict(
                result
            )

        final_report = (
            normalize_verification_report(
                final_report
            )
        )

        decision = str(
            final_report.get(
                "decision",
                "",
            )
        )

        feedback = (
            final_report.get(
                "feedback"
            )
        )

        trace = list(
            state.get(
                "trace",
                [],
            )
        )

        trace.append(
            "verification_reporting_agent"
        )

        return {
            "final_report":
                final_report,

            "verification_decision":
                decision,

            "verification_feedback":
                feedback,

            "verification_complete":
                True,

            "trace":
                trace,
        }