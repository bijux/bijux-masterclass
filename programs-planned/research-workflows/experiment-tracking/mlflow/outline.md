# MLflow Deep Dive

## Module 01: Tracking as the System of Record

### 01. Mental Model: The Governance Surface of MLflow

* MLflow is lifecycle infrastructure (tracking + packaging + registry), not training logic
* Entities: experiments, runs, params, metrics, tags, artifacts
* Reproducibility contract: **code + data reference + environment + artifacts** (missing one ⇒ not reproducible)
* **Diagram:** *Training code → MLflow run → backend store + artifact store → searchable history*

### 02. Logging Strategy + Tag Taxonomy (Make Runs Machine-Queryable)

* Correct semantics: params vs metrics vs tags; step discipline; avoid metric spam
* Artifact discipline: stable structure, reports/plots, dataset pointers vs heavy snapshots
* Team taxonomy template: `data_version`, `feature_set`, `model_family`, `train_mode`, `git_sha`, `pipeline_id`, `owner`

### 03. Autologging vs Manual Logging + Run Lineage

* Autologging: coverage, blind spots, and why it’s insufficient alone
* Manual logging for domain metrics, diagnostics, failure context, and artifacts
* Nested runs: parent/child patterns for HPO, multi-stage pipelines, ablations
* **Diagram:** *Pipeline run → child runs (train/eval/tune) → consolidated comparison*

### 04. Search API Mastery (Comparisons, Automation, Policy Enforcement)

* Filter expressions and ordering (e.g., `metrics.f1 > 0.8 AND params.lr < 1e-3`)
* Programmatic “best run” selection, baselines, regression guards, and promotion triggers
* Building dashboards/automation directly from search + tags (no manual browsing)

### 05. Tracking Server Topology: Stores, Security, Retention

* Backend store (SQL) vs artifact store (S3/GCS/FS): scaling and failure modes
* Deployment patterns: reverse proxy, auth integration, backups/migrations
* Retention/lifecycle: what to keep, what to expire, and how to enforce it

## Module 02: Models — Packaging, `pyfunc`, Evaluation, Registry

### 01. MLflow Models: Flavors, Signatures, and the Environment Contract

* Flavors overview; **`pyfunc` as the universal interface**
* Signatures + input examples: enforceable IO contracts and drift prevention
* Embedded environment in the model artifact (`conda.yaml` / `pip_requirements.txt`): conflict patterns and hardening strategies
* **Diagram:** *Model artifact = code + weights + signature + env spec + artifacts*

### 02. Custom `pyfunc` Deep Dive (Real Deployment Logic)

* `load_context()` for resource initialization (tokenizers, large tables, GPU handles, config)
* `predict()` as a pure batch function: strict typing, batching strategy, deterministic outputs
* Operational constraints: cold-start, caching, thread-safety, controlled external calls

### 03. Evaluation as an Artifact (Comparable and Auditable)

* Stable evaluation protocol: holdout vs CV, calibration, thresholding
* Store evaluation reports as artifacts (tables/plots), not only scalar metrics
* Dataset lineage: pointers + checksums + metadata (no “mystery data”)

### 04. Registry Contract: Versioning, Aliases, Promotion, Lineage

* Versioning and aliases; promotion gates; stage/alias-driven release control
* Auditability: who/when/why; policy-driven metadata requirements
* Multi-env strategy: dev/stage/prod isolation with traceable lineage

### 05. Serving Interfaces: Real-Time vs Batch Scoring

* Real-time REST serving vs high-throughput batch scoring (distinct operational patterns)
* Packaging for deployment: container builds, dependency pinning, signature smoke tests
* Orchestrator integration (Airflow/Prefect/Argo) and data-platform hooks

## Module 03: Production MLflow — Scale, Compliance, Operational Excellence

### 01. Production Topology: Multi-Team Governance + SLO Thinking

* Isolation: experiments, naming conventions, permissions boundaries
* Artifact store design: partitioning, retention rules, lifecycle policies
* Reliability: HA choices, bottlenecks, and failure containment
* **Diagram:** *Teams → tracking server → shared artifact store → registry → deployment targets*

### 02. Scaling: Logging Volume and Artifact Economics

* Preventing bloat: compress, chunk, deduplicate, and externalize heavy assets
* Large-model patterns (embeddings/LLM adapters): what to store vs reference
* Explicit cost vs reproducibility tradeoffs with enforceable policy

### 03. Security and Compliance: “Do Not Log” + Secrets Hygiene

* AuthN/AuthZ and network boundaries; least-privilege access patterns
* PII/PHI constraints: redaction/hashing and audit posture
* Secrets: never in params/tags/artifacts; use env vars, mounted files, Vault/KMS

### 04. Observability and Debugging the Lifecycle

* Lineage reconstruction via tags and search; consistent metadata for queries
* Debugging run failures: environment replay, artifact inspection, model load failures
* Rollback: alias-based rollback, promotion audit trails, incident playbooks

### 05. Capstone: End-to-End Lifecycle With Enforced Contracts

* Train → track → evaluate → register → gate → deploy → monitor
* Hard contracts: signatures, dataset IDs, environment lock, promotion policy
* Reference repo layout: tracking utils, model package, CI checks, deploy hooks
