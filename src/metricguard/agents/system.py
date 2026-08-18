class MetricGuardAgentSystem:
    """
    Simple application-facing wrapper
    around the compiled LangGraph workflow.
    """

    def __init__(
        self,
        *,
        graph,
        max_revisions: int = 1,
    ) -> None:

        self.graph = graph

        self.max_revisions = (
            max_revisions
        )

    def investigate(
        self,
        question: str,
    ) -> dict:

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        return self.graph.invoke(
            {
                "question":
                    question,

                "trace": [],

                "revision_count":
                    0,

                "max_revisions":
                    self.max_revisions,

                "verification_feedback":
                    None,
            }
        )