# MetricGuard AI — Project State

> This document is the authoritative checkpoint for the current state of the MetricGuard AI project.

**Last Updated:** August 11, 2026
**Current Phase:** Phase 1.3A — SQL Staging Layer Complete
**Next Phase:** Phase 1.3B — Facts and Business Marts

---

## Project

**Name:** MetricGuard AI

**Synthetic Organization:** Northstar Commerce

**Purpose:** Build a conflict-aware, version-aware, lineage-aware Agentic Retrieval-Augmented Generation system for analytics metric governance and discrepancy investigation.

---

## Core RAG Roadmap

### Layer 1 — Build the Knowledge Base

1. Collect source documents
2. Load and parse text
3. Chunk documents
4. Add metadata
5. Mark versions
6. Add freshness fields
7. Build lineage map
8. Build impact map
9. Create embeddings
10. Store in vector database

### Layer 2 — Answer a User Question

1. User asks
2. Input guardrail
3. Check cache
4. Embed query
5. Retrieve chunks
6. Filter by metadata
7. Optional rerank
8. Check freshness and versions
9. Check lineage
10. Check impact
11. Build prompt
12. Call main LLM API
13. Structured output
14. Add sources
15. Add confidence
16. Apply fallback if weak
17. Write audit log

### Layer 3 — Quality Control

1. Create evaluation questions
2. Test retrieval
3. Test answers
4. Monitor cost and errors
5. Access control
6. Track privacy and cost

---

## Agentic AI Architecture

MetricGuard will use a multi-agent workflow with three planned agents.

### Agent 1 — Evidence Retrieval Agent

Retrieves relevant evidence from the knowledge base.

### Agent 2 — Metric Investigation Agent

Investigates metric definitions, conflicts, versions, freshness, lineage, and downstream impact.

### Agent 3 — Verification and Reporting Agent

Verifies whether retrieved evidence supports the conclusion and generates the structured final response.

Planned orchestration framework: LangGraph.

---

## Security and Access Control

MetricGuard must support authentication and role-based access control.

### Viewer / Standard User

Can:

* ask questions
* receive answers
* inspect supporting sources

Cannot:

* upload source documents
* trigger ingestion
* update the knowledge base
* manage metric versions

### Authorized / Admin User

Can:

* perform all viewer operations
* upload source files
* trigger ingestion
* update the knowledge base
* process new versions

---

## Development Architecture

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

---

## Repository Structure

```text
metricguard-ai/
├── notebooks/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── ground_truth/
│   └── samples/
├── src/metricguard/
├── app/
├── tests/
├── configs/
├── docs/
└── outputs/
```

---

## Technology Plan

* Python
* Google Colab
* VS Code
* Git
* GitHub
* Pandas
* SQLGlot
* NetworkX
* Sentence Transformers
* Qdrant
* LangGraph
* Pydantic
* Streamlit
* pytest

---

# Northstar Commerce

Northstar Commerce is a fictional omnichannel e-commerce organization.

Primary analytics teams:

* Executive Leadership
* Finance
* Marketing
* Growth
* Operations
* Data & Analytics

---

## Raw Operational Tables

Created:

* `raw_customers.csv`
* `raw_orders.csv`
* `raw_order_items.csv`
* `raw_payments.csv`
* `raw_refunds.csv`
* `raw_web_sessions.csv`

Location:

`data/raw/tabular/`

Approximate dataset scale:

* 2,000 customers
* 8,000 orders
* approximately 20,000 order items
* payment transactions including chargebacks
* refund transactions
* 20,000 web sessions

Synthetic generation seed:

`42`

---

## Core Metrics

Planned metrics:

1. Gross Revenue
2. Net Revenue
3. Total Orders
4. Active Customers
5. Conversion Rate
6. Refund Rate

---

## Flagship Metric Conflict — Net Revenue

### Version 1

Gross Revenue
− Refunds

### Version 2

Gross Revenue
− Discounts
− Refunds

### Version 3 — Current

Gross Revenue
− Discounts
− Refunds
− Chargebacks

Planned inconsistency:

* Finance Dashboard → V3
* Executive Dashboard → V2
* Legacy Monthly Report → V1

---

## Other Planned Conflicts

### Active Customers

Finance:
Customer with at least one completed paid order in the previous 30 days.

Growth:
Customer with website or mobile activity in the previous 30 days.

### Total Orders

Operations:
All valid placed orders.

Finance:
Completed and paid orders only.

### Conversion Rate

Marketing:
Purchasing customers divided by website sessions.

Growth/Product:
Completed checkouts divided by checkout starts.

---

# SQL Warehouse

## Staging Layer — COMPLETE

Created:

* `stg_customers.sql`
* `stg_orders.sql`
* `stg_order_items.sql`
* `stg_payments.sql`
* `stg_refunds.sql`
* `stg_web_sessions.sql`

Location:

`data/raw/sql/staging/`

Staging responsibilities:

* datatype standardization
* text normalization
* column preparation
* preservation of raw business records

Major metric business logic is intentionally not applied at the staging layer.

---

## Current Lineage

```text
raw_customers
    ↓
stg_customers

raw_orders
    ↓
stg_orders

raw_order_items
    ↓
stg_order_items

raw_payments
    ↓
stg_payments

raw_refunds
    ↓
stg_refunds

raw_web_sessions
    ↓
stg_web_sessions
```

---

# Completed Work

## Phase 0 — Project Foundation

* GitHub repository created
* Local repository cloned
* Production-style folder structure created
* `.gitignore` configured
* `.env.example` created
* local `.env` protected from Git
* Python installed
* project `.venv` created
* VS Code Python interpreter configured
* Notebook 00 created
* Colab ↔ GitHub workflow established
* `settings.yaml` created
* README foundation created
* system architecture documentation created
* project version initialized at `0.1.0`
* authentication/RBAC requirement defined

## Phase 1.1 — Business Universe

* Northstar Commerce defined
* business teams defined
* metrics selected
* version conflicts designed
* planned incidents and analyst notes defined

## Phase 1.2 — Synthetic Raw Data

* six operational datasets generated
* relationship validation performed
* CSV files exported
* raw datasets committed to GitHub

## Phase 1.3A — SQL Staging

* six staging SQL models created
* raw → staging lineage established

---

# Next Work

## Phase 1.3B — Facts and Business Marts

Next planned work:

1. Create fact-level models
2. Create business marts
3. Define correct reusable transformations
4. Begin separating Finance, Executive, Growth, and Operations logic
5. Prepare the environment in which metric-version conflicts will emerge

After this:

* metric SQL versions
* dashboard metadata
* dbt-style YAML
* business-rule documents
* incident tickets
* analyst notes
* intentional stale logic
* ground-truth evaluation files

---

# Continuity Rule

Whenever a major project phase is completed:

1. Run tests or validation
2. Inspect Git status
3. Commit changes
4. Push to GitHub
5. Update this document
6. Record the completed work in `docs/build_log.md`


