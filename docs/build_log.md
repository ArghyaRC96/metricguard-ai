# MetricGuard AI ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Build Log

This document records major implementation milestones and architectural decisions made during development.

---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Project Foundation

### Completed

* Created `metricguard-ai` GitHub repository.
* Established local development under `Desktop/Projects/metricguard-ai`.
* Created production-style repository structure.
* Configured Git and GitHub workflow.
* Added `.gitignore`, `.env.example`, and dependency planning.
* Installed Python and created project-specific `.venv`.
* Configured VS Code interpreter.
* Created `00_project_setup.ipynb`.
* Established Google Colab ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Â GitHub workflow.
* Added initial application configuration.
* Added README and architecture documentation.

### Architecture Decision

Experiments will be performed in notebooks, while reusable application logic will progressively move into `src/metricguard/`.

---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Security Architecture

### Decision

MetricGuard will implement authentication and role-based access control.

Standard users receive read/query access.

Only authorized/admin users can modify the knowledge base or trigger ingestion.

---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Northstar Commerce Created

### Decision

Created fictional omnichannel company **Northstar Commerce** as the synthetic analytics environment.

Primary analytics domains:

* Executive
* Finance
* Marketing
* Growth
* Operations

Core metrics:

* Gross Revenue
* Net Revenue
* Total Orders
* Active Customers
* Conversion Rate
* Refund Rate

---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Synthetic Operational Dataset

### Completed

Generated:

* customers
* orders
* order items
* payments
* chargebacks
* refunds
* web sessions

All datasets were validated before export.

Synthetic records are deterministic using random seed `42`.

---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SQL Staging Layer

### Completed

Created six SQL staging models.

The staging layer performs cleaning and standardization without applying major metric business logic.

Current warehouse flow:

```text
Raw Operational Data
        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Staging Layer
        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Facts / Marts
        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Metrics
        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Dashboards
```

### Next

Build fact tables and business marts.

---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 1.3B ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Facts and Business Marts

### Completed

- Created `fct_orders`.
- Created `fct_web_sessions`.
- Created Finance Daily mart.
- Created Executive Daily mart.
- Created Operations Daily mart.
- Created Growth Daily mart.

### Architecture Decision

Fact models remain reusable analytical event layers.

Business marts represent team-specific analytical interpretations.

### Intentional Conflict

Finance uses Net Revenue Version 3 and deducts chargebacks.

Executive uses Net Revenue Version 2 and does not deduct chargebacks.

This creates MetricGuard's first deliberate version-aware metric discrepancy.


---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 1.4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Metric Definitions and Version History

### Completed

Created version-controlled business rules and SQL definitions for:

- Net Revenue
- Total Orders
- Active Customers
- Conversion Rate
- Refund Rate

### Architecture Decision

Metric definitions are represented in more than one source type.

Business-rule Markdown documents capture governance history and effective dates.

SQL files capture executable metric logic.

This allows MetricGuard to compare documentation against implementation rather than relying on a single source of truth.

### Conflict Design

Several downstream assets intentionally continue using older or semantically different metric definitions so that version-aware and conflict-aware retrieval can be evaluated later.


---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 1.5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Dashboard Metadata and dbt-Style Documentation

### Completed

Created structured metadata for four Northstar dashboards.

Created dbt-style documentation for:

- source tables
- staging models
- fact models
- business marts
- current enterprise metric definitions

### Architecture Decision

Dashboard metadata explicitly records the metric version consumed by each reporting asset.

Current enterprise definitions are separately represented in `metrics.yml`.

This enables MetricGuard to compare downstream dashboard usage against approved metric governance documentation.

### Intentional Conflicts Preserved

- Executive Net Revenue remains on v2 while enterprise Net Revenue is v3.
- Operations Total Orders remains on v1 while enterprise Total Orders is v2.
- Growth Active Customers remains on v1 while enterprise Active Customers is v2.


---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 1.6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Incident Tickets and Analyst Notes

### Completed

Created four incident tickets and four analyst investigation notes.

### Design Decision

Not every dashboard disagreement represents a defect.

The synthetic knowledge base intentionally includes:

- true stale-version conflicts
- semantic metric disagreements
- resolved expected behavior
- legitimate differences between team-specific operational metrics

This will allow MetricGuard evaluation to test whether the system can
distinguish an actual governance problem from an expected business difference.

### Important Evidence

INC-001 and the Revenue v3 migration note independently support the conclusion
that the Executive KPI Dashboard remains on Net Revenue v2 while Finance uses
v3.

INC-003 establishes that the Operations versus Finance Total Orders
discrepancy is an expected semantic difference rather than a data failure.


