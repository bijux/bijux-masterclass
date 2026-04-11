# Typed Pipelines


<!-- page-maps:start -->
## Lesson Map

```mermaid
flowchart LR
  mismatch["Start with a pipeline mismatch"] --> surface["Make stage input/output types explicit"]
  surface --> typecheck["Use typing to reject invalid composition"]
  typecheck --> preserve["Preserve decorator and context signatures honestly"]
```
<!-- page-maps:end -->

This lesson is about making pipeline mistakes visible before runtime.

## Start With the Runtime Failure

Without types, pipeline bugs often look like this:

- one stage returns a different shape than the next stage expects
- a decorator quietly erases the real call signature
- a context parameter gets threaded through `*args` and disappears from review

Typing helps when it tells the truth about those boundaries. It hurts when it becomes a
layer of `Any` that only hides the mismatch better.

## Keep This Question In View

> How do you use Python’s static typing to describe pure functions and higher-order pipelines so that composition errors are caught by the type checker instead of at 02:00 in production?

By the end of this lesson, you should be able to explain:

- where the type boundary between two stages actually is
- when a generic helper needs `TypeVar`
- when a decorator or context binder needs `ParamSpec` or `Concatenate`

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Default to precise type hints on pure functions and higher-order utilities; if the type checker struggles, simplify the API instead of weakening everything to `Any`.**

### 1.2 Typed FP Pipelines in One Precise Sentence

> A typed functional pipeline is a chain of pure functions whose input/output types line up via TypeVars, with decorators and context binders expressed using ParamSpec and Concatenate so that invalid pipelines fail to type-check.

### 1.3 Why This Matters Now

Typed pipelines are useful because they turn "I think these stages line up" into something
the tooling can check repeatedly. The type system is not the goal. Honest pipeline
boundaries are the goal.

### 1.4 Typed Spectrum Table (Recap with Focus on Typing)

| Level              | Description                          | Example                              |
|--------------------|--------------------------------------|--------------------------------------|
| Untyped            | Any everywhere                       | `def fmap(fn, xs): return [fn(x) for x in xs]` |
| Partially Typed    | Hard-coded types                     | `def fmap(fn: Callable[[int], str], xs: list[int]) -> list[str]: ...` |
| Fully Typed        | Generics with TypeVar                | `def fmap(fn: Callable[[T], U], xs: Iterable[T]) -> list[U]: ...` |

**Note on Typing:** Good annotations make data flow easier to review. If the annotations
make the code harder to understand than the pipeline itself, the API usually needs
simplification.

---

## 2. Mental Model: Untyped Jungle vs Typed Contracts

### 2.1 One Picture

```text
Untyped pipeline                           Typed pipeline
+---------------------------+             +-----------------------------+
| stage output shape unclear |            | each stage states input/out  |
| decorators return Any      |            | bad composition is rejected  |
| context hidden in *args    |            | context binding is explicit  |
| crash discovered late      |            | mismatch discovered early    |
+---------------------------+             +-----------------------------+
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

## What comes next

This lesson should leave you able to design a typed pipeline surface that is still
readable. The next step is to decide whether the typed form actually buys safety and how
to compare it with the simpler baseline it replaced.

Continue with [Typed Pipeline Review](typed-pipeline-review.md) before you move into
[Isolating Side Effects](isolating-side-effects.md).
