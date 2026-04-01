# Module 3: Lazy Iteration and Streaming

## Progression Note
By the end of Module 3, you will master lazy generators, itertools mastery, and streaming pipelines that never materialize unnecessary data. This prepares you for safe recursion and error handling in streams (Module 4). See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus                                   | Key Outcomes                                           |
|--------|-----------------------------------------|--------------------------------------------------------|
| 2      | First-Class Functions & Expressive Python | Configurable pure pipelines without globals           |
| 3      | Lazy Iteration & Generators             | Memory-efficient streaming, itertools mastery, short-circuiting |
| 4      | Recursion & Error Handling in Streams   | Safe recursion, Result/Option, streaming errors        |

## M03C03: Composing Iterators with itertools – chain, islice, groupby, tee

> **Core question:**  
> How do you use itertools tools like chain, islice, groupby, and tee to compose lazy iterators into efficient pipelines, avoiding materialization while preserving order and equivalence?

This core builds on **Core 1**'s generators and **Core 2**'s expressions by introducing **itertools** for composing lazy stages:
- Chain multiple iterators without lists.
- Slice lazily to short-circuit.
- Group contiguous keys (contiguity by construction—no interleaving of equal keys).
- Tee duplicates with bounded caching—avoid unbounded unless both branches are consumed in lockstep.
- Preserve laziness and equivalence to eager.

We continue the **running project** from `m03-rag.md`, now composing stages with itertools.

**Audience:** Developers with lazy stages who need to merge, slice, or branch streams without losing laziness.

**Outcome:**
1. Spot composition smells like list chaining.
2. Refactor to itertools in < 10 lines.
3. Prove composition laws with Hypothesis.

**Laws (frozen, used across this core):**
- E1 — Equivalence: For any finite re-iterable sequence xs: list(pipe(xs)) == eager_equiv(list(xs)).
- O1 — Global order: Output preserves input order.
- O2 — Monotone per-key: Within a key (e.g., doc_id), indices are non-decreasing.
- D1 — Demand-boundedness: list(islice(pipe(xs), k)) pulls ≤ k upstream elements from the source iterable (for the current RAG composition, c = 0 at the RawDoc level).
- F1 — Failure immediacy: On exception at item i, no further upstream pulls occur.
- M1 — No hidden materialization: Core paths avoid list/tuple/sorted/[*xs]/tee on unbounded data; bounded taps (tuple(islice(...,K))) are allowed only for observability; list(grp) is allowed only for bounded groups (size ≤ K).
- G1 — Groupby: Only valid if equal keys occur contiguously (by construction, not sorting).

Note (A1): In the current RAG composition we assume each `CleanDoc` yields at least one chunk (zero-chunk docs are filtered earlier). Under A1, D1 holds with c = 0 at the `RawDoc` level.


In this core, pipe is concretely gen_pipeline and gen_chunked_docs ∘ gen_clean_docs.

---

## 1. Conceptual Foundation
### 1.1 Contracts
> **Boxed Rule: Compose lazy iterators with itertools: use chain.from_iterable to flatten, islice to fence demand, groupby only when keys are contiguous by construction (enforce with guards/asserts), and avoid tee unless both branches are consumed in lockstep—prefer lockstep fan-out alternatives.**

### 1.2 Itertools Composition in One Precise Sentence
> itertools provides pure, lazy combinators: chain merges iterables, islice bounds them, groupby clusters contiguous equal keys, and tee duplicates with bounded caching.

Use for pipeline assembly.

### 1.3 Why This Matters Now
Manual loops/lists break laziness; itertools keeps streams efficient, enabling unbounded data and short-circuits.

### 1.4 chain.from_iterable Flattens Lazily
```python
from itertools import chain
iter1 = (x for x in range(3))
iter2 = (x for x in range(3, 6))
chained = chain(iter1, iter2) # No materialization
print(next(chained)) # 0
```
Lazy merge without allocation.

---

## 2. Mental Model: Manual vs Itertools

### 2.1 One Picture

