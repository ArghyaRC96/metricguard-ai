from typing import Any


def validate_agent_evidence(
    evidence: list[dict[str, Any]],
) -> None:
    """Protect the production evidence boundary."""

    for item in evidence:

        source_path = str(
            item.get(
                "source_path",
                "",
            )
        )

        if (
            "ground_truth"
            in source_path
        ):
            raise ValueError(
                "Ground-truth leakage "
                "detected in agent evidence."
            )


def validate_agent_evidence_ids(
    evidence_ids: list[str],
    evidence: list[dict[str, Any]],
) -> None:
    """Ensure agent citations refer only to supplied evidence."""

    allowed = {
        f"E{index}"
        for index in range(
            1,
            len(evidence) + 1,
        )
    }

    invalid = (
        set(evidence_ids)
        - allowed
    )

    if invalid:
        raise ValueError(
            "Agent returned invalid "
            f"evidence IDs: "
            f"{sorted(invalid)}"
        )


def collect_version_observations(
    evidence: list[dict[str, Any]],
) -> list[str]:

    observations: list[str] = []

    for index, item in enumerate(
        evidence,
        start=1,
    ):

        metric = item.get(
            "metric_name"
        )

        if not metric:
            continue

        observed = item.get(
            "observed_version"
        )

        authoritative = item.get(
            "authoritative_version"
        )

        relation = item.get(
            "version_relation"
        )

        observations.append(
            (
                f"E{index}: metric={metric}; "
                f"observed_version={observed}; "
                f"authoritative_version="
                f"{authoritative}; "
                f"relation={relation}"
            )
        )

    return observations


def collect_freshness_observations(
    evidence: list[dict[str, Any]],
) -> list[str]:

    observations: list[str] = []

    for index, item in enumerate(
        evidence,
        start=1,
    ):

        status = item.get(
            "freshness_status"
        )

        if status is None:
            continue

        observations.append(
            (
                f"E{index}: "
                f"freshness_status="
                f"{status}"
            )
        )

    return observations


def collect_lineage_observations(
    evidence: list[dict[str, Any]],
) -> list[str]:

    observations: list[str] = []

    for index, item in enumerate(
        evidence,
        start=1,
    ):

        node = item.get(
            "lineage_node"
        )

        if not node:
            continue

        upstream = item.get(
            "direct_upstream",
            [],
        )

        downstream = item.get(
            "direct_downstream",
            [],
        )

        observations.append(
            (
                f"E{index}: "
                f"lineage_node={node}; "
                f"direct_upstream={upstream}; "
                f"direct_downstream={downstream}"
            )
        )

    return observations


def build_investigation_tool_context(
    evidence: list[dict[str, Any]],
) -> dict[str, list[str]]:
    """
    Run deterministic MetricGuard investigation tools.
    """

    validate_agent_evidence(
        evidence
    )

    return {
        "version_observations":
            collect_version_observations(
                evidence
            ),

        "freshness_observations":
            collect_freshness_observations(
                evidence
            ),

        "lineage_observations":
            collect_lineage_observations(
                evidence
            ),
    }