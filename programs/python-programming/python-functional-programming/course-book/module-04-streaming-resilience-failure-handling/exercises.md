# Module 04 Exercises

These exercises extend or review the Module 04 FuncPipe reference state. They
are cumulative: keep each accepted contract in place while adding the next
decision.

Before changing code:

1. write the expected source demand and output sequence;
2. identify whether failure is a record value, terminal policy event, or
   exception;
3. state which Module 03 streaming behavior must remain true;
4. choose the smallest proof route; and
5. record what the proof cannot establish.

Use this command shape from the repository root:

```bash
course=programs/python-programming/python-functional-programming
state="$course/capstone/module-reference-states/module-04"
venv=artifacts/venv/python-programming/python-functional-programming/capstone

PYTHONPATH="$state/src" \
  "$venv/bin/pytest" -q \
  "$state/tests/learning/test_module_04_resilient_streaming.py" \
  -k TEST_FRAGMENT
```

## Hierarchical ingestion: preserve order while fusing evidence

Starting context: run the tests selected by `-k
"hierarchical_document or fused_tree_fold"`. Draw the current four-node tree
with its paths.

Objective: add a second child under node `b`, then extend the fused fold with an
empty-text-node count.

Constraints:

- preserve preorder and `depth == len(path)`;
- leave the recursive traversal as a specification, not the production route;
- keep three-item prefix demand on the 1,200-node chain;
- compute all four observations in one fused pass; and
- use an immutable accumulator.

Expected evidence:

- the exact text/path sequence for the changed tree;
- equality between the fused four-tuple and four separate folds;
- a cycle or shared-subtree case that demonstrates the tree boundary; and
- the original Module 03 bounded-prefix claim still passes.

Acceptance check: a reviewer can distinguish output equivalence, stack safety,
input validity, and traversal count. The test need not claim a measured
speedup.

## Embedding memoization: repair an incomplete semantic key

Starting context: run `-k semantic_memo_key`. The shipped key treats normalized
text as the whole embedding input.

Objective: make the deterministic embedding depend on both normalized text and
`doc_id`, then redesign the memo key.

Constraints:

- first add a failing characterization with equal text and different document
  IDs;
- include every observed input in the repaired key;
- preserve one cache hit for whitespace-equivalent text within the same
  document;
- keep the output immutable; and
- do not add a disk cache or benchmark.

Expected evidence:

- cached and uncached outputs agree for both document IDs;
- two semantic inputs cause two computations;
- whitespace-only differences within one document share work; and
- the answer states why a hit count alone cannot establish correctness.

Earlier contract to preserve: deterministic local embedding returns the same
value for the same complete semantic input.

## Record failures: retain position without catching invariants

Starting context: run `-k "option_absence or result_stream"`. Review the
existing `DOC/MISSING` and `EMBED/INVALID` errors.

Objective: classify and emit one retryable embedding failure, one permanent
embedding failure, one expected absence, and one invariant exception.

Constraints:

- use stable codes, the `embed` stage, and source-position paths for record
  failures;
- do not convert the invariant exception to `Err`;
- do not convert a provenance-bearing failure to `Option` before its reason is
  observed;
- keep one `Result` per requested record; and
- take a prefix and prove a later source item was not requested.

Expected evidence:

- the exact `Ok`/`Err` sequence and paths;
- success-only work is not called for `Err`;
- the invariant exception escapes at the named boundary; and
- the source counter equals the requested prefix.

Earlier contract to preserve: successful Module 03 inputs retain encounter
order and values.

## Run policy: separate aggregation from early termination

Starting context: run `-k "error_fold or emitting_breaker"`. Use the same mixed
result stream for both paths.

Objective: provide an interactive fail-fast route and an offline diagnostic
route, then add an emitting count breaker to the latter.

Constraints:

- predict source demand for every route;
- cap retained diagnostic samples without claiming the full scan is lazy;
- treat `max_errs` as tolerated errors, so the next error triggers;
- retain the threshold-crossing record before `BreakInfo`; and
- do not use the truncating breaker where normal exhaustion and policy
  termination would be ambiguous.

Expected evidence:

- fail-fast demand stops at the first `Err`;
- capped collection consumes the finite source and marks overflow;
- the breaker emits the consumed prefix plus one terminal value; and
- a source item after the trigger is not requested.

Acceptance check: the choice is justified by whether partial success and full
diagnostics are useful, not by helper names.

## Recovery boundary: combine cleanup and bounded retry

Starting context: run `-k "managed_stream or retry_classification"`. Record the
current retry completion order.

Objective: consume a factory-created chunk source through the retry engine and
stop it with a breaker after the permanent-error budget is exceeded.

Constraints:

- acquisition begins inside `managed_stream`;
- only `EMBED/UNAVAILABLE` is retryable;
- policy attempts may not exceed the engine cap;
- no synchronous sleeping is added;
- source order is not claimed after fair retries; and
- cleanup must be observed after early termination.

Expected evidence:

- attempt counts for stable, transient, and permanent chunks;
- the exact completion-order result sequence;
- final retry metadata for an exhausted retryable failure;
- an unattempted chunk after breaker termination; and
- the source's cleanup observation after leaving the context.

Earlier contract to preserve: every attempted embedding remains deterministic,
and all requested work is bounded by declared limits.

## Review artifact: explain the complete resilient stream

Starting context: run `-k retry_breaker_and_report`, then read
`capstone-delta.md`.

Objective: add a second permanent error code and produce a JSON-safe report
that distinguishes record failures from the terminal breaker event.

Constraints:

- predict `total_items`, `total_errs`, code counts, and attempts before running;
- keep `max_samples=1`;
- retain the nested last error and immutable retry context in serialized
  `BreakInfo`;
- use stable low-cardinality codes; and
- identify recovered and unattempted failures outside the report's observation
  boundary.

Expected evidence:

- exact attempt and output traces;
- counts can exceed retained samples;
- `json.dumps(payload)` succeeds;
- the nested terminal sample retains code, path, and retry context; and
- Module 03's successful chunk values remain unchanged when no failure policy
  triggers.

Move to the refactoring guide only when you can narrate the complete route from
source acquisition to terminal report without treating the capstone as a set
of disconnected utility modules.
