# Module 08 Exercises

Work from `capstone/module-reference-states/module-08/`. That directory is the
completed Module 08 application state; Module 07 is the before-state, while
Modules 09 and 10 must retain every behavior proved here.

For each exercise, distinguish constructing a description from driving it. Keep
the existing pure RAG transformations synchronous, express coordination policy as
data, and state which Module 07 effect or resource contract remains true.

## Async plans: prove fresh execution without promising equal effects

**Starting context:** read `async_lift` in
`domain/effects/async_/plan.py` and
`test_async_plan_is_deferred_and_creates_fresh_awaitables`.

**Objective:** replace the fresh-coroutine factory with one cached coroutine
object, predict the second-await failure, and then restore the callable factory.

**Constraints:**

- constructing the plan must not increment the call counter;
- each `plan()` call must return a fresh awaitable;
- do not run `asyncio.run` inside the domain package;
- do not claim repeated effectful executions return equal values.

**Expected evidence:** the call count stays zero until the first await, then
increments once per plan execution.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k async_plan_is_deferred_and_creates_fresh_awaitables
```

Earlier contract preserved: Module 07 still owns effect interpretation at a
shell; Module 08 changes the description type, not that boundary.

## Async generators: observe a partial pull

**Starting context:** read `async_gen_map` in
`domain/effects/async_/stream.py` and
`test_async_stream_pulls_only_what_the_consumer_requests`.

**Objective:** extend the source to four values, consume three mapped results,
close the iterator, and make the pull trace prove the fourth value was never
requested.

**Constraints:**

- do not materialize the entire stream;
- assert both mapped results and the source pull trace;
- explicitly close the partially consumed iterator;
- keep the source a replayable `AsyncGen` thunk.

**Expected evidence:** construction records no pulls, three `anext` calls record
exactly three source values, and the fourth value remains untouched.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k async_stream_pulls_only_what_the_consumer_requests
```

Earlier contract preserved: Module 07 resource ownership still ends at an
interpreter boundary; laziness does not permit abandoning an owned iterator
without closing it.

## Backpressure: expose the bounded window

**Starting context:** read `BackpressurePolicy` and
`async_gen_bounded_map` in `domain/effects/async_/concurrency.py`, then run
`test_bounded_map_caps_in_flight_work_and_preserves_order`.

**Objective:** change the input to six values and the limit to three, then prove
the maximum active worker count is three while ordered output remains aligned
with input.

**Constraints:**

- record active work around the awaited scheduling point;
- assert the maximum rather than a timing threshold;
- keep `ordered=True`;
- do not create tasks outside the combinator.

**Expected evidence:** all six mapped results are ordered and no observation
exceeds the configured three-worker window.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k bounded_map_caps_in_flight_work_and_preserves_order
```

Earlier contract preserved: the Module 07 effect boundary still owns execution;
Module 08 adds an explicit interpreter policy for how much execution may overlap.

## Retry policy: keep repetition at the embedding boundary

**Starting context:** read `resilient_mapper` in
`domain/effects/async_/resilience.py` and the application proofs whose names
contain `retries_only` and `retry_exhaustion`. Draw the application composition
before editing a test:

```text
documents → filter/clean/chunk → bounded map → resilient embedding plan
```

**Objective:** build one three-document stream that distinguishes recovery from
exhaustion:

1. `recovers` returns `TRANSIENT` once and then succeeds;
2. `exhausts` returns `TRANSIENT` on both permitted attempts; and
3. `after` succeeds on its first attempt.

Use one chunk per document and predict the complete output before running:

```text
ok:recovers
err:MAX_RETRIES
ok:after
```

**Constraints:**

- wrap the embedder with `resilient_mapper`;
- use `RetryPolicy(max_attempts=2)`;
- restrict `retriable_codes` to `TRANSIENT`;
- inject zero backoff and zero jitter;
- use `BackpressurePolicy(max_concurrent=1, ordered=True)`;
- record cleaning calls and embedding attempts by document ID;
- do not wrap or replay the complete `async_rag_chunks` stream;
- preserve `clean_doc`, `embed_chunk`, and typed `Result` values; and
- do not add a network client or an exercise-only RAG pipeline.

**Required evidence:**

| Document | Cleaning calls | Embedding attempts | Final position |
| --- | ---: | ---: | --- |
| `recovers` | predict | predict | predict |
| `exhausts` | predict | predict | predict |
| `after` | predict | predict | predict |

Your assertions should prove:

- every document is cleaned exactly once;
- attempts are `{"recovers": 2, "exhausts": 2, "after": 1}`;
- exhaustion contains `ctx["attempts"] == 2`;
- the later success remains visible; and
- constructing the stream records no attempt.

**Review questions:**

1. Why is the recovered `TRANSIENT` absent from output?
2. Why does exhaustion become `MAX_RETRIES` rather than returning the last raw
   `TRANSIENT`?
3. Which work would be duplicated if the complete stream were retried?
4. Why does `idempotent=True` express a claim rather than prove one?
5. How long can one backpressure slot remain occupied?

**Acceptance checks:**

```bash
make capstone-embedding-resilience-proof
make capstone-module-state-proof MODULE=08
```

Earlier contracts preserved:

- Module 03 document and chunk order remains observable;
- Module 04 failures remain typed values;
- Module 07 owns execution and the idempotency argument; and
- bounded Module 08 coordination still owns the concurrency ceiling.

## Deterministic testing: defend the boundary of a fake timeout

**Starting context:** read `FakeClock`, `FakeTimeout`,
`make_fake_timeout_ctx`, and
`test_async_rag_chunks_replays_logical_embedding_timeout`.

**Objective:** extend the application timeout proof to three documents:

1. `before` completes without advancing logical time;
2. `deadline` advances the clock by exactly `0.050` seconds under a 50 ms
   timeout; and
3. `after` completes without advancing logical time.

Run the complete description twice from fresh fixtures and predict:

```text
ok:before
err:TIMEOUT
ok:after
```

**Constraints:**

- create the clock, attempt trace, embedder, resilience environment, timeout
  context, and stream inside `run_once`;
- use `RetryPolicy(max_attempts=1)`;
- pass the same `FakeClock` to the test environment and timeout context;
- use `BackpressurePolicy(max_concurrent=1, ordered=True)`;
- compare the complete result labels, attempt trace, and final logical time;
- use no real delay, timing tolerance, global patch, or shared clock; and
- do not claim that the fake interrupts a running task.

**Required evidence:**

```python
first = run_once()
second = run_once()

