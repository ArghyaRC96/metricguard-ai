"""Streamlit interface for MetricGuard AI."""

from __future__ import annotations

import sys
from pathlib import Path


# Adding the repository src directory to Python's import path.

REPOSITORY_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

SRC_ROOT = (
    REPOSITORY_ROOT
    / "src"
)

if str(SRC_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(SRC_ROOT),
    )


from dataclasses import (
    asdict,
    is_dataclass,
)
from typing import Any

import streamlit as st

from metricguard.application.bootstrap import (
    REPO_ROOT,
    RuntimeConfigurationError,
    build_metricguard,
    create_qdrant_client,
)
# Importing the MetricGuard authorization policy.

from metricguard.indexing import (
    rebuild_knowledge_base_index,
)

from metricguard.application.rbac import (
    AuthorizationError,
    resolve_user_access,
)

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MetricGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Resolving public guest access or authenticated Google RBAC access.

def resolve_app_access():

    if st.user.is_logged_in:

        st.session_state[
            "guest_mode"
        ] = False

        user_claims = (
            st.user.to_dict()
        )

        email = str(
            user_claims.get(
                "email",
                "",
            )
        )

        try:

            rbac_config = dict(
                st.secrets[
                    "rbac"
                ]
            )

            admin_emails = list(
                rbac_config.get(
                    "admin_emails",
                    [],
                )
            )

            user_access = (
                resolve_user_access(
                    email=email,
                    admin_emails=
                        admin_emails,
                )
            )

            role_value = getattr(
                user_access.role,
                "value",
                user_access.role,
            )

            return {
                "mode":
                    "authenticated",
                "email":
                    email,
                "role":
                    str(role_value),
                "user_access":
                    user_access,
            }


        except AuthorizationError as exc:

            st.error(
                "Your authenticated "
                "identity could not "
                "be authorized."
            )

            st.caption(
                str(exc)
            )

            st.button(
                "Log out",
                on_click=st.logout,
            )

            st.stop()


    if st.session_state.get(
        "guest_mode",
        False,
    ):

        return {
            "mode":
                "guest",
            "email":
                "Public demo user",
            "role":
                "guest",
            "user_access":
                None,
        }


    st.title(
        "MetricGuard AI 🛡️"
    )

    st.subheader(
        "Analytics Metric Governance"
    )

    st.write(
        "Explore the live MetricGuard "
        "demo instantly, or sign in "
        "with Google for authenticated "
        "access."
    )


    guest_col, login_col = (
        st.columns(2)
    )


    with guest_col:

        if st.button(
            "🚀 Explore Demo",
            type="primary",
            use_container_width=True,
        ):

            st.session_state[
                "guest_mode"
            ] = True

            st.rerun()


    with login_col:

        st.button(
            "🔐 Sign in with Google",
            on_click=st.login,
            use_container_width=True,
        )


    st.caption(
        "Guest access is read-only. "
        "Knowledge-base administration "
        "requires authorized access."
    )

    st.stop()


app_access = (
    resolve_app_access()
)


# Resolving application permissions from the current access mode.

access_role_value = (
    str(
        app_access[
            "role"
        ]
    )
    .strip()
    .lower()
)

is_guest = (
    access_role_value
    == "guest"
)

is_admin = (
    access_role_value
    == "admin"
)

can_investigate = True

can_manage_knowledge_base = (
    is_admin
)

# =========================================================
# PRODUCTION SERVICE
# =========================================================

@st.cache_resource(
    show_spinner=False
)
def get_metricguard():
    """
    Load the production MetricGuard runtime once
    and reuse it across Streamlit reruns.
    """

    return build_metricguard(
        qdrant_url=str(
            st.secrets[
                "QDRANT_URL"
            ]
        ),

        qdrant_api_key=str(
            st.secrets[
                "QDRANT_API_KEY"
            ]
        ),

        gemini_api_key=str(
            st.secrets[
                "GEMINI_API_KEY"
            ]
        ),
    )


# =========================================================
# DISPLAY HELPERS
# =========================================================

def to_mapping(
    value: Any,
) -> dict[str, Any]:

    if value is None:
        return {}

    if isinstance(
        value,
        dict,
    ):
        return value

    if is_dataclass(
        value
    ):
        return asdict(
            value
        )

    if hasattr(
        value,
        "model_dump",
    ):
        return value.model_dump()

    if hasattr(
        value,
        "__dict__",
    ):
        return dict(
            vars(value)
        )

    return {
        "value":
            str(value)
    }


def format_confidence(
    confidence: Any,
) -> str:

    try:

        return (
            f"{float(confidence) * 100:.0f}%"
        )

    except (
        TypeError,
        ValueError,
    ):

        return "N/A"


def format_score(
    score: Any,
) -> str:

    try:

        return (
            f"{float(score):.3f}"
        )

    except (
        TypeError,
        ValueError,
    ):

        return "N/A"


def humanize(
    value: Any,
) -> str:

    if value is None:
        return "N/A"

    return (
        str(value)
        .replace("_", " ")
        .strip()
        .title()
    )


