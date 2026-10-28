
# The Complete, Practical Primer to Python Testing
**pytest • unittest • Hypothesis (property-based testing) • Strategies • Patterns • CI • Beyond**

> A production-grade guide for building **fast**, **deterministic**, and **high-signal** tests in serious Python codebases.

---

## 0) Why test at all? (Executive summary)

- **Confidence:** Ship without fear. Tests detect regressions before users do.
- **Design pressure:** Good tests force modular, explicit, dependency-injected code.
- **Documentation:** Executable examples clarify intended behavior and edge cases.
- **Refactor safety:** Cleanups are easy when invariants are specified and enforced.
- **Reproducibility:** Deterministic tests make bugs finite and debuggable.

**Non-goals:** 100% line coverage, testing trivial getters, or snapshotting complex outputs without invariants.

**Primary goals:** High **defect-detection rate** at **low maintenance cost** and **short feedback loops**.

---

## 1) Test taxonomy: choose the right level for the job

| Level | Scope | Primary value | Pitfalls | When to prioritize |
|------:|------|---------------|----------|--------------------|
| Unit | Single function / class | Fast, precise failure localization | Over-mocking, brittle internals | Core logic, invariants, algorithms |
| Component | Small set of modules with fakes | Interface correctness, realistic edges | Fake drift vs real infra | IO boundaries, adapters |
| Integration | Real dependencies (DB, FS, net) | Contract correctness under realism | Slower, flakier | Critical adapters, migrations |
| End-to-end | Full system via public API/CLI | User-centered confidence | Slow, opaque failures | Very few, high-value scenarios |
| Property-based | Generative at any level | Spec coverage beyond hand-picked cases | Poorly stated properties | Core algebra/invariants/contracts |
| Contract / Golden | API stability & backwards-compat | Drift detection | Overfitting to current output | Public APIs, file formats |

Heuristic: **80–90%** unit/property, **10–20%** integration/e2e. Keep **one** end-to-end “walking skeleton”.

---

## 2) `unittest` in 10 minutes (baseline you can always fall back on)

### 2.1 Minimal structure

```python
# test_example_unittest.py
import unittest
from mypkg.mathops import clamp

class TestClamp(unittest.TestCase):
    def test_in_range(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_below(self):
        self.assertEqual(clamp(-1, 0, 10), 0)

    def test_above(self):
        self.assertEqual(clamp(11, 0, 10), 10)

if __name__ == "__main__":
    unittest.main()
```

### 2.2 Setup/teardown
```python
class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = connect_for_tests()  # expensive, class-scoped

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        self.db.reset()  # fast, per-test cleanup
```

### 2.3 Pros/cons
- ✅ Batteries included, explicit, no magic.
- ❌ Verbose assertions, weaker fixtures/parametrization ergonomics than pytest.

If team is split: write tests compatible with **both**—pytest runs `unittest` tests seamlessly.

---

## 3) `pytest`: productivity and power

### 3.1 What you actually use daily
- **Function tests** with simple `assert`.
- **Fixtures** for clean setup/teardown & dependency injection.
- **Parametrization** for cross-product testing.
- **Markers** to group/select/skip.
- **Plugins**: `xdist` (parallel), `benchmark`, `cov`, `mock`, `hypothesis` (integration).

### 3.2 Minimal example
```python
# test_example_pytest.py
from mypkg.mathops import clamp

def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10
```

Run: `pytest -q`

### 3.3 Fixtures (DI without pain)
```python
# conftest.py (auto-discovered by pytest)
import tempfile, pathlib, shutil
import pytest

@pytest.fixture(scope="session")
def tmp_repo():
    path = pathlib.Path(tempfile.mkdtemp(prefix="repo-"))
    try:
        (path / "README.md").write_text("# test-repo\n")
        yield path
    finally:
        shutil.rmtree(path)
```

Usage:
```python
def test_repo_readme(tmp_repo):
    assert (tmp_repo / "README.md").exists()
```

**Scopes:** `function` (default), `class`, `module`, `package`, `session`. Choose the **lowest** scope that amortizes cost without introducing inter-test coupling.

