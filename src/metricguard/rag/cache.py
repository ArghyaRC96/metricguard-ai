from .schemas import (
    RAGResult,
)


class InMemoryRAGCache:

    def __init__(
        self,
    ) -> None:

        self._cache: dict[
            str,
            RAGResult,
        ] = {}

    @staticmethod
    def normalize_question(
        question: str,
    ) -> str:

        return " ".join(
            question
            .strip()
            .lower()
            .split()
        )

    def get(
        self,
        question: str,
    ) -> RAGResult | None:

        key = (
            self.normalize_question(
                question
            )
        )

        return self._cache.get(
            key
        )

    def set(
        self,
        question: str,
        result: RAGResult,
    ) -> None:

        key = (
            self.normalize_question(
                question
            )
        )

        self._cache[
            key
        ] = result

    def clear(
        self,
    ) -> None:

        self._cache.clear()