```text
Manual Loops (Eager/Mutable)            Itertools (Lazy/Pure)
+-------------------------------+       +------------------------------+
| lists + append/for            |       | chain / islice / groupby /   |
|               ↓               |       | tee (discouraged)            |
| materialize + mutate          |       | compose iterators            |
| result = full data            |       | lazy, no allocation          |
+-------------------------------+       +------------------------------+
         ↑ Breaks laziness                     ↑ Efficient pipelines
```

### 2.2 Behavioral Contract
| Aspect                    | Manual (Eager)                              | Itertools (Lazy)                              |
|---------------------------|---------------------------------------------|-----------------------------------------------|
| Computation               | Eager loops                                 | Lazy composition                              |
| Memory (transform)        | O(n) additional objects                     | O(1) additional transform state               |
| Purity                    | Mutation possible                           | Pure functions                                |
| Equivalence               | list(composed) == manual                    | list(itertools_pipeline(xs)) == manual_output(xs) |

**Note on Manual Choice:** Rarely, for custom state; prefer itertools.

**When Not to Use Itertools:** Complex state; use custom iterators (later cores).

**Known Pitfalls:**
- tee caches if branches lag.
- groupby requires contiguous keys.
- islice consumes prefix.
- chain order matters.

**Materialization Policy:**
- Policy applies to the hot path (core pipeline functions). Exceptions are allowed only in taps/tests.
- Hot path bans: list( · ), sorted( · ), [*xs]
- Allowed exceptions: tuple(islice(xs,K)) for taps; list(group) only for bounded groups (size ≤ K)

**Building Blocks (the four tools of this core):**
- chain / chain.from_iterable
- islice
- groupby (contiguity-only)
- tee (avoid; use lockstep fanout instead)

Additional itertools tools (batched, accumulate, heapq.merge, sliding windows, etc.) appear in later cores.

### 2.3 Anti-Patterns
```python
# BAD: eager chain
flat = [y for xs in xss for y in xs]  # builds full list

# BAD: immediate list(...) after a gen-exp
ys = list(f(x) for x in xs)  # defeats laziness

# BAD: tee with drifting consumers
from itertools import tee
a, b = tee(xs)        # b lags ⇒ cache grows unbounded
next(a); # ... many ops ...
next(b); # memory ballooned
```
---

## 3. Running Project: Composed Pipelines in RAG
Our **running project** (from `m03-rag.md`) composes Core 1/2 stages.
- **Goal:** Chain cleaning/chunking lazily.
- **Start:** Manual list-based.
- **End (this core):** Itertools-composed core.
### 3.1 Types (Canonical, Used Throughout)
From `rag_types.py` (as in Core 1).
### 3.2 Manual Start (Anti-Pattern)
```python
# core3_start.py: Manual composition (materializes)
chunks = []
for cd in gen_clean_docs(docs):
    for c in gen_chunk_doc(cd, env):
        chunks.append(c) # Full list
```
**Smells:** Materializes; no short-circuit.
---

## 4. Refactor to Lazy: Itertools in RAG
### 4.1 Lazy Core
Use itertools for composition.
```python
# Lazy refactor: Itertools-based
from __future__ import annotations
from itertools import chain, islice
from collections.abc import Iterable, Iterator
from rag_types import RawDoc, CleanDoc, RagEnv, ChunkWithoutEmbedding
from core1 import gen_chunk_doc # your Core 1
from core2 import gen_clean_docs # your Core 2
def gen_chunked_docs(cleaned: Iterable[CleanDoc], env: RagEnv) -> Iterator[ChunkWithoutEmbedding]:
    """Flatten per-doc chunk streams lazily (E1, O1/O2, D1, F1, M1)."""
    return chain.from_iterable(gen_chunk_doc(cd, env) for cd in cleaned)
def tap_prefix(xs: Iterable, k: int, hook) -> Iterator:
    """Bounded side-effect tap; avoids tee’s unbounded cache."""
    it = iter(xs)
    head = tuple(islice(it, k)) # bounded, explicit
    hook(head)
    yield from head
    yield from it
def gen_pipeline(docs: Iterable[RawDoc], env: RagEnv, tap=None) -> Iterator[ChunkWithoutEmbedding]:
    cleaned = gen_clean_docs(docs)
    if tap:
        cleaned = tap_prefix(cleaned, 5, tap) # bounded tap
    yield from gen_chunked_docs(cleaned, env)
# Composed: Lazy
cleaned = gen_clean_docs(docs)
chunked = gen_chunked_docs(cleaned, env)
first = next(chunked) # Computes minimal
```
**Wins:** Lazy merge; no lists.
**Complexity:**
| Tool | Time | Aux space | Notes |
|------|------|-----------|-------|
| chain.from_iterable | Θ(total items) | O(1) | Preserves upstream laziness |
| islice(xs, k) | O(k) | O(1) | Pulls ≤ k |
| groupby (contiguous) | Θ(n) | O(size of current run) | One group in memory at a time |
| tee(a, b) | Θ(n) | Unbounded (up to lag × elem) | Avoid unless lockstep |

