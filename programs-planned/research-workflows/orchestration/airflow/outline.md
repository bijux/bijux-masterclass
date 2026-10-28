# Airflow Deep Dive

## Module 01 — First Principles: Correctness, Scheduling Semantics, Runtime Model

**Outcome:** you can predict what will run, when, and why—across retries, backfills, and upgrades.

### Core 1 — Architecture & the Orchestration Loop

* Components: scheduler, workers/executor, triggerer, web/UI, metadata DB
* Parse → schedule → queue → execute → state reconcile (and why parse-time code is risky)

### Core 2 — Scheduling Semantics (the real correctness trap)

* Data intervals vs logical dates, timezone discipline
* Catchup/backfill, `max_active_runs`, concurrency knobs
* Timetables: when cron is the wrong model

### Core 3 — Determinism + Idempotency as the DAG contract

* Deterministic DAG structure, stable task IDs, restartability
* Exactly-once *effects* via atomic writes + partition contracts
* Anti-patterns: mutable globals, “now() logic”, implicit state

### Core 4 — Metadata DB as source of truth

* What the DB tracks and why it dominates runtime behavior
* Common failure modes and what to inspect when “stuck”

### Core 5 — Executors & cost model

* Executor contract and isolation boundaries
* Queue time vs run time vs IO overhead (why “fast tasks” still choke)

**Lab:** build an ETL DAG with strict output contracts + safe backfill (no accidental recompute).

---

## Module 02 — Authoring Building Blocks: Task SDK, Operators, XCom, Sensors, Mapping

**Outcome:** you author scalable DAGs without XCom abuse, slot-waste sensors, or untestable control flow.

### Core 1 — Public interface & Task SDK (Airflow 3)

* `airflow.sdk` as the stable DAG authoring surface ([Apache Airflow][4])
* Task SDK purpose and runtime resource access model ([Apache Airflow][5])

### Core 2 — Operators vs TaskFlow vs “pure tasks”

* When TaskFlow clarifies intent vs hides cost/debuggability
* Templating, params, macros (logical-date discipline)

### Core 3 — XCom discipline: metadata only

* Strict “references only” rule; artifact-store pattern
* Serialization traps and accidental payload blowups

### Core 4 — Sensors done right: deferrable + triggerer

* Poke vs reschedule economics
* Deferrable waiting as default expectation; triggerer capacity planning

### Core 5 — Dynamic task mapping & runtime expansion

* `expand`, `expand_kwargs`, partials; fan-out limits
* Mapping vs loops: scheduler load, observability, debuggability

**Lab:** runtime-discovered N items → mapped fan-out → aggregate via artifact references only.

---

## Module 03 — Production Airflow: Reliability, Observability, Performance, CI/CD, Deploy

**Outcome:** you can run Airflow as a service with measurable health, controlled blast radius, and reproducible deployments.

### Core 1 — Scheduler/triggerer performance engineering

* Parse-time budgets, DAG import errors, heartbeat pressure
* Zombie tasks, stuck queues: triage decision trees

### Core 2 — Scaling execution safely

* Celery vs Kubernetes reality: tuning, isolation, noisy neighbors
* Pools/queues/priority weights for fairness and backpressure

### Core 3 — Observability that matters

* The only metrics that count: queue time, run time, retries, success rate
* Logs shipping, auditability, tracing hooks

### Core 4 — Alerting after SLAs (Airflow 3)

* SLAs removed; replace with **Deadline Alerts + Notifiers** ([cwiki.apache.org][6])
* Failure callbacks and escalation policies

### Core 5 — CI/CD + deployment packaging (Airflow 3)

* Static checks + import tests + deterministic DAG tests
* Ephemeral smoke tests
* **DAG Bundles** and version-safe deployments ([Apache Airflow][7])

**Lab:** CI that fails on slow parsing, broken imports, and non-idempotent task behavior.

---

## Module 04 — Advanced: Data-Aware Scheduling, Extensibility, Governance, Decision Boundaries

**Outcome:** you scale teams and complexity without turning Airflow into a brittle monolith.

### Core 1 — Data-aware scheduling with Datasets at scale

* Dataset-triggered workflows; mixed time + dataset schedules
* Failure modes: partial datasets, late arrivals, duplicate triggers

### Core 2 — Advanced scheduling: timetables + logical-date pitfalls

* Custom timetables; business calendars; backfill correctness
* Migration away from legacy `ds` mental models

### Core 3 — Extensibility without footguns

* Writing maintainable hooks/operators/triggers
* Provider packaging, versioning, public interface boundaries

### Core 4 — Governance & multi-tenancy

* RBAC, secrets boundaries, policy via pools/queues
* Guardrails for mapping runaway fan-out

### Core 5 — When not to use Airflow

* Airflow vs Temporal/Dagster/Prefect: decision rules
* Orchestration vs compute vs streaming boundaries; hybrid patterns

**Capstone:** dataset-triggered, dynamically mapped, deferrable waiting, CI/CD-protected, deadline-alerted pipeline + ops runbook.
