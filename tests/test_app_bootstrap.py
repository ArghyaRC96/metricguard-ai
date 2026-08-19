from types import SimpleNamespace

import pytest

from metricguard.application import bootstrap

from metricguard.agents.service import (
    AgenticServiceConfig,
    MetricGuardAgenticRAG,
)
from metricguard.agents.retrieval_agent import (
    EvidenceRetrievalAgent,
)
from metricguard.agents.investigation_agent import (
    MetricInvestigationAgent,
)
from metricguard.agents.verification_agent import (
    VerificationReportingAgent,
)


class FakeQdrantClient:
    pass


class FakeLLM:
    pass


class FakeGraph:
    pass


def test_build_metricguard_wires_components(
    monkeypatch,
    tmp_path,
):

    captured = {}

    fake_qdrant = (
        FakeQdrantClient()
    )

    fake_llm = (
        FakeLLM()
    )

    fake_retrieval = object()


    def fake_build_retrieval_pipeline(
        *,
        repo_root,
        qdrant_client,
    ):
        captured[
            "retrieval_repo_root"
        ] = repo_root

        captured[
            "qdrant_client"
        ] = qdrant_client

        return fake_retrieval


    def fake_build_graph(
        *,
        evidence_agent,
        investigation_agent,
        verification_agent,
    ):
        captured[
            "evidence_agent"
        ] = evidence_agent

        captured[
            "investigation_agent"
        ] = investigation_agent

        captured[
            "verification_agent"
        ] = verification_agent

        graph = FakeGraph()

        captured[
            "graph"
        ] = graph

        return graph


    monkeypatch.setattr(
        bootstrap,
        "build_retrieval_pipeline",
        fake_build_retrieval_pipeline,
    )

    monkeypatch.setattr(
        bootstrap,
        "load_relevance_config",
        lambda repo_root:
            SimpleNamespace(
                enabled=True,
                top1_rerank_threshold=
                    0.27,
            ),
    )

    monkeypatch.setattr(
        bootstrap,
        "build_metricguard_agent_graph",
        fake_build_graph,
    )

    monkeypatch.setattr(
        bootstrap,
        "load_agent_config",
        lambda repo_root:
            SimpleNamespace(
                max_revisions=1
            ),
    )

    monkeypatch.setattr(
        bootstrap,
        "load_agentic_service_config",
        lambda repo_root:
            AgenticServiceConfig(
                minimum_confidence=
                    0.60,

                cache_enabled=
                    True,

                cache_max_entries=
                    128,
            ),
    )


    service = (
        bootstrap.build_metricguard(
            repo_root=
                tmp_path,

            qdrant_client=
                fake_qdrant,

            llm=
                fake_llm,
        )
    )


    assert isinstance(
        service,
        MetricGuardAgenticRAG,
    )

    assert (
        captured[
            "qdrant_client"
        ]
        is fake_qdrant
    )

    assert isinstance(
        captured[
            "evidence_agent"
        ],
        EvidenceRetrievalAgent,
    )

    assert (
        captured[
            "evidence_agent"
        ]
        .retrieval_pipeline
        is fake_retrieval
    )

    assert (
        captured[
            "evidence_agent"
        ]
        .relevance_gate
        .threshold
        == 0.27
    )

    assert isinstance(
        captured[
            "investigation_agent"
        ],
        MetricInvestigationAgent,
    )

    assert (
        captured[
            "investigation_agent"
        ]
        .investigator
        .llm
        is fake_llm
    )

    assert isinstance(
        captured[
            "verification_agent"
        ],
        VerificationReportingAgent,
    )

    assert (
        captured[
            "verification_agent"
        ]
        .verifier
        .llm
        is fake_llm
    )

    assert (
        service
        .agent_system
        .graph
        is captured[
            "graph"
        ]
    )

    assert (
        service
        .agent_system
        .max_revisions
        == 1
    )

    assert (
        service
        .config
        .minimum_confidence
        == 0.60
    )


def test_create_qdrant_client_uses_credentials(
    monkeypatch,
):

    captured = {}


    class FakeClient:

        def __init__(
            self,
            **kwargs,
        ):
            captured.update(
                kwargs
            )


    monkeypatch.setattr(
        bootstrap,
        "QdrantClient",
        FakeClient,
    )


    bootstrap.create_qdrant_client(
        qdrant_url=
            "https://example.qdrant.test",

        qdrant_api_key=
            "secret-key",
    )


    assert captured == {
        "url":
            "https://example.qdrant.test",

        "api_key":
            "secret-key",
    }


def test_missing_qdrant_url_is_rejected(
    monkeypatch,
):

    monkeypatch.delenv(
        "QDRANT_URL",
        raising=False,
    )


    with pytest.raises(
        bootstrap
        .RuntimeConfigurationError,
        match="QDRANT_URL",
    ):

        bootstrap.create_qdrant_client()


def test_negative_llm_interval_is_rejected(
    tmp_path,
):

    with pytest.raises(
        ValueError,
        match=(
            "minimum_request_interval_seconds"
        ),
    ):

        bootstrap.build_metricguard(
            repo_root=
                tmp_path,

            qdrant_client=
                FakeQdrantClient(),

            llm=
                FakeLLM(),

            minimum_request_interval_seconds=
                -1.0,
        )