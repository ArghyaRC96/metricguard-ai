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


---

## 2026-08-11 — Phase 2.1 — Document Loading and Parsing

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

## 2026-08-15 — Phase 2.2 — Production Ingestion Parser

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

## 2026-08-15 — Phase 3.2 — Production Chunking and Metadata

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

## 2026-08-18 — Phase 4.2 — Governance-Enriched Retrieval Chunks

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

---

## 2026-08-18 — Phase 5.2 — Lineage-Enriched Retrieval Layer

### Completed

Integrated deterministic lineage and downstream-impact relationships into
retrieval chunks.

The final pre-embedding knowledge representation now combines semantic content
with governance and graph intelligence.

### Architecture

Production ingestion, chunking, metadata, governance, and lineage components
are composed into one deterministic enrichment pipeline.

The resulting chunk objects are ready for embedding generation and Qdrant
payload storage.

### Notebook

Added Notebook 04 for lineage inspection, focused graph visualization, and
evaluation against the hidden expected-lineage reference.

### Next

Embeddings and Qdrant vector storage.

---

## 2026-08-18 — Phase 6.1 — Embeddings and Qdrant Retrieval Prototype

### Completed

Implemented the first dense-vector retrieval layer in Google Colab.

Notebook 05 imports the production MetricGuard knowledge pipeline and
regenerates fully enriched retrieval chunks before embedding.

### Embeddings

Sentence Transformers is used to generate normalized dense embeddings for each
retrieval chunk.

The initial model is:

`sentence-transformers/all-mpnet-base-v2`

### Vector Database

Qdrant local mode is used for the prototype.

Each point stores:

- deterministic point ID
- embedding vector
- source content
- governance metadata
- lineage metadata
- impact metadata
- provenance information

### Retrieval

Implemented:

- semantic top-k retrieval
- payload metadata filtering
- metric-specific filtering
- lineage-aware result inspection
- reusable candidate retrieval helper

### Architecture Decision

Dense retrieval is only the first-stage candidate generator.

It is not considered sufficient by itself for the production MetricGuard
retrieval pipeline.

Cross-Encoder reranking is mandatory and will rerank the initial candidate
set before final evidence selection.

### Evaluation Decision

Later retrieval evaluation will compare:

- dense retrieval quality before reranking
- retrieval quality after reranking

This will demonstrate the actual benefit of reranking rather than merely
listing it as a framework feature.

### Next

Implement mandatory Cross-Encoder reranking and select final evidence for
baseline RAG.

---

## 2026-08-18 — Phase 6.2 — Mandatory Cross-Encoder Reranking

### Completed

Implemented and validated the mandatory reranking stage in Notebook 05.

A Cross-Encoder now reranks the broader candidate set returned by Qdrant
dense retrieval.

### Architecture

First-stage retrieval:

Sentence Transformer query embedding
→ Qdrant semantic search
→ optional metadata filter
→ top 20 candidates

Second-stage ranking:

query + candidate pairs
→ Cross-Encoder
→ relevance scores
→ top 5 final evidence chunks

### Model

`cross-encoder/ms-marco-MiniLM-L6-v2`

### Design Decision

Dense retrieval scores and Cross-Encoder scores are treated as separate
ranking signals and are not numerically combined.

The first-stage retriever generates candidates efficiently.

The second-stage Cross-Encoder performs more expensive pairwise relevance
scoring only over the retrieved candidate set.

### Next

Productionize retrieval and reranking into `src/metricguard/retrieval/`
before building baseline RAG.

---

## 2026-08-18 — Phase 6.3 — Production Retrieval and Mandatory Reranking

### Completed

Moved dense retrieval and mandatory Cross-Encoder reranking from Notebook 05
into reusable production modules.

### Production Components

The retrieval package now separates:

- configuration
- dense candidate retrieval
- reranking
- evidence formatting
- runtime model construction

### Testing

Local unit tests validate orchestration with lightweight fake components.

Real end-to-end integration is validated in Colab with:

- `all-mpnet-base-v2`
- local Qdrant
- `ms-marco-MiniLM-L6-v2`

### Final Retrieval Contract

