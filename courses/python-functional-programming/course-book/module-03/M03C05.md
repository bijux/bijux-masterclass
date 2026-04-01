# Module 3: Lazy Iteration and Streaming

## Progression Note
By the end of Module 3, you will master lazy generators, itertools mastery, and streaming pipelines that never materialize unnecessary data. This prepares you for safe recursion and error handling in streams (Module 4). See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus                                   | Key Outcomes                                           |
|--------|-----------------------------------------|--------------------------------------------------------|
| 2      | First-Class Functions & Expressive Python | Configurable pure pipelines without globals           |
| 3      | Lazy Iteration & Generators             | Memory-efficient streaming, itertools mastery, short-circuiting |
| 4      | Recursion & Error Handling in Streams   | Safe recursion, Result/Option, streaming errors        |

## M03C05: Infinite & Unbounded Sequences – Fencing with islice, takewhile, dropwhile

> **Core question:**  
> How do you safely handle infinite or unbounded sequences in lazy pipelines by using fencing tools like islice, takewhile, and dropwhile to bound demand, short-circuit computation, and prevent resource exhaustion?

This core builds on **Core 4**'s streaming aggregations by introducing defensive fencing techniques for truly unbounded or potentially infinite sources:
- Use `islice` for hard numeric caps.
- Use `takewhile` / `dropwhile` for predicate-driven stops and skips.
- Combine with generator expressions for filtering, then fence.
- Make it possible to guarantee termination and bounded work even on infinite inputs by placing explicit fences.

We continue the **running project** from `m03-rag.md`, now adding robust fences to protect against pathological inputs (huge docs, infinite streams, malicious APIs).

**Audience:** Developers processing untrusted or potentially infinite streams (logs, network, generators) who need hard guarantees against hangs and OOM.

**Outcome:**
1. Spot any unfenced consumption of an iterator that could be unbounded and know it's a denial-of-service vulnerability.
2. Add a safe fence in ≤ 3 lines.
3. Write a Hypothesis property proving exact demand bounds and short-circuit.

**Laws (frozen, used across this core):**
- E1 — Prefix equivalence: For any re-iterable finite prefix S and k ≥ 0: list(islice(P(iter(S)), k)) == eager_equiv(S)[:k].
- D1a — islice demand: list(islice(xs, k)) pulls exactly min(k, |xs|) elements from xs; no extra probe.
- D1b — takewhile demand: If predicate eventually fails after n yields, pulls exactly n+1; if source exhausts while predicate True, pulls exactly n.
- D1c — dropwhile demand: If predicate eventually fails after m elements, pulls exactly m+1; if source exhausts while predicate True, pulls exactly m.
- F1 — Safe on infinite: 
  - islice(xs, k) terminates for any finite k.
  - takewhile(pred, xs) terminates iff pred eventually False on xs.
  - dropwhile(pred, xs) terminates iff xs is finite or pred eventually False on xs.
- S1 — Single-pass discipline: Pipelines never assume re-iterability unless explicitly fenced or duplicated.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Always fence consumption of any iterator that is not provably finite and small with islice (hard cap) or takewhile/dropwhile (predicate cap) — never trust unbounded sources.**

### 1.2 Fencing in One Precise Sentence

> islice bounds to a fixed prefix (exact demand), takewhile yields while predicate holds (pulling one extra on failure), dropwhile skips while predicate holds (pulling one extra on failure) — all lazy, O(1) aux, exact demand.

### 1.3 Why This Matters Now

Core 4 gave you chunking, windows, and grouping — all safe on finite data.  
Real systems have infinite logs, malicious APIs, or bugs that produce unbounded output.  
Unfenced pipelines become denial-of-service vulnerabilities.

Fencing is the final defensive layer that makes lazy pipelines production-hardened.

### 1.4 Fencing in 5 Lines

```python
from itertools import islice, count, takewhile

inf = count()                          # truly infinite
bounded = islice(inf, 10)              # hard cap
print(list(bounded))                   # [0..9], then stops

inf2 = count()                         # fresh infinite source
pred_bounded = takewhile(lambda x: x < 10, inf2)
print(list(pred_bounded))              # [0..9], stops on first False (pulls 11th to check)
```

Safe termination even on infinite sources.

---

## 2. Mental Model: Unfenced vs Fenced Streams

### 2.1 One Picture

