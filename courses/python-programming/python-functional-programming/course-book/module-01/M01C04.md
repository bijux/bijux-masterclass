# Module 1: Foundational FP Concepts

## Progression Note
By the end of Module 1, you'll master purity laws, write pure functions, and refactor impure code using Hypothesis. This builds the foundation for lazy streams in Module 3. See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus | Key Outcomes |
|--------|-------|--------------|
| 1: Foundational FP Concepts | Purity, contracts, refactoring | Spot impurities, write pure functions, prove equivalence with Hypothesis |
| 2: ... | ... | ... |
| ... | ... | ... |

## M01C04: Higher-Order Functions & Composition – map, filter, reduce, Pipelines

> **Core question:**  
> How do you build concise, reusable, composable transformations using functions as first-class citizens—so that complex logic emerges from simple, testable building blocks without imperative loops or hidden state?

This core builds on **Core 1**'s mindset, **Core 2**'s contracts, and **Core 3**'s immutability by adding **higher-order functions and composition**:  
- Treat functions as values (`lambda`, `def`, partial).  
- Transform data with `map`, `filter`, `reduce`.  
- Build pipelines via composition (our `flow` helper) and generator chains.  

We continue the **running project** from Core 1-3: refactoring the FuncPipe RAG Builder, now using HO functions for stages like cleaning and chunking.

**Audience:** Developers who passed Core 3's immutability checks but still write imperative loops, duplicate transformation code, or struggle with callback hell in data processing.  
**Outcome:**  
1. Refactor any imperative loop into a declarative pipeline in < 15 lines.  
2. Explain why declarative pipelines beat nested loops for reasoning (and are usually comparable or faster in performance when idiomatic).  
3. Add properties proving identity and equivalence for your compositions.  
4. Spot and fix three classic HO violations: side-effects in map/filter, manual indexing, non-associative reduce.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Default to declarative pipelines over imperative loops; compose small, pure, testable functions into readable chains.**

### 1.2 Higher-Order Composition in One Precise Sentence

> Higher-order functions take functions as arguments or return them; composition chains them into pipelines that apply sequentially while preserving purity and immutability.

### 1.3 Why This Matters Now

HO composition glues Core 3's immutable data with Core 2's pure functions into efficient pipelines, enabling local refactorings (Core 5) and combinators (Core 6); without it, code remains imperative spaghetti.

---

## 2. Mental Model: Imperative Loop vs Declarative Pipeline

### 2.1 One Picture

```text
Imperative Loop                            Declarative Pipeline
+--------------------------------+        +-------------------------------------+
| total = 0                      |        | from operator import add            |
| for x in xs:                   |        | total = reduce(add,                 |
|     if x > 0:                  |        |                filter(pos,          |
|         total += x * x         |        |                       map(sq, xs)), |
| print(total)                   |        |                0)                   |
+--------------------------------+        +-------------------------------------+
                                           Reads top-to-bottom, no hidden state
```

### 2.2 Contract Table

| Clause                     | Violation Example                      | Detected By                              |
|----------------------------|----------------------------------------|------------------------------------------|
| Identity laws              | flow(identity, f) ≠ f                  | Hypothesis identity property             |
| Equivalence                | Pipeline ≠ known-correct impl          | Hypothesis equivalence vs imperative     |
| Laziness / Memory          | Eager list(map()) on large data        | Manual memory profiling                  |

**Note on Pipelines:** Only as strong as parts; impure functions or mutable data break everything—guard with Core 2/3. In Python, declarative pipelines often mean comprehensions + small pure functions, with map/filter/reduce as optional tools.

### 2.3 How This Relates to Plain Python

Python has multiple ways to express transformations; choose based on readability and laziness:

