# Module 3: Lazy Iteration and Streaming

## Progression Note
By the end of Module 3, you will master lazy generators, itertools mastery, and streaming pipelines that never materialize unnecessary data. This prepares you for safe recursion and error handling in streams (Module 4). See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus                                   | Key Outcomes                                           |
|--------|-----------------------------------------|--------------------------------------------------------|
| 2      | First-Class Functions & Expressive Python | Configurable pure pipelines without globals           |
| 3      | Lazy Iteration & Generators             | Memory-efficient streaming, itertools mastery, short-circuiting |
| 4      | Recursion & Error Handling in Streams   | Safe recursion, Result/Option, streaming errors        |

## M03C07: Fan-In and Fan-Out for Streams – Merging, Splitting, and Multicasting Iterators Safely

> **Core question:**  
> How do you safely merge multiple input streams (fan-in) and split or multicast a single stream to multiple consumers (fan-out) in lazy, pure iterator pipelines without breaking equivalence or introducing side-effects?

This core builds on **Core 6**'s reusable stages by introducing fan-in/fan-out patterns:
- Use `chain`/`chain.from_iterable` for sequential fan-in, `roundrobin` for fair interleaving, `heapq.merge` for sorted fan-in.
- Use `fork2_lockstep` for strict 1:1 fan-out; bounded multicast for variable-cardinality or independent consumption.
- Handle independence, buffering, and fairness.
- Preserve laziness, purity, and freshness.

We extend the **running project** from Core 6 (FuncPipe RAG Builder from `m03-rag.md`) and add cross-domain examples like multi-log merging, stream splitting for analytics, and API fan-in to prove scalability.

**Audience:** Developers building scalable, multi-source pipelines needing merge/split without materialization.

**Outcome:**
1. Identify single-stream limitations.
2. Add fan-in/out in < 10 lines.
3. Prove merge/fork laws with Hypothesis.

**Laws (frozen, used across this core):**
- E1 — Equivalence: merged/fanned == eager_equiv (no reordering unless specified).
- P1 — Purity: No side-effects; explicit configs.
- R1 — Reusability: Factories yield fresh multis.
- M1 — Merge order: 
  - `chain`: sequential (preserves per-source order).
  - `roundrobin`: interleaving without starvation (in practice, no source is delayed indefinitely).
  - `heapq.merge`: sorted by key, stable per-source for ties.
- T1 — Tee/multicast cost: Memory overhead is Θ(Δ), where Δ is the maximum difference in items consumed between the fastest and slowest branch; lockstep fork keeps Δ ≤ 1; bounded multicast enforces Δ≤maxlen else raises BufferError.
- DTR — Determinism: Equal inputs/config → equal outputs.
- FR — Freshness: 
  - For Source factories: src() and src() are independent iterators.
  - For Transform factories: mk = factory(config); mk(xs) and mk(xs) are independent iterators.
- Fencing after fan-out: After any fan-out, fence each branch before any amplifying transform (n-grams, chunking, network I/O).

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Use chain/roundrobin/merge for fan-in and fork2_lockstep/bounded multicast for fan-out to handle multi-streams lazily, ensuring independence without full materialization.**

### 1.2 Fan-In/Out in One Precise Sentence

> Fan-in merges sources (chain seq, roundrobin interleaving, merge sorted); fan-out forks/multicasts for independent consumers with explicit buffering discipline.

### 1.3 Why This Matters Now

Single-stream pipes limit scalability; fan-in/out enables multi-source/consumer without eagerness.

### 1.4 Fan-In/Out in 5 Lines

Fan-in example:

```python
merged = make_chain(src1, src2)()  # lazy merge
```

Fan-out:

```python
fork = fork2_lockstep(stage1, stage2)
paired = fork(stream)  # strict lockstep pairs
```

Safe, lazy.

### 1.5 Minimal Fan Harness (Extends Core 6)

Build on Core 6 harness; add fan helpers. We reuse the functional pipeline types and combinators from M03C06:
`Transform`, `compose`, `ffilter`, `fence_k`, and `source_to_transform`.

