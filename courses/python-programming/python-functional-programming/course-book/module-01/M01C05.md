# Module 1: Foundational FP Concepts

## Progression Note
By the end of Module 1, you'll master purity laws, write pure functions, and refactor impure code using Hypothesis. This builds the foundation for lazy streams in Module 3. See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus | Key Outcomes |
|--------|-------|--------------|
| 1: Foundational FP Concepts | Purity, contracts, refactoring | Spot impurities, write pure functions, prove equivalence with Hypothesis |
| 2: ... | ... | ... |
| ... | ... | ... |

## M01C05: Local FP Refactorings – Replace In-Place Loops with Small Pure Transforms

> **Core question:**  
> How do you systematically refactor imperative, stateful code into small, pure, composable functions—so that hidden mutations vanish, equational reasoning becomes possible, and every change is locally verifiable?

This core builds on **Core 1**'s mindset, **Core 2**'s contracts, **Core 3**'s immutability, and **Core 4**'s composition by applying it locally: **refactor one function at a time**, turning loops, mutable accumulators, and in-place updates into pure transforms over immutable data.

We continue the **running project** from Core 1-4: refactoring the FuncPipe RAG Builder, now replacing imperative accumulators with pure equivalents.

**Audience:** Developers who love Core 4 pipelines but still have legacy functions full of `for` loops, `while`, list.append(), dict updates, and index juggling.  
**Outcome:**  
1. Refactor any stateful function into pure equivalent in < 20 lines.  
2. Explain why manual accumulators hurt reasoning/testing vs comprehensions/folds.  
3. Add Hypothesis properties proving refactor equivalence + new purity.  
4. Spot and fix three classic refactor blockers: multiple accumulators, index-dependent logic, mutable defaults.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Default to no mutation of inputs/shared state; keep loops index-free when possible; express work as map/filter/fold over immutable data.**

### 1.2 Local Refactoring in One Precise Sentence

> Local FP refactoring replaces stateful code by extracting pure functions, eliminating mutable accumulators/shared state, and preferring comprehensions/folds over index-heavy loops while preserving observable behavior.

### 1.3 Why This Matters Now

Local refactoring operationalizes Core 1-4's tools on real code, enabling typed pipelines (Core 6) and effect extraction (Core 7); without it, legacy state blocks progress.

### 1.4 Refactor Moves in This Core

1. Loop → map  
2. Accumulator → comprehension  
3. In-place update → new object  

### 1.5 Purity Spectrum Table

| Level              | Description                          | Example                              |
|--------------------|--------------------------------------|--------------------------------------|
| Fully Pure         | Explicit inputs/outputs only         | `def add(x: int, y: int) -> int: return x + y` |
| Semi-Pure          | Observational taps (e.g., logging)   | `def add_with_log(x: int, y: int) -> int: log(f"Adding {x}+{y}"); return x + y` |
| Impure             | Globals/I/O/mutation                | `def read_file(path: str) -> str: ...` |

**Note on Semi-Pure:** This is a pragmatic category for functions that are observationally transparent for business logic (i.e., they behave as if pure for callers) but are still impure in the strict FP sense due to side effects like logging. Allow this only at edges or in debugging taps.

---

## 2. Mental Model: Stateful Mess vs Pure Transform

### 2.1 One Picture

```text
Stateful Loop                               Pure Transform
+----------------------------------+        +--------------------------------+
| results = []                     |        | results = [                    |
| totals = {}                      |        |     f(x) for x in xs           |
| for x in xs:                     |        |     if pred(x)                 |
|     results.append(f(x))         |        | ]                              |
|     totals[x] = totals.get(x,0)+1|        | totals = Counter(xs)           |
| return results, totals           |        +--------------------------------+
+----------------------------------+        No mutation of inputs/shared state
```

### 2.2 Contract Table

| Clause                     | Violation Example                      | Detected By                              |
|----------------------------|----------------------------------------|------------------------------------------|
| No shared mutation         | In-place list.sort() / append          | Hypothesis + deepcopy equality           |
| Equivalence                | Old vs new disagree                    | Hypothesis golden-test property          |
| No hidden state            | Closure over mutable                   | Manual review + Hypothesis               |
| Determinism                | Random/state inside loop               | Hypothesis determinism                   |

