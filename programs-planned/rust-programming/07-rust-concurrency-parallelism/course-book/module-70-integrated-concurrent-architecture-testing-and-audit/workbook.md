# Workbook — Module 70: Integrated Concurrent Architecture, Testing, and Audit

[Chapter](index.md) · [Laboratory](../../labs/module-10-concurrent-verifier/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Integrated Concurrent Architecture, Testing, and Audit** has become a usable model rather than remembered vocabulary. Its governing question is: *How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?* Preserve your first prediction and record decisive facts in a **concurrent architecture dossier**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 69 — Rayon, Work Stealing, and Deterministic Parallelism that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?**
3. Draw the smallest **concurrent architecture dossier** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

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

### Interleaved reasoning pass

1. For **Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the concurrent architecture dossier.
2. For **Maintain ownership, synchronization, liveness, failure, determinism, and resource ledgers together**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the concurrent architecture dossier.
3. For **Prove boundedness for jobs, payloads, queue slots, workers, result messages, report threads, and output storage**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the concurrent architecture dossier.
4. For **Derive exactly one terminal outcome per manifest job under success, domain failure, panic, cancellation, and submission interruption**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the concurrent architecture dossier.

5. Identify one guarantee from an earlier course that a careless implementation of **Integrated Concurrent Architecture, Testing, and Audit** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Concurrent Verifier](../../labs/module-10-concurrent-verifier/README.md) from the starter. Before opening the solution, produce:

- all six architecture ledgers;
- bounded worker and queue configuration;
- one indexed terminal result per artifact;
- panic and cancellation tests with complete joining;
- deterministic report equality across worker counts and schedules;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Concurrent Verifier**, record:

- the public behavior that demonstrates **Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Complete BatchWeave as a library and CLI. Implement manifest parsing, queue, workers, operations, result protocol, cancellation, metrics, Rayon reporting, deterministic rendering, and exit status. Add integration tests for zero jobs, capacity one, skewed duration, domain failure under continue and fail-fast, job panic, closed push, worker join, duplicate result rejection, and stable output across worker counts.

Required capstone evidence:

- complete ownership, synchronization, liveness, failure, determinism, and resource ledgers;
- a termination proof for every CLI path;
- a sequential report oracle and deterministic-output tests;
- a final claim ledger separating guarantees from unmeasured performance hypotheses;
- an independent feature change with updated code, tests, ledgers, and documentation;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 70 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What are the six architecture ledgers and why must they agree?
2. How is exactly-one outcome established for jobs never pushed, queued, active, or panicked?
3. Why do result count, sender disconnect, and joins provide different evidence?
4. How is deterministic output built without deterministic scheduling?
5. Which concurrency and performance claims remain deliberately open after Course 7?

### Independent transfer

Add bounded retries for domain failures to BatchWeave. Each job may have at most three attempts with deterministic attempt numbering. Update the manifest model if policy is configurable, queue capacity reasoning, cancellation checkpoints, result messages, live metrics, final outcome model, report ordering, and tests. Preserve exactly one final job outcome while retaining a complete attempt history. Defend why retries do not duplicate irreversible effects.

### Closed-book defense

In five minutes, answer “How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?” using the **concurrent architecture dossier**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
