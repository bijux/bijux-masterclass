# A Small Combinator Library

A combinator captures a reusable way to combine functions or values. A good small
library removes repetition without replacing domain language with a private
framework.

Module 01's tracked `fp.py` exports only:

- `identity`
- `flow`
- `fmap`

`RagPipe` lives in `rag_pipe.py` as an alternative typed composition surface. This
small scope is deliberate. Filtering, flattening, folding, partial application,
instrumentation, and explicit context appear when later application pressures need
them.

## Start from repeated structure

Do not begin by listing abstractions you know. Begin with repetition in real code.

```python
cleaned = [clean_doc(doc) for doc in docs]
embedded = [embed_chunk(chunk) for chunk in chunks]
```

Both expressions repeat the same sequencing rule: apply one element transform to
every input and collect a list. `fmap` names that rule:

```python
cleaned = fmap(clean_doc)(docs)
embedded = fmap(embed_chunk)(chunks)
```

The domain functions remain named. The reusable part is only the mapping structure.

## `identity`

```python
def identity(value: A) -> A:
    return value
```

Production code rarely needs a named identity function by itself. It matters because
it defines a law:

```python
fmap(identity)(values) == values
```

If mapping identity changed values, `fmap` would be adding behavior beyond applying
the supplied function.

An identity callback can also be a defensible default when an API needs an optional
pure transform:

```python
def inspect_with(
    chunk: Chunk,
    transform: Callable[[Chunk], Chunk] = identity,
) -> Chunk:
    return transform(chunk)
```

Do not use identity to conceal that an API has too many optional extension points.

## `fmap`

Module 01 accepts any iterable but returns a list:

```python
def fmap(func: Callable[[A], B]) -> Callable[[Iterable[A]], list[B]]:
    def mapped(items: Iterable[A]) -> list[B]:
        return [func(item) for item in items]

    return mapped
```

Three facts belong in review:

1. callback type: `A -> B`;
2. accepted source: `Iterable[A]`;
3. evaluation strategy: eager `list[B]`.

This is not a general functor protocol. It is one list-producing helper with two
tested list laws.

### Failure route: unbounded input

```python
from itertools import count

fmap(str)(count())  # never finishes; attempts to build an infinite list
```

Module 01 has not introduced bounded streaming. Use `fmap` only when materializing the
input is acceptable. Module 03 changes this evaluation pressure explicitly.

## `flow`

`flow` composes unary stages left to right:

```python
clean_length = flow(clean_doc, lambda doc: len(doc.abstract))

assert clean_length(raw_doc) == len(clean_doc(raw_doc).abstract)
```

It is useful when stage shapes align and the chain becomes easier to name as one
operation.

### Failure route: type mismatch

The implementation uses `Callable[[Any], Any]`, so this construction is accepted:

```python
broken = flow(clean_doc, embed_chunk)
```

Execution fails because `embed_chunk` cannot consume `CleanDoc`. The library chooses
runtime simplicity over static composition checking. Learners should see that
trade-off rather than infer type safety from the word "pipeline."

## `RagPipe`

`RagPipe[A, B]` preserves adjacent generic types through `.then`:

```python
clean_length = RagPipe(clean_doc).then(lambda doc: len(doc.abstract))
```

It gives type checkers more information than `flow`, but it introduces a wrapper
object and method syntax. It is not automatically clearer for a two-stage
transformation.

| Surface | Strength | Cost |
| --- | --- | --- |
| direct call | explicit and easy to debug | nesting can grow |
| `flow` | readable left-to-right unary order | adjacent types use `Any` |
| `RagPipe.then` | typed adjacent stages | wrapper and generic vocabulary |
| explicit orchestration | handles configuration and one-to-many stages honestly | more domain-specific code |

Module 01 uses explicit orchestration for the full RAG behavior because the simple
combinators do not model `RagEnv` binding and document-to-chunks expansion cleanly.

## What is intentionally absent

The comments at the bottom of `fp.py` identify later concepts:

```text
pipe                 Module 02
ffilter and foldl    Module 03+
with_context         Module 06
log_calls            Module 07
```

That list protects the learning sequence. Adding these helpers early would create
code the matching lesson has not earned and a reference state learners cannot explain.

The same rule applies to a learner extension: experiment locally, but do not call the
experiment part of the Module 01 application contract.

## Law and behavior review

The law suite proves:

```python
fmap(identity)(xs) == xs
fmap(lambda x: g(f(x)))(xs) == fmap(g)(fmap(f)(xs))
```

These laws assume pure `f` and `g` when used as refactoring permissions. With effects,
the returned lists may be equal while logs, counters, or call timing differ.

The law suite does not currently establish algebraic laws for `flow` or `RagPipe`.
Treat those as readable implementations whose source and focused examples must still
be reviewed.

Run:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/test_laws.py
```

## Extension decision checklist

Before adding a combinator, answer:

1. What repeated sequencing rule exists in at least two meaningful places?
2. Can the rule be named without erasing domain intent?
3. What input, output, and evaluation strategy does it expose?
4. What law or focused behavior constrains it?
5. What effect does it preserve or duplicate?
6. Is the concept already part of the course sequence?
7. Is a direct comprehension or named function clearer?

If those answers are weak, keep the code explicit.

## Learner work

Implement a local `map_tuple` experiment:

```python
def map_tuple(func: Callable[[A], B]) -> Callable[[tuple[A, ...]], tuple[B, ...]]:
    ...
```

Provide:

- identity and composition tests;
- a test showing returned container type;
- a counterexample explaining why an effectful callback weakens refactoring laws;
- a short decision explaining why this helper should or should not enter FuncPipe.

Do not add it to the tracked reference state. The exercise is about earning an
abstraction, not expanding the library.

Continue with
[Combinator Laws and Trade-Offs](combinator-laws-and-tradeoffs.md), which examines
what these laws permit and where Python evaluation details limit them.