### 3.4 Parametrization
```python
import pytest
from mypkg.mathops import clamp

@pytest.mark.parametrize("x,lo,hi,expected", [
    (5, 0, 10, 5),
    (-1, 0, 10, 0),
    (11, 0, 10, 10),
])
def test_clamp_param(x, lo, hi, expected):
    assert clamp(x, lo, hi) == expected
```

### 3.5 Useful builtin fixtures
- `tmp_path` / `tmp_path_factory`: isolated filesystem.
- `capsys` / `caplog`: capture stdout/logging.
- `monkeypatch`: replace env vars/attrs.
- `request`: introspection, dynamically add finalizers.

### 3.6 Markers and selection
```python
# pytest.ini
[pytest]
markers =
    slow: long-running tests
    net: tests requiring network

# Mark & run
@pytest.mark.slow
def test_big_case(): ...

# CLI
pytest -m "not slow" -q
```

### 3.7 xfail/skip
```python
import sys, pytest

@pytest.mark.xfail(reason="awaiting fix", strict=True)
def test_pending():
    assert 0

@pytest.mark.skipif(sys.platform == "win32", reason="not supported")
def test_posix_only(): ...
```

---

## 4) Property-based testing with Hypothesis

### 4.1 Why: tests that **discover** edge cases you didn’t imagine
- Generates many inputs, shrinks failing examples to minimal counterexamples.
- Encodes **invariants** (e.g., idempotence, associativity) rather than example values.

### 4.2 Quick start
```python
# test_normalize_hypothesis.py
from hypothesis import given, settings
from hypothesis import strategies as st
from mypkg.text import normalize  # e.g., " ".join(s.split()).lower()

@given(st.text())
@settings(deadline=None)  # avoid spurious timeouts in CI
def test_normalize_idempotent(s):
    assert normalize(normalize(s)) == normalize(s)

@given(st.text(), st.text())
def test_normalize_casefold_vs_lower(a, b):
    norm = normalize(a + b)
    # Basic invariant: no runs of whitespace
    assert "  " not in norm
```

### 4.3 The strategy zoo (90% you need)
- `st.booleans()`, `st.integers()`, `st.floats(allow_infinity=False, allow_nan=False)`, `st.decimals()`
- `st.text()`, `st.from_regex()`, `st.just(x)`, `st.sampled_from(seq)`
- Collections: `st.lists(s, min_size=..., unique=...)`, `st.dictionaries(ks, vs)`
- `st.tuples(...)`, `st.sets(...)`, `st.permutations(seq)`
- Datetime: `st.datetimes()`, `st.dates()`, `st.timezones()`
- Advanced: `st.one_of(...)`, `st.recursive(...)`, `st.builds(cls, ...)`, `st.from_type(T)`
- Stateful: `RuleBasedStateMachine` for APIs with sequences of actions

### 4.4 Custom strategies (composite)
```python
from hypothesis.strategies import composite, integers, text

@composite
def user_ids(draw):
    prefix = draw(text(min_size=1, max_size=5, alphabet="abcdefghijklmnopqrstuvwxyz"))
    num = draw(integers(min_value=0, max_value=9999))
    return f"{prefix}-{num:04d}"
```

### 4.5 Patterns for properties
- **Round-trip:** `decode(encode(x)) == x`
- **Idempotence:** `f(f(x)) == f(x)`
- **Monotonicity:** `x <= y ⇒ f(x) <= f(y)`
- **Associativity/commutativity:** operations on sets, merges, math
- **Invariants:** e.g., output is sorted + deduped; lengths preserved
- **Metamorphic:** when exact outputs unknown, assert relations under transformations
- **Differential testing:** compare two implementations (e.g., new vs reference)

### 4.6 Settings and determinism
- Add `@settings(max_examples=..., deadline=None)` for CI stability.
- Pin **versions**; do **not** pin seeds globally—allow Hypothesis to find bugs. When reproducing a failure, Hypothesis prints a **reproduction seed**—commit it next to the failing test until fixed.

### 4.7 Shrinking discipline
State properties so that **shrunk** counterexamples are still valid. Avoid “accidental” constraints hiding bugs (e.g., `text(min_size=1)` when empty strings should be allowed).

---

## 5) Tests as design: make code testable by construction

