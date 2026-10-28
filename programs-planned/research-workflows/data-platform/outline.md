### A+ Elite Data Platform Mastery Path (December 2025–2026 Reference Grade)

**Total: 200 cores (40 modules × 5 cores each)**  
**Plus: 40 module-specific capstones (not counted in cores)**  
**Pace:** 40 weeks intensive (5 cores/week) or 18–24 months part-time  
**Prerequisites (0 cores, non-negotiable):**  
- SQL fluency capable of inducing reviewer discomfort if absent  
- Python fluency with Polars (pandas classified as legacy technical debt)  
- Git, Docker, and operational experience with at least one major cloud provider  

**Core Principle (December 2025):**  
The data platform exists to deliver reliable, cost-effective decisions at the speed and scale required by the business — whether that is real-time for agents, near-real-time for dashboards, or batch for regulatory workloads. Elite architects ruthlessly match technology to business value, eliminate complexity, and design for organizational reality. Real-time is a tool, not a religion.

#### Phase I — Reliability & Governance with Organizational Reality (8 modules / 40 cores)

**Module 1 — Consumer-Driven Contracts with Hard Enforcement (5 cores)**  
- Contracts as enforceable APIs with graduated enforcement (observe → warn → fail)  
- PR-time compatibility checking and adoption metrics tracking  
- Schema evolution across heterogeneous producers (mobile, third-party, legacy)  
- Cross-team negotiation patterns and RFC processes for breaking changes  
- Portability: mapping contract concepts to Delta/Hudi or warehouse-native schemas  

**Capstone:** Implement graduated contract enforcement across 3 domains with realistic adoption timeline.

**Module 2 — dbt Mesh Mastery & Multi-Project Architecture (5 cores)**  
- dbt Mesh patterns for multi-domain projects and cross-project governance  
- dbt Core + generic CI/CD (GitHub Actions, GitLab, Argo) alongside Cloud options  
- Lineage sanity: detecting dead models, duplicated logic, and graph simplification  
- Monolith-to-mesh migration with incremental adoption and rollback paths  
- Decomplexification: identifying and safely removing unnecessary models/views  

**Capstone:** Migrate a monolithic dbt project to mesh while decommissioning ≥20% of models.

**Module 3 — Data Quality Tooling Stack 2025 (5 cores)**  
- Elementary/Monte Carlo/Soda with precision/recall tuning to minimize false positives  
- Business-aligned quality checks prioritized by decision impact  
- Embedding and distribution drift detection with actionable alerting  
- Phased rollout strategies and pager fatigue reduction patterns  
- Portability: implementing equivalent quality gates in Great Expectations or warehouse-native tools  

**Capstone:** Deploy quality suite that reduces alert volume ≥70% while catching all critical issues.

**Module 4 — SLOs/SLIs for Decision Systems (5 cores)**  
- Freshness, correctness, hallucination-risk, and end-to-end question→answer latency SLOs  
- Shared SLO negotiation across infra, data, AI, and product teams  
- Retrieval confidence and LLM token latency/completion accuracy metrics  
- Error budgets that align with business outcomes, not just uptime  
- When to accept lower SLOs for cost or simplicity  

**Capstone:** Negotiate and instrument cross-team SLOs for a live decision pipeline.

**Module 5 — WAP++ with Controlled Rollback (5 cores)**  
- Write–Audit–Publish with automatic + manual rollback triggers  
- Blast-radius analysis and consumer impact assessment before promotion  
- Human-in-the-loop approval policies with clear criteria  
- Rollback communication blueprints and consumer notification processes  
- Portability: equivalent patterns in Delta Lake or warehouse change management  

**Capstone:** Execute WAP++ pipeline with deliberate bad deployment and controlled rollback.

**Module 6 — Semantic Layer as Single Source of Truth (5 cores)**  
- MetricFlow/Malloy with strict metric governance (approval workflow, naming conventions)  
- Conflict resolution for duplicate/near-duplicate metrics across teams  
- Consistency across BI, agents, reverse ETL, and APIs  
- Text-to-SQL integration with fallback to curated metrics  
- Metric lifecycle management: alpha → GA → deprecate → retire  

