import json
from typing import Any

from metricguard.rag import (
    build_evidence_context,
)

from .schemas import (
    VerificationResult,
)
from .tools import (
    build_investigation_tool_context,
    validate_agent_evidence_ids,
)


class VerificationReporter:
    """
    Verify the investigation against evidence
    before allowing a final answer.
    """

    def __init__(
        self,
        *,
        llm: Any,
    ) -> None:

        self.llm = llm

    def verify(
        self,
        *,
        question: str,
        evidence: list[dict],
        investigation: dict,
    ) -> VerificationResult:

        evidence_context = (
            build_evidence_context(
                evidence
            )
        )

        tool_context = (
            build_investigation_tool_context(
                evidence
            )
        )

        investigation_text = (
            json.dumps(
                investigation,
                indent=2,
                default=str,
            )
        )

        tool_text = json.dumps(
            tool_context,
            indent=2,
            default=str,
        )

        prompt = f"""
You are MetricGuard's Verification and Reporting Agent.

Your responsibility is to independently verify Agent 2's investigation
against the supplied evidence and deterministic tool observations.

You must choose exactly one decision:

approved
revise
insufficient_evidence

APPROVED:
The investigation is supported by the evidence and does not overstate
what is known.

REVISE:
The investigation contains unsupported reasoning, ignores contradictions,
misclassifies the discrepancy, or needs correction.

INSUFFICIENT_EVIDENCE:
The available evidence cannot support a reliable conclusion.

RULES:

- Never trust Agent 2 merely because it sounds confident.
- Check every important conclusion against the evidence.
- A version mismatch alone does not prove a pipeline defect.
- Intentional semantic differences must not be labeled as bugs.
- Do not invent facts.
- Do not use outside knowledge.
- Use only valid evidence IDs E1, E2, etc.
- If decision="revise", give concrete actionable feedback.
- If decision="approved", produce the final grounded answer.

USER QUESTION:

{question}

DETERMINISTIC TOOL OBSERVATIONS:

{tool_text}

RETRIEVED EVIDENCE:

{evidence_context}

AGENT 2 INVESTIGATION:

{investigation_text}

Return the structured verification report required by the schema.
""".strip()

        result = self.llm.generate(
            prompt=prompt,
            response_schema=
                VerificationResult,
        )

        validate_agent_evidence_ids(
            result.evidence_ids,
            evidence,
        )

        return result