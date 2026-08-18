from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(
    slots=True,
    frozen=True,
)
class LLMConfig:
    provider: str
    model: str
    thinking_level: str
    structured_output: bool


def load_llm_config(
    repo_root: Path,
) -> LLMConfig:
    """Load the production LLM configuration."""

    config_path = (
        repo_root
        / "configs"
        / "settings.yaml"
    )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        settings = (
            yaml.safe_load(file)
            or {}
        )

    llm = (
        settings.get("llm")
        or {}
    )

    provider = str(
        llm.get(
            "provider",
            "",
        )
    ).strip()

    model = str(
        llm.get(
            "model",
            "",
        )
    ).strip()

    thinking_level = str(
        llm.get(
            "thinking_level",
            "medium",
        )
    ).strip()

    structured_output = bool(
        llm.get(
            "structured_output",
            False,
        )
    )

    if not provider:
        raise ValueError(
            "llm.provider is required."
        )

    if not model:
        raise ValueError(
            "llm.model is required."
        )

    if not structured_output:
        raise ValueError(
            "MetricGuard requires "
            "structured LLM output."
        )

    return LLMConfig(
        provider=provider,
        model=model,
        thinking_level=
            thinking_level,
        structured_output=
            structured_output,
    )