The downstream RAG layer receives only the final top-5 reranked evidence items
with source provenance and governance/lineage context.

### Next

Implement baseline grounded RAG and structured answers.

---

## 2026-08-18 — Phase 7.1 — Baseline Gemini Grounded RAG

### Completed

Integrated Google Gemini with MetricGuard's production retrieval pipeline.

### Model

`gemini-3.7-flash`

### Implementation

Gemini receives only the final top-5 evidence items produced after mandatory
Cross-Encoder reranking.

Structured outputs are validated with Pydantic.

Evidence references use internal evidence IDs which are resolved
deterministically to real source metadata by MetricGuard.

### Fallback

The baseline system supports insufficient-evidence responses and an
application-level confidence threshold.

### Provider Strategy

Gemini is the primary LLM provider.

Paid OpenAI or an AWS-hosted model may be substituted later through the
production LLM abstraction if necessary.

### Next

Move Gemini integration and RAG orchestration into production modules.

---

## 2026-08-19 — Phase 7.1 — Validated Gemini Baseline Grounded RAG

### Completed

MetricGuard's first complete grounded RAG pipeline has been successfully
validated.

### LLM

Google Gemini API is operational with:

`gemini-3.7-flash`

Billing has been activated for the MetricGuard Google project.

Secrets remain outside source control and are loaded through Colab Secrets.

### Working Pipeline

question
→ dense retrieval
→ Qdrant top 20
→ mandatory Cross-Encoder reranking
→ top 5 evidence
→ grounded prompt
→ Gemini
→ structured answer
→ evidence validation
→ deterministic source resolution
→ confidence/fallback

### Reliability Improvements

Added:

- Gemini request throttling
- development answer caching
- structured Pydantic validation
- evidence-ID validation
- source-path resolution outside the LLM
- confidence threshold handling
- insufficient-evidence fallback

### Validation Result

End-to-end Gemini responses were successfully generated.

All baseline validation checks passed.

### Architecture Boundary

The LLM remains downstream of deterministic knowledge processing.

Gemini does not calculate:

- metric versions
- freshness
- SQL lineage
- downstream impact
- source provenance

Those are calculated by MetricGuard's deterministic production engines and
provided to the LLM as evidence.

### Next

Productionize Gemini and baseline RAG under `src/metricguard/`.

---

## 2026-08-19 — Phase 7.2 — Production Gemini Grounded RAG

### Completed

Moved the validated Gemini baseline RAG prototype into reusable production
modules.

### LLM Architecture

Introduced a provider-independent structured LLM interface.

Gemini currently implements this interface using the Google GenAI
Interactions API.

### RAG Architecture

Production RAG now handles:

- retrieval orchestration
- evidence formatting
- grounded prompt creation
- structured output
- citation validation
- deterministic source resolution
- confidence fallback
- insufficient-evidence handling
- runtime answer caching

### Testing

Local tests use fake providers and do not consume Gemini API requests.

Real Gemini integration was validated separately in Colab.

### Architecture Milestone

Notebook 06 is now an experiment and integration-validation environment.

The canonical RAG implementation lives under:

`src/metricguard/`

### Next

Build Agentic RAG orchestration with LangGraph.


---

## 2026-08-19 - Phase 8.1 and 8.2 - Agentic RAG Foundation

### Completed

MetricGuard has moved from production grounded RAG into a three-agent
LangGraph architecture.

### Phase 8.1

Introduced:

Evidence Retrieval Agent
-> Metric Investigation Agent
-> Verification and Reporting Agent

Agent 1 reuses the deterministic production retrieval pipeline.

### Phase 8.2

Added conditional routing and self-correction.

Verification decisions:

- approved
- revise
- insufficient_evidence

A revise decision routes execution back to the Metric Investigation Agent.

### Revision Control

Configured:

`max_revisions = 1`

If verification continues to request revision, MetricGuard exits through the
revision-limit fallback instead of looping indefinitely.

### No-Evidence Routing

If retrieval returns no usable evidence, the workflow exits through the
deterministic insufficient-evidence path without invoking Agents 2 or 3.

