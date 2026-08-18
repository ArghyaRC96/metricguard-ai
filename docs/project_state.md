# MetricGuard AI — Project State

> This document is the authoritative checkpoint for the current state of the MetricGuard AI project.

**Last Updated:** August 11, 2026
**Current Phase:** Phase 8.3 - Real Agentic RAG Integration Complete
**Next Phase:** Phase 8.4 - Agentic Safeguards, Relevance Gate and Final Result Assembly

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



---

## Phase 1.3B — Facts and Business Marts

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

## Phase 1.4 — Metric Definitions and Version History

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

## Phase 1.5 — Dashboard Metadata and dbt-Style Documentation

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

## Phase 1.6 — Incident Tickets and Analyst Notes

### Incident Tickets Created

- INC-001 — Executive vs Finance Net Revenue mismatch
- INC-002 — Active Customer definition mismatch
- INC-003 — Operations vs Finance Total Orders discrepancy
- INC-004 — Conversion Rate migration change

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

## Phase 1.7 — Ground Truth and Evaluation Dataset

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

## Phase 2.1 — Document Loading and Parsing

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

## Phase 2.2 — Production Ingestion Parser

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
→ metadata filtering
→ reranking
→ version/freshness/lineage reasoning

`rerank_enabled` is now set to true in the project configuration.


---

## Phase 3.2 — Production Chunking and Metadata

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
→ metadata filtering
→ mandatory reranking
→ version/freshness/lineage reasoning

---

## Phase 4.2 — Governance-Enriched Retrieval Chunks

### Completed

Governance intelligence is now attached directly to retrieval-ready
KnowledgeChunk objects.

Created:

- `src/metricguard/governance/enrichment.py`
- `src/metricguard/governance/enrichment_pipeline.py`
- `tests/test_governance_enrichment.py`

### Enrichment Flow

raw sources
→ production parser
→ source-aware chunker
→ metadata
→ version authority
→ freshness analysis
→ governance-enriched retrieval chunks

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

---

## Phase 5.2 — Lineage-Enriched Retrieval Layer

### Completed

Lineage and downstream impact intelligence are now attached directly to
retrieval-ready KnowledgeChunk objects.

Created:

- `src/metricguard/lineage/enrichment.py`
- `src/metricguard/lineage/enrichment_pipeline.py`
- `tests/test_lineage_enrichment.py`
- `notebooks/04_lineage_impact.ipynb`

### Final Pre-Embedding Pipeline

raw sources
→ ingestion
→ source-aware chunking
→ base metadata
→ version authority
→ freshness intelligence
→ lineage graph
→ downstream impact
→ fully enriched retrieval chunks

### Lineage Metadata

Applicable chunks now carry:

- lineage node
- lineage availability
- direct upstream assets
- all upstream assets
- direct downstream assets
- all downstream assets
- upstream count
- downstream impact count

### Generated Retrieval Artifact

`data/processed/fully_enriched_chunks.jsonl`

This is now the canonical input to the embedding and vector-database stage.

### Notebook 04

Notebook 04 imports the production lineage engine rather than reimplementing
lineage logic.

It provides:

- graph inspection
- upstream lineage examples
- downstream impact examples
- focused revenue-lineage visualization
- evaluation against hidden expected lineage

### Next

Generate embeddings for the fully enriched chunks and store them in Qdrant.

Mandatory reranking remains part of the later retrieval pipeline.

---

## Phase 6.1 — Embeddings and Qdrant Retrieval Prototype

### Completed

Created `notebooks/05_embeddings_qdrant.ipynb`.

MetricGuard now has a working dense semantic retrieval prototype built from
the fully enriched retrieval chunks.

### Input to Embedding Stage

The embedding stage consumes:

`data/processed/fully_enriched_chunks.jsonl`

These chunks already contain:

- parsed source content
- source-aware chunking
- provenance metadata
- metric/version metadata
- freshness intelligence
- SQL lineage
- downstream impact

### Embedding Strategy

The prototype uses:

- Sentence Transformers
- `sentence-transformers/all-mpnet-base-v2`
- normalized dense embeddings
- cosine similarity

Embedding text contains the source content plus compact contextual metadata.

