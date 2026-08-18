from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(
    slots=True,
    frozen=True,
)
class AgentConfig:
    max_revisions: int


def load_agent_config(
    repo_root: Path,
) -> AgentConfig:
    """Load MetricGuard agent orchestration settings."""

    path = (
        repo_root
        / "configs"
        / "settings.yaml"
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        settings = (
            yaml.safe_load(file)
            or {}
        )

    agentic = (
        settings.get("agentic")
        or {}
    )

    max_revisions = int(
        agentic.get(
            "max_revisions",
            1,
        )
    )

    if max_revisions < 0:
        raise ValueError(
            "max_revisions cannot "
            "be negative."
        )

    return AgentConfig(
        max_revisions=
            max_revisions
    )