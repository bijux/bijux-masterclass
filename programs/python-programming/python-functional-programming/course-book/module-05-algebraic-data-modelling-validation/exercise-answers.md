# Module 05 Exercise Answers

Use these answers to review a completed attempt, not as starting code. A
defensible alternative may use different syntax, but it must preserve the
observable, the ownership boundary, and the earlier cumulative RAG contract.

## Product and sum types

`ChunkWithoutEmbedding` is a product: its identity, text, offsets, and metadata
must travel together. The outcome is the existing sum
`Result[Chunk, ErrInfo]`. A defensible reporter has one branch per variant:

```python
def report(result: Result[Chunk, ErrInfo]) -> str:
    match result:
        case Ok(value=Chunk(doc_id=doc_id, start=start, end=end)):
            return f"ready:{doc_id}:{start}-{end}"
        case Err(error=ErrInfo(stage=stage)):
            return f"failed:{stage}"
        case other:
            assert_never(other)
```

Avoid a Boolean paired with optional error and embedding fields: that recreates
contradictory states. Avoid adding a second `ChunkState` union solely for this
exercise; `Result` already owns the success/failure decision.

The evidence proves that the real product keeps its tested fields together,
metadata rejects top-level mutation, and both result alternatives are
distinguishable. It does not prove arbitrary JSON is safe, deep-freeze nested
metadata, or show that embedding itself cannot fail.

## Domain states

Use the application operations in order:

```python
raw = RawDoc("state-1", "Types", "  Typed   values  ", "fp")
cleaned = clean_doc(raw)
prepared = chunk_doc(cleaned, RagEnv(chunk_size=32))[0]
indexed = embed_chunk(prepared)

assert indexed.doc_id == prepared.doc_id
assert indexed.text == prepared.text
assert (indexed.start, indexed.end) == (prepared.start, prepared.end)
assert raw.abstract == "  Typed   values  "
```

The most important decision is what not to add. A timestamped job lifecycle
has no owner, persistence surface, or user-visible behavior in this indexing
path. It would be an unrelated application hidden inside the lesson.

Common wrong turns are mutating `prepared`, checking only `isinstance`, or
calling a two-value vector an indexed `Chunk`. The focused route proves the
declared stages execute and preserve the listed observables. It does not prove
that Python enforces annotations at runtime or that boundary input is valid.

## Functors

Use `result_map(word_count)(cleaned)`. The mapper should run exactly once for
`Ok` and never for `Err`; the same error value should be returned.

Manual unboxing duplicates container policy, while `result_try_map` would add
exception conversion that this pure projection does not need. The test proves
map behavior for the modeled branches, not that every callable is pure or that
mapping can sequence a function which itself returns `Result`.

## Applicative validation

Create three independent `Validation` values, then combine them with
`v_liftA3`. A failed input should preserve errors in the same left-to-right
order as the arguments.

Using fail-fast `Result` loses later feedback; inventing `bind` for
`Validation` falsely implies the checks are dependent. This proves
accumulation for these independent fields. It does not prove that cross-field
rules can be checked before the individual values exist.

## Monoids

Add `rejected` component-wise, retain `0` as the identity, and retain `max` for
maximum latency. Verify both `(a <> b) <> c` and `a <> (b <> c)`.

Summing maximum latency changes its meaning; averaging during each combine is
not associative without carrying count and sum. The proof establishes the
declared metric operation for generated or chosen finite inputs, not safe
distributed aggregation under arbitrary floating-point regrouping.

## Pydantic smart constructors

Call `ChunkModel.model_validate` before `to_core_chunk` and compare the complete
round-trip:

```python
edge = ChunkModel.model_validate({
    "doc_id": "edge-1",
    "text": "valid",
    "start": 4,
    "end": 9,
    "metadata": {"source": "exercise"},
    "embedding": (0.0,) * 16,
})
core = to_core_chunk(edge)
assert from_core_chunk(core) == edge
assert deserialize_model(serialize_model(edge), ChunkModel) == edge
```

Do not catch all validation errors and construct the core value anyway. Do not
compare only text and metadata; that can hide discarded identity, offsets, or
embedding. The proof establishes complete preservation plus the declared
dimension, finiteness, and offset rejections. It does not establish migration
compatibility with a future schema or make Pydantic the owner of the core.

## Pattern matching

Use the explicit `Ok` and `Err` branches shown in the product-and-sum answer,
and leave `assert_never` as the final statement. Destructure the fields needed
for the public label rather than reaching through nullable attributes.

A wildcard makes future variants silently look handled; an `isinstance` chain
without a final impossibility check loses the closed-union review signal. The
test proves runtime coverage of the two constructed variants. Static
exhaustiveness still depends on the type checker understanding the annotated
union; the runtime test alone cannot detect a future unconstructed variant.

## Serialization

Use `to_json(failure, enc_result())` and
`from_json(encoded, dec_result())`, then compare the complete `Err` value.
Change only `ver` to exercise rejection.

Serializing `__dict__` or `repr` couples storage to implementation layout.
Dropping `stage` or `path` preserves an error message but loses provenance. The
round-trip proves the current envelope contract for the tested value, not
compatibility with an unregistered future version.

## Compositional domain models

Let `ChunkText`, `ChunkMetadata`, and `Embedding` remain independently
constructible. Put model/dimension agreement in `assemble`, where all three
values are visible, and normalize tags without reordering first occurrences.

Making each subsystem import the combined `Chunk` creates circular ownership.
Returning only the first mismatch defeats accumulating validation. The proof
establishes the current cross-field rules and tag normalization; it does not
prove all business invariants have been discovered.

## ADT performance

Run both modes on the same immutable input batch. Compare IDs, order, text,
metadata, embedding model, and vectors with the declared floating-point
tolerance.

Comparing only lengths can hide reordering or identity loss. Exact float
equality may reject a correct representation change, while an undocumented
large tolerance can hide drift. The proof establishes observable equivalence
for the generated domain, not that the hybrid route is faster on production
workloads.

## Refactoring guide

Characterize the accepted legacy dictionary shape first. For those inputs,
compare its complete core `Chunk` with
`to_core_chunk(ChunkModel.model_validate(raw))`. Test malformed input
separately as an intentional contract tightening.

Changing accepted normalization and adapter structure together makes a
difference impossible to diagnose. Keeping both adapters indefinitely creates
two owners. The evidence proves equality on the characterized accepted set and
one deliberate rejection; it does not prove equivalence for every dictionary
or replace migration planning for existing stored data.