---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 1.7 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ground Truth and Evaluation Dataset

### Completed

Created the hidden evaluation reference set for MetricGuard.

Ground truth now defines:

- approved current metric versions
- known conflicts
- expected conflict classifications
- correct lineage relationships
- evaluation questions
- required answer facts

### Architecture Decision

Ground-truth files are strictly separated from the RAG knowledge base.

MetricGuard must derive answers from real synthetic evidence sources rather
than retrieving the expected answers directly.

This prevents evaluation leakage and enables meaningful testing of retrieval,
reasoning, conflict detection, lineage, and answer generation.

### Phase 1 Status

The Northstar Commerce synthetic data universe is complete and ready for
document ingestion and parsing.


---

## 2026-08-11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 2.1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Document Loading and Parsing

### Completed

Implemented the first heterogeneous ingestion prototype in Google Colab.

Supported formats:

- SQL
- Markdown
- JSON
- YAML
- CSV

### Architecture Decision

All source formats are normalized into one canonical document structure before
chunking.

Structured CSV operational data is represented to RAG through dataset-level
summaries rather than row-level embeddings.

### Safety Decision

Ground-truth evaluation resources are explicitly excluded from ingestion to
prevent evaluation leakage.

### Next

Move the validated parser implementation from the experimental notebook into
`src/metricguard/ingestion/` and add automated tests.


---

## 2026-08-15 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Phase 2.2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Production Ingestion Parser

### Completed

Moved the validated heterogeneous parsing prototype from Google Colab into
`src/metricguard/ingestion/`.

Introduced:

- typed canonical parsed-document model
- format-specific parser module
- reusable ingestion pipeline
- deterministic SHA-256 document identity
- parser validation
- JSONL output
- parsing manifest
- automated pytest coverage
- editable local MetricGuard package installation

### Engineering Decision

Notebook code is used for experimentation and validation.

Once validated, reusable logic is refactored into the MetricGuard source
package and covered by automated tests.

### Retrieval Decision

Reranking is no longer optional.

The production retrieval architecture must rerank initially retrieved evidence
before downstream conflict, version, freshness, lineage, and answer reasoning.

### Next

Implement source-aware chunking and metadata enrichment.


---

## 2026-08-15 Ã¢â‚¬â€ Phase 3.2 Ã¢â‚¬â€ Production Chunking and Metadata

### Completed

Moved validated source-aware chunking and metadata logic from the
experimental notebook into the MetricGuard production package.

Added dedicated chunking and metadata modules and automated tests.

### Architecture Decision

MetricGuard does not apply identical fixed-size splitting to every source.

Chunking strategy depends on document structure and source type, while
recursive splitting remains the fallback for oversized logical sections.

### Metadata Decision

Retrieval chunks carry strong provenance and source-level metadata before
embedding.

Current metadata establishes the foundation for later:

- filtering
- citations
- version analysis
- freshness analysis
- lineage
- impact analysis
- reranking
- auditability

### Next

Implement explicit metric-version authority and freshness intelligence.

---

## 2026-08-18 â€” Phase 4.2 â€” Governance-Enriched Retrieval Chunks

### Completed

Integrated version and freshness intelligence directly into retrieval chunks.

The governance enrichment layer now composes the production ingestion,
chunking, metadata, version authority, and freshness systems.

### Retrieval Architecture

Chunks entering the future embedding and vector database stages can carry
governance-aware payload fields before semantic retrieval occurs.

This enables future retrieval filtering and reranking to reason over both
semantic relevance and governance state.

### Design Principle

Version mismatch and freshness are signals, not final defect classifications.

Conflict-aware reasoning will combine these signals with lineage, impact,
source evidence, incidents, and business semantics.

### Next

Build SQL lineage extraction and downstream impact mapping.

---

## 2026-08-18 — Phase 5.1 — Production SQL Lineage and Impact

### Completed

Added deterministic lineage extraction using SQLGlot and directed graph
analysis using NetworkX.

### Architecture

The lineage engine consumes the canonical documents produced by the existing
MetricGuard ingestion pipeline.

SQLGlot extracts source relations from SQL syntax trees while excluding
temporary CTE aliases.

Dashboard metadata extends SQL lineage from analytical marts to final
reporting assets.

NetworkX provides upstream and downstream graph traversal for lineage and
impact analysis.

### Important Design Decision

LLMs do not calculate SQL lineage.

The deterministic lineage engine calculates dependency relationships first.
Agents and the final LLM will consume these computed relationships as tools
and evidence.

### Next

Enrich retrieval chunks with lineage and impact information and build Notebook
04 for inspection and visualization.
