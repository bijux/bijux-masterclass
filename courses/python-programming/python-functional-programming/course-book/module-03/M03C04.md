# Module 3: Lazy Iteration and Streaming

## Progression Note
By the end of Module 3, you will master lazy generators, itertools mastery, and streaming pipelines that never materialize unnecessary data. This prepares you for safe recursion and error handling in streams (Module 4). See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus                                   | Key Outcomes                                           |
|--------|-----------------------------------------|--------------------------------------------------------|
| 2      | First-Class Functions & Expressive Python | Configurable pure pipelines without globals           |
| 3      | Lazy Iteration & Generators             | Memory-efficient streaming, itertools mastery, short-circuiting |
| 4      | Recursion & Error Handling in Streams   | Safe recursion, Result/Option, streaming errors        |

## M03C04: Chunking, Windowing, Grouping – Streaming Aggregations

> **Core question:**  
> How do you implement lazy chunking, sliding windows, and contiguous grouping in streaming pipelines to perform aggregations without materializing full collections, while preserving order and coverage?

This core builds on **Core 3**'s itertools composition by introducing the final classic patterns for streaming aggregations:
- Fixed-size chunking with configurable overlap and tail policy.
- Sliding windows with bounded deque auxiliary space.
- Contiguous grouping with streaming per-group processing.
- All purely lazy, with mathematically tight coverage and demand laws.

We continue the **running project** from `m03-rag.md`, now adding overlapping chunks (for better retrieval recall) and per-doc grouping (for future dedup/embedding stages).

**Audience:** Developers who have lazy pipelines but still materialise lists for chunking, windowing, or grouping — and pay the memory price.

**Outcome:**
1. Spot any `for i in range(0, len(text), step): text[i:i+k]` loop and instantly know you can make it lazy with overlap and tail handling.
2. Refactor it to a streaming generator in < 10 lines.
3. Write a Hypothesis property proving perfect reconstruction/coverage + exact demand bounds.

**Laws (frozen, used across this core):**
- E1 — Equivalence: For any finite re-iterable sequence xs: list(pipe(xs)) == eager_equiv(list(xs)).
- O1 — Global order: Output preserves input order (chunks/windows in appearance order).
- O2 — Monotone per-key: Within each key/doc_id, chunk.start values are non-decreasing.
- C1 — Coverage (chunking): 
  - tail_policy="emit_short": perfect reconstruction possible (concat with overlap drop).
  - tail_policy="pad": perfect reconstruction possible after stripping "\0".
  - tail_policy="drop": reconstruction covers the maximal prefix obtainable by a first chunk of length k followed by zero or more steps of size (k−o); whenever chunks are emitted we have len(rec) = k + m·(k−o) and len(text) − len(rec) < (k−o).

- D1 — Demand-boundedness: 
  - Sliding windows (deque): producing n windows pulls ≤ n + (w-1) upstream elements.
  - Chunking over indexable text: no upstream iterator pull; exactly one slice per emitted chunk.
- G1 — Groupby: Only valid if equal keys occur contiguously (by construction, not sorting).

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Implement chunking with fixed-step indexing, sliding windows with deque(maxlen=w), and grouping with groupby only on contiguous keys — never materialise the full collection for aggregation.**

### 1.2 Streaming Aggregations in One Precise Sentence

> Chunking divides indexable sequences into overlapping blocks, sliding windows emit bounded overlapping tuples via deque, and contiguous grouping streams (key, sub-iterator) pairs for per-group reductions — all with O(max(window, group)) auxiliary memory.

### 1.3 Why This Matters Now

Core 3 gave you composition primitives (chain, islice, groupby, tee).  
In real pipelines you still need to break text into chunks, create context windows, or aggregate per document — and doing it eagerly kills the laziness you just won.

These three patterns are the final building blocks that make truly unbounded, memory-constant pipelines possible.

### 1.4 Streaming Aggregations in 5 Lines

Sliding window with deque:

```python
from collections import deque

def sliding(xs, w: int):
    buf = deque(maxlen=w)
    for x in xs:
        buf.append(x)
        if len(buf) == w:
            yield tuple(buf)

Input: a b c d e f g
Window size 3:
    [a b c]
      [b c d]
        [c d e]
          [d e f]
            [e f g]
```

Bounded aux O(w); lazy; produces exactly len(xs) - w + 1 windows.

---

## 2. Mental Model: Eager vs Streaming Aggregations

### 2.1 One Picture

```text
Eager Aggregations (Full Materialize)   Streaming Aggregs (Lazy/Bounded)
+-------------------------------+       +------------------------------+
| list(xs) → windows/chunks     |       | xs → yield windows/chunks    |
|      → dict-of-lists          |       |      → groupby (contig)      |
| full everything in memory     |       | ↓                            |
| O(n) allocation               |       | O(max window/group) aux      |
+-------------------------------+       +------------------------------+
         ↑ OOM risk                            ↑ Unbounded-safe default
```

### 2.2 Behavioral Contract

