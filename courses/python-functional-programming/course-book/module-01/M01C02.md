# Module 1: Foundational FP Concepts

## Progression Note
By the end of Module 1, you'll master purity laws, write pure functions, and refactor impure code using Hypothesis. This builds the foundation for lazy streams in Module 3. See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus | Key Outcomes |
|--------|-------|--------------|
| 1: Foundational FP Concepts | Purity, contracts, refactoring | Spot impurities, write pure functions, prove equivalence with Hypothesis |
| 2: ... | ... | ... |
| ... | ... | ... |

## M01C02: Pure Functions & Contracts – Inputs, Outputs, No Shared Mutation

> **Core question:**  
> How do you constrain functions so that purity violations—hidden inputs, nondeterministic outputs, or shared mutation—are detectable early by signatures, properties, and optional runtime checks?

This core builds on **Core 1**'s functional mindset by adding **detectable contracts** for purity:  
- Make **all inputs explicit** (no globals, OS env, time, RNG).  
- Aim for **deterministic outputs** (same args → same result).  
- **Never mutate shared state** (return new values).  

We continue the **running project** from Core 1: refactoring the FuncPipe RAG Builder to pure, now with contracts on stages like `clean_doc`, `chunk_doc`, and `embed_chunk`.

**Audience:** Developers who refactored to pure in Core 1 but still see flaky tests from hidden globals, nondeterministic RNG/time, or accidental argument mutation.  
**Outcome:**  
1. Write a pure function whose purity is checkable by Hypothesis in < 10 lines.  
2. Explain why `random.random()` or `os.getenv` breaks purity—and how to fix it with explicit params.  
3. Add properties detecting determinism + no input mutation whenever those are part of the contract.  
4. Spot and fix three classic violations: hidden inputs, nondeterministic outputs, shared mutation.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Make every input explicit, every output deterministic, and never mutate shared state—or mark the function impure and isolate it.**

### 1.2 Pure Function Contract in One Precise Sentence

> A pure function contract requires: all inputs explicit parameters, outputs deterministic, no shared state mutated, no side effects (except raising exceptions based on inputs)—detectable with high confidence by property tests and, to a lesser extent, type hints and runtime checks.

### 1.3 Why This Matters Now

Detectable contracts catch purity violations early, ensuring functions from Core 1 compose safely in pipelines (Core 4) and satisfy equational laws (Core 9); without detection, hidden state leads to flaky tests and races.

### 1.4 Contracts: Three Layers

Contracts go beyond purity to include preconditions (e.g., "amount >= 0"), postconditions (e.g., "sum of balances unchanged"), and invariants (e.g., "abstract has no double spaces"). Enforce them across three layers:

| Layer              | Description                          | Examples                             | When to Use                          |
|--------------------|--------------------------------------|--------------------------------------|--------------------------------------|
| Static (typing)    | Shape and domain of data             | Type hints like `list[RawDoc]`       | For structure/shape; encourages explicitness |
| Dynamic (asserts)  | Runtime checks that raise errors     | `assert amount >= 0`                 | For simple, enforceable conditions   |
| Behavioral (Hypothesis) | Relational properties over inputs/outputs | `f(g(x)) == g(f(x))`                | For subtle behaviors like determinism, no mutation, invariants |

**Guidance:** If it's about data shape/structure → use types. If it's a simple check → use asserts. If it's relational (e.g., output properties, no side effects) → use property tests.

---

## 2. Mental Model: Contract Violations vs Detection

### 2.1 One Picture

```text
Leaky Contract (violations)               Detected Contract
+---------------------------+            +---------------------------+
| hidden globals / time     |            | explicit params only      |
| hidden RNG / OS env vars  |            |                           |
| mutates caller data       |            | returns new values        |
| prints / logs / I/O       |            |                           |
| same args → different out |            | same args → same out      |
+---------------------------+            +---------------------------+

Hypothesis falsifies leaks; types + runtime checks catch them early.
```

### 2.2 Contract Table

| Clause                     | Violation Example                      | Detected By                              |
|----------------------------|----------------------------------------|------------------------------------------|
| Explicit inputs            | Globals, `os.getenv`, `datetime.now()` | Code review + discipline; types encourage explicitness |
| Deterministic outputs      | `random`, time, external state         | Hypothesis determinism property          |
| No shared mutation         | `list.sort()`, `dict.update()`         | Hypothesis mutation check + deepcopy     |
| No side effects            | `print`, logging, I/O                  | Manual review                            |

**Note on Shared Mutation:** Includes nested structures (aliasing); use `deepcopy` in properties for detection. Unseeded RNG violates determinism; seeded RNG is acceptable if the seed is an explicit argument. Note that Hypothesis cannot automatically detect side effects like printing; capture streams manually if needed.

