# Layered Containers: Decide Which Outcome Dominates

A retrieval can succeed and find a document, succeed and find nothing, or
fail. One container is not enough to distinguish all three outcomes:

```text
found:    Ok(Some(document))
missing:  Ok(NoneVal())
failed:   Err(retrieval_error)
```

That public meaning is:

```text
Result[Option[CleanDoc], ErrInfo]
```

Read from the outside inward:

1. Did retrieval succeed?
2. If it succeeded, was a document present?

The order is a domain decision. It is not decorative type syntax.

## Run the three retrieval cases

The Module 06 learning proof constructs:

```python
found: Result[Option[CleanDoc], ErrInfo] = Ok(
    Some(doc)
)

missing: Result[Option[CleanDoc], ErrInfo] = Ok(
    NoneVal()
)

failed: Result[Option[CleanDoc], ErrInfo] = Err(
    ErrInfo(
        code="RETRIEVAL",
        msg="index unavailable",
    )
)
```

The cases remain distinguishable. In particular, `missing` is not an error and
`failed` is not absence.

Run the proof:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k layer_order_distinguishes_missing_document_from_retrieval_failure
```

Before running, write the expected result for each case. If you cannot name the
outer and inner decision, the type is not yet helping.

## Why transpose the layers?

The reference state provides:

```python
transpose_result_option(
    value: Result[Option[T], E],
) -> Option[Result[T, E]]
```

and the reverse:

```python
transpose_option_result(
    value: Option[Result[T, E]],
) -> Result[Option[T], E]
```

For the three cases:

| Input | Transposed output |
| --- | --- |
| `Ok(Some(doc))` | `Some(Ok(doc))` |
| `Ok(NoneVal())` | `NoneVal()` |
| `Err(error)` | `Some(Err(error))` |

The failed retrieval becomes `Some(Err(error))`, not `NoneVal()`. Error
dominates absence in the shipped conversion.

Transposition can be useful when an API or combinator expects the other layer
order. It should not be performed merely to make a type look familiar.

## Prove the conversion does not lose a case

The learning proof round-trips every declared case:

```python
assert transpose_option_result(
    transpose_result_option(found)
) == found
```

The same assertion holds for `missing` and `failed`.

The property suite generalizes this as an involution over generated values:

```text
transpose back (transpose value) == value
```

Run it:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/test_layering.py
```

Round-trip equality proves the helper preserves the modeled cases. It does not
prove that the original public type is the right product decision.

## Choose the public meaning before the container

Consider an empty query. Several contracts are possible:

- `Err(EMPTY_QUERY)`: the caller supplied invalid input;
- `Ok(NoneVal())`: an empty query is valid but has no result;
- a separate query ADT that prevents emptiness at construction.

No transpose helper can make that decision for you. State the public meaning
first, then select the type that represents it.

For FuncPipe, treating an empty query as a typed input failure is defensible
because no retrieval attempt should occur. A valid non-empty query with no
matching document remains successful absence.

## Outer context determines control

Compare:

```text
Result[Option[T], E]
Option[Result[T, E]]
```

With Result outside, the program first decides whether the operation failed.
With Option outside, absence can prevent there being an inner Result at all.

The difference becomes more consequential with State or Writer:

```text
State[S, Result[T, E]]
Result[State[S, T], E]

Writer[Result[T, E]]
Result[Writer[T], E]
```

Questions to answer before layering:

- If the domain operation fails, are state changes retained?
- Can trace entries describe work before a failure?
- Does absence suppress an error, or can errors occur independently?
- Which context owns short-circuiting?
- What does the outer boundary need to pattern-match first?

Module 06 deliberately does not ship one universal transformer stack. Explicit
small types and transpose helpers keep the policy visible.

## Prefer a dedicated domain sum when combinations are constrained

Layered generic containers can represent more combinations than the product
allows. If the application has a small closed set of retrieval states, a
domain type may be clearer:

```python
type Retrieval = (
    Retrieved
    | NoMatch
    | RetrievalFailed
)
```

Use generic layering when the independent meanings and existing APIs compose
naturally. Use a domain sum when named cases communicate the workflow better
or prevent nonsensical combinations.

This is the same modelling judgment from Module 05 applied to flow.

## Common wrong turns

- **Using `None` for every non-value.** It erases failure provenance.
- **Converting `Err` to `NoneVal`.** A failed operation becomes
  indistinguishable from successful absence.
- **Choosing the outer container by convenience.** The outer layer controls
  which decision happens first.
- **Transposing without a round-trip test.** A case may disappear silently.
- **Building deeply nested stacks.** If reviewers cannot state the public
  cases, introduce a named domain type or boundary adapter.
- **Calling one order universally correct.** The product contract determines
  dominance.

## What the focused proof establishes

The learning test proves that found, missing, and failed retrieval cases remain
distinct through both transpose functions and round-trip to their original
values.

It does not prove that all applications should use
`Result[Option[T], E]`, or that an empty query must be classified in one
particular way.

Continue with [Writer Pattern](writer-pattern.md) to model ordered side
information without emitting it as an effect.