```python
from typing import TypeVar, Iterable, Iterator, Callable, Any
import heapq
from itertools import tee
from collections import deque

A = TypeVar("A"); B = TypeVar("B"); C = TypeVar("C"); T = TypeVar("T")
Source = Callable[[], Iterator[T]]

def make_chain(*srcs: Source[T]) -> Source[T]:
    def merged() -> Iterator[T]:
        for s in srcs:
            yield from s()
    return merged

def make_roundrobin(*srcs: Source[T]) -> Source[T]:
    def merged() -> Iterator[T]:
        active = [s() for s in srcs]
        while active:
            nxt = []
            for it in active:
                try:
                    yield next(it)
                    nxt.append(it)
                except StopIteration:
                    pass
            active = nxt
    return merged

def make_merge(*srcs: Source[T], key: Callable[[T], Any] | None = None, reverse: bool = False) -> Source[T]:
    def merged() -> Iterator[T]:
        iters = [s() for s in srcs]
        yield from heapq.merge(*iters, key=key, reverse=reverse)
    return merged

def fork2_lockstep(t: Transform[A,B], u: Transform[A,C]) -> Transform[A, tuple[B,C]]:
    """
    Strict 1:1 lockstep fan-out.
    Raises ValueError on cardinality mismatch (one branch shorter/longer).
    """
    def stage(xs: Iterable[A]) -> Iterator[tuple[B,C]]:
        a, b = tee(xs, 2)
        it1, it2 = t(a), u(b)
        while True:
            try:
                v1 = next(it1)
            except StopIteration:
                # ensure second branch also exhausted
                try:
                    next(it2)
                    raise ValueError("fork2_lockstep: second branch produced extra items")
                except StopIteration:
                    return
            try:
                v2 = next(it2)
            except StopIteration:
                raise ValueError("fork2_lockstep: second branch shorter than first")
            yield (v1, v2)
    return stage

_SENTINEL = object()
def multicast_bounded(xs: Iterable[T], n: int, maxlen: int = 1024) -> tuple[Iterator[T], ...]:
    """
    Bounded multicast.
    If any consumer lags by more than maxlen items, raises BufferError.
    If one branch is never drained, the producer will eventually hit BufferError when skew reaches maxlen.
    """
    upstream = iter(xs)
    qs = [deque() for _ in range(n)]
    done = False

    def pump_once():
        nonlocal done
        if done: return
        try:
            x = next(upstream)
        except StopIteration:
            done = True
            for q in qs: q.append(_SENTINEL)
            return
        for q in qs:
            if len(q) >= maxlen:
                raise BufferError(f"multicast buffer exceeded (maxlen={maxlen})")
            q.append(x)

    def sub(i: int) -> Iterator[T]:
        while True:
            if not qs[i]:
                pump_once()
            y = qs[i].popleft()
            if y is _SENTINEL:
                return
            yield y

    return tuple(sub(i) for i in range(n))
```

Use with compose; e.g., compose(source_to_transform(make_chain(s1, s2)), ...). Use fork2_lockstep only for strict 1:1 stages; otherwise use bounded multicast or separate sinks. Always fence branches before amplification.

---

## 2. Mental Model: Single vs Multi-Stream

### 2.1 One Picture

```text
Single-Stream (Limited)                 Multi-Stream (Scalable)
+-----------------------+               +------------------------------+
| one src → one sink    |               | multi-src → merge → split    |
|        ↓              |               |        ↓                     |
| rigid, no parallel    |               | fan-in/out, independent      |
| reuse = rebuild       |               | lazy, pure, testable         |
+-----------------------+               +------------------------------+
   ↑ Bottlenecked                          ↑ Composable / Multi
```

### 2.2 Behavioral Contract

| Aspect | Single-Stream | Multi-Stream (Fan-In/Out) |
|-------------------|------------------------------|------------------------------|
| Sources | One | Many (merged) |
| Consumers | One | Many (forked/multicast) |
| Order | As-is | Seq (chain), interleaving (roundrobin), or sorted (merge) |
| Independence | N/A | Fork/multicast ensures |

**Note on Single Choice:** For simple; else multi.

**When Not to Fan:** No multi needs; use Core 6.

**Known Pitfalls:**
- Fork requires strict 1:1 cardinality; mismatch raises ValueError.
- Merge requires sorted inputs.

**Forbidden Patterns:**
- Multiple consumes without fork/multicast.
- Enforce with no repeated iter calls.

**Building Blocks Sidebar:**
- chain for seq fan-in.
- roundrobin for interleaving.
- heapq.merge for sorted.
- fork2_lockstep for strict 1:1 fan-out.

**Resource Semantics:** Fans close resources on exhaustion.

**Error Model:** Propagate; no auto-retry (use Core 6 wrappers).

**Backpressure:** Fence after merge/before split; multicast raises on buffer exceed.

---

## 3. Cross-Domain Examples: Proving Scalability

Production-grade examples using the harness. Each pure, lazy.

### 3.1 Example 1: Merging Multiple CSV Sources (Fan-In)

