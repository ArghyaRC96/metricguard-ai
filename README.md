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