assert first == second
assert first == (
    ["ok:before", "err:TIMEOUT", "ok:after"],
    ["before", "deadline", "after"],
    0.050,
)
```

Then write two separate conclusions:

- one sentence stating what the fake proves about policy; and
- one sentence stating what it does not prove about production cancellation.

**Failure experiment:** move the `FakeClock` outside `run_once`. Explain why
the two executions no longer begin from equivalent state, then restore fresh
fixtures.

**Review questions:**

1. Why does equality at the deadline trigger timeout?
2. Why is the successful value computed by the deadline-crossing plan not
   emitted?
3. Why does `after` still receive a fresh per-attempt deadline?
4. Which test would be needed to prove cancellation cleanup?
5. Why would a wall-clock assertion weaken this proof?

**Acceptance checks:**

```bash
make capstone-embedding-resilience-proof
make capstone-module-state-proof MODULE=08
```

Earlier contract preserved: the fake interpreter drives the same Module 07
effect description and the same Module 08 RAG composition. It replaces timing
capabilities only; it does not replace domain logic or resource ownership.

## Fairness: inspect a weighted prefix

**Starting context:** read `FairnessPolicy` and `async_gen_fair_merge` in
`domain/effects/async_/concurrency.py`, then run
`test_weighted_fair_merge_makes_each_share_observable`.

**Objective:** reverse the weights so stream B has weight two, consume six
results, and derive the expected deterministic tag sequence.

**Constraints:**

- use two always-ready replayable streams;
- assert both the exact prefix and each stream's count;
- close the partially consumed merged iterator;
- do not introduce sleeps to influence scheduling.

**Expected evidence:** the weight-two stream receives four of six positions and
the other stream receives two without starvation.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k weighted_fair_merge_makes_each_share_observable
```

Earlier contract preserved: Module 07 still owns each tenant capability and its
resources; fairness only selects among already described streams.

## Async adapters: preserve the synchronous core

**Starting context:** read `lift_sync` in
`domain/effects/async_/lifts.py` and run
`test_sync_lift_defers_work_and_translates_exceptions`.

**Objective:** add a successful input alongside the failing input and prove both
plans remain deferred, with one `Ok` and one normalized `Err`.

**Constraints:**

- leave the core function synchronous;
- construct both plans before driving either;
- assert the call trace after each execution;
- do not catch the core exception in the test.