### 5.1 Pure core + effectful shell (dependency injection)
- Pure functions depend only on inputs.
- Effectful wrappers receive explicit **env** (clock, RNG, OS, network) so tests can pass fakes.

```python
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Clock:
    now: Callable[[], float]

def timestamped_normalize(clock: Clock, s: str) -> tuple[float, str]:
    # effect (time) is isolated as value, not global
    return clock.now(), " ".join(s.split()).lower()
```

### 5.2 Replace hidden globals with fixtures/fakes
- Never call `datetime.now()`, `random.random()`, or `os.getenv` inside core logic.
- Access them via parameters (fixtures create fakes).

```python
# test_timestamped_normalize.py
import pytest

class FakeClock:
    def __init__(self, t): self._t = t
    def now(self): return self._t

@pytest.fixture
def fixed_clock(): return FakeClock(1700000000.0)

def test_timestamped_normalize(fixed_clock):
    ts, out = timestamped_normalize(fixed_clock, "Hello   World ")
    assert ts == 1700000000.0
    assert out == "hello world"
```

---

## 6) Mocking, fakes, stubs: use sparingly and correctly

- **Prefer fakes** (small in-memory implementations) over deep mocks.
- Use `unittest.mock.patch` to replace process-level calls only at **module boundaries**.

```python
from unittest.mock import patch

def test_env():
    with patch.dict("os.environ", {"API_KEY": "test"}):
        assert load_key_from_env() == "test"
```

**Smells:** mocking standard library internals, or mocking the object under test’s private methods. Better: redesign for injection.

---

## 7) Filesystem, subprocesses, and network safely

- Filesystem: use `tmp_path`, avoid shared temp dirs.
- Subprocess: capture output via `subprocess.run(..., capture_output=True, text=True)` and assert on **exit code** + **stdout/stderr**. Prefer **pure libraries** over shell out.
- Network: mark `@pytest.mark.net`; use **record/replay** (e.g., `pytest-vcr`) or **fakes**. Timeouts mandatory.

---

## 8) Golden tests and snapshots that don’t rot

- Keep **golden files** small, human-auditable, stable (no timestamps). Normalize before writing.
- Assert **invariants** around snapshots (e.g., JSON keys, schema, order) instead of byte-for-byte when appropriate.
- Prefer schema + property checks to massive snapshots.

---

## 9) Performance and memory assertions

- Use `pytest-benchmark` for micro-benchmarks (pin CPU governor in CI).
- Use `pytest` + `tracemalloc` for memory regressions on hot paths.
- Never benchmark random/unseeded workloads; fix input size and seed.

---

## 10) Flakiness: detect, quarantine, eradicate

- **Causes:** time, randomness, concurrency, network, reliance on wall clock.
- **Playbook:**
  1. Re-run with `-k "flaky_test_name" -vv --maxfail=1 --lf` to isolate.
  2. Add logs/diagnostics; **never** add sleeps—replace with deterministic handshakes.
  3. Inject clocks, RNGs, and fakes (see §5).

- Quarantine with marker `@pytest.mark.flaky` and run separately while fixing root cause.

---

## 11) Concurrency testing (threads/async/processes)

- Threads: test **invariants** (no data races), not interleavings.
- Async: use `pytest.mark.asyncio`; avoid real sleeps—use `asyncio.advance_time` via test clock or `freezegun`-style libs.
- Multiprocessing: isolate global state; ensure `if __name__ == "__main__"`; avoid implicit forks on import in tests.

---

## 12) Coverage that means something

- `coverage.py` with **branch coverage**: `pytest --cov=mypkg --cov-report=term-missing --cov-branch`.
- Aim for **risk-weighted** coverage: critical logic at ~100%, glue code less.
- Use **mutation testing** (mutmut / cosmic-ray) to validate test quality.

---

## 13) Structure, naming, and layout

```
repo/
  src/mypkg/...
  tests/
    unit/
    integration/
    e2e/
    data/                 # small, stable fixtures/goldens
  pyproject.toml
  pytest.ini
```

Naming patterns:
- Test modules mirror source modules: `tests/unit/test_mathops.py` ↔ `src/mypkg/mathops.py`.
- One assertion per property; group logically.

---

