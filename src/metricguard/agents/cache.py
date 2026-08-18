from collections import OrderedDict

from metricguard.rag.agentic_result import (
    AgenticRAGResult,
)


class AgenticResultCache:
    """
    Small bounded LRU cache for runtime
    MetricGuard agent results.

    Suitable for a single-process portfolio
    deployment such as Streamlit.
    """

    def __init__(
        self,
        *,
        max_entries: int = 128,
    ) -> None:

        if max_entries <= 0:
            raise ValueError(
                "max_entries must be positive."
            )

        self.max_entries = int(
            max_entries
        )

        self._items: OrderedDict[
            str,
            AgenticRAGResult,
        ] = OrderedDict()


    @staticmethod
    def normalize_question(
        question: str,
    ) -> str:

        return (
            " ".join(
                question
                .strip()
                .split()
            )
            .casefold()
        )


    def get(
        self,
        question: str,
    ) -> AgenticRAGResult | None:

        key = self.normalize_question(
            question
        )

        result = self._items.get(
            key
        )

        if result is None:
            return None

        self._items.move_to_end(
            key
        )

        return result.model_copy(
            deep=True,
            update={
                "cached": True,
            },
        )


    def set(
        self,
        question: str,
        result: AgenticRAGResult,
    ) -> None:

        key = self.normalize_question(
            question
        )

        self._items[key] = (
            result.model_copy(
                deep=True,
                update={
                    "cached": False,
                },
            )
        )

        self._items.move_to_end(
            key
        )

        while (
            len(self._items)
            > self.max_entries
        ):
            self._items.popitem(
                last=False
            )


    def clear(
        self,
    ) -> None:

        self._items.clear()


    def __len__(
        self,
    ) -> int:

        return len(
            self._items
        )