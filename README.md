# MetricGuard AI

**Conflict-Aware, Version-Aware Agentic RAG for Analytics Metric Governance**

MetricGuard AI is a production-style Retrieval-Augmented Generation (RAG) and Agentic AI system designed to investigate disagreements between analytics metrics across SQL transformations, dashboard definitions, business rules, documentation, incident tickets, and analyst notes.

## Problem

Analytics teams often encounter situations where two dashboards report different values for what appears to be the same metric.

The underlying cause may include:

* conflicting metric definitions
* outdated business rules
* stale dashboards
* different SQL transformations
* version mismatches
* broken or incomplete lineage
* undocumented logic changes

MetricGuard AI is designed to retrieve the relevant evidence, trace metric lineage, compare versions, detect conflicts, and explain why discrepancies exist.

## Core Capabilities

* Multi-source document ingestion
* Metadata-aware Retrieval-Augmented Generation
* Metric definition conflict detection
* Version tracking
* Freshness checks
* SQL lineage analysis
* Downstream impact analysis
* Agentic investigation workflow
* Source-grounded answers
* Confidence scoring
* Fallback handling
* Audit logging
* Authentication and role-based access control

## Access Model

MetricGuard AI separates knowledge-base management from normal query access.

**Viewer / Standard User**

* Ask questions
* View answers
* View supporting sources

**Authorized / Admin User**

* All viewer capabilities
* Upload new source documents
* Trigger ingestion
* Update the knowledge base
* Process new metric versions

## Development Approach

The project follows a notebook-to-production workflow:

```text
Google Colab
    ↓
Experiment and validate
    ↓
Reusable logic identified
    ↓
src/metricguard/
    ↓
Production-style Python modules
    ↓
Automated tests
    ↓
Streamlit application
```

## Planned Technology Stack

* Python
* Google Colab
* Git and GitHub
* SQLGlot
* NetworkX
* Sentence Transformers
* Qdrant
* LangGraph
* Pydantic
* Streamlit
* pytest

## Project Status

🚧 **Currently under active development — Phase 0: Project Foundation**

Detailed implementation, architecture diagrams, evaluation results, screenshots, and deployment instructions will be added progressively as the system is built.

<!-- METRICGUARD_PRODUCTION_START -->

## Live Production Demo

**MetricGuard AI:**  
https://metricguard-ai.streamlit.app

MetricGuard AI is a conflict-aware, version-aware, freshness-aware, lineage-aware Agentic RAG system for investigating analytics metric discrepancies across heterogeneous business and technical sources.

### Production capabilities

- Public recruiter-friendly Guest Demo with no login required.
- Google OIDC authentication for authenticated users.
- Role-based access control with Guest, Viewer, and Admin access modes.
- Admin-only knowledge-base management controls.
- Source-aware parsing for SQL, Markdown, CSV, JSON, and YAML knowledge assets.
- Structure-aware chunking with governance metadata.
- Metric version and freshness analysis.
- Lineage and downstream-impact enrichment.
- Dense retrieval using `sentence-transformers/all-mpnet-base-v2`.
- Persistent vector storage in Qdrant Cloud.
- Mandatory CrossEncoder reranking using `cross-encoder/ms-marco-MiniLM-L6-v2`.
- Calibrated relevance gate for rejecting unsupported questions before investigation LLM calls.
- Three-agent LangGraph workflow:
  1. Evidence Retrieval Agent
  2. Metric Investigation Agent
  3. Verification & Reporting Agent
- Gemini structured-output reasoning.
- Grounded answers with sources, confidence, diagnosis, and execution trace.
- Deterministic production indexing pipeline for rebuilding the Qdrant collection.

### Production knowledge base

Current production deployment:

- Qdrant collection: `metricguard_dense_v1`
- Indexed chunks: **167**
- Embedding dimension: **768**
- Vector similarity: cosine
- Qdrant collection status: **green**

### Evaluation snapshot

Formal Phase 9 benchmark:

- Execution success: **100%**
- Human-audited factual coverage: **82.86%**
- Full-question factual accuracy: **60%**
- Classification accuracy: **80%**
- Supported retrieval acceptance: **100%**
- Unsupported-query rejection: **100%**
- False acceptance rate: **0%**
- Source presence: **100%**
- Mean confidence: **0.968**

> The synthetic Northstar Commerce ground-truth dataset is used only for evaluation and is excluded from the retrieval knowledge base.

<!-- METRICGUARD_PRODUCTION_END -->
