# Module 1: Foundational FP Concepts

## Progression Note
By the end of Module 1, you'll master purity laws, write pure functions, and refactor impure code using Hypothesis. This builds the foundation for lazy streams in Module 3. See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus | Key Outcomes |
|--------|-------|--------------|
| 1: Foundational FP Concepts | Purity, contracts, refactoring | Spot impurities, write pure functions, prove equivalence with Hypothesis |
| 2: ... | ... | ... |
| ... | ... | ... |

## M01C10: Idempotent & Canonicalizing Transforms – Stability Under Repeated Application

> **Core question:**  
> How do you design pure transforms that are safe to apply repeatedly—idempotent (f(f(x)) == f(x)) and canonicalizing (mapping to a standard form like sorted and deduped)—so pipelines converge reliably without loops or guards?

This core builds on **Core 1**'s mindset, **Core 2**'s contracts, **Core 3**'s immutability, **Core 4**'s composition, **Core 5**'s refactorings, **Core 6**'s combinators, **Core 7**'s typed pipelines, **Core 8**'s explicit deps, and **Core 9**'s equational reasoning by ensuring pure transforms are **stable under repetition**:  
- Idempotent: applying twice = applying once.  
- Canonicalizing: output order determined by key, not by original input order; maps to a standard form that doesn’t depend on input order or duplicates.  
- Convergent: repeated application reaches fixed point (often in 1 step).  
- Checked with Hypothesis + manual bounds.  

We continue the **running project** from Core 1-9: refactoring the FuncPipe RAG Builder, now with stable transforms.

**Audience:** Developers who use Core 9 equations but still write `while changed: apply()` loops in normalization/dedup/cleaning code.  
**Outcome:**  
1. Refactor any “repeat until stable” loop into a single idempotent/canonicalizing call in < 10 lines.  
2. State and check idempotence + canonicalization (e.g. sorted, deduped, deterministic) for your domain transforms.  
3. Add Hypothesis properties checking convergence and fixed-point reachability.  
4. Spot and fix three classic instability smells: non-idempotent normalize, order-flipping ops, divergent iteration.  
5. Perform a non-trivial data-cleaning refactor using only stable combinators + Hypothesis verification.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Prefer idempotent + canonicalizing pure transforms when possible; only keep “repeat until stable” loops when you’ve checked convergence with Hypothesis and can’t refactor to a single pass.**

### 1.2 Idempotent & Canonicalizing Transforms in One Precise Sentence

> An idempotent transform satisfies f(f(x)) == f(x), reaching a fixed point in one step; when also canonicalizing (e.g., sorted, deduped, deterministic), it maps to a standard form that doesn’t depend on input order or duplicates.

**Note on Canonicalization:** In data pipelines, “canonicalizing” usually means: dedupe, sort by a key, and produce a deterministic representation so that logically-equal collections look byte-for-byte the same.

### 1.3 Why This Matters Now

Stable transforms add convergence to Core 9's equations; without it, pipelines need guards/loops.

### 1.4 Fixed Points in One Sentence

> If f(f(x)) == f(x), then f reaches a fixed point in 1 step for any input; extra applications do nothing.

```text
x --> f(x) --> f(f(x)) = f(x)  (fixed point; no change)
```

### 1.5 Purity Spectrum Table

| Level              | Description                          | Example                              |
|--------------------|--------------------------------------|--------------------------------------|
| Fully Pure         | Explicit inputs/outputs only         | `def add(x: int, y: int) -> int: return x + y` |
| Semi-Pure          | Observational taps (e.g., logging)   | `def add_with_log(x: int, y: int) -> int: log(f"Adding {x}+{y}"); return x + y` |
| Impure             | Globals/I/O/mutation                | `def read_file(path: str) -> str: ...` |

**Note on Purity Spectrum:** Only fully pure functions can sensibly be idempotent; semi-pure ‘log + return’ can be repeated but the log side-effect will accumulate.

---

## 2. Mental Model: Unstable Loop vs Stable Transform

### 2.1 One Picture

```text
Unstable Loop (imperative)                 Stable Transform (pure)
+---------------------------+            +---------------------------+
| changed = True            |            | result = normalize(data)  |
| while changed:            |            | # f(f(x)) == f(x)         |
|     changed = False       |            | # apply once → fixed point|
|     if bad:               |            |                           |
|         fix()             |            | no loop, no guard         |
|         changed = True    |            +---------------------------+
+---------------------------+            
```

