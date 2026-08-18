import json
from typing import Any

from metricguard.rag import (
    build_evidence_context,
)

from .schemas import (
    InvestigationResult,
)
from .tools import (
    build_investigation_tool_context,
    validate_agent_evidence_ids,
)


class MetricInvestigator:
    """
    LLM-backed metric investigation service.

    Deterministic tools calculate facts.
    The LLM reasons over those facts.
    """

    def __init__(
        self,
        *,
        llm: Any,
    ) -> None:

        self.llm = llm

    def investigate(
        self,
        *,
        question: str,
        evidence: list[dict],
        previous_investigation:
            dict | None = None,
        verification_feedback:
            str | None = None,
    ) -> InvestigationResult:

        tool_context = (
            build_investigation_tool_context(
                evidence
            )
        )

        evidence_context = (
            build_evidence_context(
                evidence
            )
        )

        previous_text = (
            json.dumps(
                previous_investigation,
                indent=2,
                default=str,
            )
            if previous_investigation
            else "None"
        )

        feedback_text = (
            verification_feedback
            or "None"
        )

        tool_text = json.dumps(
            tool_context,
            indent=2,
            default=str,
        )

        prompt = f"""
You are MetricGuard's Metric Investigation Agent.

Investigate the analytics discrepancy using ONLY:

1. retrieved evidence,
2. deterministic MetricGuard tool observations,
3. verifier feedback when this is a revision.

Do not use outside knowledge.

IMPORTANT RULES:

- A non-current version is not automatically a defect.
- Different dashboard values may represent intentional semantic differences.
- Separate version drift from freshness problems.
- Separate metric migration from genuine pipeline failure.
- Never invent lineage.
- Never invent SQL logic.
- Never invent source documents.
- Evidence may be referenced only using IDs E1, E2, etc.
- If the evidence is contradictory, explicitly record the contradiction.
- If verifier feedback is present, address it directly.

USER QUESTION:

{question}

DETERMINISTIC TOOL OBSERVATIONS:

{tool_text}

RETRIEVED EVIDENCE:

{evidence_context}

PREVIOUS INVESTIGATION:

{previous_text}

VERIFIER FEEDBACK:

{feedback_text}

Produce the structured investigation required by the schema.
""".strip()

        result = self.llm.generate(
            prompt=prompt,
            response_schema=
                InvestigationResult,
        )

        validate_agent_evidence_ids(
            result.evidence_ids,
            evidence,
        )

        return result