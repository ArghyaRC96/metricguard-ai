# MetricGuard AI ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Project State

> This document is the authoritative checkpoint for the current state of the MetricGuard AI project.

**Last Updated:** August 11, 2026
**Current Phase:** Phase 5.1 — Production SQL Lineage and Impact Engine Complete
**Next Phase:** Phase 5.2 — Lineage-Enriched Retrieval Chunks and Notebook 04

---

## Project

**Name:** MetricGuard AI

**Synthetic Organization:** Northstar Commerce

**Purpose:** Build a conflict-aware, version-aware, lineage-aware Agentic Retrieval-Augmented Generation system for analytics metric governance and discrepancy investigation.

---

## Core RAG Roadmap

### Layer 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Build the Knowledge Base

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

### Layer 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Answer a User Question

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

### Layer 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Quality Control

1. Create evaluation questions
2. Test retrieval
3. Test answers
4. Monitor cost and errors
5. Access control
6. Track privacy and cost

---

## Agentic AI Architecture

MetricGuard will use a multi-agent workflow with three planned agents.

### Agent 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Evidence Retrieval Agent

Retrieves relevant evidence from the knowledge base.

### Agent 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Metric Investigation Agent

Investigates metric definitions, conflicts, versions, freshness, lineage, and downstream impact.

### Agent 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Verification and Reporting Agent

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
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Experiment and validate
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Reusable logic identified
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
src/metricguard/
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Production-style Python modules
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Automated tests
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Streamlit application
```

---

## Repository Structure

```text
metricguard-ai/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ notebooks/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ data/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ raw/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ processed/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ground_truth/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ samples/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ src/metricguard/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ app/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ tests/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ configs/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ docs/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ outputs/
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

## Flagship Metric Conflict ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Net Revenue

### Version 1

Gross Revenue
ÃƒÂ¢Ã‹â€ Ã¢â‚¬â„¢ Refunds

### Version 2

Gross Revenue
ÃƒÂ¢Ã‹â€ Ã¢â‚¬â„¢ Discounts
ÃƒÂ¢Ã‹â€ Ã¢â‚¬â„¢ Refunds

### Version 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Current

Gross Revenue
ÃƒÂ¢Ã‹â€ Ã¢â‚¬â„¢ Discounts
ÃƒÂ¢Ã‹â€ Ã¢â‚¬â„¢ Refunds
ÃƒÂ¢Ã‹â€ Ã¢â‚¬â„¢ Chargebacks

Planned inconsistency:

* Finance Dashboard ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V3
* Executive Dashboard ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V2
* Legacy Monthly Report ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V1

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

## Staging Layer ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â COMPLETE

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
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
stg_customers

raw_orders
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
stg_orders

raw_order_items
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
stg_order_items

raw_payments
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
stg_payments

raw_refunds
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
stg_refunds

