# MetricGuard AI — Build Log

This document records major implementation milestones and architectural decisions made during development.

---

## 2026-08-11 — Project Foundation

### Completed

* Created `metricguard-ai` GitHub repository.
* Established local development under `Desktop/Projects/metricguard-ai`.
* Created production-style repository structure.
* Configured Git and GitHub workflow.
* Added `.gitignore`, `.env.example`, and dependency planning.
* Installed Python and created project-specific `.venv`.
* Configured VS Code interpreter.
* Created `00_project_setup.ipynb`.
* Established Google Colab ↔ GitHub workflow.
* Added initial application configuration.
* Added README and architecture documentation.

### Architecture Decision

Experiments will be performed in notebooks, while reusable application logic will progressively move into `src/metricguard/`.

---

## 2026-08-11 — Security Architecture

### Decision

MetricGuard will implement authentication and role-based access control.

Standard users receive read/query access.

Only authorized/admin users can modify the knowledge base or trigger ingestion.

---

## 2026-08-11 — Northstar Commerce Created

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

## 2026-08-11 — Synthetic Operational Dataset

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

## 2026-08-11 — SQL Staging Layer

### Completed

Created six SQL staging models.

The staging layer performs cleaning and standardization without applying major metric business logic.

Current warehouse flow:

```text
Raw Operational Data
        ↓
Staging Layer
        ↓
Facts / Marts
        ↓
Metrics
        ↓
Dashboards
```

### Next

Build fact tables and business marts.

---

## 2026-08-11 — Phase 1.3B — Facts and Business Marts

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

## 2026-08-11 — Phase 1.4 — Metric Definitions and Version History

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

## 2026-08-11 — Phase 1.5 — Dashboard Metadata and dbt-Style Documentation

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

## 2026-08-11 — Phase 1.6 — Incident Tickets and Analyst Notes

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

## 2026-08-11 — Phase 1.7 — Ground Truth and Evaluation Dataset

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

