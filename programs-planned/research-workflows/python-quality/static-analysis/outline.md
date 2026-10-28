# Python Static Analysis Deep Dive

## Module 01: The Static Analysis System — Guarantees, Costs, Boundaries

### 01. Mental Model: Layers, Authority, and the Noise Budget

* Four layers: **format** (Black) → **lint** (Ruff) → **types** (mypy/pyright/pytype) → **hygiene** (deptry/vulture) + **security** (Bandit/pip-audit)
* “Proof” vs “heuristic”: what each tool can guarantee, and where it will lie to you
* Noise budget as policy: warnings must be actionable or they get removed
* **Diagram:** *Single `pyproject.toml` policy → tools → CI gates → developer feedback loop*

### 02. Formatting as Normalization: Black (or Ruff Format) as a Hard Gate

* Deterministic formatting reduces churn and stabilizes lint/type diffs
* Boundary rule: never duplicate formatter concerns in linters
* Choose exactly one formatter and enforce it everywhere (editor + pre-commit + CI)

### 03. Ruff as the Frontline: Bug Rules + Documentation Hygiene

* Correctness-first rules (imports, exceptions, undefined names, bad patterns) before style
* **Docstring enforcement**: Ruff “D” rules (pydocstyle) and choosing a docstyle (NumPy/Google) that matches your team’s typing habits
* Keeping Ruff fast and low-noise: rule selection by defect yield, not ideology

### 04. Type Checking Landscape: mypy vs pyright vs pytype (Pick a Truth Source)

* **pyright**: speed + IDE alignment + strong inference; great default for many teams
* **mypy**: deep configurability + plugins; best when your stack needs it
* **pytype**: alternative inference model; niche use, evaluate explicitly
* Primary-checker rule: one source of truth; dual-check only with a clear ROI

### 05. “Beyond Lint”: Dependency Hygiene and Security Scanning as Parallel Tracks

* **deptry**: declared vs imported deps (missing/unused deps are production bugs)
* **vulture**: dead code detection (with false-positive controls for public APIs)
* **Bandit** (SAST-ish) and **pip-audit/Safety** (CVE scanning): separate CI stages, separate expectations

## Module 02: Policy & Configuration — Make Tools Coherent in Real Codebases

### 01. `pyproject.toml` as a Policy Contract (With Ownership)

* Centralize config; document intent; keep it reviewable in PRs
* Exclusions: generated/vendored/build outputs with explicit rationale
* Directory policies as design: `src/` vs `tests/` vs `scripts/` (different risk profiles)

### 02. Ruff Configuration at Scale: Targets, Overrides, and Suppressions

* Rule selection by risk category: bug → maintainability → style
* Target-specific allowances: tests can be pragmatic; production code cannot
* Suppressions as debt: `# noqa: <code>` only, localized, justified, auditable

### 03. Typing Policy Engineering: Strict Where It Pays, Practical Where It Doesn’t

* Gradual typing without “Any leakage” spirals
* Public API strictness; internal glue pragmatic; typed boundaries as contracts
* Stubs (`.pyi`), `Protocol`, and narrowing patterns that reduce ignores

### 04. Runtime Magic: Pydantic/ORM Strategy (Non-Negotiable in Production)

* Pydantic/attrs/dataclasses and ORMs: why they break naïve typing
* **mypy plugins** (when needed) vs **pyright’s handling** (when sufficient)
* Practical rule: pick the checker that best matches your framework reality, not preference

### 05. Cross-Tool Consistency: Stop Contradictions Before They Ship

* Align Python target versions, import roots (`src/` layout), namespace packages
* Ensure editor/CLI/CI agree (same config, same working dir, same interpreter)
* Avoid duplicate checks (imports once, docstrings once, formatting once)

## Module 03: Production Static Analysis — CI, Monorepos, Adoption, Sustainability

### 01. CI Pipeline Design: Layered Gates, Deterministic Results

* Recommended gates: **format → ruff → typecheck → deptry/vulture → security → tests**
* Pin versions, cache aggressively, fail fast
* Merge-blocking vs advisory checks: explicit policy, no ambiguity

### 02. Incremental Adoption (Legacy-Safe): Baseline + Ratchet

* Baseline current violations; enforce “no new issues” immediately
* Tighten in the right order: Ruff bug rules → typing on public APIs → deps → dead code → docstrings
* Progress tracking: budgets, trendlines, and scheduled tightening

### 03. Monorepos and Multi-Package Reality: Paths, Roots, Versions

* Multiple packages, multiple Python versions, different policies per target
* Path/root resolution: `src/` layouts, namespace packages, per-package configs
* Keeping analysis stable across tooling and virtualenv boundaries

### 04. Developer Workflow: IDE Alignment, Pre-commit, and Reproducible Envs

* Choose the authoritative type checker in-editor (pyright/Pylance or mypy) and match CI
* Pre-commit for fast local feedback; keep slow checks in CI
* Stable environments (uv/pip-tools/poetry) so “works on my machine” disappears

### 05. Capstone: A Reference “Static Analysis Stack” Blueprint

* Black (format gate)
* Ruff (bug lint + import hygiene + docstring policy)
* One primary type checker (mypy **or** pyright; pytype optional)
* deptry + vulture (semantic hygiene)
* Bandit + pip-audit/Safety (security track)
* Governance: rule-change RFCs, suppression ownership, periodic audits and tightening
