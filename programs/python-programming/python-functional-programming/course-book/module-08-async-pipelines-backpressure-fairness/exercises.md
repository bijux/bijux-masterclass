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
