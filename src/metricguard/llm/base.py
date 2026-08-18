from typing import Protocol, TypeVar

from pydantic import BaseModel


T = TypeVar(
    "T",
    bound=BaseModel,
)


class StructuredLLM(Protocol):
    """
    Provider-independent interface for structured LLM generation.
    """

    def generate(
        self,
        *,
        prompt: str,
        response_schema: type[T],
    ) -> T:
        ...