```text
Unfenced (Dangerous)                    Fenced (Safe)
+-----------------------+               +------------------------------+
| inf → for/list/[*]    |               | inf → islice/takewhile       |
|        ↓              |               |        ↓                     |
| hangs / OOM / DoS     |               | bounded termination*         |
| never returns         |               | bounded work                 |
+-----------------------+               +------------------------------+
   ↑ Vulnerability                        ↑ Production-ready default

(* assuming fences and predicates satisfy F1.)
```

### 2.2 Behavioral Contract

| Aspect               | Unfenced                            | Fenced (islice/takewhile/dropwhile) |
|----------------------|-------------------------------------|-------------------------------------|
| Termination          | Never on infinite                   | Always with islice; with take/dropwhile iff predicate eventually fails or source finite |
| Demand               | Unbounded                           | Exactly specified (D1a/D1b/D1c)     |
| Memory               | Risk of explosion                   | O(1) aux                            |
| Short-circuit        | No                                  | Immediate on bound/predicate        |

**When Unfenced is Acceptable:** Only for provably finite, small, trusted sources (e.g., in-memory config of < 100 items).

**Fence Placement Rules (memorise):**
1. Filter/map first → then fence.
2. After any fan-out → fence each branch.
3. Before expensive work (embedding, network, disk).
4. At pipeline sink → always fence user/configurable bounds.

**Known Pitfalls:**
- `takewhile`/`dropwhile` pull one extra element to check predicate.
- `islice` consumes prefix permanently (single-pass).
- Predicate must be pure and fast (called on every element).

**Forbidden Patterns (CI-greppable):**
- `for x in unbounded_source:` without fence
- `list(unbounded_source)`
- `[*unbounded_source]`

---

## 3. Running Project: Fenced Streams in RAG

### 3.1 Types (Canonical, Used Throughout)

From previous cores; RagEnv unchanged.

### 3.2 Unfenced Risk (Anti-Pattern)

```python
# Dangerous: no bound
chunks = gen_rag_chunks(read_docs(path), env)   # infinite/malicious docs → hangs forever
list(chunks)                                    # never returns, OOM possible
```

**Smells:** Trusts input size; vulnerable to huge/malicious streams.

---

## 4. Refactor to Safe: Fencing in RAG

### 4.1 Defensive Core – Hardened Patterns

```python
from __future__ import annotations
from itertools import islice, takewhile, dropwhile
from collections.abc import Iterable, Iterator
from rag_types import RawDoc, RagEnv, ChunkWithoutEmbedding
from core2 import gen_clean_docs
from core4 import gen_rag_chunks   # overlapping + tail policy

def gen_bounded_chunks(
    docs: Iterable[RawDoc],
    env: RagEnv,
    *,
    max_chunks: int | None = None,
) -> Iterator[ChunkWithoutEmbedding]:
    """
    Hard cap on total chunks produced.
    D1a: pulls at most max_chunks (or less if source exhausts).
    """
    if max_chunks is None:
        yield from gen_rag_chunks(docs, env)
        return

    chunked = gen_rag_chunks(docs, env)
    yield from islice(chunked, max_chunks)

def gen_long_docs_only(
    docs: Iterable[RawDoc],
    min_abstract_len: int = 1000
) -> Iterator[RawDoc]:
    """Skip leading short docs only — useful when short docs are noise at the beginning."""
    return dropwhile(lambda d: len(d.abstract) < min_abstract_len, docs)

def gen_sufficient_context_chunks(
    chunks: Iterable[ChunkWithoutEmbedding],
    min_tokens_per_chunk: int = 100
) -> Iterator[ChunkWithoutEmbedding]:
    """Stop at the first chunk that is too short — assumes monotone degradation (e.g. tail chunks shrink)."""
    return takewhile(lambda c: len(c.text.split()) >= min_tokens_per_chunk, chunks)

# Composed production pattern
def safe_rag_pipeline(
    docs: Iterable[RawDoc],
    env: RagEnv,
    *,
    max_chunks: int = 10_000,
    min_doc_len: int = 500,
) -> Iterator[ChunkWithoutEmbedding]:
    docs = gen_long_docs_only(docs, min_doc_len)          # drop leading short docs
    chunks = gen_rag_chunks(docs, env)
    chunks = gen_sufficient_context_chunks(chunks)        # takewhile good chunks (monotone assumption)
    yield from islice(chunks, max_chunks)                 # hard global cap
```

**Wins:** Guaranteed termination; bounded work; composable defenses.

