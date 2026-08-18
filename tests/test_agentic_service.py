from metricguard.agents.cache import (
    AgenticResultCache,
)

from metricguard.agents.service import (
    AgenticServiceConfig,
    MetricGuardAgenticRAG,
)


class FakeAgentSystem:

    def __init__(
        self,
    ):
        self.calls = 0


    def investigate(
        self,
        question,
    ):

        self.calls += 1

        return {
            "verification_decision":
                "approved",

            "retrieval_relevant":
                True,

            "retrieval_top1_score":
                0.80,

            "revision_count":
                0,

            "trace": [
                "evidence_retrieval_agent",
                "metric_investigation_agent",
                "verification_reporting_agent",
            ],

            "evidence": [
                {
                    "source_path":
                        "data/raw/test.md",

                    "file_name":
                        "test.md",
                }
            ],

            "final_report": {
                "decision":
                    "approved",

                "diagnosis":
                    "version_mismatch",

                "answer":
                    "Definitions differ.",

                "key_findings": [
                    "Versions differ."
                ],

                "evidence_ids": [
                    "E1"
                ],

                "confidence":
                    0.90,
            },
        }


def test_agentic_service_uses_cache():

    system = FakeAgentSystem()

    service = (
        MetricGuardAgenticRAG(
            agent_system=
                system,

            config=
                AgenticServiceConfig(
                    minimum_confidence=
                        0.60,

                    cache_enabled=
                        True,

                    cache_max_entries=
                        8,
                ),

            cache=
                AgenticResultCache(
                    max_entries=8
                ),
        )
    )


    first = service.ask(
        "Why do definitions differ?"
    )

    second = service.ask(
        "Why do definitions differ?"
    )


    assert system.calls == 1

    assert first.cached is False
    assert second.cached is True

    assert (
        second.answer
        == first.answer
    )


def test_empty_question_is_rejected():

    system = FakeAgentSystem()

    service = (
        MetricGuardAgenticRAG(
            agent_system=
                system,

            config=
                AgenticServiceConfig(
                    minimum_confidence=
                        0.60,

                    cache_enabled=
                        False,

                    cache_max_entries=
                        8,
                ),
        )
    )


    try:
        service.ask("   ")

    except ValueError:
        pass

    else:
        raise AssertionError(
            "Empty question was not rejected."
        )