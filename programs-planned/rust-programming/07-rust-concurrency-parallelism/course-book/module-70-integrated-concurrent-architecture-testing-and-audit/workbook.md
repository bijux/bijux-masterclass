# Workbook — Module 70: Integrated Concurrent Architecture, Testing, and Audit

[Return to the chapter](index.md) · [Open the BatchWeave engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze predictions, protocol diagrams, and invariants before compiling. Concurrency is unusually forgiving of explanations written after observing one successful run; that is exactly why the reasoning record must come first.

## Part 1 — Predict

### Prediction 1

Final completion is decided when `completed + failed == submitted` in relaxed metrics. Predict authority.

Record: **metric coherence and final source of truth**.

### Prediction 2

A worker panics after incrementing started but before sending an outcome. Predict final reconciliation.

Record: **instrumentation versus identity accounting**.

### Prediction 3

Fail-fast closes the queue while submission is blocked. Predict ownership of the current job and later manifest jobs.

Record: **unsent and unsubmitted classification**.

### Prediction 4

Reporting begins before all workers join because every expected result message arrived. Predict remaining lifecycle risk.

Record: **join obligation and hidden panic**.

### Prediction 5

A result vector is sorted by nonunique job name. Predict deterministic but incorrect identity association.

Record: **stable identity requirement**.

### Prediction 6

Rayon report reduction concatenates diagnostics in merge order. Predict output stability.

Record: **reduction law and normalization**.

### Prediction 7

Queue capacity is bounded but each job payload is unlimited. Predict the resource claim.

Record: **multi-dimensional bound**.

### Prediction 8

A new retry feature resubmits jobs without changing exactly-one-outcome invariant. Predict model conflict.

Record: **attempt identity versus job terminal identity**.

## Part 2 — Diagnose and repair

Review a batch engine that starts reporting after receiving N messages, does not join workers, uses live atomics as final counts, sorts outcomes by display name, keeps an unbounded payload in each bounded queue slot, catches every panic around the whole worker loop, and uses Rayon closures to print diagnostics directly.

Produce all six ledgers and mark every contradiction. Repair authority, identity, resource limits, panic boundaries, join order, and report effects. Then add one test per repaired invariant using causal coordination or a sequential oracle.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- increasing timeouts until tests stop hanging;
- calling live metrics final because they usually match;
- receiving the expected count without joining workers;
- sorting by a display field that is not stable unique identity;
- bounding queue slots while leaving payload or accepted input unbounded;
- adding retries without distinguishing attempts from one job outcome;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Write BatchWeave’s six ledgers.

Required evidence: Every row must name the owner, synchronization edge, wait dependency, failure, deterministic projection, and resource maximum.

### Construction 2

Prove exactly-one terminal outcome by case analysis.

Required evidence: Cover successful push, failed push on close, queued cancellation, active domain error, active panic, result-send failure, and worker infrastructure loss.

### Construction 3

Design deterministic rendering.

Required evidence: Specify source ordering, status ordering, key ordering, diagnostic tie-breaking, and stable exit policy.

### Construction 4

Replace a sleep-based blocked-queue test with a causal protocol.

Required evidence: Use handshakes to establish preconditions and retain timeout only as a harness guard.

### Construction 5

Impact-analyze a retry feature.

Required evidence: Separate job identity from attempt identity, bound attempts, update cancellation, metrics, output, and final invariant.

## Part 4 — Independent laboratory

Build [Concurrent Verifier](../../labs/module-10-concurrent-verifier/README.md) from the starter. Before opening the solution, produce:

- all six architecture ledgers;
- bounded worker and queue configuration;
- one indexed terminal result per artifact;
- panic and cancellation tests with complete joining;
- deterministic report equality across worker counts and schedules;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

## Part 5 — Capstone transfer

Complete BatchWeave as a library and CLI. Implement manifest parsing, queue, workers, operations, result protocol, cancellation, metrics, Rayon reporting, deterministic rendering, and exit status. Add integration tests for zero jobs, capacity one, skewed duration, domain failure under continue and fail-fast, job panic, closed push, worker join, duplicate result rejection, and stable output across worker counts.

Required capstone evidence:

- complete ownership, synchronization, liveness, failure, determinism, and resource ledgers;
- a termination proof for every CLI path;
- a sequential report oracle and deterministic-output tests;
- a final claim ledger separating guarantees from unmeasured performance hypotheses;
- an independent feature change with updated code, tests, ledgers, and documentation;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What are the six architecture ledgers and why must they agree?
2. How is exactly-one outcome established for jobs never pushed, queued, active, or panicked?
3. Why do result count, sender disconnect, and joins provide different evidence?
4. How is deterministic output built without deterministic scheduling?
5. Which concurrency and performance claims remain deliberately open after Course 7?

### Independent transfer

Add bounded retries for domain failures to BatchWeave. Each job may have at most three attempts with deterministic attempt numbering. Update the manifest model if policy is configurable, queue capacity reasoning, cancellation checkpoints, result messages, live metrics, final outcome model, report ordering, and tests. Preserve exactly one final job outcome while retaining a complete attempt history. Defend why retries do not duplicate irreversible effects.