**Note:** Compose further with islice for bounds, groupby for per-doc. list(islice(gen_pipeline(...), 10)) pulls at most 10 docs from the source.

**Re-iterability Warning:** Generators are single-pass; don’t iterate twice; if re-use needed, re-materialize bounded or re-source.

### 4.2 Lazy Shell (Edge Only)
```python
cleaned = gen_clean_docs(read_docs())
chunked = gen_chunked_docs(cleaned, env)
write_jsonl_atomic(output_path, chunked)
```
**Note:** Streams; atomic.
### 4.3 Groupby Safety
Do not call groupby unless you can assert contiguity; if not, sort or use an external aggregator.
```python
from itertools import groupby
from operator import attrgetter

# Guard to enforce contiguity-by-construction
_S = object()
def ensure_contiguous(stream, key):
    seen, prev = set(), _S
    for x in stream:
        k = key(x)
        if k != prev and k in seen:
            raise ValueError("Non-contiguous key encountered")
        seen.add(k); prev = k
        yield x

# Contract: doc_id is contiguous by construction
def assert_contiguous_doc_ids(chunks):
    seen, prev = set(), None
    for c in chunks:
        if prev is not None and c.doc_id != prev and c.doc_id in seen:
            raise AssertionError("doc_id not contiguous")
        seen.add(c.doc_id); prev = c.doc_id
```
```python
def groups_by_doc(chunks):
    chunks = ensure_contiguous(chunks, key=attrgetter("doc_id"))
    for doc_id, grp in groupby(chunks, key=attrgetter("doc_id")):
        yield doc_id, grp  # stream; avoid list(grp) unless bounded

# Pitfall:
# If you advance to the next (doc_id, grp) without fully consuming `grp`,
# the shared underlying iterator has advanced; you cannot resume the old group.
# Always fully consume each `grp` (or explicitly materialize a *bounded* group)
# before moving on, otherwise elements for that key are lost.
```


Non-contiguous splits silently:
```python
# Bad: non-contiguous keys ⇒ split groups silently
xs = [{"k":"a"},{"k":"b"},{"k":"a"}]
[(k, len(list(g))) for k, g in groupby(xs, key=lambda r: r["k"])]
# => [("a",1), ("b",1), ("a",1)]  # WRONG if you expected a single "a" group
```
In RAG, contiguity is by construction (chunks per doc sequentially); assert in tests that doc_id does not regress. Note: At most one run in memory; list(grp) is allowed only if the run is bounded.
### 4.4 Tee Alternative: Lockstep Fan-Out
Avoid tee's cache with:
```python
# Lockstep fan-out (no tee cache)
def fanout(xs, *funcs):
    """Apply funcs in lockstep without caching; yields tuples.
    All funcs should be pure; side-effects break referential transparency."""
    for x in xs:
        yield tuple(f(x) for f in funcs)

# Use `tee` only when *both* consumers advance in strict lockstep.
# If one branch lags, `tee` grows an unbounded cache proportional to the lag.
# Prefer lockstep fan-out (above) or explicit bounded taps.
```
Concrete usage:
```python
# Instead of: from itertools import tee; a, b = tee(xs); ys = (f(next(a)) for _ in xs); zs = (g(next(b))...)
ys_zs = fanout(xs, f, g)  # lockstep; no cache growth
```
### 4.5 Backpressure and More Combinators
Use islice at the sink to bound upstream: `list(islice(gen_pipeline(...), 10))` pulls at most 10 docs from the source. Test with counters (e.g., wrap CleanDoc.abstract in a counting proxy to prove ≤k slices, as in Core 1).