### Deterministic Investigation

Added deterministic observations for:

- metric versions
- authoritative versions
- freshness
- lineage

The LLM interprets these facts but does not calculate or invent them.

### Structured Agent Outputs

Added Pydantic schemas:

- InvestigationResult
- VerificationResult

Both reasoning services use MetricGuard's provider-independent structured LLM
interface.

### Safety

Added:

- evidence-ID validation
- ground-truth leakage protection
- no-evidence fallback
- revision-limit fallback
- bounded revision count

### Application Interface

Added:

`MetricGuardAgentSystem`

This provides one application-facing entry point for the compiled LangGraph
workflow.

### Testing

Local tests validate:

- graph routing
- first-pass approval
- revision and re-verification
- revision-limit handling
- no-evidence handling
- investigator output
- verifier output

Fake components allow these tests to run without consuming Gemini API calls.

### Dependencies

LangGraph was added to:

- pyproject.toml
- requirements.txt

Agent configuration was added to:

`configs/settings.yaml`

Current setting:

`agentic.max_revisions: 1`

### Next

Create and validate:

`notebooks/07_agentic_rag.ipynb`

using real retrieval, mandatory reranking, Gemini reasoning, Gemini
verification, and LangGraph conditional routing.


---

## 2026-08-19 - Phase 8.3 - Real Agentic RAG Integration

### Completed

Integrated the production MetricGuard three-agent system with the real
retrieval and Gemini runtime in Notebook 07.

### Real Runtime

Validated:

Qdrant
-> dense retrieval
-> mandatory Cross-Encoder reranking
-> Evidence Retrieval Agent
-> Gemini Metric Investigation Agent
-> Gemini Verification and Reporting Agent
-> LangGraph conditional routing

### Agentic Validation

Real integration cases include:

- Net Revenue disagreement
- Total Orders intentional semantic difference
- Active Customers disagreement
- unsupported out-of-domain question

### Self-Correction

The verification agent can request one revision.

LangGraph then routes the workflow back to the investigation agent and
returns the revised investigation for re-verification.

The workflow remains bounded by:

`max_revisions = 1`

### Safety

Validated production boundaries for:

- evidence IDs
- ground-truth isolation
- structured outputs
- revision limits
- deterministic governance facts

### Development Cost Protection

Notebook 07 uses an in-memory development result cache to avoid duplicate
Gemini calls when identical test questions are rerun.

### Next

Phase 8.4 will add production agent safeguards, explicit relevance gating,
final source-resolved result assembly, confidence/fallback integration and
production caching before formal evaluation.


---

## 2026-08-19 - Phase 8.4 - Production Agentic Safeguards

### Completed

Finished production hardening of MetricGuard's Agentic RAG workflow.

### Decision Normalization

Added deterministic normalization for the case where verification approves
an investigation whose diagnosis is insufficient_evidence.

Application-level final state now correctly becomes insufficient_evidence.

### Retrieval Relevance Calibration

Calibrated the mandatory Cross-Encoder against supported and unsupported
MetricGuard questions.

Top-1:

minimum supported = 0.5278
maximum unsupported = 0.0120
production threshold = 0.27

Top-3 mean also showed clean separation.

### Relevance Gate

Added a deterministic gate before LLM investigation.

Unsupported questions below the calibrated threshold now:

- skip Metric Investigation Agent
- skip Verification and Reporting Agent
- return deterministic insufficient evidence
- avoid Gemini token usage

### Final Application Service

Added a reusable application-facing Agentic RAG service.

Final outputs include:

- status
- decision
- diagnosis
- answer
- findings
- deterministic sources
- confidence
- fallback reason
- revision count
- retrieval relevance metadata
- graph trace
- cache indicator

### Confidence Guard

Configured minimum final confidence:

0.60

Approved results below this threshold fall back to insufficient evidence.

### Production Runtime Cache

Added bounded LRU caching.

Configured maximum:

128 entries

Identical normalized questions reuse the previously validated final result.

### Validation

Validated:

- supported Net Revenue investigation
- deterministic source resolution
- production cache hit
- unsupported-query relevance rejection
- no Agent 2 or Agent 3 execution for rejected evidence
- insufficient-evidence final result
- full local pytest suite