**Capstone:** Resolve real-world metric conflict case and implement governance workflow.

**Module 7 — Governance & Policy-as-Code 2025 (5 cores)**  
- ABAC with Open Policy Agent, including performance tuning and caching  
- Policy testing, debugging workflows, and policy diff on change  
- Column-level lineage and PII classification across tools  
- Governance operating model that survives politics and skills gaps  
- Policy engine overhead measurement and mitigation strategies  

**Capstone:** Implement and performance-tune policies that enforce domain isolation without >50ms overhead.

**Module 8 — Data Products & Product Thinking (5 cores)**  
- Data product lifecycle: alpha → GA → deprecated → sunset with forced migration  
- Internal pricing/chargeback models aligned with FinOps  
- Consumer SLA tracking and adoption/NPS metrics  
- ROI measurement and kill criteria for underused products  
- Organizational rollout: training, migration paths, and handling resistant teams  

**Capstone:** Launch and sunset one data product with full lifecycle documentation.

#### Phase II — Storage Mastery with Portability & Tradeoffs (8 modules / 40 cores)

**Module 9 — Iceberg v3 Core Specification Deep Dive (5 cores)**  
- v3 features and operational consequences of spec choices  
- Multi-catalog and multi-cloud federation strategies  
- Migration paths from Delta/Hudi with zero-downtime patterns  
- Bootstrap and disaster recovery across catalog implementations  
- When Iceberg is overkill vs raw Parquet or warehouse tables  

**Capstone:** Migrate a production-like Delta table to Iceberg v3 with full portability testing.

**Module 10 — Layout Optimization at Exabyte Scale (5 cores)**  
- Query log analysis → layout simulation → cost/performance comparison  
- Partitioning/clustering/Z-order tradeoffs with rolling refactor patterns  
- Small-file elimination and manifest caching tricks  
- Layout design pipeline with business approval gates  
- Decomplexification: when to consolidate partitions or revert to simpler layouts  

**Capstone:** Optimize a 10 TB table using query logs, achieving ≥50% cost or latency improvement.

**Module 11 — Schema Evolution & Time Travel Forensics (5 cores)**  
- Safe evolution patterns with consumer communication RFCs and timelines  
- Time-travel forensics playbooks for incident response  
- Schema contract negotiation between producer and consumer teams  
- Broadcasting schema changes to downstream apps/ML teams  
- Rollback vs forward-fix decision framework  

**Capstone:** Execute breaking schema change with full communication and consumer sign-off process.

**Module 12 — Object Storage Engineering 2025 (5 cores)**  
- Prefix design, tiering, and egress minimization strategies  
- Cross-cloud and hybrid (on-prem + cloud) patterns  
- Data gravity and placement simulation tools  
- Cost modeling including network egress and multi-region replication  
- When to repatriate or stay multi-cloud vs single-provider lock-in  

**Capstone:** Design storage architecture reducing annual cost ≥40% with documented tradeoffs.

**Module 13 — DuckDB/MotherDuck as Primary Analytics Engine (5 cores)**  
- DuckDB/MotherDuck for local-first and collaborative workflows  
- Clear boundaries: when regulated metrics or high concurrency require warehouse  
- Comparison vs warehouse BI for executive reporting  
- Integration patterns with Iceberg and semantic layer  
- Migration path from pandas/notebooks to DuckDB  

**Capstone:** Replace a warehouse-heavy analytics workflow with DuckDB while maintaining governance.

**Module 14 — Polars Lazy Execution Mastery (5 cores)**  
- Polars for transformation logic with lazy execution and query optimization  
- Migration toolkit and patterns from pandas/Spark  
- Debugging, profiling, and memory leak detection workflows  
- Performance vs readability tradeoffs at team scale  
- When to fall back to Spark for distributed execution  

**Capstone:** Migrate a complex Spark job to Polars with ≥8× speedup and full test coverage.

