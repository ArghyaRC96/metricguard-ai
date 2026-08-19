"""Production assembly for the MetricGuard application."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient

from metricguard.agents.config import (
    load_agent_config,
)
from metricguard.agents.graph import (
    build_metricguard_agent_graph,
)
from metricguard.agents.investigation_agent import (
    MetricInvestigationAgent,
)
from metricguard.agents.investigator import (
    MetricInvestigator,
)
from metricguard.agents.retrieval_agent import (
    EvidenceRetrievalAgent,
)
from metricguard.agents.service import (
    MetricGuardAgenticRAG,
    load_agentic_service_config,
)
from metricguard.agents.system import (
    MetricGuardAgentSystem,
)
from metricguard.agents.verification_agent import (
    VerificationReportingAgent,
)
from metricguard.agents.verifier import (
    VerificationReporter,
)
from metricguard.llm.factory import (
    build_structured_llm,
)
from metricguard.retrieval.factories import (
    build_retrieval_pipeline,
)
from metricguard.retrieval.relevance import (
    RelevanceGate,
    load_relevance_config,
)


REPO_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)


class RuntimeConfigurationError(
    RuntimeError
):
    """Raised when required application configuration is missing."""


def _resolve_required_value(
    *,
    explicit_value: str | None,
    environment_name: str,
) -> str:
    """
    Resolve an explicit runtime value first,
    then fall back to an environment variable.
    """

    value = (
        explicit_value
        or os.getenv(
            environment_name
        )
    )

    if not value:
        raise RuntimeConfigurationError(
            "Missing required runtime "
            f"configuration: {environment_name}"
        )

    return value


def create_qdrant_client(
    *,
    qdrant_url: str | None = None,
    qdrant_api_key: str | None = None,
) -> QdrantClient:
    """
    Create the production Qdrant client.

    QDRANT_URL is required.

    QDRANT_API_KEY is optional so the same
    bootstrap can also connect to an unsecured
    local Qdrant server during development.
    """

    resolved_url = (
        _resolve_required_value(
            explicit_value=
                qdrant_url,
            environment_name=
                "QDRANT_URL",
        )
    )

    resolved_api_key = (
        qdrant_api_key
        or os.getenv(
            "QDRANT_API_KEY"
        )
    )

    kwargs: dict[str, Any] = {
        "url":
            resolved_url,
    }

    if resolved_api_key:
        kwargs[
            "api_key"
        ] = resolved_api_key

    return QdrantClient(
        **kwargs
    )


def build_metricguard(
    *,
    repo_root: Path = REPO_ROOT,
    qdrant_client: Any | None = None,
    llm: Any | None = None,
    qdrant_url: str | None = None,
    qdrant_api_key: str | None = None,
    gemini_api_key: str | None = None,
    minimum_request_interval_seconds:
        float = 14.0,
) -> MetricGuardAgenticRAG:
    """
    Assemble the complete production MetricGuard service.

    Dependencies may be injected for testing.
    Runtime credentials are resolved only when
    the corresponding dependency is not injected.
    """

    repo_root = Path(
        repo_root
    ).resolve()

    if (
        minimum_request_interval_seconds
        < 0
    ):
        raise ValueError(
            "minimum_request_interval_seconds "
            "cannot be negative."
        )


    # -----------------------------------------------------
    # VECTOR DATABASE
    # -----------------------------------------------------

    if qdrant_client is None:

        qdrant_client = (
            create_qdrant_client(
                qdrant_url=
                    qdrant_url,

                qdrant_api_key=
                    qdrant_api_key,
            )
        )


    # -----------------------------------------------------
    # RETRIEVAL
    # -----------------------------------------------------

    retrieval_pipeline = (
        build_retrieval_pipeline(
            repo_root=
                repo_root,

            qdrant_client=
                qdrant_client,
        )
    )


    # -----------------------------------------------------
    # CALIBRATED RELEVANCE GATE
    # -----------------------------------------------------

    relevance_config = (
        load_relevance_config(
            repo_root
        )
    )

    relevance_gate = (
        RelevanceGate(
            enabled=
                relevance_config
                .enabled,

            threshold=
                relevance_config
                .top1_rerank_threshold,
        )
    )


    # -----------------------------------------------------
    # SHARED STRUCTURED LLM
    # -----------------------------------------------------

    if llm is None:

        resolved_gemini_key = (
            _resolve_required_value(
                explicit_value=
                    gemini_api_key,

                environment_name=
                    "GEMINI_API_KEY",
            )
        )

        llm = (
            build_structured_llm(
                repo_root=
                    repo_root,

                api_key=
                    resolved_gemini_key,

                minimum_request_interval_seconds=
                    minimum_request_interval_seconds,
            )
        )


    # -----------------------------------------------------
    # AGENT 1 — EVIDENCE RETRIEVAL
    # -----------------------------------------------------

    evidence_agent = (
        EvidenceRetrievalAgent(
            retrieval_pipeline=
                retrieval_pipeline,

            relevance_gate=
                relevance_gate,
        )
    )


    # -----------------------------------------------------
    # AGENT 2 — METRIC INVESTIGATION
    # -----------------------------------------------------

    investigator = (
        MetricInvestigator(
            llm=llm
        )
    )

    investigation_agent = (
        MetricInvestigationAgent(
            investigator=
                investigator
        )
    )


    # -----------------------------------------------------
    # AGENT 3 — VERIFICATION + REPORTING
    # -----------------------------------------------------

    verifier = (
        VerificationReporter(
            llm=llm
        )
    )

    verification_agent = (
        VerificationReportingAgent(
            verifier=
                verifier
        )
    )


    # -----------------------------------------------------
    # LANGGRAPH
    # -----------------------------------------------------

    graph = (
        build_metricguard_agent_graph(
            evidence_agent=
                evidence_agent,

            investigation_agent=
                investigation_agent,

            verification_agent=
                verification_agent,
        )
    )


    # -----------------------------------------------------
    # AGENT SYSTEM
    # -----------------------------------------------------

    agent_config = (
        load_agent_config(
            repo_root
        )
    )

    agent_system = (
        MetricGuardAgentSystem(
            graph=
                graph,

            max_revisions=
                agent_config
                .max_revisions,
        )
    )


    # -----------------------------------------------------
    # APPLICATION SERVICE
    # -----------------------------------------------------

    service_config = (
        load_agentic_service_config(
            repo_root
        )
    )

    return MetricGuardAgenticRAG(
        agent_system=
            agent_system,

        config=
            service_config,
    )