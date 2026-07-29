# Module 04 Capstone Delta: Resilient Streaming

Module 03 leaves FuncPipe with a lazy document pipeline. It can normalize,
chunk, trace, group, fan out, and stop after a bounded prefix. Those guarantees
make large inputs tractable, but they do not answer what happens when one
document is hierarchical, one embedding attempt fails, or a consumer stops
before the source is exhausted.

Module 04 keeps the stream and makes its failure decisions inspectable.

## The application delta

| Contract question | Module 04 answer |
| --- | --- |
| Previous capability | A lazy, ordered, bounded document-to-chunk stream with deterministic local embedding |
| New pressure | Hierarchical documents can exceed Python's recursion limit; individual records can fail; retries can monopolize work; early termination can strand a producer; operators still need bounded evidence |
| Concepts introduced | Explicit-stack traversal, folds and scans, memoization, `Result`/`Option`, result-valued streams, error aggregation, circuit breakers, managed streams, retry policies, and structured reports |
| Source surfaces | `rag_types.py`, `tree/`, `result/`, `policies/`, and the RAG API split under `api/` |
| Teaching proof | `tests/learning/test_module_04_resilient_streaming.py` plus the focused Module 04 unit tests |
| Preserved behavior | Module 03 cleaning and chunking results, encounter order when no retry reorders completion, lazy prefix demand, explicit materialization, and deterministic embedding |
| Completed state | `capstone/module-reference-states/module-04/` |
| Learner route | Run the Module 04 learning proof, then compare Modules 03 and 04 through generated history |
| Later states affected | Modules 05 through 09 and the live Module 10 endpoint retain the Module 04 `tree`, `result`, and `policies` contracts |

This is a policy delta, not a claim that every failure should become a value.
Programmer errors and broken process invariants can still raise. Expected
record-level failures become `Err` values when the caller needs to continue,
retry, aggregate, or report them.

## One RAG pressure, ten decisions

The module's cores are not ten independent utility tours. They answer a
sequence of questions about the same ingestion and embedding flow:

1. Can a deeply nested document be traversed without consuming the Python call
   stack?
2. Can several traversal observations be computed in one pass?
3. Can a deterministic embedding calculation avoid repeated work without
   changing its answer?
4. Can expected absence and expected failure be distinguished in the return
   type?
5. Can one bad chunk remain evidence in a stream instead of aborting every
   later chunk?
6. Should this run stop on the first error or collect bounded evidence?
7. At what observed threshold should the system stop asking the source for
   more work?
8. Who closes the source when the consumer stops early?
9. Which failures may be retried, for how many attempts, and with what
   scheduling semantics?
10. What bounded report lets a reviewer explain the run after it ends?

The order matters. A breaker cannot make a useful decision until failure is
data. A retry policy cannot be reviewed until retryable errors are classified.
Cleanup cannot be inferred merely because a generator stopped yielding.

## Before and after

Module 03's happy-path shape is intentionally simple:

```text
documents -> normalize -> chunk -> embed -> consume
```

Module 04 preserves that route and adds explicit alternatives around the
fallible stage:

```text
hierarchical document
        |
        v
stack-safe chunks -> embed attempt -> Ok(chunk) --------------------+
                                   -> Err(info) -> retry policy -----+-> breaker
                                                                       |
                                                                       +-> bounded report
source lifetime ------------------------------------------------------> cleanup
```

The arrows do not promise that retry completion order equals source order.
`retry_map_iter` uses a bounded fair queue, so an item that succeeds immediately
may complete before an earlier item that is retried. Preserve source order only
when the downstream contract requires it, and make the buffering cost visible.

## Source ownership

The Module 03→04 snapshot contains both behavioral additions and a code split.
Review them separately.

| Surface | Durable responsibility | Intended behavior change |
| --- | --- | --- |
| `tree/` | Traverse and fold hierarchical documents without recursive call-stack growth | New hierarchical ingestion capability |
| `result/` | Represent expected failure and compose streams that carry it | New value-level failure path |
| `policies/retries.py` | Classify and schedule bounded retry attempts | New recovery policy |
| `policies/breakers.py` | Stop demand after an observed failure threshold | New terminal policy and evidence |
| `policies/resources.py` | Tie iterator lifetime to a context boundary | New cleanup guarantee |
| `policies/reports.py` | Fold failures into bounded operator evidence | New review surface |
| `policies/memo.py` | Cache deterministic work under an explicit semantic key | New optimization with a correctness condition |
| `api/chunking.py`, `api/rag_api.py`, `api/streaming_rag.py` | Separate the existing RAG API from the export-heavy `api/core.py` | Organization only; existing RAG outputs should remain equivalent |

The code split is not evidence of resilience. The learning proof targets the
new behavior, while the existing RAG API tests protect the behavior that the
split must preserve.

## Proof ladder

From the repository root:

```bash
course=programs/python-programming/python-functional-programming
state="$course/capstone/module-reference-states/module-04"
venv=artifacts/venv/python-programming/python-functional-programming/capstone

PYTHONPATH="$state/src" \
  "$venv/bin/pytest" -q \
  "$state/tests/learning/test_module_04_resilient_streaming.py"
```

The focused route is deliberately small. Read each test name before reading its
body, predict the demand and output, run it, and then explain any mismatch.

To inspect the complete transition:

```bash
make PROGRAM=python-programming/python-functional-programming history-refresh
diff -ru \
  "$course/capstone/_history/worktrees/module-03/src/funcpipe_rag" \
  "$course/capstone/_history/worktrees/module-04/src/funcpipe_rag"
```

Do not interpret every diff hunk as a new concept. Use the ownership table to
separate behavior from file movement, and use tests to decide whether a
preservation claim is true.

## Preserved contracts

After completing Module 04, you should still be able to demonstrate:

- consuming a prefix requests only the work needed for that prefix;
- successful records retain their values and failure records retain their
  provenance;
- a fail-fast fold does not inspect values after its first `Err`;
- a breaker closes a closable upstream iterator when it terminates early;
- retry attempts are bounded by both the policy and the engine cap;
- cleanup occurs on normal exhaustion, consumer failure, producer failure, and
  partial consumption; and
- reports cap stored samples even though their counts cover the consumed run.

These claims do not prove production readiness. The reference implementation
does not perform real network waits, provide cross-process cache coordination,
or promise source order after fair retries. It provides deterministic local
semantics that make those later engineering decisions reviewable.
