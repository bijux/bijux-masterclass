# Module 08 Exercise Answers

Use these answers only after running the corresponding proof. Compare reasoning,
failure analysis, and architectural boundaries rather than copying assertions.

## Async plans: prove fresh execution without promising equal effects

Calling an `async def` function creates a coroutine object. A coroutine object is
single-use, so caching it and returning it twice makes the second await fail with
`RuntimeError: cannot reuse already awaited coroutine`.

The defensible shape is a callable such as `lambda: read_sequence()`.
`async_lift` stores that callable as the plan. Construction does not call it;
each `plan()` call asks it for a new coroutine.

Common wrong turns:

- creating `coroutine = read_sequence()` outside the plan performs premature
  coroutine allocation and makes replay invalid;
- asserting the two results are equal confuses replayability with deterministic
  effect output;
- driving the plan from domain code erases the interpreter boundary;
- testing only `callable(plan)` says nothing about deferral.

The test proves zero calls during construction and one fresh execution per plan
call. It does not prove the external capability is deterministic, idempotent, or
safe to retry.

In FuncPipe, the shell may replay an async description when policy allows it.
Whether the underlying storage or embedding effect may be repeated remains a
separate domain decision.

## Async generators: observe a partial pull

`async_gen_map` returns a new `AsyncGen`; it does not iterate its input. The
mapped iterator requests one source result for each downstream `anext`, applies
the pure mapping only to `Ok`, and yields that result. A four-value source
consumed three times must therefore produce a three-entry pull trace.

Closing the iterator is part of the proof. It states that the consumer owns the
active traversal and is responsible for ending partial consumption. The
description remains replayable because the source is a callable that creates a
new async iterator.

Common wrong turns:

- list-comprehending the output consumes every source value and hides the
  demand boundary;
- asserting only mapped output misses eager upstream work;
- omitting `aclose` teaches unsafe partial-consumption habits;
- returning one cached async generator object destroys replayability.

The proof establishes demand-driven evaluation for this composition. It does
not establish bounded parallelism; Core 3 adds an explicit concurrency policy
for that separate concern.

## Backpressure: expose the bounded window

The worker increments its active counter immediately before the await and
decrements it immediately after. A scheduling yield allows several calls to
overlap without introducing real-time delays. `maximum_active` therefore
captures the widest observed window directly.

With six inputs and `max_concurrent=3`, the bounded combinator starts no fourth
worker until one of the first three releases capacity. In ordered mode it also
buffers completions by input index, so the resulting values retain input order
even if individual workers finish differently.

Common wrong turns:

- checking only output order says nothing about bounded fan-out;
- sleeping for fixed real durations makes the proof slow and timing-sensitive;
- asserting exact task scheduling order promises more than the policy;
- putting a semaphore inside every worker creates separate limits instead of
  one shared stream limit.

The policy is immutable description data. The semaphore, tasks, active counter,
and work all come into existence only when the shell drives the returned
`AsyncGen`.

## Retry policy: keep repetition at the embedding boundary

Predict the calls before writing code:

| Document | Cleaning calls | Embedding attempts | Final position |
| --- | ---: | ---: | --- |
| `recovers` | 1 | 2 | `ok:recovers` |
| `exhausts` | 1 | 2 | `err:MAX_RETRIES` |
| `after` | 1 | 1 | `ok:after` |

Cleaning happens before the resilient mapper, so an embedding retry cannot
re-enter `clean_doc`. The mapper owns one plan per chunk and repeats only that
plan. Exhaustion is emitted as a value, allowing the bounded stream to request
the next prepared chunk.

A defensible proof is:

