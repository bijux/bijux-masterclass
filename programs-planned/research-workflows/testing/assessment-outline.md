Below is a tight 3-module plan that hits your targets (unittest, `unittest.mock`, Hypothesis, `conftest.py`), plus core patterns and anti-patterns at a serious depth.

# Module 1 — Foundations & Base Patterns (pytest + unittest)

1. Test Architecture & Taxonomy

   * Unit vs component vs integration. Determinism, isolation, reproducibility. Testing pyramid and budget.
2. Test Organization & Discovery

   * Layout: `tests/`, package mirrors, `test_*.py`. Naming rules that surface intent. Keeping tests import-clean.
3. pytest + unittest Interop

   * When to prefer `pytest` runner/fixtures with `unittest.TestCase`. Avoid subclassing by default; use functions unless xUnit features are needed.
4. `conftest.py` as Composition Root

   * Fixture scoping (function/class/module/session), autouse with restraint, dependency injection via fixtures, layering (thin fixtures + helpers).
5. Assertion Discipline

   * `assert` vs `self.assert*`; custom assertion helpers; failure messages that diagnose root cause; differential testing & golden files with strict update gates.
6. Parametrization & Matrix Testing

   * `@pytest.mark.parametrize`, cartesian products, shrinking the matrix (pairwise), marking slow/flaky, selective CI shards.
7. IO & Time Boundaries

   * Temp dirs (`tmp_path`), atomic file writes, `freezegun`/clock fixtures; random seeds and reproducible RNG; locale/timezone guards.
8. Async & Concurrency Basics

   * `pytest.mark.asyncio`, taskgroups, fake executors; not blocking the loop; quarantining thread/process pools in tests.
9. Anti-Patterns (Base Level)

   * Fixtures that hide state; overuse of `autouse`; shared mutable globals; order-dependent tests; broad try/except swallowing; sleeping for timing.
10. Quality Gates & Tooling

* Coverage thresholds by layer, mutation testing (Hypothesis + mutmut), linters for tests, xdist/flake hunting, test runtime budgets.

**Outcomes:** Clean structure, fixture discipline, deterministic tests, minimal surface for future brittleness.

---

# Module 2 — Test Doubles & Mocking Discipline (unittest.mock)

*(Assuming “nmock” = `unittest.mock`.)*

1. Test Doubles Taxonomy

   * Dummy/Stub/Spy/Mock/Fake; prefer fakes where feasible; verify state before interactions.
2. `mock` Fundamentals with Spec Safety

   * `spec=True`, `autospec=True`, `create_autospec`; preventing attribute typos; signature conformance.
3. Where & How to Patch

   * Patch the **use site**, not the definition site; `patch`, `patch.object`, context vs decorator vs fixture forms; cleanup guarantees.
4. Side Effects & Returns

   * `side_effect` for exceptions/iterables; chaining call behaviors; `wraps` for partial real behavior; spies.
5. Filesystem/OS/Env/Time

   * Patching `Path`, `open`, env vars; clock seams; temp dirs + fake FS libraries trade-offs; subprocess isolation.
6. Network & External Services

   * Session-level fakes for HTTP (responses/httpx mocks), contract tests at the port boundary; retry/circuit tests with deterministic timers.
7. Async & Concurrency Mocks

   * `AsyncMock`, awaiting rules, patching coroutines, ensuring tasks complete; thread/process boundary seams (queues, pipes).
8. Interaction Testing Rules

   * Verify the **minimal** interactions; avoid asserting incidental calls; structured call assertions; tolerating harmless extra kwargs.
9. Anti-Patterns (Mocking)

   * Over-mocking internals; patching transitive deps; brittle call-order assertions; leaking patches; mocking standard library RNG/time without fixtures.
10. Patterns & Checklists

* “Fake-first, mock-last” heuristic; capability seams; fixture-backed patch factories; contract tests for adapters; rollback to state checks when possible.

**Outcomes:** Safe, spec-checked mocks; stable seams; fewer brittle, interaction-heavy tests.

---

# Module 3 — Property-Based Testing with Hypothesis (strategies & beyond)

1. Hypothesis Core Model

   * Generators vs search; shrinking; examples database; falsification mindset; health checks.
2. Strategies 101

   * `st.integers()`, `text()`, `lists()`, `dictionaries()`, `one_of`, `tuples`; closed domains; bounds and invariants.
3. Combinators & Composite Strategies

   * `@st.composite` for dependent data; `builds` for dataclasses/pydantic; constraining while keeping shrinkability.
4. Custom & Domain Strategies

   * Regex/text alphabets; numeric stability (floats with `allow_nan=False`, `decimals`); graph/tree generators.
5. Invariants & Oracles

   * Round-trip (serialize/deserialize), algebraic laws (associativity, idempotence), metamorphic relations; model-based oracles.
6. Stateful Testing

   * Rule-based state machines; sequences of ops; verifying typestate contracts; differential testing against reference impls.
7. Integration with pytest/unittest

   * Parametrized + PBT hybrids; per-test settings (deadline, max examples); seeding and DB isolation in CI.
8. Performance & Diagnostics

   * Targeting, example simplification, shrinking triage; minimizing `assume` (filtering); profiling failing cases; coverage hints.
9. Anti-Patterns (Hypothesis)

   * Over-filtering with `assume`; huge objects by default; unstable RNG/clock inside property; hidden I/O; non-idempotent oracles.
10. Patterns & Rollout

* Start with contracts on pure code; add metamorphic tests at edges; property suites as regression guards; ghostwriter to bootstrap.

**Outcomes:** Domain-faithful strategies, actionable counterexamples, regression-proofing through properties.

---

## Deliverables per module

* **Templates:** `conftest.py` skeletons, patch-factory fixtures, Hypothesis strategy modules.
* **Checklists:** “Add a test” PR checklist; mocking checklist; Hypothesis property checklist.
* **Reference examples:** One small service (file→transform→HTTP sink) tested across the three disciplines.

If you want, I’ll produce the starter repo layout with `pyproject.toml`, `pytest.ini`, a `tests/` scaffold (fixtures, fakes, property suites), and exemplar tests demonstrating each item above.
