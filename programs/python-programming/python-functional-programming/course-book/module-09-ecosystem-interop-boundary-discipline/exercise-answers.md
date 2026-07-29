# Module 09 Exercise Answers

Use these answers after producing your own evidence. The point is to compare
reasoning, not only final output.

## Standard library tools: prove laziness before preferring a helper

`merge_streams` returns `itertools.chain(*streams)`. Constructing the chain does not
ask any source for a value. A pull log owned by the source generator therefore
stays empty until the consumer calls `next`.

A defensible extension is:

```python
merged = merge_streams(source("left", (1,)), source("middle", (2,)), source("right", (3,)))

assert pulls == []
assert next(merged) == 1
assert pulls == [("left", 1)]
assert next(merged) == 2
assert pulls == [("left", 1), ("middle", 2)]
```

The important decision is to test an observable consumption contract. Testing
that the return value happens to be an `itertools.chain` would freeze an
implementation detail while proving nothing about future wrappers.

Common wrong turns:

- `list(merge_streams(...))` proves order but destroys the laziness evidence.
- counting generator construction as consumption confuses creating an iterator
  with advancing it.
- using `tee` for this exercise introduces a cache and a different memory
  question.

The result proves deferred, ordered consumption for the tested sources. It does
not prove constant memory for every stdlib iterator composition; `tee`, for
example, can buffer an unbounded skew between consumers.

In the application architecture, this keeps document ingestion on the lazy side
of the boundary. Later adapters may supply documents, but they do not gain
permission to materialize the whole corpus.

## Helper libraries: require semantic parity

The compatibility module is the public boundary. Calling `toolz` directly from
RAG stages would make installation state part of domain behavior. The exercise
therefore composes only the compatibility functions and asserts the same plain
Python result: `[5, 4]`.

The defensible dependency decision is conditional. Enable `toolz` when a team
already understands its left-to-right vocabulary and repeated pipelines become
easier to review. Keep the fallback when the helper only replaces a readable
generator expression with unfamiliar syntax.

Common wrong turns:

- testing `TOOLZ_AVAILABLE` instead of output tests installation state, not the
  contract
- returning a `toolz`-specific container leaks the library into the core
- materializing after every stage preserves values but abandons streaming

The result proves parity for the exercised compose, filter, map, and pipe route.
It does not prove every `toolz` operator has a compatible fallback. Each added
operator needs its own boundary contract.

In FuncPipe, the facade protects `RawDoc` and `Chunk` flows from optional-library
types. Removing the dependency should be a packaging decision, not a RAG rewrite.