```python
def test_embedding_retry_review() -> None:
    docs = [
        RawDoc("recovers", "Recovers", "first", "demo"),
        RawDoc("exhausts", "Exhausts", "second", "demo"),
        RawDoc("after", "After", "third", "demo"),
    ]
    cleaned: list[str] = []
    attempts: dict[str, int] = {}

    def tracked_clean(doc: RawDoc) -> CleanDoc:
        cleaned.append(doc.doc_id)
        return clean_doc(doc)

    def scheduled_embedder(chunk: ChunkWithoutEmbedding) -> AsyncPlan[Chunk]:
        async def run() -> Result[Chunk, ErrInfo]:
            attempt = attempts.get(chunk.doc_id, 0) + 1
            attempts[chunk.doc_id] = attempt

            if chunk.doc_id == "recovers" and attempt == 1:
                return Err(ErrInfo(code="TRANSIENT", msg="retry once"))
            if chunk.doc_id == "exhausts":
                return Err(ErrInfo(code="TRANSIENT", msg="still unavailable"))
            return Ok(embed_chunk(chunk))

        return run

    resilient_embedder = resilient_mapper(
        scheduled_embedder,
        RetryPolicy(
            max_attempts=2,
            retriable_codes=frozenset({"TRANSIENT"}),
            backoff_base_ms=0,
            jitter_factor=0,
        ),
        env=make_test_resilience_env(),
    )
    stream = async_rag_chunks(
        async_gen_from_list(docs),
        RagEnv(chunk_size=32),
        tracked_clean,
        resilient_embedder,
        BackpressurePolicy(max_concurrent=1, ordered=True),
    )

    assert attempts == {}

    async def collect() -> list[Result[Chunk, ErrInfo]]:
        return [item async for item in stream()]

    results = asyncio.run(collect())
    labels = [
        f"ok:{item.value.doc_id}"
        if isinstance(item, Ok)
        else f"err:{item.error.code}"
        for item in results
    ]

    assert labels == [
        "ok:recovers",
        "err:MAX_RETRIES",
        "ok:after",
    ]
    assert cleaned == ["recovers", "exhausts", "after"]
    assert attempts == {"recovers": 2, "exhausts": 2, "after": 1}
    assert isinstance(results[1], Err)
    assert results[1].error.ctx is not None
    assert results[1].error.ctx["attempts"] == 2
```

The recovered `TRANSIENT` is an intermediate interpreter observation, not a
stream output. The exhausted item is different: policy has no permitted attempt
left, so it produces `MAX_RETRIES` and preserves the last failure in its
context.

The last `Ok` proves continuation. Without it, a broken short-circuiting stream
could still satisfy the exhaustion assertions.

Common wrong turns:

- wrapping `async_rag_chunks` in a retry loop repeats source, cleaning, and
  already successful embedding work;
- using `max_attempts=3` while expecting only three retries confuses total
  attempts with additional attempts;
- returning the last `TRANSIENT` after exhaustion contradicts the shipped
  wrapper contract;
- incrementing the cleaning trace inside the embedder stops proving the
  boundary; and
- treating `idempotent=True` as enforcement ignores the external effect's real
  contract.

This proof establishes local repetition, bounded attempts, ordered output, and
continuation for deterministic fakes. It does not establish that a remote
embedding request is idempotent, that retries improve availability, or that a
backoff value is operationally appropriate.

Architecturally, the composition remains:

```text
one clean/chunk pass
        ↓
one bounded worker slot
        ↓
one resilient plan with up to two embedding attempts
        ↓
one visible Result position
```

## Deterministic testing: defend the boundary of a fake timeout

The fake timeout uses `>=`, so reaching exactly `0.050` seconds crosses a
50 ms deadline. Each attempt gets a new timeout context. The clock itself keeps
its current value, but the `after` attempt records its deadline relative to that
current value and completes without advancing it.

One complete implementation is:

```python
def test_embedding_timeout_review() -> None:
    def run_once() -> tuple[list[str], list[str], float]:
        clock = FakeClock()
        attempted: list[str] = []

        def timed_embedder(chunk: ChunkWithoutEmbedding) -> AsyncPlan[Chunk]:
            async def run() -> Result[Chunk, ErrInfo]:
                attempted.append(chunk.doc_id)
                if chunk.doc_id == "deadline":
                    clock.advance_s(0.050)
                return Ok(embed_chunk(chunk))

            return run

        resilient_embedder = resilient_mapper(
            timed_embedder,
            RetryPolicy(max_attempts=1),
            TimeoutPolicy(timeout_ms=50),
            env=make_test_resilience_env(clock=clock),
            timeout_ctx=make_fake_timeout_ctx(clock),
        )
        stream = async_rag_chunks(
            async_gen_from_list(
                [
                    RawDoc("before", "Before", "first", "demo"),
                    RawDoc("deadline", "Deadline", "second", "demo"),
                    RawDoc("after", "After", "third", "demo"),
                ]
            ),
            RagEnv(chunk_size=32),
            clean_doc,
            resilient_embedder,
            BackpressurePolicy(max_concurrent=1, ordered=True),
        )

        async def collect() -> list[Result[Chunk, ErrInfo]]:
            return [item async for item in stream()]

        labels = [
            f"ok:{item.value.doc_id}"
            if isinstance(item, Ok)
            else f"err:{item.error.code}"
            for item in asyncio.run(collect())
        ]
        return labels, attempted, clock.now_s()

    first = run_once()
    second = run_once()

    assert first == second
    assert first == (
        ["ok:before", "err:TIMEOUT", "ok:after"],
        ["before", "deadline", "after"],
        0.050,
    )
```

The deadline-crossing embedder computes an `Ok`, but `FakeTimeout.__aexit__`
observes the crossed deadline and raises before the wrapper can return that
value. The resilience interpreter translates the exception to `TIMEOUT`.

