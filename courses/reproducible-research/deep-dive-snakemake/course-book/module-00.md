# Snakemake Deep Dive

## Module 01: First Principles — The File-DAG Contract

### 01. Mental Model: Rules → Files → DAG → Jobs

* Snakemake is a **file-driven DAG engine**, not a scripting framework
* Inputs/outputs define state; re-runs via timestamps/checksums and parameter changes
* Reproducibility and provenance as non-negotiable constraints
* **Diagram:** *Rules + file patterns → DAG → scheduled jobs*

### 02. Rule Anatomy: Wildcards, Resources, and Safe File Semantics

* Inputs/outputs/params/log/benchmark; wildcards and constraints to prevent ambiguity
* `threads` vs `resources` (time/mem/partition/GPU): correctness and scheduling implications
* `temp()`, `protected()`, `ancient()`, `touch()`—when they’re safe vs when they create lies
* **`shadow`**: per-job working directories to reduce NFS contention and isolate temp files

### 03. Configuration Discipline: Config-as-Data + Profiles

* `config.yaml` as the single source of truth; no hidden globals
* Profiles as “site policy” (cluster args, default resources, latency-wait, retries)
* Validation patterns: schemas, defensive defaults, and fail-fast config checks

### 04. Modularity: Includes, Modules, Interfaces, and Boundaries

* `include:` vs `module` vs subworkflows; when each is justified
* Split by stage with explicit contracts (file formats, naming, metadata)
* Shared utilities without state leakage; keep “library code” pure and testable

### 05. Observability: Debugging the DAG, Not the Symptoms

* `-n`, `--reason`, `--summary`, `--dag`, `--rulegraph`, `--lint`
* Why a rule re-runs: inputs/code/params/env changes; diagnosing with evidence
* Failure triage: isolate minimal repro, logs per rule, strict output discipline

## Module 02: Advanced Mechanics — Dynamic DAGs, Integrity, and Performance Patterns

### 01. Wildcard Mastery: Metadata-Driven Expansion Without Explosions

* Sample sheets/metadata → `expand`, `glob_wildcards`, structured target lists
* Preventing accidental cartesian products; constraints as correctness tools
* **Validation checkpoints** for “are all samples present?” before full expansion

### 02. Checkpoints: Dynamic DAGs Done Safely (and When They’re a Smell)

* Two-phase execution model; reading discovered outputs correctly
* Discovery traps: nondeterminism, “moving target” outputs, hidden dependencies
* Strong pattern: external discovery logic is deterministic; checkpoint validates/stabilizes

### 03. Data Integrity and Provenance as First-Class Outputs

* Logs/benchmarks/reports per rule; structured artifact layout
* Provenance: tool versions, params, config snapshots, `--report` discipline
* Rerun semantics beyond timestamps: parameter drift and environment changes

### 04. Environments and Containers: Reproducibility Without Slowness

* Per-rule `conda:` (or container) as default; pinning versions and channels
* Singularity/Apptainer realities on HPC (binds, caches, performance)
* Avoiding “env churn”: caching, reuse strategy, and minimizing solver pain

### 05. Performance Patterns: DAG Shape, Scheduler Load, and I/O

* `group` / `localrules` to control scheduler overhead and job granularity
* Scatter/gather patterns; staging temp intermediates; compression tradeoffs
* Filesystem constraints: metadata storms, small-file pathologies, and mitigation

## Module 03: Production Snakemake — HPC/Cloud Execution, Error Handling, Data Locality, Governance

### 01. Execution Backends: Cluster-First Operation via Profiles

* Local vs cluster vs cloud backends; what changes in failure and latency behavior
* SLURM essentials through profiles; resource modeling as policy (not ad hoc flags)
* **Custom jobscript templates**: pre/post hooks, modules, scratch setup, advanced allocation

### 02. Robustness: Atomic Outputs, Exit Codes, and Recovery Semantics

* Atomic writes, temp staging, and safe cleanup; resumability by construction
* **Error handling**: exit codes, optional failures, and explicit “fail vs continue” policy
* Partial outputs, `--rerun-incomplete`, checkpoint recovery, retries/backoff discipline