Large lineage arrays are preserved in payload metadata rather than embedded
directly into the semantic representation.

### Qdrant Prototype

A local Qdrant instance is created inside the Colab runtime.

Each Qdrant point contains:

- deterministic UUID
- dense embedding vector
- original chunk content
- MetricGuard metadata payload
- embedding model identifier

### Retrieval

Implemented dense semantic retrieval using Qdrant's vector search.

The prototype supports:

- top-k semantic retrieval
- Qdrant payload metadata filtering
- metric-specific filtering
- lineage-aware payload inspection
- conversion of Qdrant results into reusable candidate dictionaries

### Evaluation Protection

Ground-truth files remain excluded from:

- parsing
- chunking
- embeddings
- Qdrant storage
- semantic retrieval

### Retrieval Architecture

Current retrieval flow:

user question
→ query embedding
→ Qdrant dense retrieval
→ optional metadata filtering
→ candidate evidence

### Mandatory Reranking Decision

Reranking is a required production component.

The next retrieval stage will use a Cross-Encoder to rerank the initial dense
retrieval candidates before evidence is passed to RAG.

Planned flow:

query
→ dense retrieval top 20
→ metadata filtering
→ mandatory Cross-Encoder reranking
→ top 5 evidence chunks
→ baseline RAG

### Next

Implement and evaluate mandatory Cross-Encoder reranking.

---

## Phase 6.2 — Mandatory Cross-Encoder Reranking

### Completed

Extended `notebooks/05_embeddings_qdrant.ipynb` with a mandatory second-stage
reranker.

### Retrieval Architecture

MetricGuard now uses:

query
→ bi-encoder query embedding
→ Qdrant dense retrieval
→ optional payload metadata filtering
→ top 20 candidate chunks
→ mandatory Cross-Encoder reranking
→ top 5 evidence chunks

### Reranker

Current prototype:

`cross-encoder/ms-marco-MiniLM-L6-v2`

The Cross-Encoder evaluates the user query jointly with each retrieved
candidate rather than comparing independently generated embeddings.

### Candidate Strategy

Dense retrieval prioritizes broad candidate recall.

The reranker operates only on the smaller retrieved candidate set and improves
the final evidence ordering.

Current settings:

- candidate_top_k: 20
- final_top_k: 5
- reranking: mandatory

### Reranking Metadata

The reranker receives compact contextual evidence including:

- source file
- asset type
- metric name
- observed version
- authoritative version
- version relation
- freshness state
- source content

Large lineage arrays remain payload metadata and are not inserted directly
into the Cross-Encoder text.

### Evidence Output

The final evidence package contains:

- reranker rank
- reranker score
- source provenance
- metric/version state
- freshness state
- lineage node
- source content

This package becomes the input to baseline RAG.

### Evaluation Direction

Later evaluation will compare dense retrieval ranking against reranked ranking
using retrieval metrics and known evaluation questions.

### Next

Move dense retrieval and Cross-Encoder reranking from the notebook prototype
into `src/metricguard/retrieval/`.

---

## Phase 6.3 — Production Retrieval and Mandatory Reranking

### Completed

Productionized MetricGuard's two-stage retrieval architecture.

Created:

- `src/metricguard/retrieval/models.py`
- `src/metricguard/retrieval/config.py`
- `src/metricguard/retrieval/text.py`
- `src/metricguard/retrieval/dense.py`
- `src/metricguard/retrieval/reranker.py`
- `src/metricguard/retrieval/pipeline.py`
- `src/metricguard/retrieval/factories.py`
- `src/metricguard/retrieval/__init__.py`
- `tests/test_retrieval.py`

### Production Retrieval Flow

query
→ dense query embedding
→ Qdrant top-20 candidate retrieval
→ optional metadata filtering
→ mandatory Cross-Encoder reranking
→ top-5 final evidence
→ provenance validation
→ RAG-ready evidence package

### Configuration

Production retrieval settings are stored in:

`configs/settings.yaml`

Current models:

Embedding:
`sentence-transformers/all-mpnet-base-v2`

Reranker:
`cross-encoder/ms-marco-MiniLM-L6-v2`

Qdrant collection:
`metricguard_dense_v1`

