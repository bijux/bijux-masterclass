# Typed Pipelines

Type annotations make stage boundaries reviewable before execution. In a pipeline,
the key question is:

```text
Does each stage accept the value produced by the preceding stage?
```

Module 01 answers that question with domain dataclasses, typed stage signatures, and
the generic `RagPipe` wrapper. It does not yet introduce `ParamSpec`,
`Concatenate`, typed decorators, or context injection.

## Domain transitions are the first type system

FuncPipe models its stage order with distinct values:

```python
def clean_doc(doc: RawDoc | CleanDoc) -> CleanDoc: ...
def chunk_doc(
    doc: CleanDoc,
    env: RagEnv,
) -> list[ChunkWithoutEmbedding]: ...
def embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk: ...
```

The types expose an invalid composition:

```python
embed_chunk(clean_doc(raw_doc))
```

`clean_doc` returns `CleanDoc`, while `embed_chunk` requires
`ChunkWithoutEmbedding`. The missing chunking transition is visible without tracing
field access at runtime.

## Container shape is part of the contract

`chunk_doc` returns many slices for one document:

```text
CleanDoc -> list[ChunkWithoutEmbedding]
```

`embed_chunk` transforms one slice:

```text
ChunkWithoutEmbedding -> Chunk
```

They cannot be directly composed as unary functions. The caller must map embedding
over the returned list:

```python
chunks = chunk_doc(clean_doc(raw_doc), env)
embedded = [embed_chunk(chunk) for chunk in chunks]
```

A type annotation should reveal this one-to-many boundary instead of hiding it behind
`Any`.

## Configuration belongs in the signature

`RagEnv` makes chunk policy explicit:

```python
def chunk_doc(
    doc: CleanDoc,
    env: RagEnv,
) -> list[ChunkWithoutEmbedding]:
    ...
```

The annotation alone does not validate runtime values. The frozen dataclass checks
that `chunk_size` is an exact positive integer. Static and runtime responsibilities
are complementary:

| Mechanism | Catches |
| --- | --- |
| annotation | callers passing a statically known wrong type |
| constructor validation | invalid values at runtime |
| behavioral test | incorrect slicing despite valid values |

## `flow` is intentionally weakly typed

Module 01's `flow` accepts:

```python
Callable[[Any], Any]
```

This makes the implementation small, but a type checker cannot reject mismatched
adjacent stages:

```python
broken = flow(clean_doc, embed_chunk)
```

The construction type-checks through `Any`; execution fails when `embed_chunk`
receives a `CleanDoc`.

Use `flow` when the chain is obvious and separately typed domain functions make the
boundary clear. Do not present it as machine-checked pipeline composition.

## `RagPipe` preserves adjacent types

The generic wrapper records input and output:

```python
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class RagPipe(Generic[A, B]):
    def __init__(self, stage: Callable[[A], B]):
        self._stage = stage

    def __call__(self, value: A) -> B:
        return self._stage(value)

    def then(self, next_stage: Callable[[B], C]) -> "RagPipe[A, C]":
        return RagPipe(lambda value: next_stage(self._stage(value)))
```

A valid chain:

```python
clean_length: RagPipe[RawDoc, int] = (
    RagPipe(clean_doc)
    .then(lambda doc: len(doc.abstract))
)
```

A static checker can reject:

```python
RagPipe(clean_doc).then(embed_chunk)
```

because `embed_chunk` does not accept `CleanDoc`.

`RagPipe` still models only unary stages. It does not bind `RagEnv`, flatten chunk
lists, or prove purity. Types constrain shape, not effects.

## Why `full_rag` stays explicit

The tracked Module 01 application uses:

```python
def docs_to_embedded(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    cleaned = [clean_doc(doc) for doc in docs]
    chunked = [chunk for doc in cleaned for chunk in chunk_doc(doc, env)]
    embedded = [embed_chunk(chunk) for chunk in chunked]
    return embedded
```

The intermediate names and annotations describe:

- batch mapping;
- one-to-many expansion;
- configuration use;
- another batch mapping.

Forcing this through `RagPipe` would require new adapters whose types are more complex
than the domain behavior. The explicit function is the better teaching surface.

## A typing mismatch the module repaired

The cleaning law is:

```python
clean_doc(clean_doc(raw)) == clean_doc(raw)
```

If `clean_doc` accepted only `RawDoc`, that executable law would contradict its type
signature because the inner call returns `CleanDoc`. Module 01 therefore types the
input as `RawDoc | CleanDoc`.

This is a useful review lesson: a runtime test can pass while the public type contract
rejects the same expression. Tests and annotations must describe the same domain.

## What types do not prove

These functions have identical shapes:

```python
def pure_length(text: str) -> int:
    return len(text)


def recorded_length(text: str) -> int:
    audit.append(text)
    return len(text)
```

Typing cannot distinguish their effects. It also cannot establish determinism,
canonical ordering, idempotence, or resource bounds.

Use types with behavior tests and source review:

```text
types:      adjacent values fit
examples:   named behavior is understandable
properties: law holds over a wider domain
review:     hidden effects and ownership are acceptable
```

## Proof route

Inspect:

```text
capstone/module-reference-states/module-01/src/funcpipe_rag/rag_types.py
capstone/module-reference-states/module-01/src/funcpipe_rag/pipeline_stages.py
capstone/module-reference-states/module-01/src/funcpipe_rag/rag_pipe.py
```

Run:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py
```

The short proof checks runtime invariants and behavior. A type checker is a separate
route; passing tests do not substitute for it.

## Learner work

Define a typed unary adapter:

```python
def chunk_count(env: RagEnv) -> Callable[[CleanDoc], int]:
    ...
```

Use it in:

```python
RagPipe(clean_doc).then(chunk_count(env))
```

Provide:

- exact annotations with no `Any`;
- an example for an empty abstract;
- an example for a final short chunk;
- a deliberately incompatible `.then` call for static inspection;
- an explanation of why the adapter captures policy and why Module 02, not Module 01,
  develops that configurator pattern further.

Continue with [Typed Pipeline Review](typed-pipeline-review.md) for the compact review
checklist before moving to effect ownership.
