# Module 04 Exercise Answers

Use these answers after recording your own predictions and evidence. Different
syntax is defensible when it preserves the same demand, ordering, provenance,
and lifetime contracts.

## Hierarchical ingestion

Add the new child as a sibling under `b`, then derive its path from child
position. If `c` remains first and the new node is second, the paths are
`(1, 0)` and `(1, 1)`. Do not sort nodes after traversal; encounter order is
part of the RAG provenance.

Extend the accumulator from `(count, length, max_depth)` to
`(count, length, max_depth, empty_count)`. The combiner returns a new tuple:

```python
return (
    count + 1,
    length + len(node.node.text),
    max(max_depth, depth),
    empty_count + int(not node.node.text),
)
```

Compare this fused result with four independent `fold_tree_no_path` calls. The
comparison establishes output equivalence for the constructed tree. Reading
the implementation establishes one fused traversal; the equality assertion
alone does not count visits or prove a speedup.

A common wrong turn is to put a mutable list or set in the accumulator and
mutate it in place. That can work, but aliases make the intermediate states
harder to reason about and make scan behavior surprising. Another wrong turn
is assuming stack safety implies cycle safety. The Module 04 folds require a
valid finite tree; use `assert_acyclic` at an untrusted construction boundary.

The result proves preorder metadata and fused observations for the tested
tree. It does not prove arbitrary graphs are accepted or that fusion is faster
on the production workload.

## Embedding memoization

Once the function observes `doc_id`, text alone is no longer a congruent key.
Two chunks can share normalized text while producing different results. A
defensible key is a tuple of every observed semantic input:

```python
def embedding_key(chunk: ChunkWithoutEmbedding) -> tuple[str, str]:
    normalized = " ".join(chunk.text.strip().lower().split())
    return chunk.doc_id, normalized
```

Use the same normalization policy in the embedding function. Two document IDs
should cause two calls; whitespace variants within one ID should reuse the
first result.

Do not “repair” the test by removing `doc_id` from the output. That changes the
function to fit an incomplete cache key. Do not append object identity or
source offsets unless the function observes them; overspecifying the key is
correct but destroys valid reuse.

The comparison between cached and uncached outputs proves the chosen cases are
observationally equivalent. The call counter proves reuse. Neither proves all
possible collisions are safe, that concurrent misses are single-flight, or
that a persistent cache would stay valid after an embedding-model change.

## Record failures

Keep the classifications distinct:

| Situation | Defensible representation |
| --- | --- |
| No optional search match | `Nothing()` |
| Provider temporarily unavailable | `ErrInfo(code="EMBED/UNAVAILABLE", ...)` |
| Chunk violates the embedding input contract | `ErrInfo(code="EMBED/INVALID", ...)` |
| Impossible negative offset inside trusted core state | Exception |

Use source index or document-section path in `ErrInfo.path`. Messages may change
for readers; paths and stable codes are machine-consumed provenance.

Apply success-only work with `map` and record whether the function ran. For the
stream, use `try_map_iter` only at the generic exception-adapter boundary or
return `Result` directly from a domain-aware embedder. Take a prefix with
`islice` and count source requests.

Common wrong turns are converting every exception to `Err`, using `Option` for
provider failure, or filtering errors before their original positions are
observed. Those choices respectively hide defects, erase cause, and shift the
meaning of later positions.

The result proves the declared cases preserve their chosen evidence and the
serial prefix bounds demand. It does not prove the failure taxonomy is
complete or that a parallel adapter requests exactly the same prefix.

## Run policy

Use separate functions or named routes because interactive and offline
requirements differ.

The interactive route can use `fold_results_fail_fast`; a source counter should
stop at the first `Err`. The offline route can use
`fold_results_collect_errs_capped`; it consumes the finite stream, retains at
most the declared number of error values, and sets the overflow flag.

Place `circuit_breaker_count_emit` around a result stream when the run should
stop after the tolerated error budget. For `max_errs=1`, expect:

```text
first Err, second Err, Err(BreakInfo), stop
```

The second record is the threshold-crossing failure and remains visible.

Do not use capped collection to claim bounded work: it bounds retained samples
while scanning the complete finite input. Do not use a truncating breaker for
an operator report unless another channel already records termination.

The checks prove demand and output for the tested sequence. They do not prove a
chosen error threshold is operationally appropriate or statistically robust.

## Recovery boundary

Create the source only inside `managed_stream`, and consume the retry/breaker
composition inside the same `with` block:

```python
with managed_stream(source_factory) as chunks:
    retried = retry_map_iter(
        embed,
        chunks,
        classifier=is_retriable_errinfo,
        policy=fixed_policy(3),
        stage="embed",
        max_attempts=2,
        inflight_cap=2,
    )
    observed = list(circuit_breaker_count_emit(retried, max_errs=1))
```

The engine cap of two wins over the three-attempt policy. A permanent
`EMBED/INVALID` error receives one call. A transient failure can be requeued,
allowing a later stable item to complete first. Predict that completion order
from the queue instead of comparing it with source order.

Record cleanup in the source's `finally` block and assert it only after leaving
the context. Also record attempts so a prefetched but never attempted chunk is
distinguishable from an attempted failure.

Wrong turns include sleeping inside the policy engine, retrying every code,
returning the iterator after its context exits, and asserting source order on a
fair completion stream. If downstream order is required, tag items before
retry and restore order at an explicit bounded buffering boundary.

The result proves bounded attempts, the chosen completion semantics, and
cooperative source cleanup. It does not prove an external provider request is
idempotent or a remote client released its socket.

## Review artifact

Write the trace before changing input. With a second permanent code, calculate
each final `Result`, including the terminal breaker value. Count only values
that reach `fold_error_report`; recovered transient attempts and never-called
items are outside that report.

Keep codes low-cardinality, for example `EMBED/INVALID` and
`EMBED/DIMENSION`. With `max_samples=1`, each group's `count` may exceed one
while `samples` stays length one. The breaker group remains
`BREAK/ERR_COUNT`.

Serialize the report and inspect:

```python
terminal = payload["by_code"]["BREAK/ERR_COUNT"]["samples"][0]
assert terminal["last_error"]["code"] in {
    "EMBED/INVALID",
    "EMBED/DIMENSION",
}
assert terminal["last_error"]["ctx"]["attempt"] == 1
```

The field-by-field breaker serializer is essential because the nested
`ErrInfo.ctx` is immutable. Passing the whole breaker to
`dataclasses.asdict()` attempts a deep copy and fails for `mappingproxy`.

Common wrong turns are counting the breaker as an ordinary record without a
separate code, deriving codes from error messages, claiming `max_samples`
bounds group cardinality, or treating a JSON-safe dictionary as a versioned
wire schema.

Finally, run the successful Module 03-compatible path without injected
failures and compare complete chunk values. That preservation check proves the
resilience wrappers do not change tested successful outputs. It does not prove
production scale, external timing, cross-process cache behavior, or monitoring
backend compatibility.

You are ready for the refactoring guide when your review can state:

- what was requested;
- what completed and in which order;
- which failures recovered or became terminal;
- why demand stopped;
- who closed the source;
- which evidence the report retained; and
- which earlier successful behavior remained unchanged.