### Next

Phase 9 - Formal Evaluation.


---

## 2026-08-19 - Phase 9 - Formal Evaluation

### Completed

Completed the formal MetricGuard production benchmark.

### Supported Evaluation

Executed 10 production analytics-governance questions against quarantined
ground truth.

Execution success:

100%

Required facts:

35

### Answer Quality

Human-audited factual coverage:

82.86% (29 / 35)

Fully complete answers:

60% (6 / 10)

Classification accuracy:

80% (4 / 5)

No manually audited required fact was found to be explicitly incorrect.

Six required facts were omitted.

### NLI Evaluator Audit

Independent NLI evaluation initially measured 48.57% entailment coverage.

Manual inspection exposed multiple false negatives.

The NLI score is retained only as an auxiliary evaluator diagnostic rather
than the primary factual metric.

### Primary Failure Modes

Observed weaknesses:

1. incomplete deep lineage traversal in Q008
2. stale semantic definition classified as intentional semantic difference
3. high verification confidence relative to factual completeness
4. no natural revision-loop activation during the supported benchmark

### Retrieval and Sources

Supported retrieval acceptance:

100%

Source presence:

100%

### Unsupported Safety Benchmark

Evaluated 6 out-of-domain questions.

Results:

- rejection rate: 100%
- false acceptance: 0%
- zero-LLM execution: 100%
- maximum unsupported rerank score: 0.012
- relevance threshold: 0.27

All six unsupported queries exited before Gemini investigation and
verification.

### Runtime

Mean supported-query latency:

approximately 65.13 seconds

Mean unsupported-query latency:

approximately 3.45 seconds

Supported benchmark LLM calls:

20

### Artifacts

Saved formal benchmark artifacts under:

`outputs/evaluation/`

Saved formal evaluation notebook:

`notebooks/08_evaluation.ipynb`

### Next

Phase 10 - Application and Deployment.

<!-- BUILD_LOG_PHASE_10_COMPLETE -->

## 2026-08-19 ? Phase 10 Production Deployment Complete

Completed the production application and deployment phase for MetricGuard AI.

### Application layer

- Built production Streamlit application.
- Added production bootstrap assembly.
- Added Google OIDC authentication.
- Added Guest, Viewer, and Admin RBAC modes.
- Added recruiter-friendly no-login Guest Demo.
- Added sample investigation shortcuts.
- Added protected knowledge-base administration UI.
- Added deterministic application tests.

### Persistent retrieval

- Added production Qdrant indexing package.
- Added deterministic UUID generation for chunk point IDs.
- Preserved chunk content and governance/lineage metadata in Qdrant payloads.
- Added collection replacement and batched upsert logic.
- Added post-index point-count validation.
- Corrected production repository-root discovery.

### Qdrant Cloud

Created persistent production collection:

`metricguard_dense_v1`

Validated:

- 167 embedding-ready chunks
- 167 persisted Qdrant points
- 768-dimensional MPNet vectors
- cosine distance
- collection status green

### Production runtime

Configured:

- `sentence-transformers/all-mpnet-base-v2`
- `cross-encoder/ms-marco-MiniLM-L6-v2`
- Gemini `gemini-3.7-flash`
- persistent Qdrant Cloud
- mandatory reranking
- calibrated relevance gate
- bounded LangGraph revision
- structured sources and confidence

### Deployment

Deployed successfully to Streamlit Community Cloud:

`https://metricguard-ai.streamlit.app`

Resolved deployment-specific issues:

- `src/` package import path on Streamlit Cloud
- production repository-root resolution
- Qdrant runtime secrets
- Gemini runtime secret injection
- Google OAuth production callback
- Streamlit Cloud secret configuration
- corrupted sidebar/UI labels

### Browser validation

Successfully validated:

- public Guest mode
- recruiter-friendly no-login access
- Google sign-in
- Admin role resolution
- production Qdrant retrieval
- agentic investigation
- grounded answer generation
- source evidence rendering
- confidence and relevance metrics

Phase 10 is complete.