| Transformation      | For-Loop (Imperative) | List Comprehension (Declarative) | map / filter (HO, lazy)     |
|---------------------|-----------------------|----------------------------------|-----------------------------|
| Apply f to xs       | res = []<br>for x in xs:<br>    res.append(f(x)) | [f(x) for x in xs]              | map(f, xs)                  |
| Filter positives    | res = []<br>for x in xs:<br>    if x > 0:<br>        res.append(x) | [x for x in xs if x > 0]        | filter(pos, xs)             |
| Pros/Cons           | Verbose, mutable accum | Readable, eager (full list)      | Lazy iterators, composable  |

**Guidance:** Use comprehensions for simple cases; map/filter for laziness; curried versions (e.g., via functools.partial) for pipelines. Inline short pipelines; name reusable ones.

---

## 3. Running Project: HO Composition in RAG Pipeline

Our **running project** (from `module-01/funcpipe-rag-01/README.md`) composes RAG stages with HO functions.  
- **Goal:** Replace imperative loops with declarative pipelines.  
- **Start:** Core 1-3's pure functions.  
- **End (this core):** HO-composed `full_rag` with properties for laws/equivalence. Semantics aligned with Core 1-3.

### 3.1 Types (Canonical)

These are defined in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_types.py` (as in Core 1) and imported as needed. No redefinition here.

### 3.2 Imperative Variants (Anti-Patterns in RAG)

Full code:

```python
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, RagEnv
from typing import List


# Imperative clean (manual loop)
def imperative_clean_doc(doc: RawDoc) -> CleanDoc:
    words = doc.abstract.strip().lower().split()
    abstract = ""
    for word in words:
        abstract += word + " "  # Mutable string accum
    return CleanDoc(doc.doc_id, doc.title, abstract.strip(), doc.categories)


# Imperative chunk (manual indexing)
def imperative_chunk_doc(doc: CleanDoc, env: RagEnv) -> List[ChunkWithoutEmbedding]:
    text = doc.abstract
    chunks = []
    i = 0
    while i < len(text):
        end = min(i + env.chunk_size, len(text))
        chunks.append(ChunkWithoutEmbedding(doc.doc_id, text[i:end], i, end))
        i = end  # Manual step; off-by-one risk
    return chunks


# Imperative embed (non-associative reduce example)
import hashlib
from typing import Tuple
from funcpipe_rag import Chunk


def imperative_embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = []
    for i in range(0, 64, step):
        val = int(h[i:i + step], 16) / (16 ** step - 1)
        vec.append(val)  # Mutable accum
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, tuple(vec))
```

**Smells:** Manual accum (mutable string/list), indexing (error-prone), non-HO (no composable parts).

---

## 4. Refactor to HO: Declarative Pipelines in RAG

### 4.1 HO Core

`module-01/funcpipe-rag-01/src/funcpipe_rag/full_rag.py` wires the pure stages together with the `fmap` and `flow` helpers from `fp.py`. Full code for fp.py:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/fp.py
from typing import Callable, TypeVar, List

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

def fmap(f: Callable[[T], U]) -> Callable[[List[T]], List[U]]:
    # fmap obeys the usual functor laws for list: identity and composition
    # This fmap is a simple list-based helper; it’s eager. In Module 3 we’ll generalize this pattern to lazy iterators.
    def mapper(xs: List[T]) -> List[U]:
        return [f(x) for x in xs]
    return mapper

def flow(*fs: Callable) -> Callable:
    def composed(x):
        for f in fs:
            x = f(x)
        return x
    return composed

def identity(x):
    return x
```

Full code for full_rag.py:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/full_rag.py
from typing import List
from funcpipe_rag import fmap, flow
from funcpipe_rag import clean_doc, chunk_doc, embed_chunk, structural_dedup_chunks
from funcpipe_rag import RawDoc, Chunk, RagEnv


def docs_to_embedded(docs: List[RawDoc], env: RagEnv) -> List[Chunk]:
    cleaned = fmap(clean_doc)(docs)
    chunked = [c for doc in cleaned for c in chunk_doc(doc, env)]
    return fmap(embed_chunk)(chunked)


def full_rag(docs: List[RawDoc], env: RagEnv) -> List[Chunk]:
    return structural_dedup_chunks(docs_to_embedded(docs, env))


