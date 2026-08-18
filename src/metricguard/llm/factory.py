from pathlib import Path
from typing import Any

from .config import (
    load_llm_config,
)
from .gemini import (
    GeminiStructuredLLM,
)


def create_gemini_client(
    *,
    api_key: str | None = None,
) -> Any:
    """
    Lazily construct Google's Gemini client.
    """

    from google import genai

    if api_key:
        return genai.Client(
            api_key=api_key
        )

    return genai.Client()


def build_structured_llm(
    *,
    repo_root: Path,
    client: Any | None = None,
    api_key: str | None = None,
    minimum_request_interval_seconds:
        float = 0.0,
):
    """
    Build the configured MetricGuard LLM provider.
    """

    config = load_llm_config(
        repo_root
    )

    if config.provider == "gemini":

        if client is None:
            client = (
                create_gemini_client(
                    api_key=api_key
                )
            )

        return GeminiStructuredLLM(
            client=client,
            model=config.model,
            thinking_level=
                config.thinking_level,
            minimum_request_interval_seconds=
                minimum_request_interval_seconds,
        )

    raise NotImplementedError(
        "Unsupported MetricGuard "
        f"LLM provider: {config.provider}"
    )