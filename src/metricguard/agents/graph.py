from typing import Literal

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from .fallbacks import (
    no_evidence_fallback,
    revision_limit_fallback,
)
from .state import (
    MetricGuardAgentState,
)


def route_after_retrieval(
    state: MetricGuardAgentState,
) -> Literal[
    "investigate",
    "no_evidence",
]:

    if state.get(
        "evidence"
    ):
        return "investigate"

    return "no_evidence"


def route_after_verification(
    state: MetricGuardAgentState,
) -> Literal[
    "end",
    "revise",
    "revision_limit",
]:

    decision = state.get(
        "verification_decision"
    )

    if decision in {
        "approved",
        "insufficient_evidence",
    }:
        return "end"

    if decision == "revise":

        revision_count = int(
            state.get(
                "revision_count",
                0,
            )
        )

        max_revisions = int(
            state.get(
                "max_revisions",
                1,
            )
        )

        if (
            revision_count
            >= max_revisions
        ):
            return "revision_limit"

        return "revise"

    return "revision_limit"


def build_metricguard_agent_graph(
    *,
    evidence_agent,
    investigation_agent,
    verification_agent,
):
    """
    Build MetricGuard's conditional three-agent workflow.
    """

    builder = StateGraph(
        MetricGuardAgentState
    )

    builder.add_node(
        "evidence_retrieval_agent",
        evidence_agent,
    )

    builder.add_node(
        "metric_investigation_agent",
        investigation_agent,
    )

    builder.add_node(
        "verification_reporting_agent",
        verification_agent,
    )

    builder.add_node(
        "no_evidence_fallback",
        no_evidence_fallback,
    )

    builder.add_node(
        "revision_limit_fallback",
        revision_limit_fallback,
    )

    builder.add_edge(
        START,
        "evidence_retrieval_agent",
    )

    builder.add_conditional_edges(
        "evidence_retrieval_agent",
        route_after_retrieval,
        {
            "investigate":
                "metric_investigation_agent",

            "no_evidence":
                "no_evidence_fallback",
        },
    )

    builder.add_edge(
        "metric_investigation_agent",
        "verification_reporting_agent",
    )

    builder.add_conditional_edges(
        "verification_reporting_agent",
        route_after_verification,
        {
            "end":
                END,

            "revise":
                "metric_investigation_agent",

            "revision_limit":
                "revision_limit_fallback",
        },
    )

    builder.add_edge(
        "no_evidence_fallback",
        END,
    )

    builder.add_edge(
        "revision_limit_fallback",
        END,
    )

    return builder.compile()