### 2.2 Contract Table

| Clause                     | Violation Example                      | Detected By                              |
|----------------------------|----------------------------------------|------------------------------------------|
| Idempotence                | f(f(x)) ≠ f(x)                         | Hypothesis f(f(x)) == f(x)               |
| Canonicalization / order invariants | Output depends on input order / duplicates | Hypothesis checks canonical form |
| Convergence                | No fixed point after N applications    | Hypothesis repeated application          |
| Stability                  | Divergence / oscillation               | Hypothesis bounded search                |
| Refactor safety            | Manual loop → infinite                 | Executable properties                    |

**Note on Contracts:** Stability catches what loops never could.

---

## 3. Running Project: Stable Transforms in RAG

Our **running project** (from `module-01/funcpipe-rag-01/README.md`) adds stability to Core 9's pure core.  
- **Goal:** Make stages idempotent/canonicalizing.  
- **Start:** Core 1-9's pure functions.  
- **End (this core):** Stable RAG pipeline. Semantics aligned with Core 1-9.

In this RAG example we focus on idempotent, canonical “sorted & deduped” transforms.

### 3.1 Types (Canonical)

These are defined in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_types.py` (as in Core 1) and imported as needed. No redefinition here.

### 3.2 Unstable Variants (Anti-Patterns in RAG)

Full code:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py (unstable helpers)
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, RagEnv, Chunk
from datetime import datetime
import hashlib


# Unstable normalize_abstract (non-idempotent, divergent)
def unstable_normalize_abstract(abstract: str) -> str:
    # truly non-idempotent: trailing spaces accumulate
    return abstract.lower() + " "


# Unstable dedupe_and_sort_chunks (order-flipping)
def unstable_dedupe_and_sort_chunks(chunks: list[ChunkWithoutEmbedding]) -> list[ChunkWithoutEmbedding]:
    seen = set()
    unique = []
    for c in chunks:
        key = (c.doc_id, c.text, c.start, c.end)
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return list(reversed(unique))  # Flips order each time, breaking idempotence


# Unstable embed (divergent)
def unstable_embed_chunk(current_time: datetime, chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(f"{current_time.isoformat()}::{chunk.text}".encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)
```

**Smells:** Non-idempotent (changes on repeat), order-flipping (violates sortedness invariant), divergent (no fixed point).

---

## 4. Refactor to Stable: Idempotent & Canonicalizing in RAG

### 4.1 Stable Core

Idempotent/canonicalizing functions.

Full code:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py (stable helpers)
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, RagEnv, Chunk
import hashlib


def normalize_abstract(abstract: str) -> str:
    return " ".join(abstract.strip().lower().split())


def clean_doc(doc: RawDoc) -> CleanDoc:
    abstract = normalize_abstract(doc.abstract)
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)


def chunk_doc(doc: CleanDoc, env: RagEnv) -> list[ChunkWithoutEmbedding]:
    text = doc.abstract
    return [ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size])) for i
            in range(0, len(text), env.chunk_size)]


def embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    vec = tuple(int(h[i:i + 4], 16) / (16 ** 4 - 1) for i in range(0, 64, 4))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)


