# Module 1: Foundational FP Concepts

## Progression Note
By the end of Module 1, you'll master purity laws, write pure functions, and refactor impure code using Hypothesis. This builds the foundation for lazy streams in Module 3. See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus | Key Outcomes |
|--------|-------|--------------|
| 1: Foundational FP Concepts | Purity, contracts, refactoring | Spot impurities, write pure functions, prove equivalence with Hypothesis |
| 2: ... | ... | ... |
| ... | ... | ... |

## M01C09: Equational Reasoning & Local Rewrite Rules for Pure Code

> **Core question:**  
> How do you use algebraic laws to rewrite pure code confidently—so that optimizations like fusing maps or moving filters are provably safe, and local changes don't break distant callers?

This core builds on **Core 1**'s mindset, **Core 2**'s contracts, **Core 3**'s immutability, **Core 4**'s composition, **Core 5**'s refactorings, **Core 6**'s combinators, **Core 7**'s typed pipelines, and **Core 8**'s explicit deps by teaching **equational reasoning and rewrite rules**:  
- Treat pure expressions as mathematical equals that can be substituted.  
- Apply laws like map fusion (map(f) ∘ map(g) = map(f ∘ g)) or filter-map commute.  
- Prove safety with Hypothesis for non-obvious cases.  
- Rewrite locally without breaking callers.  

We continue the **running project** from Core 1-8: refactoring the FuncPipe RAG Builder, now applying rewrites.

**Audience:** Developers who use Core 8's pure core but still fear optimizing pipelines without full re-testing.  
**Outcome:**  
1. Spot and apply 3–5 common rewrite rules (e.g., fuse maps, move filter before map) in < 10 lines.  
2. State side conditions for each rule (e.g., "holds if f, g are pure and total").  
3. Add Hypothesis properties backing up non-obvious rewrites.  
4. Perform a non-trivial pipeline refactor using equations + Hypothesis verification.  
5. Explain why equations beat "just test it" for local reasoning.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Treat pure code as math: if A == B, substitute freely; always check side conditions before rewriting.**

### 1.2 Equational Reasoning in One Precise Sentence

> Equational reasoning treats pure expressions as interchangeable equals under algebraic laws—so you can rewrite locally without re-testing the world, as long as side conditions (purity, totality) hold.

### 1.3 Why This Matters Now

Equations operationalize Core 8's pure core for optimization; without them, rewrites feel risky.

### 1.4 Three Rewrite Patterns You’ll Actually Use

1. Fuse maps: map(f) ∘ map(g) == map(f ∘ g)  
2. Move filter before map: If q(x) == p(f(x)) for all x, then filter(p) ∘ map(f) == map(f) ∘ filter(q)  
3. Eliminate second traversal: map(f) ∘ filter(p) == [f(x) for x in xs if p(x)]  

### 1.5 Rewrite Laws Table

| Law | Equation | Side Conditions |
|-----|----------|-----------------|
| Map fusion | map(f) ∘ map(g) = map(f ∘ g) | f, g pure & total |
| Filter–map commute | filter(p) ∘ map(f) = map(f) ∘ filter(q) | q(x) ≡ p(f(x)), f, p, q pure & total |
| Fuse filter+map passes | map(f) ∘ filter(p) = [f(x) for x in xs if p(x)] | f, p pure & total |

---

## 2. Mental Model: Risky Hack vs Safe Rewrite

### 2.1 One Picture

```text
Risky Hack (no equations)                  Safe Rewrite (with laws)
+---------------------------+            +------------------------------+
| # Before                  |            | # Equation:                  |
| for x in xs:              |            | map(f) ∘ map(g) == map(f ∘ g)|
|     y = g(x)              |            | # Side condition:            |
|     z = f(y)              |            | f,g pure/total               |
| # After (fingers crossed) |            | # After:                     |
| for x in xs:              |            | map(lambda x: f(g(x)))(xs)   |
|     z = f(g(x))           |            |                              |
+---------------------------+            +------------------------------+
```

### 2.2 Contract Table