**Note on Refactors:** Safe only when old/new agree on all inputs—prove it. Note: Some stateful variants here are observationally pure (their mutation is confined to local variables), others like stateful_add_chunk are truly impure (shared mutable defaults). We treat both as refactor targets for clarity and safety.

---

## 3. Running Project: Local Refactorings in RAG

Our **running project** (from `module-01/funcpipe-rag-01/README.md`) refactors RAG stages locally to pure.  
- **Goal:** Eliminate mutable accumulators/indexing.  
- **Start:** Core 1-4's pure functions.  
- **End (this core):** Refactored stages with equivalence properties. Semantics aligned with Core 1-4.

### 3.1 Types (Canonical)

These are defined in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_types.py` (as in Core 1) and imported as needed. No redefinition here.

### 3.2 Stateful Variants (Anti-Patterns in RAG)

Full code:

```python
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, RagEnv, Chunk
import hashlib


# Stateful clean (mutable accum)
def stateful_clean_doc(doc: RawDoc) -> CleanDoc:
    abstract = ""
    for word in doc.abstract.strip().lower().split():
        abstract += word + " "  # Mutable string accum
    return CleanDoc(doc.doc_id, doc.title, abstract.strip(), doc.categories)


# Stateful chunk (multiple accumulators)
def stateful_chunk_doc(doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    text = doc.abstract
    chunks: list[ChunkWithoutEmbedding] = []
    starts: list[int] = []
    i = 0
    while i < len(text):
        end = min(i + env.chunk_size, len(text))
        chunks.append(ChunkWithoutEmbedding(doc.doc_id, text[i:end], i, end))
        starts.append(i)  # Conflated accum
        i = end
    return tuple(chunks)  # Second accum unused; bug risk


# Stateful embed (mutable accum)
def stateful_embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = []
    for i in range(0, 64, step):
        val = int(h[i:i + step], 16) / (16 ** step - 1)
        vec.append(val)  # Mutable accum
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, tuple(vec))


# Stateful mutable default (classic blocker)
def stateful_add_chunk(chunks: list[Chunk] = []) -> list[Chunk]:  # Mutable default
    chunks.append(Chunk("id", "text", 0, 5, tuple(range(16))))
    return chunks
```

**Smells:** Mutable accum (string/list), multiple accum (error-prone), manual indexing (off-by-one risk), mutable defaults (shared across calls).

### 3.3 RAG-Specific Refactors

#### RAG Example (clean_doc): Accumulator → Comprehension

Before: abstract = "" + loop concat.

After:

```python
from funcpipe_rag import RawDoc, CleanDoc


def clean_doc(doc: RawDoc) -> CleanDoc:
    abstract = " ".join(doc.abstract.strip().lower().split())
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)
```

#### RAG Example (chunk_doc): Loop → Map

`module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py` uses a single list comprehension—no manual indexes beyond the comprehension range, and no mutable accumulators:

```python
from funcpipe_rag import CleanDoc, ChunkWithoutEmbedding, RagEnv


def chunk_doc(doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    text = doc.abstract
    return tuple(
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]))
        for i in range(0, len(text), env.chunk_size)
    )
```

**Note:** If your legacy function returns tuples, keep the same outer container type in the refactor until you’ve audited callers. Here we keep tuple for equivalence with the stateful variant; in real refactors, you’d likely keep the original type until you can safely change it.

#### RAG Example (embed_chunk): In-Place Update → New Object

Before: vec = [] + append.

After:

```python
import hashlib
from funcpipe_rag import ChunkWithoutEmbedding, Chunk


def embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)
```

---

## 4. Refactor to Pure: Small Transforms (Generic Examples)

### 4.1 Loop → Map

**How to spot this smell:** Manual iteration with mutable state (e.g., append to list) or index juggling (i=0; while i < len; i += step).

**Before/After Diff (Generic Example):**

Before (stateful loop):

```python
def double_evens(xs: list[int]) -> list[int]:
    res = []
    for x in xs:
        if x % 2 == 0:
            res.append(x * 2)
    return res