```python
def make_multi_csv_pipeline(paths: list[str], max_rows: int) -> Transform[None, Dict[str, Any]]:
    srcs = [make_csv_source(p) for p in paths]
    merged_src = make_chain(*srcs)
    return compose(
        source_to_transform(merged_src),
        ffilter(lambda r: r.get("status") == "active"),
        make_project({"id": "user_id", "amount": "total"}),
        make_cast({"amount": float}),
        fence_k(max_rows),
    )
```

**Why it's good:** Lazy merge of files; no load all.  
**Contiguity/Boundedness:** Finite sources; fence caps.

### 3.2 Example 2: Log Merge with Time Sort (Sorted Fan-In)

```python
def make_multi_log_pipeline(paths: list[str], pattern: str, k: int) -> Transform[None, str]:
    srcs = [make_log_source(p) for p in paths]
    merged_src = make_merge(*srcs, key=parse_ts)  # parse_ts: str -> comparable
    return compose(
        source_to_transform(merged_src),
        make_regex_filter(pattern),
        fence_k(k),
    )
```

**Precondition:** each input is individually non-decreasing under parse_ts; otherwise use roundrobin or a bounded-lateness merge.
**Why it's good:** Sorted merge without sort all; assumes per-log sorted.  
**Contiguity/Boundedness:** Infinite; fence ensures termination.

### 3.3 Example 3: API Fan-In from Multiple Endpoints

```python
def make_multi_api_pipeline(fetch_pages: list[Callable], pred: Callable, k: int) -> Transform[None, Dict]:
    srcs = [lambda f=f: pager(f, attempts=2) for f in fetch_pages]
    merged_src = make_roundrobin(*srcs)  # interleaving to avoid starvation
    return compose(
        source_to_transform(merged_src),
        ffilter(pred),
        fence_k(k),
    )
```

**Why it's good:** Interleaving merge of APIs.

### 3.4 Example 4: Telemetry Split for Multi-Agg (Fan-Out)

```python
def values_after_w(w: int):
    from collections import deque
    def stage(xs):
        buf = deque(maxlen=w)
        for d in xs:
            buf.append(d)
            if len(buf) == w:
                yield d['value']
    return stage

def make_telemetry_pipeline(src: Source[dict], w: int) -> Transform[None, tuple[dict, float]]:
    avg_stage   = make_rolling_avg_by_device(w)
    total_stage = values_after_w(w)
    fork = fork2_lockstep(avg_stage, total_stage)
    return compose(source_to_transform(src), fork)
```

**Why it's good:** Fork for parallel aggs; strict lockstep enforces 1:1 cardinality.

### 3.5 Example 5: FS Hash with Split for Checksum/Size

```python
def make_sha256_with_size() -> Transform[str, tuple[str, str, int]]:
    def stage(paths: Iterable[str]) -> Iterator[tuple[str, str, int]]:
        for p in paths:
            h = hashlib.sha256(); size = 0
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1024*1024), b""):
                    size += len(chunk); h.update(chunk)
            yield (p, h.hexdigest(), size)
    return stage

def make_fs_pipeline(root: str) -> Transform[None, tuple[str, str, int]]:
    return compose(
        source_to_transform(make_walk_source(root)),
        make_ext_filter({'.py'}),
        make_sha256_with_size(),
    )
```

**Why it's good:** Single-pass compute; no split needed.

### 3.6 Example 6: Text N-Grams with Bounded Multicast (Fan-Out for Variable Cardinality)

For variable-cardinality (e.g., n-grams amplify), use multicast and separate sinks or keyed join.

```python
import heapq
from collections import Counter
from itertools import islice

def topk(k: int):
    def stage(xs):
        counts = Counter()
        for x in xs:
            counts[x] += 1
            if len(counts) > 10_000:  # safety cap; document policy
                counts = Counter(dict(counts.most_common(5_000)))
        yield from heapq.nlargest(k, counts.items(), key=lambda kv: kv[1])
    return stage

def make_ngram_multi(n: int, k: int) -> Transform[str, tuple[tuple[str,...], int]]:
    base = compose(make_tokenize(), make_ngrams(n))
    def pipe(lines: Iterable[str]) -> Iterator[tuple]:
        a,b = multicast_bounded(base(lines), 2, maxlen=1000)
        freqs = topk(k)(a)
        # bounded distinct example (instead of unbounded set)
        distinct = set(islice(b, 1000))  # explicit bound
        # Keyed join or separate outputs; here assume post-process
        for f in freqs: yield f[0], f[1]  # e.g., top freqs
    return pipe
```

**Why it's good:** Bounded multicast for derived stats; explicit buffer policy.

