# Module 38 Reasoned Solutions — Supervision and Bounded Concurrency

## A. Real capacity

Calling every producer creates all side effects before a semaphore can help. A bounded runner retains source values or lazy functions and invokes only when `running.size < limit`. This bounds active work. It does not automatically bound the number of waiting source items; a service needs admission limits outside the batch.

## B. Policies

Continue mode records the first failure and keeps independent work eligible. Fail-fast stops new starts, aborts the run signal, joins the already-running sibling, and gives pending inputs explicit cancellation outcomes. Returning at the first rejection leaves resource ownership unresolved. Domain failure, timeout, cancellation, and unexpected rejection can share a terminal union but should remain distinguishable.

## C. Accounting

Initialize outcome storage with actual `undefined` elements rather than sparse holes, because array iteration methods skip holes. Attach source indices before start. On completion, reject duplicates, fill one slot, and after join verify no slot remains undefined. Render by index. The equation accounts for all accepted work even when completion order differs.

## D. Runner

The supervisor owns a running map and one controller linked to the parent. It starts producers lazily, wraps every settlement, and uses `Promise.race` only to discover the next completion—not as lifecycle completion. Fail-fast aborts but keeps looping until running tasks settle and pending inputs are classified.

## E. TaskHarbor and transfer

TaskHarbor adds dependency readiness and priority selection to the same ownership model. A resource-group test runner needs both global concurrency and per-group exclusion. Tests waiting on a group are still admitted inputs and must receive terminal outcomes under fail-fast.

## F. Fairness, permits, and metrics

Strict priority can indefinitely postpone low-priority work in an open system. Aging raises priority with wait time, weighted round robin allocates service shares, and quotas cap one class. TaskHarbor processes a finite manifest, so strict priority plus stable source order terminates; this guarantee should not be copied into a daemon without reconsideration.

A permit represents actual resource occupancy and remains held through required asynchronous cleanup. Wrap acquisition and task execution in one promise with `finally`. Synchronous throw, rejection, and cancellation all reach release. Cleanup failure still releases the permit but surfaces as an infrastructure error according to policy.

Live metrics may briefly disagree with each other and can miss updates if instrumentation fails. The terminal indexed registry is the final authority. Metrics are derived observations and can be checked against the final accounting equation after join.

## G. Capacity and accounting answers

Creating all promises before acquiring permits starts all work and retains all payloads, so active execution may appear bounded while resource creation is not. Store lazy producers, accept at most the documented queue capacity, and start only when an active slot exists. With queue 20 and active 5, at most 25 accepted payloads need be retained inside the supervisor, plus explicitly counted caller-side proposals.

Fail-fast requests cancellation after the decisive failure. Queued tasks become cancelled without starting; starting or running tasks settle according to their actual result and cancellation response. The final authoritative array is indexed by acceptance identity and satisfies `accepted = fulfilled + failed + cancelled + panicked`. Live counters are not a substitute because they may be sampled between transitions.

## H. Fairness and shutdown answers

Strict priority can starve low-priority accepted work. Aging raises effective priority with waiting time; weighted round-robin reserves service shares; a consecutive-selection cap is simpler but coarser. Each policy needs deterministic tie-breaking and tests under continuous arrivals.

A blocked submitter has not committed work until the supervisor accepts and assigns an index. Closing admission rejects those proposals explicitly. Accepted queued tasks receive cancelled terminal outcomes if shutdown prevents start. This distinction preserves the accounting equation and prevents callers from confusing admission failure with execution cancellation.

## I. Admission-state answer

A proposal is uncommitted until the supervisor assigns its stable acceptance identity. Timeout before that point is rejection-before-commit. After assignment but before start it is accepted-and-queued; after producer invocation it is active. Acknowledging the commit point lets callers interpret cancellation and prevents ambiguous terminal accounting.