def full_rag_point_free(docs: List[RawDoc], env: RagEnv) -> List[Chunk]:
    return flow(
        fmap(clean_doc),
        lambda cleaned: [c for doc in cleaned for c in chunk_doc(doc, env)],
        fmap(embed_chunk),
        structural_dedup_chunks,
    )(docs)
```

These helpers provide the declarative composition we care about: `fmap` applies a pure stage across a list, and `flow` threads data through the entire pipeline without imperative bookkeeping. Note: flow(f, g, h)(x) means h(g(f(x))) (left-to-right).

### 4.2 Non-RAG Example: Data Munging Pipeline

For a simple CSV processing pipeline. Full code:

```python
from typing import Dict, List, Tuple

# Imperative version (anti-pattern)
def imperative_process_data(rows: List[Dict[str, str]]) -> List[Dict[str, float]]:
    cleaned = []
    for row in rows:
        if row['age'] and int(row['age']) > 18:
            cleaned.append({'id': row['id'], 'score': float(row['score'])})

    normalized = []
    for item in cleaned:
        item['score'] = item['score'] / 100.0  # Mutates
        normalized.append(item)
    return normalized

# HO refactor
def is_adult(row: Dict[str, str]) -> bool:
    age = row.get('age')
    return age is not None and int(age) > 18

def parse_score(row: Dict[str, str]) -> Dict[str, float]:
    return {'id': row['id'], 'score': float(row['score'])}

def normalize_score(item: Dict[str, float]) -> Dict[str, float]:
    return {**item, 'score': item['score'] / 100.0}  # New dict

def process_data(rows: List[Dict[str, str]]) -> Tuple[Dict[str, float], ...]:
    return tuple(
        map(normalize_score,
            map(parse_score,
                filter(is_adult, rows)
            )
        )
    )
```

Here we intentionally use built-in map/filter to highlight laziness; our fmap helper above is eager and for lists only.

**Wins:** Internal stages are lazy iterators, no mutation, reusable parts. Moving filter before expensive map avoids wasted work on invalid rows.

### 4.3 Non-RAG Example: Business Logic Pipeline

For a request handler. Full code:

```python
from typing import Dict, Callable
from funcpipe_rag import flow


# Imperative version (anti-pattern)
def imperative_handle_request(req: Dict) -> Dict:
    if not authenticate(req):
        return {'error': 'unauth'}
    if not authorize(req):
        return {'error': 'unauthorized'}
    result = run_action(req)
    return {'result': result}


# HO refactor (composition)
# reusing flow from fp.py

def check_auth(req: Dict) -> Dict:
    if not authenticate(req):
        raise ValueError('unauth')
    return req


def check_authz(req: Dict) -> Dict:
    if not authorize(req):
        raise ValueError('unauthorized')
    return req


handle_request = flow(
    check_auth,
    check_authz,
    lambda req: {'result': run_action(req)},
)
```

**Wins:** Composable guards, easy to reorder/add steps without nesting. Real-world handlers often compose error-aware wrappers (like Result/Either types); here we raise exceptions to keep the example small. We’ll later replace these ValueError raises with explicit Result values.

### 4.4 Impure Shell (Edge Only)

The shell from Core 1 remains; HO focuses on core.

### 4.5 Tradeoffs in Composition

Overly long pipelines hurt readability—split if >3-4 stages. If a pipeline is only used once and short, inline it. Imperative may win in ultra-hot paths, but wrap in HO API.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Replace expressions in `full_rag`.  
1. Inline `docs_to_embedded(docs, env)` → list of chunks.  
2. Substitute into `structural_dedup_chunks` → fixed value.  
3. Result: Entire call = fixed value.  
**Bug Hunt:** In imperative_chunk_doc, substitution fails (manual indexing risks).

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

Use Hypothesis to prove laws.

You can safely skip this on a first read and still follow later cores—come back when you want to mechanically verify your own refactors.

### 6.1 Custom Strategy (RAG Domain)

From `module-01/funcpipe-rag-01/tests/conftest.py` (as in Core 1).

### 6.2 Composition & Equivalence Properties for the RAG Pipeline

Full code:

```python
# module-01/funcpipe-rag-01/tests/test_laws.py (excerpt)
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import fmap, flow, identity
from funcpipe_rag import full_rag, full_rag_point_free
from funcpipe_rag import RagEnv, RawDoc
from .conftest import doc_list_strategy, env_strategy


