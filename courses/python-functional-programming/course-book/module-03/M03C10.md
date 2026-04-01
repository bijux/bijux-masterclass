# Module 3: Lazy Iteration and Streaming

## Progression Note
By the end of Module 3, you will master lazy generators, itertools mastery, and streaming pipelines that never materialize unnecessary data. This prepares you for safe recursion and error handling in streams (Module 4). See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus                                   | Key Outcomes                                           |
|--------|-----------------------------------------|--------------------------------------------------------|
| 2      | First-Class Functions & Expressive Python | Configurable pure pipelines without globals           |
| 3      | Lazy Iteration & Generators             | Memory-efficient streaming, itertools mastery, short-circuiting |
| 4      | Recursion & Error Handling in Streams   | Safe recursion, Result/Option, streaming errors        |

## M03C10: Observability for Streams – Counting, Sampling, and Tapping Pipelines Without Breaking Laziness

> **Core question:**  
> How do you add observability to iterator pipelines through counting, sampling, and tapping, using pure or minimally effectful stages that preserve laziness, equivalence, and single-pass processing?

This core concludes **Module 3** by building on **Core 9**'s custom iterators with observability patterns:
- Use side-effect taps for logging/counting.
- Inject callbacks for metrics without globals.
- Handle single-pass and determinism.
- Preserve laziness, purity (where possible), and freshness.

We finalize the **running project** from Core 9 (FuncPipe RAG Builder from `m03-rag.md`) by adding observability, and include cross-domain examples like monitored CSV ETL, sampled logs, and tapped APIs to prove scalability.

**Audience:** Developers debugging or monitoring lazy pipelines without disrupting flow.

**Outcome:**
1. Spot opacity smells like no metrics.
2. Add tap/sample in < 10 lines.
3. Prove obs laws with Hypothesis.

**Laws (frozen, used across this core):**
- E1a — Tap equivalence: tap(S) yields exactly S.
- E1b — Sampler equivalence: sampler(S) yields a stable subset under the sampler’s policy.
- P1 — Explicit effects: Taps are intentionally effectful but confined and explicit; no globals.
- R1 — Reusability: Factories yield fresh obs iters.
- O1 — Observability: Taps log/count while preserving the original sequence and single-pass behavior (no extra iteration or materialization).
- O2 — Tap isolation: cb failures don’t corrupt or reorder the stream; behavior is explicit and tested.
- S1a — Sampling Bernoulli: Sampled subset of input; deterministic seed; order-sensitive.
- S1b — Sampling Periodic: Sampled subset of input; deterministic offset; position-sensitive.
- S1c — Sampling Content-hash: Sampled subset of input; deterministic key; order-insensitive.
- DTR — Determinism: Equal inputs/seed → equal outputs/obs.
- FR — Freshness: Factory calls independent.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Use side-effect taps for logging/counting and pure filter samplers for subsets, injecting callbacks to observe streams without breaking laziness or equivalence.**

### 1.2 Observability in One Precise Sentence

> Taps execute callbacks on items; sampling filters one branch.

In this series, preserves single-pass; explicit effects.

### 1.3 Why This Matters Now

Opaque pipes hard to debug; obs enables metrics without materialization.

### 1.4 Observability in 5 Lines

Tap example:

```python
def make_tap(cb: Callable[[T], None]) -> Transform[T, T]:
    def stage(xs: Iterable[T]) -> Iterator[T]:
        for x in xs:
            cb(x)
            yield x
    return stage
```

Observable.

### 1.5 Minimal Obs Harness (Extends Core 9)

Build on Core 9; add obs helpers. For the stable sampler, `rate` has strict semantics:
- `rate = 0.0` → guaranteed empty sample
- `rate = 1.0` → full input
- `0.0 < rate < 1.0` → approximately that fraction of items, stable per key across runs


