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

