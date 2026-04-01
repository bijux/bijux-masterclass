# Module 1: Foundational FP Concepts

## Progression Note
By the end of Module 1, you'll master purity laws, write pure functions, and refactor impure code using Hypothesis. This builds the foundation for lazy streams in Module 3. See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus | Key Outcomes |
|--------|-------|--------------|
| 1: Foundational FP Concepts | Purity, contracts, refactoring | Spot impurities, write pure functions, prove equivalence with Hypothesis |
| 2: ... | ... | ... |
| ... | ... | ... |

## M01C07: Type-Hinted Pure Functions & Higher-Order Pipelines – TypeVar, ParamSpec, Concatenate

> **Core question:**  
> How do you use Python’s static typing (TypeVar, ParamSpec, Concatenate) to precisely describe pure functions and higher-order pipelines—so that composition errors are caught by the type checker instead of at 02:00 in production?

This core builds on **Core 1**'s mindset, **Core 2**'s contracts, **Core 3**'s immutability, **Core 4**'s composition, **Core 5**'s refactorings, and **Core 6**'s combinators by making them **machine-checkable**:  
- **TypeVar** for generic pure functions over arbitrary types.  
- **ParamSpec** to preserve full call signatures across decorators and wrappers.  
- **Concatenate** to inject context/dependencies without lying to the type checker.  
- Typed `compose2` and `Pipeline` that reject incompatible stages, with notes on typing `flow`/`pipe`.  

We continue the **running project** from Core 1-6: refactoring the FuncPipe RAG Builder, now with typed pipelines.

**Audience:** Developers comfortable with Core 6 combinators who now want **static guarantees** about their pure functions and higher-order utilities.  
**Outcome:**  
1. Declare generic pure functions with `TypeVar` (`fmap`, `ffilter`, `foldl`).  
2. Implement type-safe `compose`/`Pipeline` utilities that reject incompatible stages.  
3. Write decorators with `ParamSpec` that preserve original signatures.  
4. Use `Concatenate` to bind context (config/logger/db) in a type-safe way.  
5. Add Hypothesis properties proving typed pipelines preserve behavior while the type checker guards composition.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Default to precise type hints on pure functions and higher-order utilities; if the type checker struggles, simplify the API instead of weakening everything to `Any`.**

### 1.2 Typed FP Pipelines in One Precise Sentence

> A typed functional pipeline is a chain of pure functions whose input/output types line up via TypeVars, with decorators and context binders expressed using ParamSpec and Concatenate so that invalid pipelines fail to type-check.

### 1.3 Why This Matters Now

Typed FP enforces Core 6's combinators at compile time, enabling effect extraction (Core 8) and laws (Core 9); without it, mismatches hide until runtime.

### 1.4 Typed Spectrum Table (Recap with Focus on Typing)

| Level              | Description                          | Example                              |
|--------------------|--------------------------------------|--------------------------------------|
| Untyped            | Any everywhere                       | `def fmap(fn, xs): return [fn(x) for x in xs]` |
| Partially Typed    | Hard-coded types                     | `def fmap(fn: Callable[[int], str], xs: list[int]) -> list[str]: ...` |
| Fully Typed        | Generics with TypeVar                | `def fmap(fn: Callable[[T], U], xs: Iterable[T]) -> list[U]: ...` |

**Note on Typing:** This builds on the purity spectrum from earlier cores, focusing on how types make purity enforceable.

---

## 2. Mental Model: Untyped Jungle vs Typed Contracts

### 2.1 One Picture

```text
Untyped Jungle                             Typed Contracts
+---------------------------+            +---------------------------+
| pipe: Any -> ... -> Any   |            | compose2(f: B->C, g: A->B) |
| decorators: ... -> Any    |            |         -> (A->C)          |
| context: *args/**kwargs   |            | with_context:              |
| Everything compiles...    |            |   Ctx, Callable[Concat...  |
| ...until runtime crash    |            |         -> Callable[P, R]  |
+---------------------------+            +---------------------------+
```

### 2.2 Contract Table

