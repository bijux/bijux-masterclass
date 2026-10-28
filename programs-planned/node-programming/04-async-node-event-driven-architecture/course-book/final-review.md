# Course 4 Final Review

Complete this review without the solution set. Use schedule diagrams, ownership trees, state machines, and small code fragments. A correct answer names the authority responsible for each fact and distinguishes guaranteed behavior from observed timing.

## Scenario 1 — Responsive import

A CLI reads a large JSON file asynchronously, parses it, validates 800,000 records, and writes an audit record with `void writeAudit(...)`.

1. Mark host waits, synchronous regions, and suspension points.
2. Explain why the command can freeze timers despite using promises.
3. Design a cooperative Course 4 repair and state when Course 5 streaming or Course 8 workers would be better.
4. Give the audit write an owner and shutdown obligation.

## Scenario 2 — First successful replica

A client starts three replicas and uses `Promise.any`.

5. What does the combinator prove?
6. What continues after it fulfills?
7. Design cancellation and complete joining of losers.
8. Explain the ambiguous-commit problem when replicas perform an effect rather than a read.

## Scenario 3 — Deadline tree

A command has a two-second budget and three nested helpers, each with a one-second timeout.

9. Show how relative timeouts inflate the total.
10. Derive one monotonic deadline and child budgets.
11. Preserve user abort, shutdown, fail-fast, and deadline causes.
12. Identify cleanup that must continue after the user-visible deadline.

## Scenario 4 — Event observer failure

A scheduler emits mutable task objects. One listener mutates them, another is async and rejects, and a third retains a large request body.

13. Identify authority, error, and retention defects.
14. Design immutable typed events and subscription disposal.
15. State the synchronous reentrancy policy.
16. Explain when an owned queue is required instead of an async listener.

## Scenario 5 — Time-dependent poller

A poller uses `setInterval`, overlaps slow attempts, and tests with real 20 ms sleeps.

17. Replace it with one absolute deadline and injected clock.
18. Define behavior when an attempt lasts longer than the interval.
19. Test the exact deadline and abort boundary deterministically.
20. Explain `ref` and `unref` in process-liveness terms.

## Scenario 6 — Event-to-iterator bridge

An EventEmitter feeds an unbounded array consumed through `for await`.

21. Explain why this is not backpressure.
22. Define a finite queue and overflow policy.
23. Specify close, failure, abort, and early-return behavior.
24. Distinguish single-consumer and broadcast semantics.

## Scenario 7 — Ambient context

A repository reads tenant authorization and request ID from AsyncLocalStorage.

25. Separate diagnostic correlation from security authority.
26. Explain resource-creation propagation and retention.
27. Design optional diagnostics-channel publication.
28. Prove concurrent context isolation.

## Scenario 8 — Supervised batch

A batch creates every promise before acquiring a semaphore and returns on first rejection.

29. Explain why active work is not bounded.
30. Implement lazy admission and complete terminal accounting.
31. Compare continue and fail-fast policies.
32. Preserve source-ordered reporting under reverse completion.

## Scenario 9 — Process shutdown

On SIGTERM, a service calls `process.exit(0)` while two tasks, one audit writer, and one timer remain active.

33. Draw the lifecycle state machine.
34. Give an ordered quiesce, drain, force, cleanup, and join plan under one deadline.
35. Explain startup rollback.
36. Decide exit status after cleanup failure.

## Scenario 10 — TaskHarbor change

Add task priority and then a second feature: `maxAttempts` for retryable built-in tasks.

37. Map both features through syntax, validation, trusted model, scheduler, time budget, events, rendering, tests, and compatibility.
38. Explain why retries must remain under one task deadline.
39. State which failures are retryable and how repeated effects remain safe.
40. Prove dependencies, concurrency, terminal accounting, and final source order still hold.

## Independent construction

Build a bounded notification campaign runner. Campaigns contain preparation, recipient delivery, and audit tasks. Recipient failure does not stop independent recipients. Shutdown stops new campaign admission, requests cancellation, joins accepted work, and returns one deterministic terminal record per recipient. Use typed events and correlation context, but keep campaign state authoritative outside both.

## Oral defense

Defend the construction in fifteen minutes. Your explanation must cover promise ownership, queue bounds, partial orders, cancellation limits, timer cleanup, event reentrancy, context lifetime, failure policy, signal ownership, and schedule-independent output.