## 14) CI: deterministic, parallel, cache-friendly

- Pin exact versions of Python and dependencies.
- `pytest -q -n auto` with `pytest-xdist`.
- Cache `.hypothesis/` directory between CI runs (but **don’t** rely on it for signal).
- Fail fast: `--maxfail=1` on PR runs; nightly runs can be exhaustive.
- Upload coverage; keep thresholds realistic but strict on core modules.

---

## 15) Pytest patterns you’ll reuse constantly

### 15.1 Parametrized fixtures (matrix expansion)
```python
import pytest

@pytest.fixture(params=[128, 512, 2048])
def chunk_size(request): return request.param

def test_pipeline_works(sample_docs, chunk_size):
    out = run_pipeline(sample_docs, chunk_size=chunk_size)
    assert len(out) >= 0
```

### 15.2 tmp_path + monkeypatch combo
```python
def test_config_loader(tmp_path, monkeypatch):
    p = tmp_path / "config.ini"
    p.write_text("[main]\nthreads=4\n")
    monkeypatch.setenv("MY_APP_CONFIG", str(p))
    cfg = load_config()
    assert cfg.threads == 4
```

### 15.3 caplog for structured logging assertions
```python
def test_logs(caplog):
    caplog.set_level("INFO")
    do_work()
    assert any("started" in rec.message for rec in caplog.records)
```

---

## 16) Hypothesis: advanced usage

### 16.1 `st.from_type` + type-driven generation
```python
from dataclasses import dataclass
from typing import Tuple
from hypothesis import given
from hypothesis import strategies as st

@dataclass(frozen=True)
class Chunk:
    doc_id: str
    span: Tuple[int, int]
    text: str

# Register strategy for custom type
@st.composite
def chunks(draw):
    text = draw(st.text(min_size=0, max_size=200))
    start = draw(st.integers(min_value=0, max_value=len(text)))
    end = draw(st.integers(min_value=start, max_value=len(text)))
    return Chunk(doc_id="doc", span=(start, end), text=text)

@given(st.lists(chunks(), max_size=30))
def test_spans_non_overlapping_after_canonicalize(chs):
    out = canonicalize(chs)  # your function: sort, dedupe overlaps
    # Invariants
    assert all(a[0] <= a[1] for _, a, _ in out)
    assert out == sorted(out, key=lambda c: c.span[0])
```

### 16.2 Ghostwriter
Hypothesis can **generate tests** as a starting point:
```
hypothesis write mypkg.text:normalize
```
Review and refine; don’t blindly commit.

### 16.3 Stateful testing
Model protocols/APIs as state machines.
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

class Counter:
    def __init__(self): self.x = 0
    def inc(self): self.x += 1
    def dec(self): self.x -= 1

class CounterMachine(RuleBasedStateMachine):
    def __init__(self): super().__init__(); self.c = Counter()

    @rule()  def inc(self): self.c.inc()
    @rule()  def dec(self): self.c.dec()

    @invariant()
    def bounded(self):
        assert abs(self.c.x) < 100  # example invariant

TestCounter = CounterMachine.TestCase
```

---

## 17) Example: Refactor to pure core + property tests (mini RAG-like pipeline)

### 17.1 Core functions (pure)
```python
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class CleanDoc:
    doc_id: str
    text: str

def normalize_text(s: str) -> str:
    # canonical & idempotent
    return " ".join(s.strip().lower().split())

def clean(doc_id: str, text: str) -> CleanDoc:
    return CleanDoc(doc_id=doc_id, text=normalize_text(text))

def chunk(doc: CleanDoc, size: int) -> tuple[tuple[int, int, str], ...]:
    t = doc.text
    return tuple((i, min(i+size, len(t)), t[i:i+size]) for i in range(0, len(t), size))
```

### 17.2 Properties
```python
from hypothesis import given, strategies as st

@given(st.text())
def test_normalize_idempotent(s):
    assert normalize_text(normalize_text(s)) == normalize_text(s)

@given(st.text(), st.integers(min_value=1, max_value=512))
def test_chunk_covers_string(s, size):
    doc = clean("x", s)
    chunks = chunk(doc, size)
    recon = "".join(seg for _,_,seg in chunks)
    assert recon == normalize_text(s)  # chunking preserves normalized content
    # Non-overlapping, ordered
    assert all(a2 == b1 for (_, a2, _), (b1, _, _) in zip(chunks, chunks[1:]))