In the rest of this core we turn those columns into concrete contracts on the RAG stages and one non-RAG function.

---

## 3. Running Project: Contracts on RAG Stages

Our **running project** (from `module-01/funcpipe-rag-01/README.md`) adds contracts to Core 1's pure stages.  
- **Goal:** Ensure each stage is pure and detectable.  
- **Start:** Core 1's pure functions.  
- **End (this core):** Functions with Hypothesis properties for determinism, no mutation, and invariants. Semantics aligned with Core 1.

### 3.1 Types (Canonical)

These are defined in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_types.py` (as in Core 1) and imported as needed. No redefinition here.

### 3.2 Impure Variants (Anti-Patterns in RAG)

Full code:

```python
# Impure clean (hidden global)
from funcpipe_rag import RawDoc, CleanDoc

DEBUG = True


def impure_clean_doc(doc: RawDoc) -> CleanDoc:
    abstract = " ".join(doc.abstract.strip().lower().split())
    if DEBUG:
        abstract += " (debug)"
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)


# Impure chunk (nondeterministic)
import random
from typing import List
from funcpipe_rag import CleanDoc, ChunkWithoutEmbedding, RagEnv


def impure_chunk_doc(doc: CleanDoc, env: RagEnv) -> List[ChunkWithoutEmbedding]:
    text = doc.abstract
    offset = random.randint(0, min(10, max(0, len(text) - 1)))  # Hidden RNG; violates determinism
    return [
        ChunkWithoutEmbedding(doc.doc_id, text[i + offset:i + offset + env.chunk_size], i + offset,
                              i + offset + len(text[i + offset:i + offset + env.chunk_size]))
        for i in range(0, len(text), env.chunk_size)
    ]  # Arbitrary offset for demo; not production chunking logic


# Impure embed (mutates input)
import hashlib
from dataclasses import dataclass
from funcpipe_rag import Chunk


@dataclass  # Mutable for demo
class MutableChunkWithoutEmbedding:
    doc_id: str
    text: str
    start: int
    end: int


def impure_embed_chunk(chunk: MutableChunkWithoutEmbedding) -> Chunk:
    # Mutates text (shared mutation)
    chunk.text = chunk.text.upper()
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)
```

**Smells:** Hidden global (DEBUG), nondeterministic RNG (violates determinism as offset varies), shared mutation (chunk.text). Note: Used mutable class for mutation demo; canonical types remain frozen.

---

## 4. Correct Pattern: Detectable Contracts in RAG

### 4.1 Pure Core

The canonical implementations of `clean_doc`, `chunk_doc`, `embed_chunk`, and `structural_dedup_chunks` live in `module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py` (identical to Core 1). Each function accepts only explicit parameters, returns brand-new dataclasses, and never mutates inputs—exactly the contract we want to enforce in this core.

### 4.2 Non-RAG Example

Use your own domain code (e.g., accounting transfers) to practice adding explicit inputs, determinism, and invariants—the same discipline applied to the FuncPipe stages. Keep side effects isolated just as we do with `rag_shell`.

### 4.3 Impure Shell (Edge Only)

The shell from Core 1 remains; contracts focus on pure core.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Replace expressions in `clean_doc`.  
1. Inline `abstract = " ".join(...)` → normalized string.  
2. Substitute into `CleanDoc` → fixed value.  
**Bug Hunt:** In impure_clean_doc, the value of CleanDoc(..., abstract, ...) depends on the hidden global DEBUG, so you can’t safely replace the call with its value without also knowing that global state.

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

Use Hypothesis to prove contract compliance.

You can safely skip this on a first read and still follow later cores—come back when you want to mechanically verify your own refactors.

We saw the simplest determinism property in Core 1; now we’ll apply the same idea to the RAG stages.

To enhance the explanation, here's a short demo of falsifying an impure function using Hypothesis:

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

### 6.2 Contract Properties for RAG Stages

Full code:

```python
# module-01/funcpipe-rag-01/tests/test_laws.py (excerpt)
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import clean_doc, chunk_doc, embed_chunk
from funcpipe_rag import ChunkWithoutEmbedding
from .conftest import raw_doc_strategy, env_strategy


@given(doc=raw_doc_strategy())
def test_clean_doc_deterministic(doc):
    assert clean_doc(doc) == clean_doc(doc)


@given(doc=raw_doc_strategy())
def test_clean_doc_invariants(doc):
    cleaned = clean_doc(doc)
    # no double spaces
    assert "  " not in cleaned.abstract
    # normalized whitespace and case
    assert cleaned.abstract == " ".join(doc.abstract.strip().lower().split())