### Architecture Decision

Retrieval components use dependency injection.

Heavy model libraries are loaded lazily so the production package can be
tested locally without requiring the Torch/model stack in the local Python
3.14 development environment.

Real Sentence Transformer, Qdrant and Cross-Encoder integration is validated
in Google Colab.

### Safety Boundary

Ground-truth evaluation files remain prohibited from retrieval evidence.

### Next

Build baseline RAG using only the final top-5 reranked evidence.

The baseline RAG will introduce:

- grounded prompt construction
- main LLM call
- structured answer schema
- citations/sources
- confidence
- insufficient-evidence fallback

---

## Phase 7.1 — Baseline Gemini Grounded RAG

### Completed

Created:

`notebooks/06_baseline_rag.ipynb`

MetricGuard now connects the production retrieval and mandatory reranking
pipeline to a main LLM.

### Main LLM

Provider:

Google Gemini API

Model:

`gemini-3.7-flash`

Fallback provider strategy:

1. Gemini
2. paid OpenAI model
3. AWS-hosted LLM

### Baseline RAG Flow

user question
→ production dense retrieval
→ Qdrant top-20 candidates
→ mandatory Cross-Encoder reranking
→ top-5 evidence
→ grounded prompt construction
→ Gemini
→ structured response
→ Pydantic validation
→ citation validation
→ source resolution
→ confidence/fallback

### Structured Answer

The baseline answer contains:

- answer status
- diagnosis category
- metric name when applicable
- grounded answer
- key findings
- evidence IDs
- confidence
- confidence rationale
- missing evidence

### Citation Safety

Gemini never generates source paths directly.

The LLM references evidence IDs such as E1 or E2.

Application code deterministically maps those IDs back to actual retrieved
source paths.

This prevents fabricated source-path citations.

### Important Reasoning Rule

A version mismatch is not automatically considered a defect.

The model must distinguish:

- version drift
- stale definitions
- intentional semantic differences
- metric migrations
- pipeline/data failures
- insufficient evidence

### Ground Truth

Evaluation ground truth remains excluded from:

- parsing
- chunking
- embeddings
- Qdrant
- retrieval
- reranking
- Gemini prompt context

### Next

Productionize the Gemini adapter and baseline RAG orchestration under
`src/metricguard/`.

---

## Phase 7.1 — Validated Gemini Baseline Grounded RAG

### Status

COMPLETE AND VALIDATED END-TO-END.

### Notebook

Implemented and validated:

`notebooks/06_baseline_rag.ipynb`

### Main LLM

Provider:

Google Gemini API

Model:

`gemini-3.7-flash`

Gemini is the primary MetricGuard LLM provider.

Fallback provider strategy remains:

1. Gemini
2. paid OpenAI model
3. AWS-hosted LLM

### Billing

Gemini API billing has been enabled for the MetricGuard Google project.

API secrets remain outside source control and are loaded securely through
Colab Secrets using:

`GEMINI_API_KEY`

The API key is never stored in:

- GitHub
- settings.yaml
- notebooks
- source files
- documentation

### End-to-End Baseline Pipeline

The following workflow is operational:

user question
→ query embedding
→ Qdrant dense top-20 retrieval
→ optional metadata filtering
→ mandatory Cross-Encoder reranking
→ top-5 final evidence
→ grounded prompt construction
→ Gemini
→ structured JSON response
→ Pydantic validation
→ evidence-ID validation
→ deterministic source resolution
→ confidence handling
→ insufficient-evidence fallback

### Retrieval Architecture

Embedding model:

`sentence-transformers/all-mpnet-base-v2`

Vector database:

Qdrant

Collection:

`metricguard_dense_v1`

Candidate retrieval:

Top 20

Reranker:

`cross-encoder/ms-marco-MiniLM-L6-v2`

Final evidence:

Top 5

### Gemini Protection

Notebook 06 now includes an application-level Gemini rate limiter.

Current development safety interval:

14 seconds between Gemini API calls.

A session-level answer cache was also added.

Repeated identical questions reuse the cached result instead of consuming
another Gemini request.

### Structured Output

Gemini produces a validated structured answer containing:

- status
- diagnosis
- metric name
- grounded answer
- key findings
- evidence usage
- confidence
- confidence reason
- missing evidence

### Citation Safety

Gemini never generates arbitrary source paths.

Retrieved evidence is assigned deterministic IDs such as:

E1
E2
E3
E4
E5

Gemini may reference only these IDs.

MetricGuard application code maps the IDs back to the actual retrieved
source metadata.

This prevents hallucinated source-path citations.

### Reasoning Rules

The baseline system distinguishes between:

- version mismatch
- stale definition
- intentional semantic difference
- metric migration
- data/pipeline issue
- insufficient evidence

A non-current version is not automatically treated as a defect.

### Fallback

MetricGuard supports insufficient-evidence behavior.

The application also applies the configured confidence threshold:

`0.60`

Low-confidence or insufficiently supported responses can be rejected instead
of being presented as reliable answers.

### Ground-Truth Isolation

Evaluation ground truth remains excluded from:

- parsing
- chunking
- metadata enrichment
- embeddings
- Qdrant
- retrieval
- reranking
- Gemini prompt context

Ground truth remains evaluation-only.

### Validation

The Gemini API health check passed.

The production retrieval pipeline successfully provided reranked evidence to
Gemini.

Structured output validation passed.

Evidence-ID validation passed.

Source resolution passed.

Ground-truth isolation checks passed.

Confidence/fallback validation passed.

The complete baseline MetricGuard RAG pipeline is operational.

### Next Phase

Phase 7.2 will move Gemini integration and baseline RAG orchestration out of
Notebook 06 and into reusable production modules.

Planned production components include:

- Gemini LLM adapter
- provider abstraction
- structured RAG schemas
- grounded prompt builder
- citation validation
- confidence handling
- fallback logic
- RAG orchestration
- local fake-LLM tests
- real Gemini integration validation in Colab

---

## Phase 7.2 — Production Gemini Grounded RAG

### Status

COMPLETE AND VALIDATED.

### Production LLM Layer

Created:

- `src/metricguard/llm/base.py`
- `src/metricguard/llm/config.py`
- `src/metricguard/llm/gemini.py`
- `src/metricguard/llm/factory.py`
- `src/metricguard/llm/__init__.py`

The LLM layer now provides a provider-independent structured generation
interface.

Gemini is the current implementation.

Future OpenAI or AWS-hosted providers can implement the same interface without
rewriting the RAG pipeline.

### Production RAG Layer

Created:

- `src/metricguard/rag/schemas.py`
- `src/metricguard/rag/evidence.py`
- `src/metricguard/rag/prompt.py`
- `src/metricguard/rag/cache.py`
- `src/metricguard/rag/pipeline.py`
- `src/metricguard/rag/__init__.py`

### Production Runtime

question
→ production retrieval
→ Qdrant top-20 candidates
→ mandatory Cross-Encoder reranking
→ top-5 evidence
→ grounded prompt
→ structured LLM interface
→ Gemini
→ Pydantic answer validation
→ evidence-ID validation
→ deterministic source resolution
→ confidence/fallback
→ runtime answer cache

### LLM Provider

Current provider:

Google Gemini API

Current model:

`gemini-3.7-flash`

Fallback architecture remains compatible with future OpenAI or AWS-hosted
implementations.

### Citation Safety

The LLM may select only evidence IDs.

Actual source paths are resolved deterministically by MetricGuard code.

Ground-truth paths are rejected during source resolution.

### Confidence and Fallback

Responses below the configured minimum confidence threshold are not presented
as reliable answers.

Questions without retrieval evidence can return insufficient evidence without
making an LLM API call.

### Cache

A runtime in-memory RAG cache prevents repeated identical questions from
consuming additional retrieval and LLM calls within the same application
runtime.

The cache is intentionally non-persistent so rebuilt knowledge bases do not
inherit stale answers.

### Testing

Added local fake-component tests covering:

- Gemini structured generation
- successful grounded answer
- low-confidence fallback
- invalid evidence rejection
- empty-retrieval fallback
- answer caching

Real production Gemini integration was validated in Google Colab.

### Next

Phase 8 introduces the three-agent LangGraph architecture:

1. Evidence Retrieval Agent
2. Metric Investigation Agent
3. Verification and Reporting Agent

These agents will reuse the deterministic production engines already built
rather than duplicating their logic.


---

## Phase 8.1 - LangGraph Agent Foundation

### Status

COMPLETE.

### Purpose

Introduced MetricGuard's production three-agent orchestration foundation
using LangGraph.

### Agent Architecture

The production workflow contains three logical agents:

1. Evidence Retrieval Agent
2. Metric Investigation Agent
3. Verification and Reporting Agent

### Evidence Retrieval Agent

Agent 1 reuses the existing production retrieval pipeline.

Runtime:

question
-> query embedding
-> Qdrant dense top-20 retrieval
-> metadata-aware retrieval
-> mandatory Cross-Encoder reranking
-> top-5 final evidence

Retrieval itself does not require an LLM.

### Shared LangGraph State

Introduced `MetricGuardAgentState`.

Shared workflow state includes:

- question
- retrieved evidence
- investigation
- final verification report
- revision state
- workflow trace
- error state

### Initial Graph

The initial production LangGraph workflow established:

START
-> Evidence Retrieval Agent
-> Metric Investigation Agent
-> Verification and Reporting Agent
-> END

### Testing

The graph is locally testable using fake retrieval and fake reasoning
components without Gemini API calls.


---

## Phase 8.2 - Agentic Investigation and Verification

### Status

COMPLETE AND LOCALLY VALIDATED.

### Conditional Agent Workflow

The linear LangGraph foundation was upgraded into a conditional,
self-correcting investigation workflow.

Current runtime:

question
-> Evidence Retrieval Agent
-> evidence availability check
-> Metric Investigation Agent
-> Verification and Reporting Agent
-> conditional routing

Verification decisions:

- `approved`
- `revise`
- `insufficient_evidence`

### Revision Loop

If Agent 3 returns `revise`, LangGraph routes execution back to Agent 2.

The revised investigation receives:

- original user question
- original retrieved evidence
- previous investigation
- verifier feedback
- deterministic MetricGuard observations

The revised investigation is then verified again.

### Revision Safety

Configured:

`agentic.max_revisions: 1`

This enables self-correction while preventing uncontrolled LLM loops and
unbounded API usage.

If verification still requests revision after the allowed revision count,
MetricGuard exits through a deterministic revision-limit fallback.

### No-Evidence Safety

If Agent 1 retrieves no usable evidence:

question
-> Evidence Retrieval Agent
-> no-evidence fallback
-> END

Agents 2 and 3 are skipped, avoiding unnecessary Gemini API calls.

### Deterministic Investigation Tools

Added deterministic investigation helpers for:

- metric version observations
- observed versus authoritative versions
- freshness observations
- lineage observations
- evidence-boundary validation

MetricGuard deterministic code calculates factual metadata.

The LLM reasons over those calculated facts.

The LLM does not invent versions, freshness, lineage, or source provenance.

### Metric Investigation Service

Created the production Metric Investigator.

Inputs include:

- retrieved evidence
- deterministic tool observations
- previous investigation when revising
- verifier feedback when revising

Output is validated using `InvestigationResult`.

### Verification and Reporting Service

Created the independent Verification Reporter.

It verifies Agent 2's investigation against:

- the user question
- original evidence
- deterministic observations

Output is validated using `VerificationResult`.

The verifier may return:

- approved
- revise
- insufficient_evidence

### Evidence Safety

Agent outputs may reference only supplied evidence IDs such as:

E1
E2
E3
E4
E5

Invalid evidence IDs are rejected by deterministic application code.

Ground-truth evaluation data remains prohibited from runtime agent evidence.

### Application Interface

Created `MetricGuardAgentSystem`.

Application code can invoke the compiled workflow through:

`agent_system.investigate(question)`

### Production Agent Package

`src/metricguard/agents/`

contains:

- config.py
- fallbacks.py
- graph.py
- investigation_agent.py
- investigator.py
- retrieval_agent.py
- schemas.py
- state.py
- system.py
- tools.py
- verification_agent.py
- verifier.py
- __init__.py

### Dependencies

LangGraph was added to:

- pyproject.toml
- requirements.txt

### Configuration

Added:

`agentic.max_revisions: 1`

to:

`configs/settings.yaml`

### Local Testing

Tests cover:

- first-pass approval
- revision followed by approval
- revision-limit fallback
- no-evidence fallback
- structured investigator output
- structured verifier output
- evidence-ID enforcement

Fake components allow local testing without Gemini API calls.

### Gemini Call Budget

Typical successful investigation:

Agent 1 retrieval:
0 Gemini calls

Agent 2 investigation:
1 Gemini call

Agent 3 verification:
1 Gemini call

Typical total:
2 Gemini calls

With one revision:

Agent 2 revision:
+1 Gemini call

Agent 3 re-verification:
+1 Gemini call

Maximum under the current configuration:
4 Gemini calls

### Next Phase

Phase 8.3 will implement:

`notebooks/07_agentic_rag.ipynb`

It will integrate:

- real Qdrant retrieval
- real mandatory Cross-Encoder reranking
- real deterministic investigation metadata
- real Gemini investigation
- real Gemini verification
- real LangGraph conditional routing

Initial validation cases:

1. Net Revenue version mismatch
2. Total Orders intentional semantic difference
3. Active Customers stale definition


---

## Phase 8.3 - Real Agentic RAG Integration

### Status

COMPLETE AND VALIDATED IN NOTEBOOK 07.

### Notebook

Canonical integration notebook:

`notebooks/07_agentic_rag.ipynb`

### Purpose

Connected the production three-agent LangGraph workflow to the real
MetricGuard retrieval and Gemini stack.

### Runtime

question
-> query embedding
-> Qdrant dense top-20 retrieval
-> mandatory Cross-Encoder reranking
-> top-5 evidence
-> Evidence Retrieval Agent
-> Metric Investigation Agent
-> Verification and Reporting Agent
-> conditional routing
-> approved / revise / insufficient evidence

### Agent 1

Evidence Retrieval Agent uses the real production retrieval pipeline.

No LLM is used for retrieval.

### Agent 2

Metric Investigation Agent uses the production structured LLM interface
backed by Gemini.

It reasons over:

- retrieved evidence
- deterministic version observations
- deterministic freshness observations
- deterministic lineage observations
- previous investigation when revising
- verifier feedback when revising

### Agent 3

Verification and Reporting Agent independently checks Agent 2 against the
original evidence and deterministic observations.

Possible decisions:

- approved
- revise
- insufficient_evidence

### Revision Loop

LangGraph can route Agent 3 back to Agent 2 when revision is requested.

Maximum revisions remain:

`1`

### Integration Cases

Real integration testing covers:

1. Net Revenue version/staleness disagreement
2. Total Orders intentional semantic difference
3. Active Customers current/stale-definition disagreement
4. Unsupported out-of-domain question

The Total Orders case explicitly validates that intentional semantic
differences are not automatically classified as pipeline defects.

### Safety Validation

Validated:

- bounded revision count
- valid evidence-ID usage
- ground-truth isolation
- structured investigation output
- structured verification output
- production LangGraph execution
- deterministic evidence boundaries

### Notebook Development Cache

Notebook 07 contains a development-only in-memory result cache.

This protects against duplicate Gemini calls when the same question cell is
rerun during integration testing.

This cache is not the final production cache implementation.

### Unsupported Queries

An unsupported out-of-domain question is included specifically to evaluate
whether semantic retrieval alone can surface irrelevant evidence.

Phase 8.4 will add or strengthen an explicit retrieval relevance gate before
the final production evaluation.

### Architecture Boundary

Deterministic MetricGuard components remain responsible for:

- parsing
- chunking
- metadata
- versions
- freshness
- lineage
- impact
- embeddings
- retrieval
- reranking
- evidence validation

LLM agents remain responsible for:

- investigation
- interpretation
- contradiction reasoning
- verification
- explanation

### Next Phase

Phase 8.4 will productionize final agent safeguards:

- retrieval relevance gate
- deterministic source resolution for agent reports
- final application-facing result schema
- confidence and fallback integration
- agentic response caching
- production error handling

After Phase 8.4, MetricGuard moves into formal evaluation.