raw_web_sessions
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
stg_web_sessions
```

---

# Completed Work

## Phase 0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Project Foundation

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
* Colab ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Â GitHub workflow established
* `settings.yaml` created
* README foundation created
* system architecture documentation created
* project version initialized at `0.1.0`
* authentication/RBAC requirement defined

## Phase 1.1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Business Universe

* Northstar Commerce defined
* business teams defined
* metrics selected
* version conflicts designed
* planned incidents and analyst notes defined

## Phase 1.2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Synthetic Raw Data

* six operational datasets generated
* relationship validation performed
* CSV files exported
* raw datasets committed to GitHub

## Phase 1.3A ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SQL Staging

* six staging SQL models created
* raw ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ staging lineage established

---

# Next Work

## Phase 1.3B ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Facts and Business Marts

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



---

## Phase 1.3B Ã¢â‚¬â€ Facts and Business Marts

### Fact Models Created

- `fct_orders.sql`
- `fct_web_sessions.sql`

### Business Marts Created

- `mart_finance_daily.sql`
- `mart_executive_daily.sql`
- `mart_operations_daily.sql`
- `mart_growth_daily.sql`

### Intentional Metric Discrepancy Introduced

Finance Net Revenue uses Version 3:

Gross Revenue  
- Discounts  
- Refunds  
- Chargebacks

Executive Net Revenue uses Version 2:

Gross Revenue  
- Discounts  
- Refunds

The Executive mart therefore intentionally omits chargebacks and represents stale business logic.


---

## Phase 1.4 Ã¢â‚¬â€ Metric Definitions and Version History

### Versioned Metrics Created

#### Net Revenue
- v1: Gross Revenue - Refunds
- v2: Gross Revenue - Discounts - Refunds
- v3: Gross Revenue - Discounts - Refunds - Chargebacks
- Current version: v3

#### Total Orders
- v1: All placed orders except cancelled orders
- v2: Successfully paid orders
- Current version: v2

#### Active Customers
- v1: Identified customers with digital activity during the previous 30 days
- v2: Customers with a successfully paid order during the previous 30 days
- Current version: v2

#### Conversion Rate
- v1: Distinct purchasing customers / Total sessions
- v2: Completed checkouts / Checkout starts
- Current version: v2

#### Refund Rate
- v1: Orders with any refund request / Paid orders
- v2: Orders with completed refunds / Paid orders
- Current version: v2

### Intentional Governance Issues

- Executive Net Revenue remains on deprecated v2 while Finance uses active v3.
- Operations Total Orders follows placed-order logic resembling deprecated v1.
- Growth-oriented Active Customer logic differs from the current enterprise purchasing definition.
- Legacy Marketing Conversion Rate logic differs from the current checkout-funnel definition.

Business-rule Markdown documents and SQL metric definitions now provide independent evidence sources for later conflict detection.


---

## Phase 1.5 Ã¢â‚¬â€ Dashboard Metadata and dbt-Style Documentation

### Dashboard Metadata Created

- Finance Revenue Dashboard
- Executive KPI Dashboard
- Operations Dashboard
- Growth & Marketing Dashboard

### Dashboard Version State

Finance Revenue Dashboard:
- Net Revenue v3
- Total Orders v2

Executive KPI Dashboard:
- Net Revenue v2
- Total Orders v2

Operations Dashboard:
- Total Orders v1

Growth & Marketing Dashboard:
- Active Customers v1
- Conversion Rate v2

### dbt-Style Documentation Created

- `sources.yml`
- `schema.yml`
- `metrics.yml`

### Governance Design

The current enterprise metric definitions are documented in `metrics.yml`.

Intentional stale downstream assets remain linked to older metric versions.

MetricGuard will therefore have multiple independent evidence sources for version conflicts:

- SQL metric definitions
- business-rule documents
- mart SQL
- dashboard JSON metadata
- dbt-style YAML documentation


---

## Phase 1.6 Ã¢â‚¬â€ Incident Tickets and Analyst Notes

### Incident Tickets Created

- INC-001 Ã¢â‚¬â€ Executive vs Finance Net Revenue mismatch
- INC-002 Ã¢â‚¬â€ Active Customer definition mismatch
- INC-003 Ã¢â‚¬â€ Operations vs Finance Total Orders discrepancy
- INC-004 Ã¢â‚¬â€ Conversion Rate migration change

### Incident Types

The incident set intentionally contains different classes of discrepancy:

- stale metric-version problems
- semantic-definition conflicts
- legitimate business differences
- expected metric migration effects

### Analyst Notes Created

- Revenue v3 migration notes
- Active Customer definition review
- Total Orders semantic review
- Conversion Rate migration review

### Knowledge-Base Design

MetricGuard now has human-generated evidence in addition to structured system
metadata.

The source universe currently includes:

- CSV operational tables
- SQL transformations
- SQL metric definitions
- Markdown business rules
- JSON dashboard metadata
- dbt-style YAML documentation
- incident tickets
- analyst notes

This enables later retrieval and reasoning across heterogeneous evidence types.


---

## Phase 1.7 Ã¢â‚¬â€ Ground Truth and Evaluation Dataset

### Ground-Truth Files Created

- `expected_versions.json`
- `known_conflicts.json`
- `expected_lineage.json`
- `evaluation_questions.json`
- `expected_answers.json`

### Evaluation Set

Ten initial evaluation questions were created covering:

- conflict detection
- metric-version detection
- staleness detection
- semantic conflicts
- expected semantic differences
- metric migration
- lineage
- impact analysis

### Evaluation Principle

Files under `data/ground_truth/` are evaluation-only resources.

They must not be ingested into the production RAG knowledge base or made
available to the answering agents.

They serve as the hidden reference set used to compare predicted MetricGuard
behavior against known correct outcomes.

### Current Synthetic Knowledge Base

Northstar Commerce now contains:

- synthetic operational CSV tables
- staging SQL
- fact SQL
- business marts
- versioned metric SQL
- versioned business-rule documents
- dashboard JSON metadata
- dbt-style YAML documentation
- incident tickets
- analyst notes
- hidden evaluation ground truth

Phase 1 synthetic knowledge-base construction is now complete.


---

## Phase 2.1 Ã¢â‚¬â€ Document Loading and Parsing

### Completed

Created `02_parse_documents.ipynb`.

The ingestion prototype now supports:

- SQL
- Markdown
- JSON
- YAML
- CSV

### Parsing Architecture

All heterogeneous sources are converted into a canonical parsed-document representation containing:

- document ID
- source path
- file name
- source type
- content hash
- normalized content
- optional structured data

### CSV Strategy

Operational CSV tables are summarized rather than converted into one RAG
document per row.

The complete structured records remain available for analytical processing and
validation outside semantic retrieval.

### Evaluation Protection

`data/ground_truth/` is explicitly excluded from source discovery.

Automated assertions verify that evaluation data does not enter the RAG
knowledge base.

### Generated Artifacts

- `data/processed/parsed_documents.jsonl`
- `data/processed/parse_manifest.csv`

These files are reproducible pipeline outputs and remain excluded from Git.


---

## Phase 2.2 Ã¢â‚¬â€ Production Ingestion Parser

### Completed

The heterogeneous parser prototype from `02_parse_documents.ipynb` has been
refactored into reusable production-style Python modules.

Created:

- `src/metricguard/ingestion/models.py`
- `src/metricguard/ingestion/parsers.py`
- `src/metricguard/ingestion/pipeline.py`
- `tests/test_ingestion.py`
- `pyproject.toml`

### Supported Source Types

- SQL
- Markdown
- JSON
- YAML
- CSV

### Production Architecture

The ingestion pipeline now:

1. discovers supported source files
2. dispatches files to format-specific parsers
3. calculates SHA-256 source hashes
4. converts sources into canonical ParsedDocument objects
5. validates parsed documents
6. blocks ground-truth evaluation leakage
7. writes reproducible JSONL documents
8. writes an ingestion manifest

### Testing

Automated ingestion tests validate:

- source discovery
- ground-truth exclusion
- SQL parsing
- complete knowledge-base parsing
- unique document IDs
- CSV dataset-summary behavior

### Package Architecture

MetricGuard is now installable as an editable Python package using
`pyproject.toml`.

Reusable application code can be imported directly from `metricguard`.

### Retrieval Architecture Update

Reranking is now a mandatory component of MetricGuard retrieval.

The configured retrieval flow will be:

initial retrieval
Ã¢â€ â€™ metadata filtering
Ã¢â€ â€™ reranking
Ã¢â€ â€™ version/freshness/lineage reasoning

`rerank_enabled` is now set to true in the project configuration.


---

## Phase 3.2 Ã¢â‚¬â€ Production Chunking and Metadata

### Completed

The source-aware chunking and metadata prototype from
`03_chunk_metadata.ipynb` has been moved into reusable production-style
Python modules.

### Production Modules

Created:

- `src/metricguard/chunking/models.py`
- `src/metricguard/chunking/splitters.py`
- `src/metricguard/chunking/pipeline.py`
- `src/metricguard/metadata/inference.py`
- `src/metricguard/metadata/extractors.py`

### Chunking Strategies

MetricGuard now uses source-aware chunking:

- Markdown: heading-aware splitting
- SQL: SQL-friendly recursive splitting
- JSON/YAML: structure-aware splitting
- CSV: dataset-summary splitting

Logical sections are preserved when possible and oversized sections use
recursive fallback splitting.

### Chunk Metadata

Each retrieval-ready chunk contains provenance metadata including:

- document ID
- source path
- file name
- source type
- asset type
- content hash
- chunk index
- chunk count

Additional source metadata is inferred or extracted where available,
including:

- metric name
- metric version
- dashboard ID
- dashboard name
- source mart
- owner
- business domain
- dashboard metric versions
- incident attributes
- analyst-note attributes

### Validation

Automated tests now cover ingestion, metadata inference/extraction,
source-aware chunking, unique identifiers, provenance metadata, and
ground-truth leakage prevention.

### Current Retrieval Architecture

Reranking remains mandatory.

Future retrieval flow:

initial vector retrieval
Ã¢â€ â€™ metadata filtering
Ã¢â€ â€™ mandatory reranking
Ã¢â€ â€™ version/freshness/lineage reasoning

---

## Phase 4.2 â€” Governance-Enriched Retrieval Chunks

### Completed

Governance intelligence is now attached directly to retrieval-ready
KnowledgeChunk objects.

Created:

- `src/metricguard/governance/enrichment.py`
- `src/metricguard/governance/enrichment_pipeline.py`
- `tests/test_governance_enrichment.py`

### Enrichment Flow

raw sources
â†’ production parser
â†’ source-aware chunker
â†’ metadata
â†’ version authority
â†’ freshness analysis
â†’ governance-enriched retrieval chunks

### Governance Metadata

Metric-aware chunks can now contain:

- metric name
- observed version
- authoritative version
- version relation
- authoritative owner
- authoritative effective date

All chunks also receive freshness information:

- freshness status
- days since review
- freshness reference date

### Important Design Decision

A non-current metric version is treated as evidence rather than automatically
classified as a defect.

Final conflict classification will later combine version state with semantic
differences, incidents, analyst notes, SQL logic, lineage, and impact.

### Generated Outputs

- `data/processed/governance_enriched_chunks.jsonl`
- `data/processed/governance_enriched_chunk_manifest.csv`

These are reproducible local pipeline outputs and remain excluded from Git.

### Next

Implement SQL lineage extraction and downstream impact mapping.

---

## Phase 5.1 — Production SQL Lineage and Impact

### Completed

Implemented deterministic SQL lineage extraction and downstream impact analysis.

### Production Components

Created:

- `src/metricguard/lineage/models.py`
- `src/metricguard/lineage/extractor.py`
- `src/metricguard/lineage/graph.py`
- `src/metricguard/lineage/pipeline.py`
- `tests/test_lineage.py`

### SQL Lineage

SQLGlot parses MetricGuard SQL assets and extracts actual upstream relations.

Internal CTE aliases are excluded from external lineage.

SQL models are represented as directed dependencies:

upstream relation
→ downstream model

### Dashboard Lineage

Dashboard JSON metadata contributes downstream consumption edges:

source mart
→ dashboard

### Graph Intelligence

NetworkX represents the lineage system as a directed graph.

MetricGuard can now compute:

- direct upstream dependencies
- transitive upstream dependencies
- direct downstream consumers
- transitive downstream impact
- graph cycle validation

### Generated Outputs

- `data/processed/lineage_edges.csv`
- `data/processed/lineage_graph.json`
- `data/processed/impact_report.csv`

These remain generated local artifacts and are excluded from Git.

### Design Principle

Lineage and impact are computed deterministically from source SQL and dashboard
metadata rather than inferred by the LLM.

The future investigation agents will call this engine as a tool.

### Next

Attach lineage and downstream impact metadata to retrieval chunks and create
`04_lineage_impact.ipynb` for graph inspection and portfolio visualization.