def docs_to_embedded(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    cleaned = [clean_doc(d) for d in docs]
    chunked = [c for doc in cleaned for c in chunk_doc(doc, env)]
    embedded = [embed_chunk(c) for c in chunked]
    return embedded


def structural_dedup_chunks(chunks: list[Chunk]) -> list[Chunk]:
    seen = set()
    result = []
    for c in sorted(chunks, key=lambda c: (c.doc_id, c.start)):
        key = (c.doc_id, c.text, c.start, c.end)
        if key not in seen:
            seen.add(key)
            result.append(c)
    return result


def full_rag(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    return structural_dedup_chunks(docs_to_embedded(docs, env))
```

`normalize_abstract` normalizes the abstract in an idempotent way (calling it twice yields the same string). `structural_dedup_chunks` removes duplicates while sorting by doc_id and start, so applying it twice is the same as once. Because `full_rag` simply threads the pure stages (`clean_doc` → `chunk_doc` → `embed_chunk`) and finishes with `structural_dedup_chunks`, the entire pipeline reaches a fixed point in a single pass.

**Wins:** Idempotent (repeat unchanged), canonicalizing (sorted by doc_id/start, deduped by (doc_id, text, start, end)), convergent (fixed point in 1 step), semantics aligned with Core 1-9.

### 4.2 Impure Shell (Edge Only)

The shell from Core 8 remains; stability focuses on core.

### 4.3 Case Study: Removing a real while-changed loop

A common instability smell in data cleaning is using a `while changed:` loop for repeated normalization, like collapsing multiple spaces in text. Here's how to refactor it to a single idempotent/canonicalizing transform, eliminating the loop.

**Unstable Version (with loop):**

```python
# Unstable collapse_spaces (requires loop for convergence)
def unstable_collapse_spaces(text: str) -> str:
    res = text.strip().lower()
    changed = True
    while changed:
        changed = False
        if "  " in res:
            res = res.replace("  ", " ")
            changed = True
    return res
```

**Smells:** Unnecessary loop (could converge in O(log n) worst-case but still imperative); not obviously idempotent without running.

**Stable Refactor (single pass, idempotent):**

```python
# Stable collapse_spaces (idempotent, canonicalizing)
def collapse_spaces(text: str) -> str:
    return " ".join(text.strip().lower().split())
```

**Process:** Replace loop with a canonicalizing comprehension: split on whitespace (removes extras), join with single space. Now f(f(x)) == f(x) by construction—no loop needed.

**Hypothesis Property (ties to no loop needed):**

```python
import hypothesis.strategies as st
from hypothesis import given

@given(st.text())
def test_collapse_spaces_idempotent(s: str) -> None:
    assert collapse_spaces(collapse_spaces(s)) == collapse_spaces(s)
```

**RAG Integration:** Use `collapse_spaces` inside `normalize_abstract` for cleaning abstracts. The property ensures one application suffices; extra calls (e.g., in pipelines) do nothing.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Replace expressions in `full_rag`.  
1. Inline `normalize_abstract(d.abstract)` → normalized string.  
2. Substitute into chunks → list of chunks.  
3. Result: Entire call = fixed value + logs.  
**Bug Hunt:** In unstable_normalize_abstract, substitution fails (adds space).

---

## 6. Property-Based Testing: Checking Stability (Advanced, Optional)

Use Hypothesis to check stability, tying directly to "no loop needed" by verifying fixed points in one step.

You can safely skip this on a first read and still follow later cores—come back when you want to mechanically verify your own refactors.

To bridge theory and practice, here's a simple Hypothesis example illustrating impurity detection:

```python
import random
from hypothesis import given
import hypothesis.strategies as st

def impure_random_add(x: int) -> int:
    return x + random.randint(1, 10)  # Non-deterministic

@given(st.integers())
def test_detect_impurity(x):
    assert impure_random_add(x) == impure_random_add(x)  # Falsifies due to randomness

# Hypothesis will quickly find differing outputs for the same x
```

This property test detects the impurity by showing outputs vary for identical inputs—run it to see Hypothesis in action.

### 6.1 Custom Strategy (RAG Domain)

From `module-01/funcpipe-rag-01/tests/conftest.py` (as in Core 1).

### 6.2 Equivalence Property

Properties for stability (using the helpers in `module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py`):

Full code:

```python
# module-01/funcpipe-rag-01/tests/test_laws.py (excerpt)
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import structural_dedup_chunks, full_rag
from funcpipe_rag import Chunk, RawDoc, RagEnv
from .conftest import doc_list_strategy, env_strategy


@given(st.lists(st.builds(Chunk, doc_id=st.text(min_size=1), text=st.text(min_size=1), start=st.integers(min_value=0),
                          end=st.integers(min_value=1), embedding=st.tuples(*[st.just(0.0) for _ in range(16)])))
def test_structural_dedup_idempotent(chunks: list[Chunk]) -> None:
    assert structural_dedup_chunks(structural_dedup_chunks(chunks)) == structural_dedup_chunks(chunks)


@given(st.lists(st.builds(Chunk, doc_id=st.text(min_size=1), text=st.text(min_size=1), start=st.integers(min_value=0),
                          end=st.integers(min_value=1), embedding=st.tuples(*[st.just(0.0) for _ in range(16)])))
def test_structural_dedup_no_duplicates(chunks: list[Chunk]) -> None:
    deduped = structural_dedup_chunks(chunks)
    assert len(deduped) == len(set((c.doc_id, c.text, c.start, c.end) for c in deduped))


@given(st.lists(st.builds(Chunk, doc_id=st.text(min_size=1), text=st.text(min_size=1), start=st.integers(min_value=0),
                          end=st.integers(min_value=1), embedding=st.tuples(*[st.just(0.0) for _ in range(16)])))
def test_structural_dedup_sorted(chunks: list[Chunk]) -> None:
    deduped = structural_dedup_chunks(chunks)
    assert deduped == sorted(deduped, key=lambda c: (c.doc_id, c.start))


@given(doc_list_strategy(), env_strategy())
def test_structural_dedup_fixpoint(docs: list[RawDoc], env: RagEnv) -> None:
    chunks = full_rag(docs, env)
    assert structural_dedup_chunks(chunks) == chunks


@given(doc_list_strategy(), env_strategy())
def test_full_rag_deterministic(docs: list[RawDoc], env: RagEnv) -> None:
    result1 = full_rag(docs, env)
    result2 = full_rag(docs, env)  # Repeat application
    assert result1 == result2
```

**Note:** Properties check idempotence, no duplicates, sorted order, convergence—ensuring no loop is needed.

### 6.3 Shrinking Demo: Catching a Bug

Bad refactor (divergent in full_rag):

```python
from funcpipe_rag import Chunk


def bad_structural_dedup_chunks(chunks: list[Chunk]) -> list[Chunk]:
    seen = set()
    result = []
    for c in chunks:
        if c not in seen:
            seen.add(c)
            result.append(c)
    result.reverse()  # Always flip order, breaking idempotence
    return result
```

Property:

```python
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import Chunk


@given(st.lists(st.builds(Chunk, doc_id=st.text(min_size=1), text=st.text(min_size=1), start=st.integers(min_value=0),
                          end=st.integers(min_value=1), embedding=st.tuples(*[st.just(0.0) for _ in range(16)])))
def test_bad_structural_dedup_idempotent(chunks: list[Chunk]) -> None:
    assert bad_structural_dedup_chunks(bad_structural_dedup_chunks(chunks)) == bad_structural_dedup_chunks(
        chunks)  # Falsifies due to order flip
```

Hypothesis failure trace (run to verify; example):

```
Falsifying example: test_bad_structural_dedup_idempotent(
    chunks=[Chunk(doc_id='a', text='a', start=0, end=1, embedding=(0.0, 0.0, ...)), Chunk(doc_id='b', text='b', start=0, end=1, embedding=(0.0, 0.0, ...))],
)
AssertionError
```

- Shrinks to two distinct chunks; order flip changes output. Catches bug via shrinking.

---

## 7. When Stable Transforms Aren't Worth It

Rarely, for unbounded iterations or hot paths, use loops; check convergence with Hypothesis and prove convergence on paper for critical code paths. Sometimes you genuinely have a multi-step iterative algorithm (e.g., fixed-point inference over a graph). For those, you keep the loop, but it’s still useful to make each step as close to idempotent/canonicalizing as possible.

---

## 8. Pre-Core Quiz

1. f(f(x)) ≠ f(x) → violates? → **Idempotence**  
2. Output depends on input order → violates? → **Canonicalization**  
3. No fixed point → violates? → **Convergence**  
4. "while changed:" loop → fix with? → **Stable transform**  
5. Tool to explore convergence with property-based tests? → **Hypothesis**

## 9. Post-Core Reflection & Exercise

**Reflect:** In your code, find one “repeat until stable” loop. Make idempotent/canonicalizing; check with Hypothesis; replace with single call.  
**Project Exercise:** Add stability to RAG; run properties on sample data.

All claims (e.g., referential transparency) are verifiable via the provided Hypothesis examples—run them to confirm.

**Further Reading:** For more on purity pitfalls, see 'Fluent Python' Chapter on Functions as Objects. Check free resources like Python.org's FP section or Codecademy's Advanced Python course for readers wanting basics.

**Next:** Module 2 – Closures, Expressions, and FP-Friendly APIs. (Builds on this RAG pure core.)