**Module 15 — Multi-Engine Access & Ruthless Simplification (5 cores)**  
- Query routing with cost/complexity scoring per engine  
- Engine elimination framework: what can we safely stop running?  
- Caching layers and federation patterns across Trino/DuckDB/Spark/warehouse  
- Operational overhead modeling and reduction targets  
- Single-engine convergence strategies when possible  

**Capstone:** Consolidate from 4 engines to 2 with documented complexity reduction.

**Module 16 — Privacy-Enhancing Technologies in Practice (5 cores)**  
- High-impact privacy wins: minimization, pseudonymization, access logging  
- Differential privacy deployment thresholds and regulatory triggers  
- Synthetic data for testing/agent training with utility measurement  
- Threat modeling for PII leakage in embeddings and RAG  
- When PETs are overkill vs mandatory  

**Capstone:** Implement privacy controls preserving ≥95% utility while satisfying strict regulation.

#### Phase III — Decision Latency Spectrum: Real-Time, Near-Real-Time, Batch (8 modules / 40 cores)

**Module 17 — Kafka/Redpanda KRaft Mastery 2025 (5 cores)**  
- KRaft production patterns and zero-downtime migrations  
- Tiered storage and retention with cost/complexity tradeoffs  
- Multi-tenant isolation and quota governance  
- Consumer lag monitoring with severity classification  
- When Kafka is overkill vs simpler queues or micro-batch  

**Capstone:** Operate KRaft cluster through region outage and deliberate overload.

**Module 18 — RisingWave/Materialize as Decision Serving Layer (5 cores)**  
- Materialized views for millisecond consistency where justified  
- Exactly-once patterns and backfill/recovery strategies  
- Cost/complexity comparison vs micro-batch or warehouse views  
- RisingWave vs Materialize vs incremental dbt decision framework  
- Graceful degradation paths when streaming fails  

**Capstone:** Build real-time view with documented fallback to near-real-time.

**Module 19 — RisingWave Operational Excellence (5 cores)**  
- Dynamic scaling, spot instances, and state tiering  
- Connector reliability and schema evolution handling  
- Monitoring, chaos engineering, and canary deployments  
- Multi-region active-active with latency/cost tradeoffs  
- When to choose simpler materialized views in warehouse instead  

**Capstone:** Deploy cluster surviving 50% node loss with <10s recovery and cost justification.

**Module 20 — CDC Engineering 2025 (5 cores)**  
- Debezium and native Iceberg streaming ingestion patterns  
- Schema evolution robustness and out-of-order handling  
- Reconciliation with batch sources and fallback strategies  
- CDC vs polling tradeoffs for different data velocities  
- Organizational adoption path from legacy ETL  

**Capstone:** Implement CDC pipeline surviving 5 schema changes with zero data loss.

**Module 21 — Unstructured & Multi-Modal Ingestion (5 cores)**  
- Document processing pipelines with versioning in Iceberg  
- Change detection and incremental embedding patterns  
- Multi-modal preparation for RAG with quality gates  
- Cost/latency tradeoffs for unstructured ingestion  
- When to process unstructured data vs ignore it  

**Capstone:** Build pipeline converting PDFs to embedded Iceberg tables with cost < $100/month at scale.

**Module 22 — Feature Serving Across Latency Tiers (5 cores)**  
- Real-time features via RisingWave/Redis where justified  
- Near-real-time and batch feature views with consistency guarantees  
- Point-in-time correctness without dual stores  
- Feature freshness SLOs matched to business impact  
- Decommissioning over-engineered feature pipelines  

**Capstone:** Serve features across latency tiers with documented cost/benefit analysis.

**Module 23 — Event-Driven Architectures with Bounded Contexts (5 cores)**  
- Event sourcing within bounded contexts only  
- Schema Registry governance and replay patterns  
- Dead-lettering, time-travel reprocessing, and multi-region replication  
- When not to do event sourcing (debug complexity, onboarding cost)  
- Partial adoption strategies across domains  

**Capstone:** Implement event-driven domain with explicit non-event-sourced alternative.

