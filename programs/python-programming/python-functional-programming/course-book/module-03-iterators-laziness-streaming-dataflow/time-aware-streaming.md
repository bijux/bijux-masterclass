# Time-Aware Streaming


<!-- page-maps:start -->
## Lesson Map

```mermaid
flowchart LR
  burst["Start with a stream that can run too fast"] --> time["Inject time as explicit input instead of reading globals"]
  time --> throttle["Throttle or rate-limit with a named contract"]
  throttle --> test["Test behavior against a controlled clock and sleeper"]
```
<!-- page-maps:end -->

Time needs to feel reviewable. Global configuration may already look risky, but time can still feel like an unavoidable hidden dependency. This page shows that clocks and sleeps can be modeled explicitly too.

## Start With the Hidden Clock Problem

Once a pipeline has to respect timing, it is easy to slide back into impure utilities. Slow down here: timing rules are part of the stage contract, not an excuse to stop reasoning carefully.

- If a stage reads the wall clock directly, the behavior is harder to test and explain.
- If delays are implicit, you cannot review whether the pipeline is obeying a real rate contract.
- If timing is introduced without naming monotonicity or burst behavior, the implementation may look fine while hiding unstable assumptions.

## Keep This Question In View

> **Core question:**  
> How do you incorporate time awareness into iterator pipelines for throttling and rate-limiting, using pure, functional patterns without side-effects or global clocks, while preserving laziness and equivalence?

This lesson introduces time-aware streaming as explicit dependency design:

- inject clocks and sleepers instead of reading time globally
- describe throttling and rate-limiting in terms of contracts you can inspect
- preserve lazy streaming behavior while making delays testable and deterministic under controlled inputs

The running project and side examples matter because time-sensitive pipelines are common, and they should not require giving up the explicit-boundary habits built earlier in the course.

Use this when you have real-time or bursty streams and need time controls without hiding behavior in global clocks.

**Outcome:**
1. Spot untimed smells like bursty I/O.
2. Add throttling in < 10 lines.
3. Prove time laws with Hypothesis.

**Laws (frozen, used across this core):**
- E1 — Equivalence: timed_pipe(S) == untimed_equiv(S) (ignoring delays).
- P1 — Purity: No global clocks; explicit time sources.
- R1 — Reusability: Factories yield fresh timed iters.
- T1 — Throttle monotonic: Outputs non-decreasing in logical time.
- RL1 — Rate-limit: Items/sec ≤ limit; burst handled (effective rate respects token bucket under monotonic clock).
- DTR — Determinism: Equal inputs/time-src → equal outputs/delays.
- FR — Freshness: Factory calls independent.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Use timestamped items and delta-based delays with injected monotonic clocks/sleepers for pure throttling/rate-limiting in streams, avoiding globals for testable time.**

### 1.2 Time-Aware in One Precise Sentence

> Embed time in items or via injectable monotonic clocks; throttle via sleep on deltas.

In this series, preserves purity; mock time for tests.

### 1.3 Why This Matters Now

The earlier lessons showed how to control memory, order, and demand. Time adds another control dimension. Without an explicit model, throttling and rate limiting often become opaque helpers that are hard to test and hard to trust. This lesson shows how to keep time as visible as the rest of the pipeline contract.

### 1.4 Time-Aware in 5 Lines

The next snippet matters because it shows the clock and sleeper as dependencies, not as invisible global behavior.

```python
def make_throttle(min_delta: float, clock, sleeper):
    def stage(xs):
        last = None
        for x in xs:
            now = clock()
            if last is not None:
                wait = max(0, (last + min_delta) - now)
                if wait > 0: sleeper(wait)
            last = clock()
            yield x
    return stage
```

Pure, testable.

### 1.5 Minimal Time Harness (Extends Core 7)

Build on Core 7 harness; add time helpers:

```python
from typing import Callable, Iterable, Iterator, TypeVar
T = TypeVar("T")

def make_throttle(min_delta: float,
                  clock: Callable[[], float],
                  sleeper: Callable[[float], None]) -> Callable[[Iterable[T]], Iterator[T]]:
    """Enforce ≥ min_delta between yielded items.
    Requires: clock is monotonic non-decreasing.
    Deterministic given (clock, sleeper)."""
    assert min_delta >= 0
    def stage(xs: Iterable[T]) -> Iterator[T]:
        last_emit: float | None = None
        for x in xs:
            now = clock()
            if last_emit is not None:
                wait = max(0.0, (last_emit + min_delta) - now)
                if wait > 0:
                    sleeper(wait)
                    now = clock()  # sleeper may advance time
            last_emit = now
            yield x
    return stage

def make_rate_limit(rate: float, burst: int,
                    clock: Callable[[], float],
                    sleeper: Callable[[float], None]) -> Callable[[Iterable[T]], Iterator[T]]:
    """Token bucket: rate tokens/sec, capacity=burst.
    Requires: clock is monotonic non-decreasing."""
    assert rate > 0 and burst >= 1
    def stage(xs: Iterable[T]) -> Iterator[T]:
        tokens = float(burst)
        last = clock()
        for x in xs:
            now = clock()
            tokens = min(burst, tokens + (now - last) * rate)
            if tokens < 1.0:
                wait = max(0.0, (1.0 - tokens) / rate)
                if wait > 0:
                    sleeper(wait)
                    now = clock()
                    tokens = min(burst, tokens + wait * rate)
            tokens -= 1.0
            last = now
            yield x
    return stage

def make_timestamp(clock: Callable[[], float]) -> Callable[[Iterable[T]], Iterator[tuple[float, T]]]:
    def stage(xs: Iterable[T]) -> Iterator[tuple[float, T]]:
        for x in xs:
            yield clock(), x
    return stage

def make_call_gate(min_delta: float, clock, sleeper):
    """Stateful boundary helper for pacing calls (not pure; use only at I/O edges)."""
    last: float | None = None
    def gate(fn, *args, **kwargs):
        nonlocal last
        now = clock()
        if last is not None:
            wait = max(0.0, (last + min_delta) - now)
            if wait > 0: sleeper(wait)
        result = fn(*args, **kwargs)
        last = clock()
        return result
    return gate
```

Use with compose; e.g., compose(..., make_throttle(0.5, time.monotonic, time.sleep), ...). Inject mock clocks/sleepers for tests. Note: sync versions block on sleep; unsuitable for event loops—use async variants in production.

---

## 2. Mental Model: Untimed vs Time-Aware

### 2.1 One Picture

```text
Untimed Streams (Bursty)                Time-Aware Streams (Controlled)
+-----------------------+               +------------------------------+
| fast, uncontrolled    |               | delta/sleep for pace         |
|        ↓              |               |        ↓                     |
| overload sinks        |               | throttle/limit, pure         |
| test = slow           |               | injectable time, testable    |
+-----------------------+               +------------------------------+
   ↑ Chaotic / Global                      ↑ Pure / Mockable
```

### 2.2 Behavioral Contract

| Aspect | Untimed | Time-Aware |
|-------------------|------------------------------|------------------------------|
| Pace | As-fast-as-possible | Throttled/limited |
| Time Source | N/A | Injectable monotonic clock |
| Purity | Pure | Pure (no globals) |
| Testability | Simple | Mock time for fast tests |

**Note on Untimed Choice:** For batch; else time-aware.

**When Not to Time:** No rate needs; use Core 7.

**Known Pitfalls:**
- Global time leaks nondeterminism.
- Sleep blocks thread.

**Forbidden Patterns:**
- time.time() in core; inject.
- Enforce with grep for time.time.

**Building Blocks Sidebar:**
- monotonic for deltas.
- sleep for throttle.
- Token bucket for limits.

**Resource Semantics:** Time stages delay but don't consume.

**Error Model:** Propagate; time errors raise.

**Backpressure:** Throttle after sources, before sinks.

---

## 3. Cross-Domain Examples: Proving Scalability

Production-grade examples using the harness. Each pure, timed.

### 3.1 Example 1: Throttled CSV Read (Time-Aware)

