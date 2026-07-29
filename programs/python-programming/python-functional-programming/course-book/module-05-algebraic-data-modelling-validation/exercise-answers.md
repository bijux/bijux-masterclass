# Module 05 Exercise Answers

Use these answers to review a completed attempt, not as starting code. A
defensible alternative may use different syntax, but it must preserve the
observable, the ownership boundary, and the earlier cumulative RAG contract.

## Product and sum types

Model `Skipped` as another frozen variant containing only data required to
explain the outcome. Extend the union and add one explicit match case.

Avoid a Boolean success flag paired with optional error and embedding fields:
that recreates contradictory states. Avoid silently treating an unknown tag as
`Skipped`; forward compatibility requires an explicit migration or rejection.

The evidence proves the declared variants are distinguishable and the tested
codec rejects one unknown tag. It does not prove arbitrary JSON is safe or that
every future outcome belongs in this union.

## Domain state ADTs

Add a cancellation event and transition only from states where cancellation is
a legal business action. Preserve the existing absorbing terminal branch.

Common wrong turns are mutating the current state, accepting every event from
every state, or comparing naive and aware datetimes. The focused route proves
the listed transitions and rejections; it does not prove the state machine is
correct under concurrent delivery or duplicated external events.

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

Call `ChunkModel.model_validate` before `to_core_chunk`. Keep the resulting
core value free of `BaseModel` inheritance and transport-only computed fields.

Do not catch all validation errors and construct the core value anyway. Do not
repeat the same edge constraints throughout the pure pipeline. The proof
establishes rejection and conversion for the declared schema cases, not that
Pydantic owns cross-subsystem domain invariants.

## Pattern matching

Add an explicit `case Skipped(reason=reason)` and leave `assert_never` as the
last branch. Each case should return the stable label required by callers.

A wildcard makes future variants silently look handled; an `isinstance` chain
without a final impossibility check loses the closed-union review signal. The
test proves runtime coverage of constructed variants. Static exhaustiveness
still depends on the type checker and the union annotation.

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