### 03. Scaling + Data Locality: Remote Files and Explicit Staging

* **Remote inputs/outputs**: `remote()`, `--default-remote-provider` (S3/GS/HTTP) and caching
* Data locality on HPC: `shadow` + explicit stage-in/stage-out to node-local scratch
* Controlling DAG width and batching to keep the scheduler and filesystem stable

### 04. Testing and CI/CD for Workflows (Real, Not Cosmetic)

* Rule-level tests with minimal fixtures; integration tests for critical DAG paths
* Linting, pinned profiles, reproducible env builds in CI
* Regression tests: outputs + metadata/provenance checks, not just file existence

### 05. Maintainability: Contracts, Versioning, Workflow Catalogues, Team Practice

* Stable interfaces between modules (formats, schemas, naming, directory conventions)
* Versioned configs/workflows; change control; review checklists for correctness/perf
* Workflow catalogues/registries: reusable modules with explicit semantic versioning

## Module 04: Scaling Patterns — Modularity, Interfaces, CI Gates, and Executor-Proof Semantics

### 01. Modularity That Scales: `include`, `module`, and Real Boundaries

* Why “split files” is not modularity: **interfaces** are the unit of reuse
* `include:` for organization; `module` for **reusable components with pinned versions**
* Avoiding state leakage: keep shared code pure; no hidden globals, no implicit IO
* Failure modes: circular includes, wildcard drift, hidden cross-module dependencies
* **Proof hooks:** `--list-rules`, `--rulegraph`, `--dag`, “consumer stays stable while provider internals change”

### 02. Interface Contracts: Naming, Schemas, Versioned Outputs, and Compatibility

* Files as APIs: explicit output layout, naming invariants, and format guarantees
* Config + metadata schemas (fail fast): required fields, allowed values, cross-field constraints
* Versioning strategy: `results/v1/...` vs `results/v2/...` and when to use `rule version:`
* Compatibility rules: what changes are non-breaking vs breaking (and how to force reruns correctly)
* **Failure signatures:** silent schema drift, ambiguous targets, “it ran but outputs are wrong”
* **Proof hooks:** schema break → hard failure; compatible change → no rerun; breaking change → forced rerun + version bump

### 03. Determinism and Drift Control: CI as a Correctness Boundary

* “Ran once” is not correctness: **plan stability + output stability + provenance stability**
* CI gates: `--lint`, `--dry-run`, rule/unit tests with minimal fixtures, golden outputs
* Detecting hidden entropy: timestamps, random seeds, external state, non-pinned envs
* Provenance diffs as regressions: stable params/config snapshots, `--list-changes` discipline
* **Failure signatures:** flaky tests, nondeterministic outputs, “works locally” drift
* **Proof hooks:** intentional nondeterminism → CI fails; deterministic fix → CI passes with stable diffs

### 04. Resource Semantics With Evidence: Dynamic Resources That Map to Executors

* Dynamic `threads/resources` from wildcards/input sizes (done safely, reproducibly)
* Default-resources as policy; per-rule overrides as exceptions with justification
* Mapping proof: `threads/resources` → executor constraints → rendered jobscript/log evidence
* Scheduler load controls: grouping, job sizing, and explicit batching policies
* **Failure signatures:** oversubscription, queue rejection, “resources ignored”, latency-induced flakiness
* **Proof hooks:** rendered jobscript contains expected directives; intentional under-allocation fails; corrected resources succeed

### 05. Workflow as a Product: Distribution, Pinning, Upgrade Paths, and Team Practice

* Reusable workflow modules with pinned revisions (commit/tag), explicit interfaces, and changelogs
* Repo layout conventions for scale: `workflow/`, `profiles/`, `envs/`, `scripts/`, `tests/`, `schemas/`
* Upgrade discipline: contract-compatible refactors vs breaking interface changes
* Review checklist for teams: interface changes, resource changes, provenance changes, determinism risks
* **Proof hooks:** consumer imports pinned provider; provider refactor does not break consumer; breaking change requires explicit version bump + consumer update
