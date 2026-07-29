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

## Retry policy: inspect attempts and backoff

**Starting context:** read `RetryPolicy`, `ResilienceEnv`, and
`async_with_resilience` in `domain/effects/async_/resilience.py`, then run
`test_retry_policy_records_bounded_attempts_and_backoff`.

**Objective:** make the step fail three times before succeeding, permit four
attempts, and predict the complete zero-jitter backoff trace for a 5 ms base.

**Constraints:**

- inject a recording sleep function;
- use the typed `TRANSIENT` error code;
- assert construction is effect-free;
- do not use elapsed wall-clock time.

**Expected evidence:** four executions produce success after the delays 5, 10,
and 20 ms.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k retry_policy_records_bounded_attempts_and_backoff
```

Earlier contract preserved: only a Module 07 effect known to be idempotent may
be repeated; the retry combinator does not grant idempotency.

## Deterministic testing: replay a timeout boundary

**Starting context:** read `FakeClock`, `FakeTimeout`, and
`make_fake_timeout_ctx`, then run
`test_fake_clock_replays_the_same_timeout_decision`.

**Objective:** set a 100 ms deadline, advance logical time by exactly 100 ms,
and prove two fresh executions make the same timeout decision.

**Constraints:**

- create a fresh clock and plan for each replay;
- inject both the clock and timeout context;
- assert the typed error and logical-time observation;
- do not use real sleep or a timing tolerance.

**Expected evidence:** both executions return the same `TIMEOUT` result at
exactly `0.1` logical seconds.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-08
PYTHONPATH=src pytest -q tests/learning/test_module_08_async.py \
  -k fake_clock_replays_the_same_timeout_decision
```

Earlier contract preserved: the fake interpreter exercises the same typed
Module 07 effect description; it replaces timing capabilities, not domain logic.

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