```python
from typing import Callable, Iterator, Iterable, TypeVar, Literal, Dict, Any
from collections import deque
import threading
import hashlib
T = TypeVar("T")

def make_tap(cb: Callable[[T], None], on_error: Literal["propagate","suppress"]="propagate") -> Transform[T, T]:

    def stage(xs: Iterable[T]) -> Iterator[T]:
        for x in xs:
            try:
                cb(x)
            except Exception:
                if on_error == "propagate": raise
            yield x
    return stage

def make_counter() -> tuple[Callable[[Any], None], Callable[[], Dict[str, int]]]:
    lock = threading.Lock()
    count = 0
    def cb(_: Any):
        nonlocal count
        with lock: count += 1
    def metrics() -> Dict[str, int]:
        with lock: return {"count": count}
    return cb, metrics

def make_sampler_bernoulli(rate: float, seed: int = 0) -> Transform[T, T]:
    import random
    assert 0.0 <= rate <= 1.0
    def stage(xs: Iterable[T]) -> Iterator[T]:
        rng = random.Random(seed)   # fresh RNG per call → deterministic reuse
        for x in xs:
            if rng.random() < rate:
                yield x
    return stage

def make_sampler_periodic(k: int, offset: int = 0) -> Transform[T, T]:
    assert k > 0
    def stage(xs: Iterable[T]) -> Iterator[T]:
        for i, x in enumerate(xs):
            if (i - offset) % k == 0:
                yield x
    return stage

def make_sampler_stable(rate: float,
                        key: Callable[[T], bytes]) -> Transform[T, T]:
    assert 0.0 <= rate <= 1.0
    denom = 2**64 - 1
    def stage(xs: Iterable[T]) -> Iterator[T]:
        threshold = int(rate * denom)
        for x in xs:
            h = hashlib.blake2b(key(x), digest_size=8).digest()
            val = int.from_bytes(h, 'big')
            if val <= threshold:
                yield x
    return stage

def make_sampler_stable(rate: float,
                        key: Callable[[T], bytes]) -> Transform[T, T]:
    assert 0.0 <= rate <= 1.0
    # 64-bit hash space: rate=0.0 -> empty, rate=1.0 -> full input.
    denom = 2**64
    def stage(xs: Iterable[T]) -> Iterator[T]:
        threshold = int(rate * denom)
        for x in xs:
            h = hashlib.blake2b(key(x), digest_size=8).digest()
            val = int.from_bytes(h, 'big')
            if val < threshold:
                yield x
    return stage
```

Use with compose; e.g., compose(..., make_tap(log), ...). Effects explicit in taps.

---

## 2. Mental Model: Opaque vs Observable

### 2.1 One Picture

```text
Opaque Streams (Blind)                  Observable Streams (Visible)
+-----------------------+               +------------------------------+
| no metrics/logs       |               | taps/counts without consume  |
|        ↓              |               |        ↓                     |
| debug = break flow    |               | sample/peek, lazy            |
| test = guess          |               | callbacks, testable          |
+-----------------------+               +------------------------------+
   ↑ Hidden / Fragile                      ↑ Explicit / Monitorable
```

### 2.2 Behavioral Contract

| Aspect | Opaque | Observable |
|-------------------|------------------------------|------------------------------|
| Visibility | None | Logs/metrics/samples |
| Effects | None | Explicit callbacks |
| Laziness | Preserved | Preserved (no materialization) |
| Testability | Basic | Mock callbacks for asserts |

**Note on Opaque Choice:** Simple runs; else observe.

**When Not to Observe:** No debug; use Core 9.

**Known Pitfalls:**
- Taps mutate globals.
- Sampling nondeterministic without seed.