| Clause                     | Violation Example                      | Detected By                              |
|----------------------------|----------------------------------------|------------------------------------------|
| Equational validity        | Rewrite breaks due to effects          | Hypothesis equivalence                   |
| Side conditions            | Impure f in map fusion                 | Code review + manual                     |
| Local reasoning            | Distant callers break on rewrite       | Hypothesis golden tests                  |
| Totality                   | Partial f in law                       | Hypothesis + explicit checks             |

**Note on Contracts:** Every law has side conditions (e.g., "holds if f is pure and total").

---

## 3. Running Project: Rewrites in RAG

Our **running project** (from `module-01/funcpipe-rag-01/README.md`) applies rewrites to Core 8's pure core.  
- **Goal:** Optimize with equations.  
- **Start:** Core 1-8's pure functions.  
- **End (this core):** Rewritten RAG pipeline. Semantics aligned with Core 1-8.

### 3.1 Types (Canonical)

These are defined in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_types.py` (as in Core 1) and imported as needed. No redefinition here.

### 3.2 Risky Variants (Anti-Patterns in RAG)

Full code:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py (risky helpers)
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, RagEnv, Chunk
import hashlib


# Risky clean (non-fused)
def risky_clean_doc(doc: RawDoc) -> CleanDoc:
    stripped = doc.abstract.strip()
    lower = stripped.lower()
    split = lower.split()
    abstract = " ".join(split)
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)


# Risky chunk (multi-pass, no fusion)
def risky_chunk_doc(doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    text = doc.abstract
    chunks = [text[i:i + env.chunk_size] for i in range(0, len(text), env.chunk_size)]
    with_ids = [
        ChunkWithoutEmbedding(doc.doc_id, c, i, i + len(c))
        for i, c in zip(range(0, len(text), env.chunk_size), chunks)
    ]
    return tuple(with_ids)


# Risky embed (multi-pass, non-fused)
def risky_embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    ints = [int(h[i:i + 4], 16) for i in range(0, 64, 4)]
    vec = [v / (16 ** 4 - 1) for v in ints]
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, tuple(vec))
```

**Smells:** Non-fused passes (multi-loop), no explicit equational laws for refactors, risky rewrites (no proofs).

---

## 4. Refactor to Safe: Equations & Rewrites in RAG

We still run the optimized pure core through the same Env-based shell from Core 8. For all chunking laws in this core we assume RagEnv.chunk_size >= 1 (invalid envs are excluded from the domain of the functions).

### 4.1 Fuse Maps

**Equation:** map(f) ∘ map(g) == map(f ∘ g)  
**Side condition:** f,g pure/total (total = “doesn’t raise, doesn’t loop forever, defined for all inputs of that type”).  
**When it’s not safe:** If f or g has side effects or is partial (raises on some inputs).  
**Before/After Diff (Generic Example):**

Before (two maps):

```python
def double_then_inc(xs: list[int]) -> list[int]:
    doubled = map(lambda x: x * 2, xs)
    inc = map(lambda y: y + 1, doubled)
    return list(inc)
```

After (fused):

```python
def double_then_inc(xs: list[int]) -> list[int]:
    return list(map(lambda x: (x * 2) + 1, xs))
```

**Process:** Fuse separate transforms into one; single pass.

**RAG Example (embed_chunk):** Instance of fusing multiple passes over derived hash nibbles (eliminate intermediates).

Before (multi-step):

```python
def risky_embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    ints = [int(h[i:i + 4], 16) for i in range(0, 64, 4)]
    vec = [v / (16**4 - 1) for v in ints]
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, tuple(vec))
```

After (fused map):

```python
def embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    vec = tuple(int(h[i:i + 4], 16) / (16**4 - 1) for i in range(0, 64, 4))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)
```

### 4.2 Move Filter Before Map

**Equation:** If q(x) == p(f(x)) for all x, then filter(p) ∘ map(f) == map(f) ∘ filter(q)  
**Side condition:** f,p,q pure/total; q really satisfies q(x) == p(f(x)).  
**When it’s not safe:** If p doesn't commute with f (no equivalent q exists) or f is partial.  
**Before/After Diff (Generic Example):**

Before (filter after map):

```python
def even_squares(xs: list[int]) -> list[int]:
    squares = map(lambda x: x * x, xs)
    evens = filter(lambda y: y % 2 == 0, squares)
    return list(evens)
```