| Clause                     | Violation Example                      | Detected By                              |
|----------------------------|----------------------------------------|------------------------------------------|
| Pipeline compatibility     | Wrong intermediate type                | mypy/pyright type error                  |
| Signature preservation     | Decorator returns Callable[..., Any]   | Type checker shows lost params           |
| Context injection          | Hidden ctx via *args/**kwargs          | No type hint for ctx                     |
| Generic reuse              | Hard-coded types instead of TypeVar    | Duplicate code, manual fixes             |
| Refactor safety            | Silent breakage on signature change    | Type errors guide edits                  |

**Note on Contracts:** ParamSpec/Concatenate make these enforceable; types catch what runtime never could.

### 2.3 Bug Prevention Example

Untyped (bug slips through):

```python
def bad_full_rag(docs: list[RawDoc], env: RagEnv) -> tuple[Chunk, ...]:
    return tuple(
        embed_chunk(doc)  # Wrong: doc instead of chunk
        for doc in docs
        for chunk in chunk_doc(clean_doc(doc), env)
    )  # Runtime AttributeError on doc.text
```

Typed (mypy catches):

```python
def bad_full_rag(docs: list[RawDoc], env: RagEnv) -> tuple[Chunk, ...]:
    return tuple(
        embed_chunk(doc)  # mypy error: embed_chunk expects ChunkWithoutEmbedding, got CleanDoc
        for doc in docs
        for chunk in chunk_doc(clean_doc(doc), env)
    )
```

**Wins:** Type checker complains immediately; no runtime surprise. Running mypy here will point exactly at embed_chunk(doc) as type-incompatible.

---

## 3. Running Project: Typed Pipelines in RAG

Our **running project** (from `module-01/funcpipe-rag-01/README.md`) adds types to Core 6's combinators.  
- **Goal:** Make pipelines statically verifiable.  
- **Start:** Core 1-6's pure functions.  
- **End (this core):** Typed `full_rag` with properties. Semantics aligned with Core 1-6.

### 3.1 Types (Canonical)

These are defined in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_types.py` (as in Core 1) and imported as needed. No redefinition here.

### 3.2 Untyped Variants (Anti-Patterns in RAG)

Full code:

```python
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, Chunk, RagEnv
from typing import Any
import hashlib


# Untyped clean (Any hell)
def untyped_clean_doc(doc) -> Any:
    abstract = " ".join(doc.abstract.strip().lower().split())
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)


# Untyped chunk (no safety)
def untyped_chunk_doc(doc, env) -> Any:
    text = doc.abstract
    chunks = (
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]))
        for i in range(0, len(text), env.chunk_size)
    )
    return tuple(chunks)


# Untyped embed (Any input/output)
def untyped_embed_chunk(chunk) -> Any:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)
```

**Smells:** Untyped (Any), no checker safety, hard to refactor (mismatches hide).

---

## 4. Refactor to Typed: Machine-Checkable Pipelines in RAG

### 4.1 Practical Typing: TypeVar for Generics (Layer 1)

Use TypeVar for reusable combinators. This is an evolution of the fp.py from Core 6, adding generics.

Full code:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/fp.py (excerpt)
from typing import TypeVar, Callable, Iterable, Generic
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, Chunk, RagEnv
import hashlib

T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def fmap(fn: Callable[[T], U]) -> Callable[[Iterable[T]], list[U]]:
    def inner(xs: Iterable[T]) -> list[U]:
        return [fn(x) for x in xs]

    return inner


def ffilter(pred: Callable[[T], bool]) -> Callable[[Iterable[T]], list[T]]:
    def inner(xs: Iterable[T]) -> list[T]:
        return [x for x in xs if pred(x)]

    return inner


def foldl(step: Callable[[R, T], R], init: R) -> Callable[[Iterable[T]], R]:
    def inner(xs: Iterable[T]) -> R:
        acc = init
        for x in xs:
            acc = step(acc, x)
        return acc

    return inner


def compose2(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    def inner(x: A) -> C:
        return f(g(x))

    return inner


# Simple example (not RAG) to show it off:
to_str: Callable[[int], str] = lambda n: str(n)
length: Callable[[str], int] = len

len_of_int = compose2(length, to_str)  # int -> int


# Typed clean
def clean_doc(doc: RawDoc) -> CleanDoc:
    abstract = " ".join(doc.abstract.strip().lower().split())
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)


# Typed chunk
def chunk_doc(doc: CleanDoc, env: RagEnv) -> list[ChunkWithoutEmbedding]:
    text = doc.abstract
    return [
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]))
        for i in range(0, len(text), env.chunk_size)
    ]


# Typed embed
def embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)


# Typed full_rag
def full_rag(docs: list[RawDoc], env: RagEnv) -> tuple[Chunk, ...]:
    cleaned: list[CleanDoc] = fmap(clean_doc)(docs)
    chunks: list[ChunkWithoutEmbedding] = [
        c
        for d in cleaned
        for c in chunk_doc(d, env)
    ]
    embedded: list[Chunk] = fmap(embed_chunk)(chunks)
    return tuple(embedded)
```

**Wins:** Generics with TypeVar (reusable fmap/filter/fold), compose2 rejects mismatches.

### 4.2 Advanced Typing: ParamSpec for Decorators (Layer 2)

Use ParamSpec for signature-preserving decorators.

Full code:

```python
from typing import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

# ---------- Decorator with ParamSpec ----------
def log_calls(fn: Callable[P, R]) -> Callable[P, R]:
    """Decorator that logs calls while preserving signature."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"{fn.__name__} called with {args} {kwargs}")
        return fn(*args, **kwargs)
    return wrapper

@log_calls  # Preserves signature via ParamSpec
def logged_full_rag(docs: list[RawDoc], env: RagEnv) -> tuple[Chunk, ...]:
    cleaned = fmap(clean_doc)(docs)
    chunks = [c for d in cleaned for c in chunk_doc(d, env)]
    return tuple(fmap(embed_chunk)(chunks))
```

### 4.3 Advanced Typing: Concatenate for Context (Layer 2)

Use Concatenate for type-safe dependency injection.

Full code:

```python
from typing import Concatenate

Ctx = TypeVar("Ctx")

def with_context(
    ctx: Ctx,
    fn: Callable[Concatenate[Ctx, P], R],
) -> Callable[P, R]:
    """Bind context type-safely."""
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        return fn(ctx, *args, **kwargs)
    return wrapped

# Example: Context injection (e.g., for a logger)
from logging import Logger, getLogger

logger: Logger = getLogger("funcpipe.rag")

def log_clean_doc(logger: Logger, doc: RawDoc) -> CleanDoc:
    logger.info("Cleaning doc %s", doc.doc_id)
    return clean_doc(doc)

typed_log_clean_doc = with_context(logger, log_clean_doc)  # (RawDoc) -> CleanDoc
```

**Note:** This example is intentionally impure at the boundary (logging side effect) but shows how to keep the core pure while binding dependencies in a type-safe way.

### 4.4 Advanced Typing: Pipeline Class (Layer 2)

Use a Pipeline class for multi-stage typing.

Full code:

```python
class Pipeline(Generic[A, B]):
    """Type-safe pipeline builder."""
    def __init__(self, fn: Callable[[A], B]):
        self._fn = fn

    def __call__(self, x: A) -> B:
        return self._fn(x)

    def then(self, f: Callable[[B], C]) -> "Pipeline[A, C]":
        return Pipeline(compose2(f, self._fn))
```

### 4.5 Typed Pipe/Flow (Layer 2)

To provide typed versions of pipe and flow (as promised), we can use generics for fixed-length chains or note limitations for variadic. For simplicity, here's a typed flow for two stages; extend as needed.

Full code:

```python
def typed_flow2(f: Callable[[A], B], g: Callable[[B], C]) -> Callable[[A], C]:
    return compose2(g, f)

def pipe2(x: A, f: Callable[[A], B], g: Callable[[B], C]) -> C:
    return g(f(x))

# Example usage
typed_clean_chunk = typed_flow2(clean_doc, lambda d: chunk_doc(d, RagEnv(chunk_size=512)))
```

**Note:** For longer chains, use Pipeline or accept partial typing for variadic flow/pipe due to Python limitations; we'll strengthen in later modules.

### 4.6 Impure Shell (Edge Only)

The shell from Core 1 remains; typing focuses on core. Use 'with' for resource safety in impure boundaries—full details in Module 7.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Replace expressions in `full_rag`.  
1. Inline `clean_doc(doc)` → CleanDoc.  
2. Substitute into chunk_doc → list of chunks.  
3. Result: Entire call = fixed value.  
**Bug Hunt:** In untyped_clean_doc, substitution fails (no type safety).

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

Use Hypothesis to prove behavior.

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

Properties for stages:

Full code:

```python
# module-01/funcpipe-rag-01/tests/test_laws.py (excerpt)
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import clean_doc, chunk_doc, embed_chunk, full_rag
from funcpipe_rag import untyped_clean_doc, untyped_chunk_doc, untyped_embed_chunk
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, Chunk, RagEnv
from .conftest import raw_doc_strategy, env_strategy, doc_list_strategy


# Properties for clean_doc
@given(raw_doc_strategy())
def test_clean_doc_deterministic(doc: RawDoc) -> None:
    assert clean_doc(doc) == clean_doc(doc)


# Properties for chunk_doc
@given(st.builds(CleanDoc, doc_id=st.text(min_size=1), title=st.text(), abstract=st.text(), categories=st.text()),
       env_strategy())
def test_chunk_doc_deterministic(doc: CleanDoc, env: RagEnv) -> None:
    assert chunk_doc(doc, env) == chunk_doc(doc, env)


@given(st.builds(CleanDoc, doc_id=st.text(min_size=1), title=st.text(), abstract=st.text(), categories=st.text()),
       env_strategy())
def test_chunk_doc_covers_abstract(doc: CleanDoc, env: RagEnv) -> None:
    chunks = chunk_doc(doc, env)
    reconstructed = "".join(c.text for c in chunks)
    assert reconstructed == doc.abstract  # Invariant: covers entire text; assumes positive chunk sizes from env_strategy


# Properties for embed_chunk
@given(st.builds(ChunkWithoutEmbedding, doc_id=st.text(min_size=1), text=st.text(min_size=1),
                 start=st.integers(min_value=0), end=st.integers(min_value=1)))
def test_embed_chunk_deterministic(chunk: ChunkWithoutEmbedding) -> None:
    assert embed_chunk(chunk) == embed_chunk(chunk)


# Composite property (full_rag)
@given(doc_list_strategy(), env_strategy())
def test_full_rag_deterministic(docs: list[RawDoc], env: RagEnv) -> None:
    assert full_rag(docs, env) == full_rag(docs, env)


@given(doc_list_strategy(), env_strategy())
def test_full_rag_equivalence(docs: list[RawDoc], env: RagEnv) -> None:
    untyped = tuple(
        untyped_embed_chunk(c)
        for d in docs
        for c in untyped_chunk_doc(untyped_clean_doc(d), env)
    )
    assert full_rag(docs, env) == untyped  # Equivalence
```

**Note:** Properties enforce determinism, equivalence, invariants.

### 6.3 Shrinking Demo: Catching a Bug

Bad refactor (wrong intermediate in pipeline):

```python
from typing import List, Tuple
from funcpipe_rag import clean_doc, chunk_doc, embed_chunk
from funcpipe_rag import RawDoc, Chunk, RagEnv


def bad_full_rag(docs: List[RawDoc], env: RagEnv) -> Tuple[Chunk, ...]:
    return tuple(
        embed_chunk(doc)  # Wrong: doc instead of chunk
        for doc in docs
        for chunk in chunk_doc(clean_doc(doc), env)
    )
```

Property:

```python
from hypothesis import given
from funcpipe_rag import RawDoc, RagEnv
from .conftest import doc_list_strategy, env_strategy


@given(doc_list_strategy(), env_strategy())
def test_bad_full_rag_equivalence(docs: List[RawDoc], env: RagEnv) -> None:
    imperative = tuple(
        embed_chunk(c)
        for d in docs
        for c in chunk_doc(clean_doc(d), env)
    )
    assert bad_full_rag(docs, env) == imperative  # Falsifies on mismatch
```

Hypothesis failure trace (run to verify; example):

```
Falsifying example: test_bad_full_rag_equivalence(
    docs=[RawDoc(doc_id='a', title='', abstract='a', categories='')], 
    env=RagEnv(chunk_size=128),
)
AssertionError
```

- Shrinks to minimal doc; wrong intermediate fails equivalence. Catches bug via shrinking.

---

## 7. When Typed FP Isn't Worth It

Rarely, for dynamic boundaries (e.g., JSON parsing), use Any; rely on properties in tests.

---

## 8. Pre-Core Quiz

1. `Callable[..., Any]` vs `Callable[P, R]` – which preserves signature? → **ParamSpec version**  
2. When to use `Concatenate` instead of normal arg? → **Context injection**  
3. What does `TypeVar("T")` buy over `Any`? → **Generic reuse + safety**  
4. Why ParamSpec for decorators? → **Preserve exact args/kwargs**  
5. Tool to prove typed pipeline ≡ untyped? → **Hypothesis equivalence**

## 9. Post-Core Reflection & Exercise

**Reflect:** In your code, find one higher-order utility. Add types; run mypy.  
**Project Exercise:** Type RAG pipelines; run properties on sample data.

All claims (e.g., referential transparency) are verifiable via the provided Hypothesis examples—run them to confirm.

**Further Reading:** For more on purity pitfalls, see 'Fluent Python' Chapter on Functions as Objects. Check free resources like Python.org's FP section or Codecademy's Advanced Python course for readers wanting basics.

**Next:** Core 8 – Extracting Side Effects. (Builds on this RAG pure core.)