| Aspect               | Eager (Lists/Dicts)                 | Streaming (Generators)                |
|----------------------|-------------------------------------|---------------------------------------|
| Memory               | O(n) full collections               | O(max window/group) bounded           |
| Computation          | All upfront                         | Per-item or per-group on demand       |
| Purity               | Mutation possible                   | Pure yields                           |
| Short-circuit        | No                                  | Yes (islice fence)                    |
| Equivalence          | Trivial                             | Proven via reconstruction (C1)        |

**When Eager Wins:** Tiny data you will random-access many times.

**Known Pitfalls:**
- groupby on non-contiguous keys silently splits groups.
- Sliding windows with deque: must consume fully or use tuple(buf) snapshots.
- Chunking may split grapheme clusters (code-point only).

**Unicode Policy:** Pure code-point slicing (Python native). For grapheme-aware chunking use third-party libraries (not in stdlib).

**Forbidden Patterns (CI-greppable):**
- `list(` or `sorted(` or `[*` in core pipeline files.
- `dict[` grouping without bounded groups.

---

## 3. Running Project: Windowed & Grouped Chunks in RAG

### 3.1 Types (Canonical, Used Throughout)

Extend RagEnv for overlap and tail policy (as defined in `rag_types.py`):

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RagEnv:
    chunk_size: int
    overlap: int = 0                  # New: 0 ≤ overlap < chunk_size
    tail_policy: str = "emit_short"   # "emit_short" | "drop" | "pad"
```

### 3.2 Eager Start (Anti-Pattern)

```python
# Eager overlapping chunks + grouping
chunks = []
for cd in list(gen_clean_docs(docs)):
    text = cd.abstract
    for i in range(0, len(text), env.chunk_size - env.overlap):
        j = i + env.chunk_size
        s = text[i:j]
        if s:
            chunks.append(ChunkWithoutEmbedding(cd.doc_id, s, i, j))

grouped = {}
for c in chunks:
    grouped.setdefault(c.doc_id, []).append(c)   # Full dict-of-lists
```

**Smells:** Full materialization of all chunks and all groups.

---

## 4. Refactor to Lazy: Aggregations in RAG

### 4.1 Lazy Core – The Final RAG Patterns

```python
from __future__ import annotations
from collections.abc import Iterable, Iterator
from collections import deque
from itertools import groupby, chain
from operator import attrgetter
from rag_types import RawDoc, CleanDoc, RagEnv, ChunkWithoutEmbedding
from core2 import gen_clean_docs  # M03C02
from core3 import ensure_contiguous  # M03C03

def gen_overlapping_chunks(
    doc_id: str,
    text: str,
    *,
    k: int,
    o: int = 0,
    tail_policy: str = "emit_short"
) -> Iterator[ChunkWithoutEmbedding]:
    """
    Laws:
      C1 (coverage): With emit_short/pad → perfect reconstruction possible.
                     With drop → covers the maximal floor-division prefix.
      D1: Exactly one slice per emitted chunk.
      Note: For tail_policy="pad", logical end j may exceed len(text).
    """
    if k <= 0 or not 0 <= o < k:
        raise ValueError("invalid chunk/overlap")
    step = k - o
    n = len(text)
    i = 0
    while i < n:
        j = i + k
        short_tail = j > n
        if short_tail and tail_policy == "drop":
            break
        segment = text[i:j]
        if short_tail and tail_policy == "pad":
            segment += "\0" * (k - len(segment))
            j = i + k   # logical end includes padding
        if segment:
            yield ChunkWithoutEmbedding(doc_id, segment, i, j)
        i += step

def sliding_windows(xs: Iterable, w: int) -> Iterator[tuple]:
    """D1: producing n windows pulls ≤ n + (w-1) upstream elements."""
    if w <= 0: raise ValueError
    buf = deque(maxlen=w)
    it = iter(xs)
    # Prime the buffer
    for _ in range(w - 1):
        try:
            buf.append(next(it))
        except StopIteration:
            return
    for x in it:
        buf.append(x)
        yield tuple(buf)

def gen_grouped_chunks(
    chunks: Iterable[ChunkWithoutEmbedding]
) -> Iterator[tuple[str, Iterator[ChunkWithoutEmbedding]]]:
    """G1: requires contiguity by construction."""
    chunks = ensure_contiguous(chunks, key=attrgetter("doc_id"))
    yield from groupby(chunks, key=attrgetter("doc_id"))

# Example streaming aggregation
def gen_per_doc_chunk_counts(
    chunks: Iterable[ChunkWithoutEmbedding]
) -> Iterator[tuple[str, int]]:
    for doc_id, grp in gen_grouped_chunks(chunks):
        yield doc_id, sum(1 for _ in grp)   # consumes group immediately

# Composed pipeline
def gen_rag_chunks(docs: Iterable[RawDoc], env: RagEnv) -> Iterator[ChunkWithoutEmbedding]:
    cleaned = gen_clean_docs(docs)
    yield from chain.from_iterable(
        gen_overlapping_chunks(cd.doc_id, cd.abstract, k=env.chunk_size, o=env.overlap, tail_policy=env.tail_policy)
        for cd in cleaned
    )