```python
def make_timed_csv_pipeline(path: str, max_rows: int, delta: float, clock, sleeper) -> Transform[None, Dict[str, Any]]:
    return compose(
        source_to_transform(make_csv_source(path)),
        ffilter(lambda r: r.get("status") == "active"),
        make_throttle(delta, clock, sleeper),
        make_project({"id": "user_id", "amount": "total"}),
        make_cast({"amount": float}),
        fence_k(max_rows),
    )
```

**Why it's good:** Paced before heavy compute.

### 3.2 Example 2: Rate-Limited Log Tail

```python
def make_timed_log_pipeline(path: str, pattern: str, k: int, rate: float, clock, sleeper) -> Transform[None, str]:
    return compose(
        source_to_transform(make_log_source(path)),
        make_regex_filter(pattern),
        make_rate_limit(rate, 1, clock, sleeper),
        fence_k(k),
    )
```

**Why it's good:** Limited after filter.

### 3.3 Example 3: Throttled API Pagination

```python
def pager_timed(fetch_page, *, attempts=3, backoff=0.5, delta: float, clock, sleeper):
    gate = make_call_gate(delta, clock, sleeper)
    token = None
    while True:
        tries = 0
        while True:
            try:
                page = gate(fetch_page, token)
                break
            except Exception:
                tries += 1
                if tries >= attempts: raise
                sleeper(backoff * tries)
        for item in page["items"]: yield item
        token = page.get("next")
        if not token: return

def make_timed_api_pipeline(fetch_page, pred: Callable, k: int, delta: float, clock, sleeper) -> Transform[None, Dict]:
    src = lambda: pager_timed(fetch_page, delta=delta, clock=clock, sleeper=sleeper)
    return compose(
        source_to_transform(src),
        ffilter(pred),
        fence_k(k),
    )
```

**Why it's good:** Paced calls; limiter in pager.

### 3.4 Example 4: Timestamped Telemetry with Throttle

```python
def make_timed_telemetry_pipeline(src: Source[Dict], w: int, delta: float, clock, sleeper) -> Transform[None, Dict]:
    return compose(
        source_to_transform(src),
        make_throttle(delta, clock, sleeper),
        make_rolling_avg_by_device(w),
    )
```

**Why it's good:** Wall-clock paced input to aggs.

### 3.5 Example 5: Rate-Limited FS Hash

```python
def make_timed_fs_pipeline(root: str, rate: float, clock, sleeper) -> Transform[None, tuple[str, str, int]]:
    return compose(
        source_to_transform(make_walk_source(root)),
        make_ext_filter({'.py'}),
        make_rate_limit(rate, 1, clock, sleeper),
        make_sha256_with_size(),
    )
```

**Why it's good:** Limited before IO.

### 3.6 Example 6: Throttled N-Gram

```python
def make_timed_ngram_pipeline(n: int, k: int, delta: float, clock, sleeper) -> Transform[str, tuple[str,...]]:
    return compose(
        make_tokenize(),
        make_throttle(delta, clock, sleeper),
        make_ngrams(n),
        fence_k(k),
    )
```

**Why it's good:** Paced before amplification.

### 3.7 Running Project: Timed RAG (Time-Aware)

Extend RAG with throttling:

```python
def make_timed_rag_fn(env: RagEnv, max_chunks: int, delta: float, clock, sleeper) -> Callable[[Iterable[RawDoc]], Iterator[ChunkWithoutEmbedding]]:
    throttle = make_throttle(delta, clock, sleeper)
    def pipe(docs: Iterable[RawDoc]) -> Iterator[ChunkWithoutEmbedding]:
        cleaned = gen_clean_docs(docs)
        throttled = throttle(cleaned)
        yield from gen_bounded_chunks(throttled, env, max_chunks)
    return pipe
```

**Wins:** Paced chunking.

---

## 4. Anti-Patterns and Fixes

- **Global Time:** time.time() nondeterministic. **Fix:** Inject clock.
- **Busy Wait:** Poll loops waste CPU. **Fix:** Sleep on deltas.
- **No Mock:** Real time in tests slow. **Fix:** Fake clock.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Inline time → equiv untimed.