### 3.7 Running Project: Multi-Source RAG (Fan-In)

Extend RAG with multi-doc sources:

```python
def make_multi_rag_fn(env: RagEnv, max_chunks: int, sources: list[Source[RawDoc]]) -> Callable[[], Iterator[ChunkWithoutEmbedding]]:
    merged_src = make_chain(*sources)
    def pipe() -> Iterator[ChunkWithoutEmbedding]:
        cleaned = gen_clean_docs(merged_src())
        yield from gen_bounded_chunks(cleaned, env, max_chunks)
    return pipe
```

**Wins:** Merge docs lazily.

---

## 4. Anti-Patterns and Fixes

- **No Fork/Multicast Consume:** Multi-iter without fork/multicast exhausts. **Fix:** Always fork/multicast.
- **Eager Merge:** List all before process. **Fix:** Chain lazy.
- **Unbounded Buffer:** Tee with skew OOM. **Fix:** Fork lockstep or multicast bounded.
- **Unfair Merge:** Chain starves later srcs. **Fix:** Roundrobin for interleaving.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Inline fan → equiv single.

**Bug Hunt:** No fork/multicast; fan explicit.

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

### 6.1 Custom Strategy

As previous.

### 6.2 Properties

```python
from hypothesis import given, strategies as st
import itertools as it

@given(st.lists(st.integers(), min_size=0, max_size=200))
def test_chain_equiv(xs):
    s1 = lambda: iter(xs)
    s2 = lambda: iter(xs)
    merged = list(make_chain(s1, s2)())
    assert merged == xs + xs

@given(st.lists(st.integers(), min_size=0, max_size=200))
def test_tee_independence(xs):
    a, b = tee(iter(xs), 2)
    _ = list(it.islice(a, 3))
    assert list(b) == xs   # tee buffers 3

@given(st.lists(st.integers(), min_size=0, max_size=200))
def test_merge_stability_ties(xs):
    xs_sorted = sorted(xs)
    s1 = lambda: ((0, x) for x in xs_sorted)   # tag source 0
    s2 = lambda: ((1, x) for x in xs_sorted)   # tag source 1
    out = list(make_merge(s1, s2, key=lambda p: p[1])())
    seen0 = [x for src, x in out if src == 0]
    seen1 = [x for src, x in out if src == 1]
    assert seen0 == xs_sorted
    assert seen1 == xs_sorted   # stable per-source for ties

@given(st.lists(st.lists(st.integers()), min_size=1, max_size=4))
def test_roundrobin_interleaving(ls):
    srcs = [lambda l=l: iter(l) for l in ls]
    out = list(make_roundrobin(*srcs)())
    # multiset equality only (basic sanity; non-starving behaviour follows from the implementation)
    assert sorted(out) == sorted([y for x in ls for y in x])

@given(st.lists(st.integers(), min_size=0, max_size=50))
def test_fork_lockstep(xs):
    inc = lambda xs: (x+1 for x in xs)
    dec = lambda xs: (x-1 for x in xs)
    fork = fork2_lockstep(inc, dec)
    out = list(fork(iter(xs)))
    assert out == [(x+1, x-1) for x in xs]

@given(st.lists(st.integers(), min_size=0, max_size=50))
def test_multicast_freshness(xs):
    a,b = multicast_bounded(iter(xs), 2, maxlen=100)
    assert list(a) == xs
    assert list(b) == xs  # independent
```

### 6.3 Additional for Examples

Similar for each; e.g., multi-CSV == concat singles.

### 6.4 Shrinking Demo

Bad (no fork/multicast): Fails independence.

---

## 7. When Fan Isn't Worth It

Single stream; else fan.

---

## 8. Pre-Core Quiz

1. Fan-in for? → **Merge srcs.**
2. Fork/multicast? → **Split independent.**
3. Chain? → **Seq merge.**
4. Equiv? → **Preserved.**
5. Independence? → **Fork/multicast ensures.**

## 9. Post-Core Reflection & Exercise

**Reflect:** Find single-stream; add fan.

**Project Exercise:** Add multi-src to RAG; test merge.

**Final Notes:**
- Fans pure; explicit order/independence.
- Document order guarantees per fan.
- Fork/multicast for multicast; balance consumption.
- For async, see future cores.

**Next:** M03C08 – Time-Aware Streaming Patterns. (Builds on this.)

### Repository Alignment

- Implementation: `module-03/funcpipe-rag-03/src/funcpipe_rag/api/core.py::multicast`.
- Tests: `module-03/funcpipe-rag-03/tests/test_module_03.py::test_multicast_independence`.

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
