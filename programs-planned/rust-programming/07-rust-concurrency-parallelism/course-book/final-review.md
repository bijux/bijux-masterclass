# Final review — Rust Concurrency and Parallelism

This review is closed-book until the final comparison. It tests whether you can reason about unfamiliar concurrency rather than repeat the architecture of BatchWeave.

## Part 1 — Model reconstruction

1. Define data race, race condition, deadlock, starvation, and nondeterminism without using any library type names.
2. Explain `Send` and `Sync` through ownership and shared references. Give one type that is neither and one synchronized alternative.
3. Draw the lifetime boundary created by `thread::scope` and explain why it permits borrowed captures without turning them into `'static` references.
4. State the invariant protected by a mutex in one of your labs. Explain why protecting “the data” is too vague.
5. Write the condition-variable loop from memory and explain every step.
6. Define a bounded channel protocol with normal completion, receiver loss, cancellation, and worker panic.
7. Draw a wait-for graph for two transfers that lock accounts in opposite orders.
8. Derive one release/acquire publication relation. Name the non-atomic writes it publishes.
9. Explain why a compare-exchange loop may retry even when no other thread changed the value.
10. State the safety argument for one slot in the SPSC ring.
11. State the algebraic requirements of a parallel reduction.
12. Explain why completion order and output order are separate product choices.

## Part 2 — Unseen diagnosis

You receive a service with these properties:

- requests enter an unbounded channel;
- eight detached workers share an `Arc<Mutex<HashMap<...>>>`;
- each worker holds the mutex while performing file I/O;
- a shutdown flag uses `Relaxed` loads and stores;
- the main thread returns after sending a stop message to only one worker;
- reports are printed as workers finish;
- tests use sleeps and assert that the last line belongs to the final request.

Produce:

1. an ownership and join map;
2. a capacity and backpressure analysis;
3. the protected invariant and guard-scope repair;
4. a shutdown protocol for all workers;
5. an ordering argument for the flag or a reason to remove it;
6. a deterministic rendering design;
7. tests that assert protocol events instead of timing.

## Part 3 — Independent construction

Build a bounded concurrent directory verifier. It accepts a list of paths, a worker count, and a queue capacity. Each worker computes a byte count and FNV-1a checksum for one file. Requirements:

- no shell or async runtime;
- every submitted path has exactly one final outcome;
- the queue is bounded;
- every worker is joined;
- cancellation stops new file work but still terminates all workers;
- a worker panic becomes a typed outcome;
- final output follows input order;
- progress counters are monotonic and documented as approximate or snapshot-consistent;
- tests do not depend on sleeps for correctness;
- malformed paths and I/O failures do not poison unrelated results.

Then add one cross-cutting feature: a maximum total byte budget. Decide whether the budget is reserved before reading, charged after reading, or enforced through another mechanism. Explain races around the boundary and test exact-limit behavior.

## Part 4 — Architecture defense

Defend these decisions orally or in writing:

- Why is the work queue blocking rather than lock-free?
- Why are results sent rather than written under one shared lock?
- Why is output reordered after execution?
- Which atomics use `Relaxed`, and why is that sufficient?
- Which cancellation observation must synchronize other memory, if any?
- What happens if a worker panics while holding a lock?
- What is bounded: queued jobs, active jobs, retained results, memory, or all of them?
- Where would Rayon simplify the system, and where would it hide required lifecycle control?
- Which claim cannot be proven by tests alone?

## Passing standard

A passing result includes working code and a causal model. You have not passed if your explanation relies on “Rust makes it safe,” “SeqCst is safest,” “channels prevent races,” or “Rayon handles everything.” Those phrases omit the product-level obligations this course exists to teach.

[Return to the course overview](index.md) · [Open BatchWeave](capstone.md)