**Forbidden Patterns:**
- list() for counts; breaks lazy.
- Enforce with grep for list(.

**Building Blocks Sidebar:**
- Tap for side-effects.
- Sampler for subsets.
- Peek for windows.

**Resource Semantics:** Obs adds no external resources (files/sockets); local state is confined inside callbacks.

**Error Model:** Taps propagate; cb errors optional.

**Backpressure:** Obs after heavy, before sinks.

---

## 3. Cross-Domain Examples: Proving Scalability

Production-grade examples using the harness. Each observable, lazy.

### 3.1 Example 1: Monitored CSV ETL (Obs)

```python
def make_obs_csv_pipeline(path: str, max_rows: int) -> tuple[Transform[None, Dict[str, Any]], Callable[[], Dict[str, int]]]:
    cb, metrics = make_counter()
    pipe = compose(
        source_to_transform(make_csv_source(path)),
        make_tap(cb),
        ffilter(lambda r: r.get("status") == "active"),
        make_project({"id": "user_id", "amount": "total"}),
        make_cast({"amount": float}),
        fence_k(max_rows),
    )
    return pipe, metrics
# Usage: pipe, metrics = make_obs_csv_pipeline(...); list(pipe(None)); print(metrics()["count"])
```

**Why it's good:** Count without consume.

### 3.2 Example 2: Sampled Log Tail

```python
def make_obs_log_pipeline(path: str, pattern: str, k: int) -> Transform[None, str]:
    return compose(
        source_to_transform(make_log_source(path)),
        make_sampler_stable(0.1, key=lambda line: line.encode()),
        make_regex_filter(pattern),
        fence_k(k),
    )
```

**Why it's good:** Subset without full read.

### 3.3 Example 3: Tapped API Pager

```python
def make_obs_api_pipeline(fetch_page, pred: Callable, k: int, emit: Callable[[dict], None]) -> Transform[None, Dict]:
    return compose(
        source_to_transform(lambda: pager(fetch_page, attempts=2)),
        make_tap(lambda item: emit({"event":"api_item","id":item.get("id")})),
        ffilter(pred),
        fence_k(k),
    )
```

**Why it's good:** Log without disrupt.

### 3.4 Example 4: Peeked Telemetry

```python
def make_obs_telemetry_pipeline(src: Source[Dict], w: int, emit: Callable[[tuple[Dict,...]], None]) -> Transform[None, Dict]:
    return compose(
        source_to_transform(src),
        make_peek(10, emit, stride=5),
        make_rolling_avg_by_device(w),
    )
```

**Why it's good:** Window inspect lazy.

### 3.5 Example 5: Counted FS Hash

```python
def make_obs_fs_pipeline(root: str) -> tuple[Transform[None, tuple[str, str, int]], Callable[[], Dict[str, int]]]:
    cb, metrics = make_counter()
    pipe = compose(
        source_to_transform(make_walk_source(root)),
        make_ext_filter({'.py'}),
        make_tap(cb),
        make_sha256_with_size(),
    )
    return pipe, metrics
```

**Why it's good:** Metrics on paths.

### 3.6 Example 6: Sampled N-Gram

```python
def make_obs_ngram_pipeline(n: int, k: int) -> Transform[str, tuple[str,...]]:
    return compose(
        make_tokenize(),
        make_sampler_periodic(5),
        make_ngrams(n),
        fence_k(k),
    )
```

**Why it's good:** Reduce amplification.

### 3.7 Running Project: Observed RAG (Obs)

Extend RAG with tap:

```python
def make_obs_rag_fn(env: RagEnv, max_chunks: int, emit: Callable[[ChunkWithoutEmbedding], None]) -> Callable[[Iterable[RawDoc]], Iterator[ChunkWithoutEmbedding]]:
    tap = make_tap(emit)
    def pipe(docs: Iterable[RawDoc]) -> Iterator[ChunkWithoutEmbedding]:
        cleaned = gen_clean_docs(docs)
        observed = tap(cleaned)
        yield from gen_bounded_chunks(observed, env, max_chunks)
    return pipe
```

**Wins:** Monitor chunks.

---

## 4. Anti-Patterns and Fixes

- **Materialize Count:** list() for len breaks lazy. **Fix:** Tap counter.
- **Random Sample No Seed:** Nondeterministic. **Fix:** Seed rng.
- **Tap mutates global/shared state:** Callback updates globals or shared mutable structures. **Fix:** Confine state inside tap closure or use logs-as-data.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Inline obs → equiv no-obs.

**Bug Hunt:** Materialize; tap explicit.

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

### 6.1 Custom Strategy

As previous.

### 6.2 Properties

```python
from hypothesis import given, strategies as st
import pytest

@given(st.lists(st.integers(), max_size=50))
def test_tap_equiv(xs):
    logged = []
    tap = make_tap(logged.append)
    out = list(tap(iter(xs)))
    assert out == xs
    assert logged == xs

def test_tap_suppress_error_keeps_stream():
    def bad_cb(x):
        if x == 2:
            raise ValueError("boom")
    tap = make_tap(bad_cb, on_error="suppress")
    xs = [1,2,3]
    assert list(tap(iter(xs))) == xs

def test_tap_propagate_error_raises():
    def bad_cb(x):
        if x == 2:
            raise ValueError("boom")
    tap = make_tap(bad_cb, on_error="propagate")
    with pytest.raises(ValueError):
        list(tap(iter([1,2,3])))

rate_st = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)

@given(st.lists(st.integers(), max_size=50), rate_st)
def test_bernoulli_sampler_reuse(xs, rate):
    sampler = make_sampler_bernoulli(rate, seed=42)
    out1 = list(sampler(iter(xs)))
    out2 = list(sampler(iter(xs)))
    assert out1 == out2

@given(st.lists(st.integers(), max_size=50), rate_st)
def test_sample_determinism(xs, rate):
    s1 = make_sampler_bernoulli(rate, seed=42)
    s2 = make_sampler_bernoulli(rate, seed=42)
    assert list(s1(iter(xs))) == list(s2(iter(xs)))

@given(st.lists(st.integers(), max_size=50))
def test_peek_pass_through(xs):
    peeks = []
    peek = make_peek(3, peeks.append)
    out = list(peek(iter(xs)))
    assert out == xs
    assert all(len(p) == 3 for p in peeks)

@given(st.lists(st.text(), min_size=0, max_size=200), rate_st)
def test_stable_sampler_order_insensitive(xs, rate):
    key = lambda s: s.encode()
    samp = make_sampler_stable(rate, key)
    out1 = list(samp(iter(xs)))
    xs_perm = xs[:]; import random; random.Random(0).shuffle(xs_perm)
    out2 = list(samp(iter(xs_perm)))
    assert sorted(out1) == sorted(out2)
```

### 6.3 Additional for Examples

Similar; e.g., obs-CSV == no-obs equiv.

### 6.4 Shrinking Demo

Bad (materialize): Breaks lazy.

---

## 7. When Obs Isn't Worth It

No debug; else observe.

---

## 8. Pre-Core Quiz

1. Tap for? → **Side log.**
2. Sample? → **Subset lazy.**
3. Materialize? → **Avoid.**
4. Equiv? → **Preserved.**
5. Determinism? → **Seed rng.**

## 9. Post-Core Reflection & Exercise

**Reflect:** Find opaque; add tap.

**Project Exercise:** Add obs to RAG; test metrics.

**Final Notes:**
- Obs explicit; minimal effects.
- Document cb per tap.
- Mock cb for tests.
- Module end; apply to projects.

**End of Module 03.**

### Repository Alignment

- Implementation: `module-03/funcpipe-rag-03/src/funcpipe_rag/api/core.py::_trace_iter` and `api/types.py::RagTraceV3`.
- Tests: `module-03/funcpipe-rag-03/tests/test_module_03.py::test_trace_neutrality` / `::test_trace_lens_samples_are_bounded`.

## itertools Decision Table – Use This

| Tool       | Use When                                      | Memory   | Pitfall                              | Safe?   |
|------------|-----------------------------------------------|----------|--------------------------------------|---------|
| chain      | Concat many iterables                         | O(1)     | None                                 | Yes     |
| groupby    | Group **contiguous** equal items              | O(1)     | Must sort first if not contiguous    | Yes     |
| tee        | Multiple consumers of same iterator           | O(skew)  | Unbounded skew → memory explosion    | Careful |
| islice     | Skip/take without consuming                   | O(1)     | None                                 | Yes     |
| accumulate | Running totals/reductions                     | O(n)     | Default op is +                      | Yes     |
| compress   | Filter by boolean mask                        | O(1)     | None                                 | Yes     |

**Further Reading:** For the deepest itertools mastery, see the official docs and Dan Bader’s ‘Python Tricks’ chapter on iterators.

> **You now own the most powerful lazy streaming toolkit in Python. Module 4 will show you how to make even failure and resource cleanup lazy and pure.**