**Complexity:**
| Fence             | Time Bound                  | Demand Pulls                  | Notes                              |
|-------------------|-----------------------------|-------------------------------|------------------------------------|
| islice(xs, k)     | O(k)                        | Exactly k (or less)           | Hard cap                           |
| takewhile(pred)   | O(n+1) where n = yield count| n+1 if pred fails; n if exhausts | Predicate-driven stop              |
| dropwhile(pred)   | O(m+1) where m = skipped    | m+1 if pred fails; all if never | Skip leading prefix                |

**Note:** Always fence user-configurable bounds and before expensive stages.

**Re-iterability Warning:** Fences consume irrevocably; design pipelines to be re-runnable from source if needed.

### 4.2 Defensive Shell (Production Pattern)

```python
chunks = safe_rag_pipeline(
    read_docs(path),
    env,
    max_chunks=config.max_chunks,      # from CLI/ config, default 10_000
    min_doc_len=config.min_doc_len,
)
write_jsonl_atomic(output_path, chunks)   # bounded write → safe
```

**Note:** Even on infinite/malicious input → terminates gracefully.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Inline islice → bounds lazily without overpull.

**Bug Hunt:** Unfenced loops exhaust infinite sources; fenced short-circuit safely.

---

## 6. Property-Based Testing: Proving Fencing Laws

### 6.1 Custom Strategy

```python
inf_st = st.lists(st.integers(), max_size=1000)   # simulate prefix of infinite
```

### 6.2 Full Suite (All Laws Enforced)

```python
@given(st.lists(st.integers(), max_size=200), st.integers(0, 300))
def test_islice_exact_demand(data, k):
    pulls = 0
    def counted():
        nonlocal pulls
        for x in data:
            pulls += 1
            yield x

    bounded = list(islice(counted(), k))
    assert len(bounded) == min(k, len(data))
    assert pulls == len(bounded)   # D1a: exactly min(k, len(xs)), no extra

@given(st.lists(st.integers(), max_size=200), st.integers(0, 100))
def test_takewhile_demand(data, stop_at):
    pulls = 0
    def counted():
        nonlocal pulls
        for x in data:
            pulls += 1
            yield x

    # leading True prefix length
    n = 0
    for x in data:
        if x < stop_at:
            n += 1
        else:
            break
    has_failure = n < len(data)

    bounded = list(takewhile(lambda x: x < stop_at, counted()))
    assert len(bounded) == n
    assert pulls == n + (1 if has_failure else 0)   # D1b exact

@given(st.lists(st.integers(), max_size=200), st.integers(0, 100))
def test_dropwhile_demand(data, start_at):
    pulls = 0
    def counted():
        nonlocal pulls
        for x in data:
            pulls += 1
            yield x

    # leading True prefix length
    m = 0
    for x in data:
        if x < start_at:
            m += 1
        else:
            break
    has_failure = m < len(data)

    dropped = list(dropwhile(lambda x: x < start_at, counted()))
    assert pulls == m + (1 if has_failure else 0)   # D1c exact
```

### 6.3 Shrinking Demo: Catching an Overpull Bug

Bad version (manual loop instead of islice):

```python
def bad_bounded(xs, k):
    i = 0
    for x in xs:
        if i >= k:
            break
        yield x
        i += 1
        next(xs)   # BUG: extra pull!
```

Property fails: pulls = 2k on long input.

---

## 7. When Fencing Isn't Worth It

Only for provably finite, small, trusted sources (e.g., in-memory config of < 100 items).

Everything else → fence aggressively.

---

## 8. Pre-Core Quiz

1. `islice` pulls extra? → **Never more than k.**  
2. `takewhile` on infinite True? → **Infinite — always fence after.**  
3. Safe on infinite source? → **Only with islice or eventual predicate failure.**  
4. Predicate in takewhile? → **Must be pure and fast.**  
5. Dropwhile demand? → **Up to and including first False.**

## 9. Post-Core Reflection & Exercise

**Reflect:** Audit every iterator consumption in your codebase — any without a fence is now a latent DoS bug.

**Project Exercise:** Add `max_chunks=10_000` and `min_doc_len=500` defaults to your RAG config. Verify on a malicious 1 TB simulated input that the pipeline terminates in < 1 second.

**Next:** M03C06 – Building Reusable Iterator-Based FuncPipe Stages. (Builds on this.)

### Repository Alignment

- Implementation: `module-03/funcpipe-rag-03/src/funcpipe_rag/api/core.py::safe_rag_pipeline`, `gen_bounded_chunks`.
- Tests: `module-03/funcpipe-rag-03/tests/test_module_03.py::test_fencing_demand_exact`, `::test_fencing_infinite_safe`.

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