`after` remains visible because timeout is local to one resilient plan. Its
deadline begins at logical time `0.050` and the plan does not advance the clock.

The two required conclusions are:

> The fake proves that the resilience policy translates a logically crossed
> per-attempt deadline into `Err(TIMEOUT)` while preserving later stream work.

> The fake does not prove that a production task receives cancellation at
> 50 ms or that its resources are released correctly.

Moving `clock` outside `run_once` mutates the second execution's initial state.
Even if the labels happened to remain equal, the test would no longer be a
replay from equivalent inputs.

Common wrong turns:

- sharing the clock, attempt list, or stream description across runs;
- injecting `FakeClock` but forgetting to pass its timeout context;
- asserting elapsed wall time in addition to logical time;
- interpreting context-exit checking as task interruption; and
- using this unit test as evidence for provider or resource cancellation.

This proof establishes repeatable policy translation, exact boundary behavior,
and application continuation. A separate controlled integration test using the
real timeout mechanism is needed for cancellation and cleanup.

## Fairness: inspect a weighted prefix

With weights `{0: 1, 1: 2}`, the selector compares emitted-count divided by
weight and breaks equal ratios by lower stream index. Over six selections, the
tags are `A, B, B, A, B, B`: two positions for A and four for B. Both streams
are assumed to remain ready throughout the observation.

Common wrong turns:

- checking only final counts misses a starving prefix;
- adding sleeps changes readiness and tests the event loop instead of policy;
- leaving an infinite iterator open abandons both source iterators;
- claiming six values prove long-run proportionality overstates the example.

The small trace explains the selection rule. Property tests provide broader
evidence across weights and prefix lengths. Rate limiting can then wrap the fair
merge to cap total throughput without changing which ready stream owns each
position.

## Async adapters: preserve the synchronous core

`lift_sync` returns a function that captures arguments in an `AsyncPlan`.
Neither lifting nor applying that function executes the synchronous core. Each
plan call performs the work and catches exceptions at the adapter boundary.

For a positive and a negative input, build both plans first and assert zero
calls. Driving the positive plan produces its original `Ok`; driving the
negative plan increments the trace again and returns `Err(ErrInfo(...))` with
code `UNEXPECTED` and the exception message.

Common wrong turns:

- invoking the core to create a `Result` before lifting loses deferral;
- making the core `async def` introduces the async creep this adapter prevents;
- wrapping the test in `try/except` accepts an escaping exception;
- sending trivial work to an executor adds scheduling overhead without benefit.

The public `lift_sync` import is preserved in later snapshots even though Module
09 consolidates its implementation into `plan.py`. Learner code depends on the
stable capability, not its internal file location.

## Service integrations: release a partial stream

The async context manager appends `enter` only when iteration begins. Each
`anext` advances the response generator once. Calling `aclose` on the outer
iterator unwinds `async_gen_using`, which exits the context manager and appends
`exit`.

For two requested values, the expected trace is therefore `enter`, `pull:0`,
`pull:1`, `exit`. No later pull is permitted because downstream demand ended.

Common wrong turns:

- opening the session when constructing the description performs an eager
  external effect;
- consuming to a list defeats the partial-demand proof;
- omitting `aclose` delegates correctness to garbage collection;
- creating a fresh long-lived HTTP client per item confuses shell and stream
  ownership.

The fake records the resource protocol directly. Provider-specific status
mapping and transport behavior remain the responsibility of focused adapter
integration tests.

## Async chunking: preserve values around errors

With `max_units=1`, each successful integer forms a singleton batch. If the
source is successes 1 and 2, the error, then successes 3 and 4, the output is
`Ok([1])`, `Ok([2])`, `Err(failure)`, `Ok([3])`, `Ok([4])`.

The error is yielded through the existing `Result` channel. Because
`flush_on_err=True`, any non-empty buffer must be emitted before the error.
Afterward, normal chunk accumulation resumes; the stream does not short-circuit.

Common wrong turns:

- wrapping the error in `Ok([error])` changes the element type and semantics;
- stopping after the error loses valid later values;
- ignoring the partial buffer loses valid earlier values;
- using real time adds no evidence when `max_delay_ms=0`.

The full sequence demonstrates order and completeness for this failure route.
Separate property tests generalize those laws over input lists, batch sizes, and
logical-time schedules.

## Pipeline laws: generalize map composition

The left description applies `str` to each success and then applies `len`. The
right description applies their composition,
`lambda value: len(str(value))`, once. Both preserve the same stream order,
cardinality, and `Result` structure.

The empty generated list matters: both descriptions must produce an empty
result without attempting either function. Signed and multi-digit integers
exercise lengths that a single positive example would miss.

Common wrong turns:

- generating separate inputs for the two sides invalidates the comparison;
- extracting only success values hides differences in error propagation;
- using an effectful mapping function makes replay order observable and leaves
  the pure composition law's preconditions;
- testing one literal list provides an example, not broad evidence.

This local law supports refactoring adjacent pure maps into a composed map.
Operational claims such as no duplicate external writes still require stable
keys, idempotent adapters, deterministic schedules, and their own properties.

## Cumulative lab: review the FuncPipe async indexing policy

Start with the value flow, not the scheduler. Filtering is the only event that
deliberately produces no stream position. A source failure is already a
`Result`, validation translates an exception into a `Result`, and the mapper
returns its embedding failure as a `Result`. Ordered coordination must therefore
preserve all three errors between the two successful chunks.

| Input event | Cleaner called? | Embedder called? | Output position |
| --- | --- | --- | --- |
| valid before | yes | yes | `ok:before` |
| filtered document | no | no | none |
| source `Err` | no | no | `err:SOURCE` |
| validation failure | yes | no | `err:UNEXPECTED` |
| embedding `Err` | yes | yes | `err:EMBED` |
| valid after | yes | yes | `ok:after` |

One complete proof is:

```python
def test_async_indexing_policy_review() -> None:
    source_failure = ErrInfo(code="SOURCE", msg="unreadable row")

    async def source_items() -> AsyncIterator[Result[RawDoc, ErrInfo]]:
        yield Ok(RawDoc("before", "Before", "valid", "keep"))
        yield Ok(RawDoc("filtered", "Filtered", "skip me", "skip"))
        yield Err(source_failure)
        yield Ok(RawDoc("invalid", "Invalid", "reject", "keep"))
        yield Ok(RawDoc("embed-fail", "Embed fail", "valid", "keep"))
        yield Ok(RawDoc("after", "After", "still valid", "keep"))

    cleaned: list[str] = []

    def clean_or_reject(doc: RawDoc) -> CleanDoc:
        cleaned.append(doc.doc_id)
        if doc.doc_id == "invalid":
            raise ValueError("document failed validation")
        return clean_doc(doc)

    active = 0
    maximum_active = 0
    embedded: list[str] = []

    def embed_later(chunk: ChunkWithoutEmbedding) -> AsyncPlan[Chunk]:
        async def run() -> Result[Chunk, ErrInfo]:
            nonlocal active, maximum_active
            embedded.append(chunk.doc_id)
            active += 1
            maximum_active = max(maximum_active, active)
            await asyncio.sleep(0)
            active -= 1
            if chunk.doc_id == "embed-fail":
                return Err(ErrInfo(code="EMBED", msg="provider rejected chunk"))
            return Ok(embed_chunk(chunk))

        return run

    stream = async_rag_chunks(
        source_items,
        RagEnv(chunk_size=32),
        clean_or_reject,
        embed_later,
        BackpressurePolicy(max_concurrent=2, ordered=True),
        keep=lambda doc: doc.categories != "skip",
    )

    async def collect() -> list[Result[Chunk, ErrInfo]]:
        return [item async for item in stream()]

    results = asyncio.run(collect())
    labels = [
        f"ok:{item.value.doc_id}"
        if isinstance(item, Ok)
        else f"err:{item.error.code}"
        for item in results
    ]

    assert labels == [
        "ok:before",
        "err:SOURCE",
        "err:UNEXPECTED",
        "err:EMBED",
        "ok:after",
    ]
    assert maximum_active == 2
    assert cleaned == ["before", "invalid", "embed-fail", "after"]
    assert embedded == ["before", "embed-fail", "after"]
```

The three trace assertions divide ownership clearly. `cleaned` proves that the
filter acts before the synchronous core. `embedded` proves that source and
validation failures bypass scheduling. `maximum_active` proves that the
application actually exercises the declared concurrency ceiling, rather than
merely constructing a policy object.

The output assertion is the continuity proof. In ordered mode, every emitted
`Result` retains the source-relative position it acquired before or during
embedding. With `ordered=False`, successes and embedding failures may be
observed in completion order; reviewers would then need stable coordinates to
relate each result to its input instead of reading that relationship directly
from the sequence.

Common wrong turns:

- making the filtered document return an `Err` changes a selection rule into a
  validation failure;
- catching errors around collection hides the typed failure channel;
- asserting only `maximum_active <= 2` can pass even if no overlap occurs;
- using a real embedding service turns a coordination proof into an integration
  test; and
- duplicating cleaning or chunking inside the fake embedder stops proving that
  the synchronous core remains authoritative.

This proof establishes deferral, filtering order, bounded overlap, ordered
continuity, and typed failure preservation for this controlled application
path. It does not establish provider rate limits, network cancellation,
retry safety, durable writes, or semantic embedding quality.