**Module 24 — Streaming SQL with Safe Deployment (5 cores)**  
- Windowing, late data, and exactly-once correctness  
- Schema changes on streams with canary and state migration  
- Operator lifecycle management and deployment rotation  
- Debugging nondeterminism and performance tuning  
- Fallback to micro-batch when streaming complexity outweighs benefits  

**Capstone:** Upgrade streaming job with schema change and canary rollout.

#### Phase IV — Retrieval & Embeddings with Portability & Governance (8 modules / 40 cores)

**Module 25 — Vector Implementation Patterns 2025 (5 cores)**  
- pgai/pgvector/pgvector scale as primary lane with clear boundaries  
- Mapping same patterns to ClickHouse, Vespa, Elasticsearch, LanceDB  
- Hybrid search in single query with portability examples  
- Billion-scale index design and cost modeling across implementations  
- When vector search is overkill vs simple filtering  

**Capstone:** Implement hybrid search in pgai and one alternative with comparable performance.

**Module 26 — Embedding Pipeline Engineering (5 cores)**  
- Batch + streaming embedding with model selection framework  
- Re-embedding strategies and drift triggers  
- PII detection/redaction and embedding governance  
- Model-induced drift detection (embedding/LLM upgrades)  
- Cost optimization across self-hosted and managed inference  

**Capstone:** Deploy embedding pipeline with governance preventing PII leakage.

**Module 27 — Advanced Hybrid Retrieval (5 cores)**  
- BM25 + vector + filters + recency with learning-to-rank integration  
- Metadata-first routing and recall optimization playbooks  
- Multi-stage retrieval across different backends  
- Offline evaluation driving layout decisions  
- Portability patterns to non-Postgres vector stores  

**Capstone:** Achieve ≥40% recall improvement with documented evaluation suite.

**Module 28 — Production RAG Architecture 2025 (5 cores)**  
- Chunking, re-ranking, and parent document strategies  
- Offline evaluation → shadow → canary → full rollout patterns  
- RAG evaluation frameworks in production CI/CD  
- Caching and latency-budgeted design  
- When RAG is not justified vs curated responses  

**Capstone:** Deploy RAG pipeline with full canary rollout and eval passing ≥90%.

**Module 29 — Agentic Retrieval with Guardrails (5 cores)**  
- Agent tool calling patterns with white/blacklists and depth limits  
- Dynamic retrieval strategy selection with safety rails  
- Failure modes: infinite loops, tool misuse, jailbreaking  
- Rate limiting, budget controls, and human escalation paths  
- Multi-hop retrieval with traceability  

**Capstone:** Build agent with guardrails surviving deliberate jailbreak attempts.

**Module 30 — Drift Detection: Data, Embeddings, Models (5 cores)**  
- Distribution, concept, and model-induced drift monitoring  
- Joint reasoning across data changes and model upgrades  
- Automatic retraining/re-embedding with approval gates  
- Alerting and rollback workflows  
- When drift monitoring itself becomes technical debt  

**Capstone:** Detect and recover from combined data + model drift scenario.

**Module 31 — Multi-Modal & Graph-Augmented Retrieval (5 cores)**  
- Image/text/tabular retrieval patterns with clear business justification  
- Graph-RAG only where relationships dominate similarity  
- Entity resolution and knowledge graph maintenance cost  
- Tiered implementation: simple metadata vs full graph  
- Neo4j + vector hybrid with portability to property graph alternatives  

**Capstone:** Implement justified multi-modal retrieval with cost/benefit analysis.

**Module 32 — Vector Infrastructure Cost & Complexity Engineering (5 cores)**  
- Tier 1 (pgai) vs Tier 2 (specialized vector DB) decision framework  
- Quantization, refresh, and multi-tenant patterns  
- Scaling to 10B vectors profitably or choosing not to  
- Decommissioning over-engineered vector infra  
- Total cost of ownership modeling across options  

**Capstone:** Design vector architecture for 1B vectors at < $80k/year or justify simpler approach.