```

**Wins:** Perfect coverage with overlap; bounded memory; streaming per-doc ops.

**Complexity:**
| Pattern          | Time          | Aux Space       | Notes                              |
|------------------|---------------|-----------------|------------------------------------|
| Overlap chunking | Θ(len(text))  | O(1)            | One slice per chunk; end may > len(text) with pad |
| Sliding windows  | Θ(n)          | O(w)            | Exactly n - w + 1 windows          |
| Contiguous group | Θ(n)          | O(current run)  | Must fully consume each group      |

**Note:** Always fully consume a groupby sub-iterator before requesting the next group.

**Re-iterability Warning:** Single-pass; consume groups immediately.

### 4.2 Lazy Shell (Edge Only)

```python
chunked = gen_rag_chunks(read_docs(path), env)
grouped = gen_grouped_chunks(chunked)
for doc_id, grp in grouped:
    write_doc_chunks(doc_id, grp)   # atomic per doc if needed
```

**Note:** Fully streaming; atomic per group possible.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Inline overlapping chunker → yields with perfect reconstruction under emit_short/pad.

**Bug Hunt:** Eager materialises all chunks; streaming emits on demand with bounded work.

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

### 6.1 Custom Strategy

```python
text_st = st.text(min_size=0, max_size=1000)
k_st = st.integers(min_value=1, max_value=128)
o_st = st.integers(min_value=0, max_value=127)
```

### 6.2 Full Suite (All Laws Enforced)

```python
@given(text_st, k_st, o_st)
def test_chunking_coverage_emit_short(text, k, o):
    assume(o < k)
    chunks = list(gen_overlapping_chunks("id", text, k=k, o=o, tail_policy="emit_short"))
    rec = chunks[0].text if chunks else ""
    rec += "".join(c.text[o:] for c in chunks[1:])
    assert rec == text

@given(text_st, k_st, o_st)
def test_chunking_coverage_pad(text, k, o):
    assume(o < k)
    chunks = list(gen_overlapping_chunks("id", text, k=k, o=o, tail_policy="pad"))
    rec = chunks[0].text if chunks else ""
    rec += "".join(c.text[o:] for c in chunks[1:])
    assert rec.rstrip("\0") == text

@given(text_st, k_st, o_st)
def test_chunking_coverage_drop(text, k, o):
    assume(o < k)
    chunks = list(gen_overlapping_chunks("id", text, k=k, o=o, tail_policy="drop"))
    rec = chunks[0].text if chunks else ""
    rec += "".join(c.text[o:] for c in chunks[1:])
    assert text.startswith(rec)
    if chunks and len(text) >= k:
        step = k - o
        assert (len(rec) - k) % step == 0
        assert len(text) - len(rec) < step

@given(st.lists(st.integers(), min_size=0, max_size=200), st.integers(1, 20))
def test_sliding_window_demand_and_coverage(data, w):
    pulls = 0
    def counted():
        nonlocal pulls
        for x in data:
            pulls += 1
            yield x
    
    windows = list(sliding_windows(counted(), w))
    expected_windows = max(0, len(data) - w + 1)
    assert len(windows) == expected_windows
    assert pulls <= len(windows) + (w - 1)

    # perfect reconstruction when len(data) >= w
    if len(data) >= w:
        recon = list(windows[0])
        recon.extend(win[-1] for win in windows[1:])
        assert recon == data
```

### 6.3 Shrinking Demo: Catching a Real Bug

Bad version (no overlap handling in reconstruction):

```python
rec = "".join(c.text for c in chunks)   # wrong: double-counts overlap
```

Fails reconstruction law on any overlap > 0.

---

## 7. When Aggregations Aren't Worth It

Non-contiguous keys (sort first, paying O(n log n)); truly random access (materialise).

---

## 8. Pre-Core Quiz

1. Window aux space? → **O(w).**  
2. Groupby needs contiguous keys? → **Yes — guard or sort.**  
3. Chunking slices per chunk? → **Exactly one.**  
4. Coverage with overlap? → **Perfect under emit_short/pad.**  
5. Demand for n windows? → **≤ n + (w-1).**

## 9. Post-Core Reflection & Exercise

**Reflect:** Find any remaining list-building aggregation in your codebase — it is now obsolete.

**Project Exercise:** Add overlap=128 and tail_policy="emit_short" to your RAG env. Verify perfect reconstruction on a sample abstract and that memory stays flat on the 10k dataset.

**Next:** M03C05 – Infinite & Unbounded Sequences. (Builds on this.)

### Repository Alignment

- Implementation: `module-03/funcpipe-rag-03/src/funcpipe_rag/api/core.py::gen_overlapping_chunks`, `sliding_windows`, `gen_grouped_chunks`.
- Tests: `module-03/funcpipe-rag-03/tests/test_module_03.py::test_overlapping_coverage`, `::test_sliding_demand`.

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