```

After (map + filter):

```python
def double_evens(xs: list[int]) -> list[int]:
    return list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, xs)))
```

**Process:** Extract predicates/transforms to small functions; chain filter/map; materialize as list for caller compatibility (we treat it immutably by convention here); you can later switch to a tuple when you know callers don’t rely on mutation. In idiomatic Python you’d usually prefer a comprehension here: list(x * 2 for x in xs if x % 2 == 0), but we’re using map/filter to make the refactor move explicit. Note: In real migrations, keep the outer container type identical (list→list) until you’ve proven no caller depends on mutability; then you can separately refactor list→tuple.

### 4.2 Accumulator → Comprehension

**How to spot this smell:** Empty list/dict/string + loop appending/updating/concatenating.

**Before/After Diff (Generic Example):**

Before (mutable accum):

```python
def sum_squares(xs: list[int]) -> int:
    total = 0
    for x in xs:
        total += x * x
    return total
```

After (comprehension + sum):

```python
def sum_squares(xs: list[int]) -> int:
    return sum(x * x for x in xs)
```

**Process:** Replace accum init + update with generator expression + built-in aggregator (sum, ''.join, dict, set).

### 4.3 In-Place Update → New Object

**How to spot this smell:** Modifying inputs/arguments (e.g., xs.sort(), d[k] = v) or mutable defaults.

**Before/After Diff (Generic Example):**

Before (in-place update):

```python
def increment_dict(d: dict[str, int]) -> dict[str, int]:
    for k in d:
        d[k] += 1
    return d
```

After (new object):

```python
def increment_dict(d: dict[str, int]) -> dict[str, int]:
    return {k: v + 1 for k, v in d.items()}
```

**Process:** Create new container from comprehension; avoid mutating inputs.

### 4.4 Non-RAG Example: API Handler Refactor

Before (stateful updates):

```python
def handle_request(req: dict) -> dict:
    if 'user' not in req:
        req['error'] = 'no user'  # Mutates input
        return req
    logs = []
    logs.append(f"User: {req['user']}")
    if 'action' in req:
        logs.append(f"Action: {req['action']}")
    req['logs'] = logs  # Mutates
    return req
```

After (new objects):

```python
def handle_request(req: dict) -> dict:
    if 'user' not in req:
        return {**req, 'error': 'no user'}
    logs = [f"User: {req['user']}"]
    if 'action' in req:
        logs += [f"Action: {req['action']}"]
    return {**req, 'logs': logs}
```

**Moves Applied:** Accumulator → comprehension (logs as list literal + concat); In-place update → new object ({**req, ...}). Local mutation of short-lived variables (like logs inside a function) is usually fine; what we’re avoiding is mutation of inputs or shared state.

### 4.5 Non-RAG Example: CLI Data Cleaner Refactor

Before (mutable accum):

```python
def clean_lines(lines: list[str]) -> list[str]:
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned.append(stripped.lower())
    return cleaned
```

After (comprehension):

```python
def clean_lines(lines: list[str]) -> list[str]:
    return [line.strip().lower() for line in lines if line.strip()]
```

**Moves Applied:** Loop → map (implicit in comprehension); Accumulator → comprehension. Note: Here we keep list→list for equivalence; change to tuple later if callers allow.

### 4.6 Impure Shell (Edge Only)

The shell from Core 1 remains; refactoring focuses on core. Use 'with' for resource safety in impure boundaries—full details in Module 7 (inspired by PEP 343).

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Replace expressions in `chunk_doc`.  
1. Inline generator → tuple of chunks.  
2. Substitute into full_rag → fixed value.  
**Bug Hunt:** In stateful_chunk_doc, substitution fails (multiple accum risks).

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

Use Hypothesis to prove refactor equivalence.

You can safely skip this on a first read and still follow later cores—come back when you want to mechanically verify your own refactors.

To bridge theory and practice, here's a short demo of falsifying an impure function using Hypothesis:

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

### 6.1 Mutation Detection Example

As mentioned in the contract table, use deepcopy to detect shared mutation:

```python
from hypothesis import given
import hypothesis.strategies as st
from copy import deepcopy

