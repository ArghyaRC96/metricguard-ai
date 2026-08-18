import json
from types import SimpleNamespace

from metricguard.llm import (
    GeminiStructuredLLM,
)
from metricguard.rag import (
    BaselineRAGAnswer,
)


class FakeInteractions:

    def __init__(
        self,
    ):
        self.last_request = None

    def create(
        self,
        **kwargs,
    ):

        self.last_request = kwargs

        payload = {
            "status": "answered",
            "diagnosis":
                "version_mismatch",
            "metric_name":
                "net_revenue",
            "answer":
                "The definitions differ.",
            "key_findings": [
                "Different versions are used."
            ],
            "evidence_used": [
                {
                    "evidence_id": "E1",
                    "supports":
                        "Version mismatch.",
                }
            ],
            "confidence": 0.90,
            "confidence_reason":
                "Evidence is consistent.",
            "missing_evidence": [],
        }

        return SimpleNamespace(
            output_text=
                json.dumps(
                    payload
                )
        )


class FakeClient:

    def __init__(
        self,
    ):
        self.interactions = (
            FakeInteractions()
        )


def test_gemini_structured_generation():

    client = FakeClient()

    llm = GeminiStructuredLLM(
        client=client,
        model="fake-gemini",
        thinking_level="medium",
    )

    answer = llm.generate(
        prompt="Investigate revenue.",
        response_schema=
            BaselineRAGAnswer,
    )

    assert (
        answer.status
        == "answered"
    )

    assert (
        answer.metric_name
        == "net_revenue"
    )

    request = (
        client.interactions
        .last_request
    )

    assert (
        request["model"]
        == "fake-gemini"
    )

    assert (
        request[
            "response_format"
        ][
            "mime_type"
        ]
        == "application/json"
    )


def test_empty_prompt_is_rejected():

    client = FakeClient()

    llm = GeminiStructuredLLM(
        client=client,
        model="fake-gemini",
    )

    try:

        llm.generate(
            prompt="",
            response_schema=
                BaselineRAGAnswer,
        )

    except ValueError:
        return

    raise AssertionError(
        "Empty prompt should fail."
    )