def source_label(
    source: Any,
    index: int,
) -> str:

    data = to_mapping(
        source
    )

    possible_keys = [
        "source_path",
        "file_path",
        "path",
        "document_path",
        "source",
        "title",
        "name",
    ]


    for key in possible_keys:

        value = data.get(
            key
        )

        if value:

            return (
                f"Source {index}: "
                f"{value}"
            )


    return (
        f"Source {index}"
    )


TRACE_LABELS = {
    "evidence_retrieval_agent":
        "Evidence Retrieval",

    "relevance_gate_rejected":
        "Relevance Gate Rejected",

    "metric_investigation_agent":
        "Metric Investigation",

    "verification_reporting_agent":
        "Verification & Reporting",

    "no_evidence_fallback":
        "Insufficient Evidence Fallback",

    "revision_limit_fallback":
        "Revision Limit Fallback",
}


def format_trace(
    trace: Any,
) -> str:

    if not trace:
        return "No trace available."

    return "  →  ".join(
        TRACE_LABELS.get(
            step,
            humanize(step),
        )
        for step in trace
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # Displaying guest or authenticated access information.

    access_mode = str(
        app_access[
            "mode"
        ]
    )

    access_role = (
        access_role_value.upper()
    )

    access_email = str(
        app_access[
            "email"
        ]
    )


    st.caption(
        "ACCESS MODE"
    )

    st.write(
        f"**{access_role}**"
    )


    if (
        access_mode
        == "authenticated"
    ):

        st.caption(
            "SIGNED IN AS"
        )

        st.write(
            f"**{access_email}**"
        )

        st.button(
            "Log out",
            on_click=st.logout,
            use_container_width=True,
        )


    else:

        st.caption(
            "PUBLIC READ-ONLY DEMO"
        )

        st.button(
            "Sign in with Google",
            on_click=st.login,
            use_container_width=True,
        )

        if st.button(
            "Exit demo",
            use_container_width=True,
        ):

            st.session_state[
                "guest_mode"
            ] = False

            st.rerun()


    st.divider()

    st.title(
        "MetricGuard AI"
    )

    st.caption(
        "Conflict-aware analytics "
        "metric governance"
    )

    st.divider()

    st.markdown(
        """
**Production pipeline**

Question  
?  
Retrieve + rerank  
?  
Relevance gate  
?  
Metric investigation  
?  
Independent verification  
?  
Grounded answer
"""
    )

    st.divider()

    st.caption(
        "Designed for metric definitions, "
        "version drift, stale logic, "
        "semantic conflicts, lineage "
        "and impact analysis."
    )


    # Showing knowledge-base administration only to admins.

    if can_manage_knowledge_base:

        st.divider()

        st.subheader(
            "?? Knowledge Base Admin"
        )

        st.caption(
            "ADMIN ONLY"
        )

        st.warning(
            "This rebuilds the production index "
            "from the repository knowledge base."
        )

        rebuild_confirmed = st.checkbox(
            "Confirm production knowledge-base rebuild",
            key="admin_rebuild_confirmed",
        )

        rebuild_clicked = st.button(
            "Rebuild Knowledge Base",
            type="primary",
            disabled=(
                not rebuild_confirmed
            ),
            use_container_width=True,
        )


        if rebuild_clicked:

            try:

                qdrant_client = (
                    create_qdrant_client(
                        qdrant_url=str(
                            st.secrets[
                                "QDRANT_URL"
                            ]
                        ),
                        qdrant_api_key=str(
                            st.secrets[
                                "QDRANT_API_KEY"
                            ]
                        ),
                    )
                )


                with st.spinner(
                    "Rebuilding production "
                    "knowledge base..."
                ):

                    rebuild_result = (
                        rebuild_knowledge_base_index(
                            repo_root=
                                REPO_ROOT,

                            qdrant_client=
                                qdrant_client,

                            batch_size=64,
                        )
                    )


                get_metricguard.clear()


                st.success(
                    "Knowledge base rebuilt successfully."
                )

                st.write(
                    "Indexed chunks:",
                    rebuild_result.chunk_count,
                )

                st.write(
                    "Vector dimension:",
                    rebuild_result.vector_size,
                )


            except Exception as exc:

                st.error(
                    "Knowledge-base rebuild failed."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.exception(
                        exc
                    )


# =========================================================
# HEADER
# =========================================================

st.title(
    "MetricGuard AI 🛡️"
)

st.subheader(
    "Analytics Metric Investigation"
)

st.write(
    "Investigate why dashboards disagree, "
    "trace metric versions and lineage, "
    "and identify stale or conflicting logic."
)


# =========================================================
# SAMPLE INVESTIGATIONS
# =========================================================

st.caption(
    "TRY A SAMPLE INVESTIGATION"
)


def select_sample_question(
    sample_question: str,
) -> None:

    st.session_state[
        "question_input"
    ] = sample_question


sample_questions = [
    (
        "Dashboard disagreement",
        (
            "Why does the Executive KPI Dashboard "
            "report different Net Revenue from "
            "Finance after April 1, 2026?"
        ),
    ),
    (
        "Definition conflict",
        (
            "Are there conflicting definitions "
            "of Net Revenue?"
        ),
    ),
    (
        "Version & freshness",
        (
            "Which Net Revenue definition is current "
            "and which logic is stale?"
        ),
    ),
]


sample_columns = st.columns(
    len(
        sample_questions
    )
)


for (
    column,
    (
        label,
        sample_question,
    ),
) in zip(
    sample_columns,
    sample_questions,
):

    with column:

        st.button(
            label,
            key=(
                "sample_"
                + label
            ),
            on_click=select_sample_question,
            args=(
                sample_question,
            ),
            use_container_width=True,
        )


st.divider()


# =========================================================
# QUESTION FORM
# =========================================================

with st.form(
    "metricguard_question_form",
    clear_on_submit=False,
):

    question = st.text_area(
        "Ask MetricGuard",
        key="question_input",
        placeholder=(
            "Example: Why does the Executive KPI "
            "Dashboard report different Net Revenue "
            "from Finance after April 1, 2026?"
        ),
        height=120,
    )

    submitted = (
        st.form_submit_button(
            "Investigate",
            type="primary",
            use_container_width=True,
        )
    )


# =========================================================
# INVESTIGATION
# =========================================================

if submitted:

    question = (
        " ".join(
            question
            .strip()
            .split()
        )
    )


    if not question:

        st.warning(
            "Enter a metric-governance "
            "question before investigating."
        )

        st.stop()


    try:

        with st.spinner(
            "Running retrieval, investigation "
            "and independent verification..."
        ):

            metricguard = (
                get_metricguard()
            )

            result = (
                metricguard.ask(
                    question
                )
            )


    except RuntimeConfigurationError as exc:

        st.error(
            "MetricGuard runtime configuration "
            "is incomplete."
        )

        st.code(
            str(exc)
        )

        st.info(
            "Configure the required runtime "
            "secrets before running an "
            "investigation."
        )

        st.stop()


    except Exception as exc:

        st.error(
            "MetricGuard could not complete "
            "the investigation."
        )

        with st.expander(
            "Technical details"
        ):

            st.exception(
                exc
            )

        st.stop()


    # =====================================================
    # RESULT SUMMARY
    # =====================================================

    st.divider()

    st.subheader(
        "Investigation Result"
    )


    decision = getattr(
        result,
        "decision",
        None,
    )

    diagnosis = getattr(
        result,
        "diagnosis",
        None,
    )

    confidence = getattr(
        result,
        "confidence",
        None,
    )

    top1_score = getattr(
        result,
        "retrieval_top1_score",
        None,
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "Decision",
            humanize(
                decision
            ),
        )


    with col2:

        st.metric(
            "Diagnosis",
            humanize(
                diagnosis
            ),
        )


    with col3:

        st.metric(
            "Confidence",
            format_confidence(
                confidence
            ),
        )


    with col4:

        st.metric(
            "Top-1 relevance",
            format_score(
                top1_score
            ),
        )


    # =====================================================
    # UNSUPPORTED QUERY RESULT
    # =====================================================

    retrieval_relevant = getattr(
        result,
        "retrieval_relevant",
        None,
    )


    if (
        retrieval_relevant
        is False
    ):

        st.info(
            "This question did not pass "
            "MetricGuard's calibrated evidence "
            "relevance gate. The investigation "
            "LLM agents were not invoked."
        )


    # =====================================================
    # FINAL ANSWER
    # =====================================================

    st.markdown(
        "### Answer"
    )

    answer = getattr(
        result,
        "answer",
        None,
    )


    if answer:

        st.markdown(
            answer
        )

    else:

        st.info(
            "No grounded answer was produced."
        )


    # =====================================================
    # KEY FINDINGS
    # =====================================================

    key_findings = getattr(
        result,
        "key_findings",
        None,
    ) or []


    if key_findings:

        st.markdown(
            "### Key Findings"
        )


        for finding in key_findings:

            st.markdown(
                f"- {finding}"
            )


    # =====================================================
    # SOURCES
    # =====================================================

    sources = getattr(
        result,
        "sources",
        None,
    ) or []


    st.markdown(
        "### Sources"
    )


    if not sources:

        st.caption(
            "No source references available."
        )


    else:

        for index, source in enumerate(
            sources,
            start=1,
        ):

            with st.expander(
                source_label(
                    source,
                    index,
                )
            ):

                source_data = (
                    to_mapping(
                        source
                    )
                )

                if (
                    list(
                        source_data.keys()
                    )
                    == ["value"]
                ):

                    st.write(
                        source_data[
                            "value"
                        ]
                    )

                else:

                    st.json(
                        source_data
                    )


    # =====================================================
    # EXECUTION TRACE
    # =====================================================

    trace = getattr(
        result,
        "trace",
        None,
    ) or []


    with st.expander(
        "Agent execution trace"
    ):

        st.write(
            format_trace(
                trace
            )
        )


        relevance_reason = getattr(
            result,
            "retrieval_relevance_reason",
            None,
        )


        if relevance_reason:

            st.caption(
                relevance_reason
            )