After (filter before map):

```python
def even_squares(xs: list[int]) -> list[int]:
    evens = filter(lambda x: x % 2 == 0, xs)
    squares = map(lambda x: x * x, evens)
    return list(squares)
```

**Process:** Find q(x) == p(f(x)); move filter before map. Here p(y) = (y % 2 == 0), f(x) = x*x, and we choose q(x) = (x % 2 == 0) because evenness is preserved by squaring.

### 4.3 Eliminate Second Traversal

**Equation:** map(f) ∘ filter(p) == [f(x) for x in xs if p(x)]  
**Side condition:** f,p pure/total.  
**When it’s not safe:** If f or p has side effects.  
**Before/After Diff (Generic Example):**

Before (separate passes):

```python
def even_doubles(xs: list[int]) -> list[int]:
    evens = filter(lambda x: x % 2 == 0, xs)
    doubles = map(lambda y: y * 2, evens)
    return list(doubles)
```

After (inline single pass):

```python
def even_doubles(xs: list[int]) -> list[int]:
    return [x * 2 for x in xs if x % 2 == 0]
```

**Process:** Fuse filter/map into comprehension.

**RAG Example (chunk_doc):** Instance of “eliminate intermediates” law (replace chunks + with_ids multi-pass with a single comprehension).

Before (multi-pass with intermediate list):

```python
def risky_chunk_doc(doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    text = doc.abstract
    chunks = [text[i:i + env.chunk_size] for i in range(0, len(text), env.chunk_size)]
    with_ids = [
        ChunkWithoutEmbedding(doc.doc_id, c, i, i + len(c))
        for i, c in zip(range(0, len(text), env.chunk_size), chunks)
    ]
    return tuple(with_ids)
```

After (single-pass comprehension, no intermediate list):

```python
def chunk_doc(doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    text = doc.abstract
    return tuple(
        ChunkWithoutEmbedding(
            doc.doc_id,
            text[i:i + env.chunk_size],
            i,
            i + len(text[i:i + env.chunk_size]),
        )
        for i in range(0, len(text), env.chunk_size)
    )
```

**RAG Example (clean_doc):** Instance of ‘fuse passes’ law on a single string value.

Before (multi-step):

```python
def risky_clean_doc(doc: RawDoc) -> CleanDoc:
    stripped = doc.abstract.strip()
    lower = stripped.lower()
    split = lower.split()
    abstract = " ".join(split)
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)
```

After (inline):

```python
def clean_doc(doc: RawDoc) -> CleanDoc:
    abstract = " ".join(doc.abstract.strip().lower().split())
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)
```

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Replace expressions in `chunk_doc`.  
1. Inline generator → tuple of chunks.  
2. Substitute into full_rag → fixed value.  
**Cost Hunt:** In risky_chunk_doc, substitution is valid but you pay for an unnecessary intermediate chunks list. Rewrite chunk_doc is equationally equivalent and cheaper.

---

## 6. Property-Based Testing: Backing Up Rewrites (Advanced, Optional)

Use Hypothesis for non-obvious rewrites.

You can safely skip this on a first read and still follow later cores—come back when you want to mechanically verify your own refactors.

### 6.1 Custom Strategy (RAG Domain)

From `module-01/funcpipe-rag-01/tests/conftest.py` (as in Core 1).

### 6.2 Equivalence Property

Properties for rewrites (using the helpers in `module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py`):

Full code:

```python
# module-01/funcpipe-rag-01/tests/test_laws.py (excerpt)
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import clean_doc, chunk_doc, embed_chunk, risky_clean_doc, risky_chunk_doc, risky_embed_chunk,
    full_rag_pure, full_rag_pure_v1
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, RagEnv, Chunk
from .conftest import raw_doc_strategy, env_strategy, doc_list_strategy
from datetime import datetime

fixed_seed = 42
fixed_time = datetime(2024, 1, 1)


@given(st.lists(st.integers()))
def test_map_fusion_equivalence(xs: list[int]) -> None:
    f = lambda x: x + 1
    g = lambda x: x * 2
    left = list(map(f, map(g, xs)))
    right = list(map(lambda x: f(g(x)), xs))
    assert left == right


@given(st.builds(CleanDoc, doc_id=st.text(min_size=1), title=st.text(), abstract=st.text(), categories=st.text()),
       env_strategy())
def test_chunk_doc_rewrite_equivalence(doc: CleanDoc, env: RagEnv) -> None:
    risky = risky_chunk_doc(doc, env)
    rewritten = chunk_doc(doc, env)
    assert risky == rewritten


@given(st.builds(ChunkWithoutEmbedding, doc_id=st.text(min_size=1), text=st.text(min_size=1),
                 start=st.integers(min_value=0), end=st.integers(min_value=1)))
def test_embed_chunk_rewrite_equivalence(chunk: ChunkWithoutEmbedding) -> None:
    risky = risky_embed_chunk(chunk)
    rewritten = embed_chunk(chunk)
    assert risky == rewritten


@given(raw_doc_strategy())
def test_clean_doc_rewrite_equivalence(doc: RawDoc) -> None:
    risky = risky_clean_doc(doc)
    rewritten = clean_doc(doc)
    assert risky == rewritten


@given(doc_list_strategy(), env_strategy())
def test_full_rag_pipeline_equivalence(docs: list[RawDoc], env: RagEnv) -> None:
    # full_rag_pure_v1: before rewrites
    # full_rag_pure: after applying map/ filter fusion etc.
    chunks_v1, logs_v1 = full_rag_pure_v1(fixed_seed, fixed_time, docs, env)
    chunks_v2, logs_v2 = full_rag_pure(fixed_seed, fixed_time, docs, env)
    assert chunks_v1 == chunks_v2
    assert logs_v1 == logs_v2
```

**Note:** Properties back up equivalence for rewrites.

### 6.3 Shrinking Demo: Catching a Bug

Bad refactor (non-commuting in embed):

```python
import hashlib
from datetime import datetime
from funcpipe_rag import ChunkWithoutEmbedding, Chunk


def bad_embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    # Non-commuting: adds time-dependent salt before hash
    salted = chunk.text + str(datetime.now())
    h = hashlib.sha256(salted.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)
```

Property:

```python
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import ChunkWithoutEmbedding


@given(st.builds(ChunkWithoutEmbedding, doc_id=st.text(min_size=1), text=st.text(min_size=1),
                 start=st.integers(min_value=0), end=st.integers(min_value=1)))
def test_bad_embed_chunk_deterministic(chunk: ChunkWithoutEmbedding) -> None:
    assert bad_embed_chunk(chunk) == bad_embed_chunk(chunk)  # Falsifies due to time salt
```

Hypothesis failure trace (run to verify; example):

```
Falsifying example: test_bad_embed_chunk_deterministic(
    chunk=ChunkWithoutEmbedding(doc_id='a', text='a', start=0, end=1),
)
AssertionError
```

- Shrinks to minimal chunk; time salt changes output. Catches bug via shrinking.

---

## 7. When Equations Aren't Worth It

Rarely, for effects or partials, use tests; rely on Hypothesis for non-obvious.

---

## 8. Pre-Core Quiz

1. map(f) ∘ map(g) == ? → **map(f ∘ g)**  
2. filter(p) ∘ map(f) == ? (if commutes) → **map(f) ∘ filter(q)** where q(x) == p(f(x))  
3. Multi-pass → fix with? → **Single comprehension**  
4. Rewrite without side conditions → violates? → **Equational validity**  
5. Tool to back up non-obvious rewrite? → **Hypothesis**

## 9. Post-Core Reflection & Exercise

**Reflect:** In your code, find one multi-pass pipeline. Fuse with equations; check side conditions; prove with Hypothesis.  
**Project Exercise:** Apply rewrites to RAG; run properties on sample data.

All claims (e.g., referential transparency) are verifiable via the provided Hypothesis examples—run them to confirm.

**Further Reading:** For more on purity pitfalls, see 'Fluent Python' Chapter on Functions as Objects. Check free resources like Python.org's FP section or Codecademy's Advanced Python course for readers wanting basics.

**Next:** Core 10 – Idempotent & Monotone Transforms. (Builds on this RAG pure core.)
