# MetricGuard AI — System Architecture Overview

## High-Level Workflow

```text
Authorized Source Upload
        ↓
Input Validation
        ↓
Raw Source Storage
        ↓
Parsing and Normalization
        ↓
Chunking and Metadata Enrichment
        ↓
Version and Freshness Processing
        ↓
Lineage and Impact Mapping
        ↓
Embedding Generation
        ↓
Vector Database
        ↓
Agentic Retrieval and Investigation
        ↓
Evidence Verification
        ↓
Structured Answer
        ↓
Sources + Confidence + Audit Log
```

## Query Access

Standard users interact with the system through the query interface.

```text
User Question
      ↓
Input Guardrail
      ↓
Cache Check
      ↓
Retrieval
      ↓
Metadata Filtering
      ↓
Optional Reranking
      ↓
Version / Freshness Analysis
      ↓
Lineage / Impact Analysis
      ↓
Agentic Investigation
      ↓
Structured Response
```

## Access Control

MetricGuard AI uses role-based access control.

### Viewer

Can:

* ask questions
* inspect answers
* inspect supporting evidence

Cannot:

* upload source documents
* trigger ingestion
* modify the knowledge base

### Authorized / Admin

Can:

* upload new source documents
* trigger ingestion
* update metric versions
* refresh the knowledge base
* perform all viewer operations

## Planned Agent Architecture

### Agent 1 — Evidence Retrieval Agent

Finds relevant evidence across the knowledge base.

### Agent 2 — Metric Investigation Agent

Analyzes conflicts, versions, freshness, lineage, and impact.

### Agent 3 — Verification and Reporting Agent

Checks whether the evidence supports the conclusion and produces the final structured response.