```

### 17.3 Differential test (reference vs new impl)
```python
def chunk_ref(doc: CleanDoc, size: int) -> tuple[tuple[int,int,str], ...]:
    t = doc.text; res = []
    i = 0
    while i < len(t):
        j = min(i+size, len(t))
        res.append((i, j, t[i:j]))
        i = j
    return tuple(res)

@given(st.text(), st.integers(min_value=1, max_value=256))
def test_chunk_equiv(s, size):
    doc = clean("x", s)
    assert chunk(doc, size) == chunk_ref(doc, size)
```

---

## 18) Test data management: factories vs Hypothesis vs fixtures

- **Fixtures**: realistic, re-usable objects/resources.
- **Factories**: `factory_boy` or simple helpers for combinations.
- **Hypothesis**: explore **data space**; don’t hand-code combinatorial sets.

Rule of thumb: prefer **Hypothesis** for **logic-heavy** code; prefer **factories/fixtures** for **schema-heavy** or **integration** scenarios.

---

## 19) Linting & type-checking are test-adjacent signal

- Run `ruff` (or `flake8`) and `mypy/pyright` in CI alongside tests.
- Type hints let you write **richer Hypothesis properties** (`from_type`), and prevent entire classes of runtime bugs.

---

## 20) Toolbelt & command lines that actually matter

- `pytest -q -n auto --maxfail=1`
- `pytest -k name_substring -x` (stop on first fail)
- `pytest --lf` (last failed) / `--ff` (failures first)
- `pytest --durations=20` (top slow tests) / `-vv` (more info)
- `pytest --cov=src --cov-report=term-missing --cov-branch`
- `pytest -m "not slow and not net"`
- `pytest --hypothesis-show-statistics` (investigate flaky props)

---

## 21) Migration playbook: `unittest` → `pytest` (incremental)

- You can **drop in** pytest without rewriting: it discovers and runs `unittest` tests.
- Gradually replace `self.assertEqual(a, b)` with `assert a == b` in new tests.
- Introduce fixtures for **new** modules; avoid big-bang rewrites.

---

## 22) Common failure smells and fixes

| Smell | Fix |
|------|-----|
| Test passes/fails depending on time | Inject clock / freezegun |
| Non-determinism from RNG | Inject RNG/seed as parameter; avoid global `random` |
| Test depends on order of dict keys | Sort keys or assert invariant that order is irrelevant |
| Over-specified tests break on refactor | Assert invariants, not full snapshots |
| Mocking internals | Design for injection; mock only module boundaries |
| Massive fixture setup across many tests | Split fixtures; use parametrization instead |
| Hidden network/file access | Fail CI offline; use fakes or record/replay |

---

## 23) Example suite: putting it all together

### 23.1 Project tree
```
src/
  app/
    core.py
    io.py
tests/
  unit/
    test_core.py
  integration/
    test_io_integration.py
  conftest.py
```

### 23.2 `src/app/core.py`
```python
from dataclasses import dataclass
from typing import Protocol, Sequence

@dataclass(frozen=True)
class Record:
    id: str
    value: int

def normalize(v: int) -> int:
    return max(0, min(100, v))

def summarize(xs: Sequence[int]) -> tuple[int, int]:
    # min, max
    return (min(xs), max(xs))
```

### 23.3 `tests/unit/test_core.py`
```python
from hypothesis import given, strategies as st
from app.core import normalize, summarize

def test_normalize_examples():
    assert normalize(-5) == 0
    assert normalize(150) == 100
    assert normalize(42) == 42

@given(st.integers(min_value=-10_000, max_value=10_000))
def test_normalize_range(x):
    y = normalize(x)
    assert 0 <= y <= 100

@given(st.lists(st.integers(), min_size=1, max_size=1000))
def test_summarize_invariants(xs):
    lo, hi = summarize(xs)
    assert lo <= hi
    assert lo == min(xs) and hi == max(xs)
```

### 23.4 `src/app/io.py` with explicit deps
```python
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class IOEnv:
    read_text: Callable[[str], str]
    write_text: Callable[[str, str], None]