#### Phase V — Platform Engineering for Real Organizations (6 modules / 30 cores)

**Module 33 — Platform-as-Product Reference Architecture 2025 (5 cores)**  
- Opinionated yet portable stack with explicit escape hatches  
- Platform roadmap discipline and ruthless prioritization  
- Saying no to shiny requests with business alignment  
- Migration playbooks from legacy warehouse/lake stacks  
- Platform team structure that survives reorgs  

**Capstone:** Produce architecture document for 500-person company with 3-year migration plan.

**Module 34 — Automation with Human Oversight (5 cores)**  
- Agents proposing (not executing) optimizations for partitions, queries, compaction  
- Human approval workflow graduating to higher automation over time  
- Rollback and safety rails for agent actions  
- Measuring agent ROI and kill criteria  
- When to disable automation entirely  

**Capstone:** Deploy agent that proposes ≥20% efficiency gain with human approval gate.

**Module 35 — Multi-Region & Resilience Engineering (5 cores)**  
- Active-active patterns only where latency/cost justifies  
- Disaster recovery with realistic RTO/RPO tradeoffs  
- Data residency and sovereignty compliance frameworks  
- Region failure drills and blast radius minimization  
- Single-region simplicity as default  

**Capstone:** Design platform surviving region loss with documented justification for multi-region scope.

**Module 36 — Security & Zero-Trust Data Platform (5 cores)**  
- Zero-trust access with threat modeling for full stack  
- Encryption, secret management, and attack surface audit  
- Offensive simulation and red-team findings integration  
- Security incident playbooks with communication plans  
- Balancing security with developer velocity  

**Capstone:** Conduct and document red-team exercise with mitigations.

**Module 37 — Developer Experience & Adoption Measurement (5 cores)**  
- Golden paths with time-to-first-success <4 hours  
- Internal platform marketplace and feedback loops  
- Adoption funnel metrics and NPS tracking  
- Training and enablement programs for resistant teams  
- When to force migration vs allow legacy continuance  

**Capstone:** Onboard new domain team in <2 hours with measured adoption metrics.

**Module 38 — Platform Observability & Decision Making (5 cores)**  
- End-to-end lineage, cost, and performance observability  
- Observability-driven architecture changes with case studies  
- Alerting that prevents rather than detects outages  
- Capacity forecasting and saturation handling  
- Observability debt cleanup and simplification  

**Capstone:** Use observability to drive and document one major architecture improvement.

#### Phase VI — FinOps, Sustainability & Organizational Resilience (2 modules / 10 cores) + Final Integrating Capstone

**Module 39 — AI-Era FinOps Mastery (5 cores)**  
- Per-token/query/GB attribution aligned with product P&L  
- Automatic routing to cheapest compliant region/model  
- GPU bursting and spot strategies with risk assessment  
- Cost per user/event/decision modeling with finance  
- Regular complexity/cost review cadence  

**Capstone:** Implement attribution reducing bill ≥30% with product team sign-off.

**Module 40 — Hallucination-Risk & Trust Management (5 cores)**  
- Detecting and responding to data-induced hallucinations  
- Retrieval confidence scoring and user-facing transparency  
- Incident communication: internal blame-free + external trust-preserving  
- Postmortems that drive guardrails and process changes  
- Long-term trust metrics and recovery playbooks  

**Capstone:** Run hallucination incident simulation with full internal/external communication plan.

**Final Integrating Capstone (not counted in cores):**  
Deploy a complete, production-grade data platform incorporating every phase:  
- 5+ real sources across latency tiers → Iceberg with contracts → dbt Mesh → decision serving (RisingWave or warehouse) → hybrid retrieval → live agents where justified  
- Must survive: region outage, schema change, embedding drift, bad deployment, cost overrun, security incident, and deliberate over-complexity introduction  
- Required decomplexification round: remove at least two non-essential components with justification  
- Deliverable: 50+ page principal-level design document defending every choice, tradeoffs, organizational rollout plan, and 5-year evolution strategy  

This curriculum produces architects who build platforms that survive companies, not just technologies.