@given(doc=raw_doc_strategy(), env=env_strategy())
def test_chunk_doc_deterministic(doc, env):
    cleaned = clean_doc(doc)
    assert chunk_doc(cleaned, env) == chunk_doc(cleaned, env)


@given(doc=raw_doc_strategy(), env=env_strategy())
def test_chunk_doc_covers_cleaned(doc, env):
    cleaned = clean_doc(doc)
    assert "".join(c.text for c in chunk_doc(cleaned, env)) == cleaned.abstract


chunk_we_strategy = st.builds(
    ChunkWithoutEmbedding,
    doc_id=st.text(),
    text=st.text(min_size=1),
    start=st.integers(min_value=0, max_value=1000),
).map(
    lambda c: ChunkWithoutEmbedding(
        c.doc_id, c.text, c.start, c.start + len(c.text)
    )
)


@given(chunk_we=chunk_we_strategy)
def test_embed_deterministic(chunk_we):
    assert embed_chunk(chunk_we) == embed_chunk(chunk_we)


@given(chunk_we=chunk_we_strategy)
def test_embed_range_and_dimension(chunk_we):
    emb = embed_chunk(chunk_we).embedding
    assert len(emb) == 16
    assert all(0.0 <= x <= 1.0 for x in emb)


import copy


@given(chunk_we=chunk_we_strategy)
def test_embed_does_not_mutate_input(chunk_we):
    original = copy.deepcopy(chunk_we)
    _ = embed_chunk(chunk_we)
    assert chunk_we == original
```

These real-world properties encode determinism, invariants, no mutation, and pure behavior directly in the repository.

### 6.3 Shrinking Demo: Catching a Bug

Bad refactor (off-by-one in chunk_doc end, dropping last char):

Full code:

```python
from typing import List
from funcpipe_rag import CleanDoc, ChunkWithoutEmbedding, RagEnv


def bad_chunk_doc(doc: CleanDoc, env: RagEnv) -> List[ChunkWithoutEmbedding]:
    text = doc.abstract
    return [
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]) - 1)
        # Off-by-one
        for i in range(0, len(text), env.chunk_size)
    ]
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
def test_bad_chunk_doc_index_invariant(doc: CleanDoc, env: RagEnv) -> None:
    chunks = bad_chunk_doc(doc, env)
    for c in chunks:
        assert c.end - c.start == len(c.text)  # Fails on off-by-one


@given(
    doc=st.builds(CleanDoc, doc_id=st.text(min_size=1), title=st.text(), abstract=st.text(min_size=1),
                  categories=st.text()),
    env=env_strategy(),
)
def test_bad_chunk_doc_covers_abstract(doc: CleanDoc, env: RagEnv) -> None:
    chunks = bad_chunk_doc(doc, env)
    reconstructed = "".join(c.text for c in chunks)
    assert reconstructed == doc.abstract  # Fails on dropped chars
```

These two properties encode the “index” and “coverage” invariants we care about for chunks.

Hypothesis failure trace (run to verify; example for index_invariant):

```
Falsifying example: test_bad_chunk_doc_index_invariant(
    doc=CleanDoc(doc_id='a', title='', abstract='a', categories=''), 
    env=RagEnv(chunk_size=128),
)
AssertionError
```

- Shrinks to minimal doc with abstract='a'; off-by-one makes end - start != len(text). For coverage, shrinks to doc with abstract length not multiple of chunk_size, dropping tail. Catches subtle bug via shrinking.

---

## 7. When Contracts Aren't Worth It

For ultra-hot paths, skip runtime checks; rely on properties in tests.

---

## 8. Pre-Core Quiz

1. Hidden global in a function → violates which clause? → **Explicit inputs**  
2. `random.random()` inside a function → violates? → **Deterministic outputs**  
3. `data.sort()` on a param → violates? → **No shared mutation**  
4. `print()` inside a function → violates? → **No side effects**  
5. Tool that searches for counterexamples to determinism? → **Hypothesis**

## 9. Post-Core Reflection & Exercise

**Reflect:** In your code, find one function that violates a contract. Apply the recipe; add properties.  
**Project Exercise:** Implement contracts on RAG stages; run properties on sample data.  

All claims (e.g., referential transparency) are verifiable via the provided Hypothesis examples—run them to confirm.

**Further Reading:** For more on purity pitfalls, see 'Fluent Python' Chapter on Functions as Objects. Check free resources like Python.org's FP section or Codecademy's Advanced Python course for basics.

**Next:** Core 3 – Immutability & Value Semantics. (Builds on this RAG pure core.)