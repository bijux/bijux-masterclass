# Higher-Order Composition

A higher-order function accepts a function, returns a function, or both. The point is
not abstraction for its own sake. It is to reuse a sequencing rule while leaving the
domain transformation visible.

Module 01 keeps this toolkit intentionally small:

```text
identity  one value -> same value
fmap      (A -> B) -> (Iterable[A] -> list[B])
flow      unary stages -> one left-to-right unary stage
RagPipe   typed wrapper for unary stage composition
```

Closures, partial application, iterator combinators, and context plumbing arrive in
later modules. Do not smuggle them into the first reference state to force a
point-free pipeline.

## Functions are values

Ordinary Python lets a function be bound and passed:

```python
from collections.abc import Callable


def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def apply_text_rule(text: str, rule: Callable[[str], str]) -> str:
    return rule(text)


assert apply_text_rule("  Pure   Python ", normalize) == "pure python"
```

`apply_text_rule` is higher-order because `rule` is a value. Its usefulness depends on
the contract of the supplied callable. Passing an impure function does not become
safe merely because the wrapper is higher-order.

## `fmap`: lift an element transform

Module 01's `fp.py` defines:

```python
A = TypeVar("A")
B = TypeVar("B")


def fmap(func: Callable[[A], B]) -> Callable[[Iterable[A]], list[B]]:
    def mapped(items: Iterable[A]) -> list[B]:
        return [func(item) for item in items]

    return mapped
```

Read the signature in two stages:

```text
give fmap:     A -> B
receive:       Iterable[A] -> list[B]
```

For the RAG domain:

```python
clean_docs = fmap(clean_doc)
cleaned: list[CleanDoc] = clean_docs(raw_docs)
```

`clean_doc` still owns normalization. `fmap` owns the repeated application and
materializes the results as a list.

The materialization is part of the contract. Module 01 is eager. Later modules change
the traversal strategy and must explain that delta.

## Why laws matter

Two laws prevent `fmap` from adding surprising behavior.

Identity:

```python
fmap(identity)(values) == values
```

Composition:

```python
fmap(lambda value: g(f(value)))(values) == fmap(g)(fmap(f)(values))
```

The Module 01 property tests check both. These laws support a refactor between one
combined pass and two mapped transformations when the functions are pure and the
extra eager intermediate list is acceptable.

They do not grant permission to reorder arbitrary functions:

```python
fmap(g)(fmap(f)(values)) != fmap(f)(fmap(g)(values))
```

in general.

## `flow`: compose unary stages

`flow` returns one function that calls unary stages left to right:

```python
def flow(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def composed(value: Any) -> Any:
        result = value
        for function in functions:
            result = function(result)
        return result

    return composed
```

Use it when each output is the next input:

```python
normalize_length = flow(normalize, len)

assert normalize_length("  Pure   Python ") == 11
```

The implementation uses `Any`, so it cannot statically prove that adjacent stages
fit. The composition is readable but weakly typed. `RagPipe` offers a typed
alternative later in this lesson sequence.

## Why Module 01 does not force `full_rag` through `flow`

The real RAG stages do not form a simple unary chain:

- `chunk_doc` needs both a `CleanDoc` and `RagEnv`;
- one document becomes many chunks;
- embedding maps over those chunks;
- deduplication needs the whole collection.

The tracked `full_rag.py` therefore keeps orchestration explicit:

```python
def docs_to_embedded(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    cleaned = [clean_doc(doc) for doc in docs]
    chunked = [chunk for doc in cleaned for chunk in chunk_doc(doc, env)]
    embedded = [embed_chunk(chunk) for chunk in chunked]
    return embedded


def full_rag(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    return structural_dedup_chunks(docs_to_embedded(docs, env))
```

There is no `full_rag_point_free` in the Module 01 reference state. Its absence is a
teaching decision. Hiding `env` or inventing a flat-map abstraction before the course
introduces those tools would make the application harder to trace.

This is an important composition judgment:

> Prefer explicit orchestration when the available abstraction does not fit the
> domain shape honestly.

## `RagPipe`: typed unary composition

`rag_pipe.py` defines a small generic wrapper:

```python
class RagPipe(Generic[A, B]):
    def __init__(self, stage: Callable[[A], B]):
        self._stage = stage

    def __call__(self, value: A) -> B:
        return self._stage(value)

    def then(self, next_stage: Callable[[B], C]) -> "RagPipe[A, C]":
        return RagPipe(lambda value: next_stage(self._stage(value)))
```

This is not a second RAG framework. It demonstrates that method chaining can still
represent ordinary function composition:

```python
clean_then_count = RagPipe(clean_doc).then(lambda doc: len(doc.abstract))
count: int = clean_then_count(raw_doc)
```

`RagPipe.then` can express a chain whose stages are genuinely unary. It does not solve
one-to-many expansion or configuration binding by itself.

## Failure routes

### Adjacent stages do not fit

```python
bad = flow(clean_doc, embed_chunk)
bad(raw_doc)
```

`clean_doc` returns `CleanDoc`; `embed_chunk` requires
`ChunkWithoutEmbedding`. The untyped `flow` construction succeeds and execution
fails. A type-aware wrapper or an intermediate `chunk_doc` stage is required.

### An effect hides inside a callback

```python
def report(doc: RawDoc) -> RawDoc:
    print(doc.doc_id)
    return doc


pipeline = fmap(report)
```

`fmap` preserves the callback's effects; it does not purify them. Repeated evaluation
prints repeatedly.

### Abstraction erases the domain

A chain of anonymous lambdas may be shorter than `docs_to_embedded`, but it can hide
normalization, expansion, and embedding behind generic plumbing. If a reviewer cannot
name the domain transition at each boundary, the composition has not earned its cost.

## Proof route

Inspect:

```text
capstone/module-reference-states/module-01/src/funcpipe_rag/fp.py
capstone/module-reference-states/module-01/src/funcpipe_rag/rag_pipe.py
capstone/module-reference-states/module-01/src/funcpipe_rag/full_rag.py
```

Then run the Module 01 law suite:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/test_laws.py
```

Review `test_fmap_identity_law`, `test_fmap_composition_law`, and
`test_refactor_preserves_chunk_structure`. The first two prove combinator behavior;
the last checks that decomposing the monolithic loop preserves RAG chunk metadata.

## Learner work

Write two versions of a pipeline that cleans documents and counts abstract lengths:

1. an explicit comprehension;
2. `flow(fmap(clean_doc), fmap(lambda doc: len(doc.abstract)))`.

Assert equal output for empty, one-document, and multi-document inputs. Then explain:

- why the `flow` stages fit;
- where eager lists are allocated;
- why the equivalent pattern cannot directly express `chunk_doc` without binding
  `RagEnv` and flattening;
- which version you would choose in a review and why.

Preserve the Module 01 learning proof. Continue with
[Local Functional Refactors](local-fp-refactors.md), which applies these judgments to
small changes instead of demanding a whole-program rewrite.