**Bug Hunt:** Global time; inject explicit.

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

### 6.1 Custom Strategy

As previous.

### 6.2 Properties

```python
from hypothesis import given, strategies as st


class FakeTime:
    def __init__(self) -> None:
        self.t: float = 0.0
        self.sleeps: list[float] = []

    def clock(self) -> float:
        return self.t

    def sleep(self, dt: float) -> None:
        assert dt >= 0.0
        self.sleeps.append(dt)
        self.t += dt


@given(
    st.lists(st.anything(), max_size=50),
    st.floats(min_value=0.1, max_value=1.0, allow_nan=False, allow_infinity=False),
)
def test_throttle_equiv(xs, delta):
    ft = FakeTime()
    throttle = make_throttle(delta, ft.clock, ft.sleep)
    out = list(throttle(iter(xs)))
    assert out == xs  # equiv ignoring time
    # Under FakeTime, we advance exactly `delta` between emits.
    assert abs(sum(ft.sleeps) - delta * max(0, len(xs) - 1)) < 1e-9


@given(
    st.lists(st.anything(), max_size=50),
    st.floats(min_value=0.1, max_value=1.0, allow_nan=False, allow_infinity=False),
)
def test_throttle_monotonic(xs, delta):
    ft = FakeTime()
    throttle = make_throttle(delta, ft.clock, ft.sleep)
    _ = list(throttle(iter(xs)))
    # T1: all waits are non-negative ⇒ logical time never goes backwards.
    assert all(dt >= 0.0 for dt in ft.sleeps)


@given(
    st.lists(st.anything(), max_size=50),
    st.floats(min_value=0.5, max_value=10.0, allow_nan=False, allow_infinity=False),
    st.integers(1, 5),
)
def test_rate_limit_respects_rate(xs, rate, burst):
    ft = FakeTime()
    limit = make_rate_limit(rate, burst, ft.clock, ft.sleep)
    out = list(limit(iter(xs)))
    assert out == xs
    n = len(xs)
    free = min(n, burst)  # initial token budget
    # Tokens from time (`rate * ft.t`) plus initial free tokens must cover tokens spent (`n`).
    assert ft.t * rate + free >= n - 1e-9


@given(
    st.lists(st.anything(), max_size=50),
    st.floats(min_value=0.5, max_value=10.0, allow_nan=False, allow_infinity=False),
)
def test_rate_limit_determinism(xs, rate):
    ft1 = FakeTime()
    limit1 = make_rate_limit(rate, 3, ft1.clock, ft1.sleep)
    out1 = list(limit1(iter(xs)))

    ft2 = FakeTime()
    limit2 = make_rate_limit(rate, 3, ft2.clock, ft2.sleep)
    out2 = list(limit2(iter(xs)))

    assert out1 == out2 == xs
```

### 6.3 Additional for Examples

Similar; e.g., timed-CSV == untimed equiv.

### 6.4 Shrinking Demo

Bad (global time): Fails determinism.

---

## 7. When Time Isn't Worth It

Batch processing; else time-aware.

---

## 8. Pre-Core Quiz

1. Throttle for? → **Pace deltas.**
2. Clock? → **Inject mock.**
3. Global time? → **Avoid.**
4. Equiv? → **Preserved.**
5. Test? → **Fast with mock.**

## 9. Post-Core Reflection & Exercise

**Reflect:** Find bursty; add throttle.

**Project Exercise:** Add time to RAG; test with mock.

**Final Notes:**
- Time pure; inject clocks.
- Document monotonicity per stage.
- Mock for deterministic tests.
- For async time, see future cores.

**Continue with:** [Custom Iterators](../module-03-iterators-laziness-streaming-dataflow/custom-iterators.md)

### Repository Alignment

- Implementation: `capstone/src/funcpipe_rag/streaming/time.py::throttle` plus `capstone/src/funcpipe_rag/fp/combinators.py::FakeTime`.
- Tests: `capstone/tests/unit/streaming/test_streaming.py::test_throttle_uses_injected_clock`.

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