**Expected evidence:** construction makes zero calls; the first execution returns
the core's `Ok`, and the second returns an `UNEXPECTED` error.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k sync_lift_defers_work_and_translates_exceptions
```

Earlier contract preserved: Module 07 keeps exceptions out of the typed effect
channel; the adapter translates at the boundary instead of changing pure core
signatures.

## Service integrations: release a partial stream

**Starting context:** read `async_gen_using` in
`domain/effects/async_/stream.py` and run
`test_service_stream_releases_resource_after_partial_consumption`.

**Objective:** consume two of four fake service responses, close the iterator,
and prove no third response is pulled before the session exits.

**Constraints:**

- acquire the resource through an async context manager;
- record acquisition, each pull, and release;
- assert construction has an empty trace;
- do not rely on garbage collection for cleanup.

**Expected evidence:** the final trace contains one enter, exactly two pulls,
and one exit in that order.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k service_stream_releases_resource_after_partial_consumption
```

Earlier contract preserved: Module 07 established explicit resource ownership;
the async adapter retains that ownership across suspension and partial demand.

## Async chunking: preserve values around errors

**Starting context:** read `ChunkPolicy` and `async_gen_chunk` in
`domain/effects/async_/stream.py`, then run
`test_chunk_policy_flushes_values_before_an_error`.

**Objective:** add two successful values after the error and set
`max_units=1`; derive the exact sequence of singleton batches and the preserved
error.

**Constraints:**

- retain `flush_on_err=True`;
- use `FakeSleeper`;
- compare the complete `Result` sequence;
- preserve source order.

**Expected evidence:** every successful value appears exactly once in order,
the error appears in its original relative position, and no batch exceeds one
item.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k chunk_policy_flushes_values_before_an_error
```

Earlier contract preserved: Module 07 typed failures remain values in the
effect channel; batching neither raises them nor erases their provenance.

## Pipeline laws: generalize map composition

**Starting context:** read `async_gen_map` and run
`test_async_stream_map_preserves_function_composition`.

**Objective:** replace the arithmetic functions with `str` and `len`, then state
the composed function and retain generated list coverage.

**Constraints:**

- compare complete `Result` sequences;
- include empty lists through the strategy;
- use the same source values for both descriptions;
- keep mapping functions pure.

**Expected evidence:** mapping integers to strings and then lengths equals one
mapping with `lambda value: len(str(value))` for every generated example.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k async_stream_map_preserves_function_composition
```

Earlier contract preserved: Module 07 effect interpretation remains outside
this law; composition equivalence applies to pure transformations of the typed
stream.

## Cumulative lab: review the FuncPipe async indexing policy

**Starting context:** read `rag/async_rag.py` and the four tests whose names
contain `async_rag_chunks`. Work in a learner branch beside the Module 08
learning tests. Do not edit `capstone/_history/`; those worktrees are generated
comparison evidence.

**Objective:** construct one application-level proof that combines filtering,
document validation, a source failure, an embedding failure, and bounded
continuation. Use the proof to defend whether ordered output is part of the
indexing contract.

Use a replayable source with these events in this order:

1. one valid document;
2. one document rejected by the `keep` rule;
3. one `Err` from the source;
4. one document whose cleaner raises `ValueError`;
5. one document whose embedding plan returns `Err`; and
6. one final valid document.

**Constraints:**

- use `async_rag_chunks`, not a parallel exercise-only pipeline;
- use `BackpressurePolicy(max_concurrent=2, ordered=True)`;
- let the fake embedder yield with `asyncio.sleep(0)`, not a wall-clock delay;
- record the maximum number of active embedding calls;
- record which document IDs reach the cleaner and embedder;
- keep failures as `ErrInfo` values;
- prove the rejected document reaches neither cleaning nor embedding;
- prove the source and validation failures never reach embedding;
- prove the final valid document is still emitted; and
- preserve the synchronous `clean_doc` and `embed_chunk` implementations.

**Required evidence:** produce a table before writing assertions:

| Input event | Cleaner called? | Embedder called? | Output position |
| --- | --- | --- | --- |
| valid before | predict | predict | predict |
| filtered document | predict | predict | predict |
| source `Err` | predict | predict | predict |
| validation failure | predict | predict | predict |
| embedding `Err` | predict | predict | predict |
| valid after | predict | predict | predict |

Then make the test prove:

```text
ok:before
err:SOURCE
err:UNEXPECTED
err:EMBED
ok:after
```

Your review note must answer:

1. Why does filtering create no output position?
2. Why do the source and validation failures retain positions?
3. Why is the embedding failure emitted even though the mapper owns the task?
4. What evidence shows the final document was not erased?
5. What would become harder to review with `ordered=False`?

**Acceptance checks:**

```bash
make capstone-async-rag-proof
make capstone-module-state-proof MODULE=08
```

Earlier contracts preserved:

- Module 02 filtering remains a value-level choice;
- Module 03 document/chunk order remains observable;
- Module 04 failures remain typed values;
- Module 07 owns effect interpretation; and
- Module 08 adds bounded coordination without replacing those contracts.