@given(xs=st.lists(st.integers()))
def test_fmap_identity(xs):
    assert fmap(lambda x: x)(xs) == xs


@given(xs=st.lists(st.integers()))
def test_fmap_composition(xs):
    inc = lambda x: x + 1
    double = lambda x: x * 2
    assert fmap(lambda x: double(inc(x)))(xs) == fmap(double)(fmap(inc)(xs))


@given(docs=doc_list_strategy(), env=env_strategy())
def test_full_rag_equivalent_forms(docs, env):
    assert full_rag(docs, env) == full_rag_point_free(docs, env)
```

These real tests enforce both the functor laws for `fmap` and the equivalence between our straight-line and point-free pipeline definitions.

### 6.3 Shrinking Demo: Catching a Bug

Bad refactor (non-associative reduce in full_rag):

Full code:

```python
from functools import reduce
from typing import List, Tuple
from funcpipe_rag import clean_doc, chunk_doc, embed_chunk
from funcpipe_rag import RawDoc, Chunk, RagEnv


def bad_full_rag(docs: List[RawDoc], env: RagEnv) -> Tuple[Chunk, ...]:
    # Buggy use of reduce: new tuple concatenated on the left reverses the doc order
    return reduce(
        lambda acc, d: tuple(embed_chunk(c) for c in chunk_doc(clean_doc(d), env)) + acc,
        docs,
        tuple()
    )  # Wrong concat (reverses order)
```

Property:

```python
from hypothesis import given
from funcpipe_rag import RawDoc, RagEnv
from .conftest import doc_list_strategy, env_strategy


@given(docs=doc_list_strategy(), env=env_strategy())
def test_bad_full_rag_equivalence(docs: List[RawDoc], env: RagEnv) -> None:
    imperative = tuple(
        embed_chunk(c)
        for d in docs
        for c in chunk_doc(clean_doc(d), env)
    )
    assert bad_full_rag(docs, env) == imperative  # Fails on order
```

Hypothesis failure trace (run to verify; example):

```
Falsifying example: test_bad_full_rag_equivalence(
    docs=[RawDoc(doc_id='a', title='', abstract='a', categories=''), RawDoc(doc_id='b', title='', abstract='b', categories='')], 
    env=RagEnv(chunk_size=128),
)
AssertionError
```

- Shrinks to two docs; reversed order fails equality. Catches bug via shrinking.

---

## 7. When HO Isn't Worth It

Rarely, for profiled hot paths (e.g., tight loops), use imperative but wrap in HO API.

---

## 8. Pre-Core Quiz

1. Side-effect in map → violates? → **Purity**  
2. Non-associative op in reduce → violates? → **Predictability**  
3. Nested for-loops → better as? → **Pipeline**  
4. List comp vs generator exp → memory trade-off? → **List comp O(n) extra**  
5. Tool to prove equivalence? → **Hypothesis**

## 9. Post-Core Reflection & Exercise

**Reflect:** In your code, find one imperative loop. Compose it; add HO properties.  
**Project Exercise:** Compose RAG stages; run properties on sample data.

All claims (e.g., referential transparency) are verifiable via the provided Hypothesis examples—run them to confirm.

**Further Reading:** For more on purity pitfalls, see 'Fluent Python' Chapter on Functions as Objects. Check free resources like Python.org's FP section or Codecademy's Advanced Python course for basics.

**Next:** Core 5 – Local FP Refactorings. (Builds on this RAG pure core.)
