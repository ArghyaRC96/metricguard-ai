from typing import Any

from .state import (
    MetricGuardAgentState,
)


class MetricInvestigationAgent:
    """
    Agent 2 — investigate versions,
    freshness, semantics, lineage and impact.
    """

    def __init__(
        self,
        *,
        investigator: Any,
    ) -> None:

        self.investigator = (
            investigator
        )

    def __call__(
        self,
        state: MetricGuardAgentState,
    ) -> dict:

        feedback = state.get(
            "verification_feedback"
        )

        previous = state.get(
            "investigation"
        )

        revision_count = int(
            state.get(
                "revision_count",
                0,
            )
        )

        if feedback:
            revision_count += 1

        result = (
            self.investigator
            .investigate(
                question=
                    state["question"],
                evidence=
                    state.get(
                        "evidence",
                        [],
                    ),
                previous_investigation=
                    previous,
                verification_feedback=
                    feedback,
            )
        )

        if hasattr(
            result,
            "model_dump",
        ):
            investigation = (
                result.model_dump()
            )
        else:
            investigation = dict(
                result
            )

        trace = list(
            state.get(
                "trace",
                [],
            )
        )

        trace.append(
            "metric_investigation_agent"
        )

        return {
            "investigation":
                investigation,

            "investigation_complete":
                True,

            "verification_complete":
                False,

            "verification_feedback":
                None,

            "revision_count":
                revision_count,

            "trace":
                trace,
        }