def bad_increment(xs: list[int]) -> list[int]:
    xs[0] += 1  # Mutates input
    return xs

@given(st.lists(st.integers(), min_size=1))
def test_no_mutation(xs: list[int]) -> None:
    original = deepcopy(xs)
    _ = bad_increment(xs)
    assert xs == original  # Fails on mutation
```

### 6.2 Custom Strategy (RAG Domain)

From `module-01/funcpipe-rag-01/tests/conftest.py` (as in Core 1).

### 6.3 Equivalence Property

`module-01/funcpipe-rag-01/tests/test_laws.py` already encodes the key refactoring guarantees. For example:

```python
from hypothesis import given
from funcpipe_rag import docs_to_embedded  # impure_chunks from full_rag.py
from funcpipe_rag import impure_chunks
from .conftest import doc_list_strategy, env_strategy


@given(docs=doc_list_strategy(), env=env_strategy())
def test_refactor_preserves_structure(docs, env):
    old = sorted(
        (c["doc_id"], c["text"], c["start"], c["end"])
        for c in impure_chunks(docs, env)
    )
    new = sorted(
        (c.doc_id, c.text, c.start, c.end)
        for c in docs_to_embedded(docs, env)
    )
    assert old == new
```

This property compares the legacy dictionary-based pipeline with the refactored pure pipeline and proves that every chunk (doc_id/text/start/end) matches exactly despite the internal rewrite. It’s the automated safety net for the refactors described in this core.

### 6.4 Shrinking Demo: Catching a Bug

Bad refactor (off-by-one in chunk_doc):

```python
from funcpipe_rag import CleanDoc, ChunkWithoutEmbedding, RagEnv


def bad_chunk_doc(doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    text = doc.abstract
    return tuple(
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]) - 1)
        # Off-by-one
        for i in range(0, len(text), env.chunk_size)
    )
```

Property:

```python
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import CleanDoc, RagEnv
from .conftest import env_strategy


@given(
    doc=st.builds(CleanDoc, doc_id=st.text(min_size=1), title=st.text(), abstract=st.text(min_size=1),
                  categories=st.text()),
    env=env_strategy(),
)
def test_bad_chunk_doc_equivalence(doc: CleanDoc, env: RagEnv) -> None:
    assert stateful_chunk_doc(doc, env) == bad_chunk_doc(doc, env)  # Fails on off-by-one
```

Hypothesis failure trace (run to verify; example):

```
Falsifying example: test_bad_chunk_doc_equivalence(
    doc=CleanDoc(doc_id='a', title='', abstract='a', categories=''), 
    env=RagEnv(chunk_size=128),
)
AssertionError
```

- Shrinks to minimal doc with abstract='a'; off-by-one drops char, failing equivalence. Catches bug via shrinking.

---

## 7. When Local Refactoring Isn't Worth It

Rarely, for profiled hot paths (e.g., tight loops), keep imperative but wrap in pure API.

---

## 8. Pre-Core Quiz

1. Mutable accumulator → violates? → **No shared mutation**  
2. Multiple temps → better as? → **Tuple/frozen record**  
3. Index juggling → better as? → **Comprehension**  
4. Deep recursion → mitigate? → **Iteration or explicit stack**  
5. Prove refactor safe? → **Hypothesis equivalence**

## 9. Post-Core Reflection & Exercise

**Reflect:** In your code, find one stateful function. Refactor to pure; add equivalence properties.  
**Project Exercise:** Refactor RAG stages; run properties on sample data.

All claims (e.g., referential transparency) are verifiable via the provided Hypothesis examples—run them to confirm.

**Further Reading:** For more on purity pitfalls, see 'Fluent Python' Chapter on Functions as Objects. Check free resources like Python.org's FP section or Codecademy's Advanced Python course for basics.

**Next:** Core 6 – Small Combinator Libraries. (Builds on this RAG pure core.)
