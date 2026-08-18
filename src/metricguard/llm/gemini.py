import time
from typing import Any, TypeVar

from pydantic import BaseModel


T = TypeVar(
    "T",
    bound=BaseModel,
)


class GeminiStructuredLLM:
    """
    Google Gemini adapter for structured MetricGuard generation.
    """

    def __init__(
        self,
        *,
        client: Any,
        model: str,
        thinking_level: str = "medium",
        minimum_request_interval_seconds: float = 0.0,
    ) -> None:

        self.client = client
        self.model = model
        self.thinking_level = (
            thinking_level
        )

        self.minimum_request_interval_seconds = (
            max(
                0.0,
                float(
                    minimum_request_interval_seconds
                ),
            )
        )

        self._last_request_time = 0.0

    def _wait_for_request_slot(
        self,
    ) -> None:

        if (
            self.minimum_request_interval_seconds
            <= 0
        ):
            return

        elapsed = (
            time.monotonic()
            - self._last_request_time
        )

        wait_time = max(
            0.0,
            (
                self.minimum_request_interval_seconds
                - elapsed
            ),
        )

        if wait_time > 0:
            time.sleep(
                wait_time
            )

    def generate(
        self,
        *,
        prompt: str,
        response_schema: type[T],
    ) -> T:

        if not prompt.strip():
            raise ValueError(
                "LLM prompt cannot be empty."
            )

        self._wait_for_request_slot()

        interaction = (
            self.client
            .interactions
            .create(
                model=self.model,
                input=prompt,
                generation_config={
                    "thinking_level":
                        self.thinking_level,
                },
                response_format={
                    "type": "text",
                    "mime_type":
                        "application/json",
                    "schema":
                        response_schema
                        .model_json_schema(),
                },
            )
        )

        self._last_request_time = (
            time.monotonic()
        )

        output_text = getattr(
            interaction,
            "output_text",
            None,
        )

        if not output_text:
            raise ValueError(
                "Gemini returned no "
                "structured output text."
            )

        return (
            response_schema
            .model_validate_json(
                output_text
            )
        )