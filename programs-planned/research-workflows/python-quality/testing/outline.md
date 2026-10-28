# Python Testing Deep Dive

## Module 01: Foundations — What Tests Prove and How Systems Fail

### 01. Mental Model: Risk, Layers, Determinism

* Unit vs integration vs system: guarantees, blind spots, typical defect locations
* Determinism as a requirement; flakiness as compounding debt
* Testability as architecture: pure core + explicit I/O edges + injectable time/randomness
* **Diagram:** *Risk hotspots → test layers → feedback speed vs confidence*

### 02. `unittest` Mastery (Baseline Skill)

* `TestCase` lifecycle, setup/teardown, subtests, custom assertions
* `unittest.mock`: patching rules, `autospec`, call contracts, common traps
* Where `unittest` remains optimal (stdlib-only, constrained environments)

### 03. pytest Mastery (Modern Default)

* Discovery, assertion introspection, parametrization as a coverage mechanism
* Fixtures: scope, composition, autouse discipline; avoiding fixture tar pits
* Markers/selection; `xfail`/`skip` as controlled, reviewed debt

### 04. Test Design: Golden Path, Negative Space, Contracts

* Golden path tests (representative success) vs edge/failure tests (representative “negative space”)
* Contract tests for boundaries: file formats, schemas, CLI/API surfaces
* Regression tests as minimal repro artifacts that permanently lock in fixes

### 05. Test Doubles: Mocks vs Fakes vs Real Components

* Prefer fakes/adapters over mocks for behavior-rich boundaries
* Interaction tests vs state tests; when each is legitimate
* Consumer-driven contracts for integrations (stable interfaces, reproducible failures)

## Module 02: pytest at Scale — Fixtures, Data-Driven Parametrization, Integration, CLI

### 01. Fixture Architecture Without the Tar Pit

* Fixture layering as an explicit graph; naming and scope hygiene
* **Yield fixtures** for resource lifecycles (DB sessions, servers, temp workspaces)
* Testing context managers/decorators: asserting enter/exit semantics correctly

### 02. Parametrization as a System (Data-Driven Testing)

* Parametrize configs, environments, feature flags—not just scalar inputs
* **External case loading**: CSV/JSON/YAML → parametrization with readable IDs
* Indirect parametrization + factory fixtures to control setup cost and readability

### 03. Plugins That Pay Rent

* `pytest-cov`, `pytest-xdist`, `pytest-timeout`, `pytest-mock`
* Observability hooks: `caplog`, `capsys`, `recwarn`
* Reruns only as quarantine tooling; never as a substitute for root-cause fixes

### 04. Integration Testing Patterns (FS/Subprocess/HTTP/DB)

* Stable boundaries: filesystem and subprocess without nondeterminism
* DB tests: transactions, ephemeral DBs, migrations, teardown guarantees
* Containers only when justified; in-process fakes when equivalent

### 05. CLI/Application Interface Testing (Click/Typer/Argparse)

* Black-box entrypoint tests: exit codes, stdout/stderr, files produced
* Click/Typer harness patterns; golden outputs vs structured outputs
* Contract-first CLI testing to prevent snapshot rot
* **Diagram:** *CLI contract: inputs → outputs/artifacts → exit code*

## Module 03: Property-Based Testing — Hypothesis as a Bug Generator

### 01. Mental Model: Properties, Oracles, Shrinking

* Example tests vs properties: complementary layers, different failure discovery modes
* Shrinking as automatic minimization; designing for readable counterexamples
* High-ROI targets: pure transforms, parsers, serializers, validators

### 02. Strategies Deep Dive: From Primitives to Domain Models

* Core strategies + `@composite` for structured records
* Schema-driven generation; constraints that mirror real invariants
* Forced edge cases: NaNs, Unicode, empties, extremes, adversarial strings

### 03. Stateful Testing: Ordering and Lifecycle Bugs

* State machines for caches, workflows, APIs
* Invariants over operation sequences; “fails only after X” discovery
* Controlled I/O boundaries: fakes + clocks; avoid nondeterministic external systems

### 04. Hypothesis in CI: Reproducibility and Budgeting

* Settings: `max_examples`, deadlines, phases, health checks
* Reproducibility: example database + seeds; stable failures
* Placement: unit layer by default; promote found failures into regressions

### 05. Properties for Data Contracts and Serialization

* Round-trip (encode/decode), idempotence, monotonicity, order invariance
* Invalid-data generation and error contracts (fail fast, fail informatively)
* Differential testing: reference vs optimized implementation

## Module 04: Data/ML + Async + Fuzzing — Modern Failure Modes

### 01. Data Pipeline Testing: Validation as a Gate

* Data contracts: schema, ranges, uniqueness, null policies, drift sentinels
* Pandera / Great Expectations-style checks integrated into pytest
* Metamorphic properties for transforms (invariants under safe transformations)

### 02. ML Testing Patterns (Beyond “Accuracy > X”)

* Deterministic training/inference: seeds, fixed splits, controlled nondeterminism
* Robustness: invariances, monotonicity, calibration, drift checks as artifacts
* Fairness/bias: metrics-as-artifacts, thresholds, and regression guards

### 03. Async Testing: Determinism Under Concurrency

* `pytest-asyncio`: event loop control, cancellation semantics, task lifecycles
* Controlling time/I/O: fake clocks, patched sleeps, mocked clients
* Race/timeout failures: reproduction-first methodology
* **Diagram:** *Event loop + tasks + controlled clock → reproducible concurrency tests*

### 04. Fuzzing: When It Beats Hypothesis

* Mutation vs grammar-based fuzzing; selecting targets with real payoff
* Tooling: Atheris (coverage-guided), harness design principles
* Oracles and crash triage: defining “bug” precisely to avoid false positives

### 05. Fuzz Harness Engineering + Corpus Discipline

* Small harnesses win: stable entrypoints, strict time/memory limits
* Corpus management: seeds, minimization, regression corpora
* CI strategy: scheduled fuzzing (nightly/weekly), not per-PR by default

## Module 05: Production Testing — CI, Coverage, Governance, Sustainability

### 01. Suite Architecture: Taxonomy, Layout, Speed Budgets

* Unit/integration/e2e separation via markers and directory structure
* Speed budgets and promotion rules; quarantine lane for slow/flaky tests
* Failure readability as a first-class design requirement

### 02. Coverage and Its Lies (Using It Without Worship)

* Statement vs branch; when mutation testing is worth it
* Coverage thresholds as guardrails, not success criteria
* Coverage targeted to risk hotspots and public contracts

### 03. Golden/Snapshot/Contract Testing Without Rot

* Golden tests when outputs are stable and meaningful
* Contract tests for schemas/CLI/HTTP; consumer-driven patterns
* Snapshot discipline: small, reviewed, generated from structured data when possible

### 04. Flaky Test Policy + Incident Workflow

* Definition of flaky; fix vs quarantine; never ignore silently
* Ownership, triage SLAs, failure budgets
* Debug workflow: reproduce → minimize → root-cause → regression-lock

### 05. Capstone Blueprint: A Complete Testing System

* Reference stack: pytest + hypothesis + coverage + xdist + timeouts + CI matrix
* Golden-path + regression + property tests + scheduled fuzzing
* Deliverables: taxonomy, fixture architecture, reproducibility knobs, CI gates, triage playbook