def canonicalize_file(env: IOEnv, src: str, dst: str):
    s = env.read_text(src)
    out = " ".join(s.split()).lower()
    env.write_text(dst, out)
```

### 23.5 `tests/integration/test_io_integration.py`
```python
import pytest
from app.io import IOEnv, canonicalize_file

class MemFS(dict):
    def read_text(self, path): return self[path]
    def write_text(self, path, data): self[path] = data

@pytest.fixture
def memfs(): return MemFS()

def test_canonicalize_integration(memfs):
    env = IOEnv(read_text=memfs.read_text, write_text=memfs.write_text)
    memfs["a.txt"] = "Hello   WORLD"
    canonicalize_file(env, "a.txt", "b.txt")
    assert memfs["b.txt"] == "hello world"
```

---

## 24) Beyond the basics

- **Mutation testing:** run mutators to see if tests kill them (`mutmut`, `cosmic-ray`).
- **Contract testing between services:** `pact`-style consumer/provider tests.
- **Fuzzers:** Hypothesis is *structured* fuzzing; raw fuzzers can complement at parsers.
- **Static analyzers:** `pyright --verifytypes` drives stricter contracts.
- **Safety net for refactors:** keep a short **golden test** suite for public APIs.

---

## 25) Minimal, opinionated boilerplate (copy/paste)

**`pyproject.toml` (excerpt):**
```toml
[tool.pytest.ini_options]
addopts = "-q --maxfail=1 --disable-warnings"
testpaths = ["tests"]
xfail_strict = true

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
show_missing = true
fail_under = 85
```

**`pytest.ini` (if not using pyproject):**
```ini
[pytest]
addopts = -q --maxfail=1 --disable-warnings
testpaths = tests
xfail_strict = true
```

**`Makefile` (optional):**
```make
test:          ## run tests
\tpytest -q

test-all:      ## run tests with coverage and property stats
\tpytest --cov=src --cov-report=term-missing --cov-branch --hypothesis-show-statistics

lint:
\truff check .

type:
\tpyright
```

---

## 26) Final checklist for a serious project

- [ ] Pure core logic; explicit env for effects.
- [ ] Deterministic tests; no hidden time/RNG/net.
- [ ] Property tests for algebra/invariants on core algorithms.
- [ ] Parametrized examples for known edge cases (hand-picked regressions).
- [ ] Golden tests for public artifacts (stable, normalized, small).
- [ ] Coverage with branch metrics; mutation testing on critical files.
- [ ] Parallel CI with realistic thresholds; cached deps; short PR runs, nightly exhaustive.
- [ ] Fixtures/fakes over mocks; narrow mocks at module boundaries only.
- [ ] Test names describe **properties** and **intent**, not implementation details.

---

### Appendix A: Quick reference — Hypothesis strategies (cheat sheet)

- Primitives: `booleans`, `integers`, `floats`, `complex_numbers`, `decimals`
- Text/bytes: `text`, `binary`, `from_regex`
- Collections: `lists`, `sets`, `tuples`, `dictionaries`
- Datetime: `dates`, `times`, `datetimes`, `timezones`, `timedeltas`
- Typed: `from_type`, `register_type_strategy`, `builds`
- Combinators: `one_of`, `recursive`, `permutations`, `sampled_from`, `just`
- Stateful: `RuleBasedStateMachine`, `@rule`, `@invariant`, `@initialize`
- Tuning: `@settings(max_examples=..., deadline=None, derandomize=True)`

### Appendix B: Useful pytest plugins
- `pytest-xdist` (parallel), `pytest-cov`, `pytest-benchmark`, `pytest-randomly` (order randomization), `pytest-timeout`, `pytest-mock`, `pytest-freezegun`, `pytest-vcr`, `syrupy` (snapshots).

### Appendix C: Anti-patterns to delete on sight
- `time.sleep()` in tests.
- Global mutable state between tests.
- Unseeded randomness in tests (except Hypothesis engine itself).
- External network calls in unit tests.
- Snapshotting entire binary blobs without invariants.
- Overuse of `patch` to reach internals instead of refactoring.

---

**EOM.**