Additional one-liners:
- takewhile: `yield from takewhile(lambda x: x < 5, xs)`
- dropwhile: `yield from dropwhile(lambda x: x < 5, xs)`
- filterfalse: `yield from filterfalse(lambda x: x % 2 == 0, xs)`
---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Inline chain → merges lazily.

**Bug Hunt:** Manual materializes; itertools defers.

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

### 6.1 Custom Strategy

As previous, plus env_st.

```python
env_st = st.builds(RagEnv, chunk_size=st.integers(min_value=32, max_value=1024))
```
### 6.2 Equivalence Property
```python
@given(st.lists(raw_doc_st, max_size=40), st.integers(min_value=64, max_value=1024))
def test_chain_equivalence(docs, chunk):
    env = RagEnv(chunk)
    eager = [c for cd in list(gen_clean_docs(docs)) for c in gen_chunk_doc(cd, env)]
    lazy = list(gen_pipeline(docs, env))
    assert lazy == eager
```
**Note:** Properties prove laws.
### 6.3 Shrinking Demo
Bad (list instead of chain): Materializes; fails memory.
### 6.4 Litmus Tests for Laws
```python
import itertools as it
import pytest
from rag_types import RawDoc, RagEnv
from core1 import gen_chunk_doc
from core2 import gen_clean_docs
from core3 import gen_pipeline, gen_chunked_docs, assert_contiguous_doc_ids

# D1_RAG (demand-boundedness from source)
docs = [RawDoc(str(i), "t", "x"*200, "c") for i in range(100)]
pulled = {"n": 0}
def gen_docs():
    for d in docs:
        pulled["n"] += 1
        yield d
k = 13
list(it.islice(gen_pipeline(gen_docs(), RagEnv(64)), k))
assert pulled["n"] <= k   # at most k docs pulled for k chunks

# F1_RAG (failure immediacy)
def gen_docs_failing_and_counted():
    for i, d in enumerate(docs):
        pulled["n"] += 1
        if i == 7:
            raise ValueError("boom at doc 7")
        yield d

it = gen_pipeline(gen_docs_failing_and_counted(), RagEnv(64))

with pytest.raises(ValueError):
    list(it)
assert pulled["n"] == 8   # pulled exactly up to the failing doc; no extra pulls

# O1/O2
out = list(gen_chunked_docs(gen_clean_docs([
    RawDoc("a","t","xx","c"), RawDoc("b","t","yy","c")]), RagEnv(1)))
assert [c.doc_id for c in out] == ["a","a","b","b"]  # O1

from collections import defaultdict
pos = defaultdict(list)
for c in out: pos[c.doc_id].append(c.start)
assert all(xs == sorted(xs) for xs in pos.values())  # O2

# G1: assert contiguity
assert_contiguous_doc_ids(out)
```
---

## 7. When Itertools Aren't Worth It

For mutable state; use custom.

---

## 8. Pre-Core Quiz
1. chain merges? → **Lazily.**
2. islice materializes? → **No.**
3. groupby needs? → **Contiguous.**
4. tee for? → **Branching.**
5. Manual equiv? → **list(composed).**

## 9. Post-Core Reflection & Exercise

**Reflect:** Find manual loop; refactor to itertools.

**Project Exercise:** Compose RAG; verify laziness.

**Next:** M03C04 – Chunking, Windowing, Grouping. (Builds on this.)

### Repository Alignment

- Implementation: `module-03/funcpipe-rag-03/src/funcpipe_rag/api/core.py::stream_chunks`, `gen_stream_embedded`, `gen_stream_deduped`.
- Tests: `module-03/funcpipe-rag-03/tests/test_module_03.py::test_stream_helpers_round_trip`.

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
