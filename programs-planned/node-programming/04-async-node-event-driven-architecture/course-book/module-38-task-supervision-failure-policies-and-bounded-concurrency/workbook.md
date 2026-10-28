# Module 38 Workbook — Supervision and Bounded Concurrency

## A. Detect false bounds

1. Explain why `inputs.map(run)` followed by a semaphore does not bound starts.
2. Draw the difference between queued source values, lazy producers, active promises, and completed outcomes.
3. State which collections require explicit bounds in a long-lived service.

## B. Compare policies

Four tasks are accepted. Two run. The first fails while the second is waiting on I/O.

4. Derive terminal behavior in continue mode.
5. Derive terminal behavior in fail-fast mode.
6. Explain why returning immediately on first rejection violates task ownership.
7. Decide how domain failure, task panic-like rejection, timeout, and parent cancellation are classified.

## C. Prove accounting

8. Implement an indexed outcome array without sparse-array iteration bugs.
9. Assert the terminal accounting equation after join.
10. Reject duplicate or missing source indices.
11. Reconstruct the final report in source order despite reverse completion.

## D. Construct a supervised runner

Accept lazy producers, finite concurrency, signal, and policy. Start only when a slot exists. Capture synchronous throw and rejection. Stop admission under fail-fast, signal running tasks, join them, and assign terminal outcomes to unstarted inputs.

## E. Independent laboratory

Complete [Supervised Task Group](../../labs/module-38-supervised-task-group/README.md). Test concurrency 1 and 3, pre-abort, reverse completion, synchronous throw, asynchronous rejection, fail-fast with running siblings, and repeated invocation with no leaked state.

## F. TaskHarbor transfer

Schedule only ready dependency nodes, sorted by priority then source index. Bound active tasks. Continue or fail fast according to run policy. Preserve one outcome per manifest task.

## G. Unseen transfer

Design a bounded test runner where some tests have exclusive resource groups. Explain how ordinary concurrency slots interact with group locks and how fail-fast accounts for not-yet-started tests.

## I. Fairness policy

A long-lived scheduler receives high-priority work continuously. Show how strict priority starves low priority despite finite concurrency. Compare aging, weighted round robin, and per-priority quotas. Explain why TaskHarbor’s finite-batch policy is simpler.

## J. Permit lifetime

A task uses a permit, performs work, then asynchronously flushes cleanup. Decide exactly when the permit is released. Write a failure matrix for synchronous throw, rejection, cancellation, and cleanup failure.

## K. Live versus authoritative state

Design metrics for accepted, running, terminal, cancelled, and blocked tasks. Then show why the final report must be reconstructed from terminal outcomes rather than the last observed counter values.

## L. Capacity and terminal-accounting proof

Given 1,000 lazy tasks, a queue bound of 20, and an active bound of 5, calculate the maximum number of retained task payloads under your proposed admission policy. Contrast it with code that first maps all tasks to promises and only then acquires permits.

For fail-fast mode, enumerate the legal terminal categories for work that is queued, starting, running, cancellation-aware, and cancellation-insensitive at the decisive failure instant. Prove that the final table contains one outcome per accepted index.

## M. Supervisor starvation analysis

A supervisor always selects high-priority work and receives a continuous high-priority stream. Show how low-priority tasks can remain accepted but never start. Design one fairness policy—aging, weighted round-robin, or bounded consecutive high-priority selections—and explain its effect on determinism and capacity.

Then model shutdown while admission is blocked on a full queue. State how blocked submitters are released, which proposals were committed, and how the join result distinguishes rejected-before-commit from cancelled-after-commit.

## N. Queue ownership review

A caller times out while waiting for admission. Determine whether its task was never accepted, accepted but queued, or already running. Design acknowledgements that let the caller distinguish these states. Explain how each state contributes to retained memory and final accounting.

Include one adversarial case in which cancellation and admission become ready together.

## H. Defense

Explain structured concurrency as an ownership discipline, distinguish active-work capacity from input-buffer capacity, and show why live counters are not the final authority.
