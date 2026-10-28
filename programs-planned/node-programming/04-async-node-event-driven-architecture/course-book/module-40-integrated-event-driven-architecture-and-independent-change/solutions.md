# Module 40 Reasoned Solutions — Integrated Event-Driven Architecture

## A. Authority

The validator alone turns unknown input into trusted manifest data. The graph validator owns dependency legality. The scheduler owns state transitions and terminal outcomes. Executors own task-specific effects. Controllers own cancellation requests; signals only expose observation. Events and diagnostics observe committed transitions. The renderer consumes complete indexed outcomes rather than inventing state. `main.ts` alone owns process handlers and exit policy.

## B. Scheduler proof

Validation occurs before task start. Readiness requires every dependency outcome to be succeeded. Indexed terminal storage, initialized without sparse holes, guarantees one slot per manifest task. Every completion writes one unique running index. On abort, pending/ready tasks receive cancellation outcomes and running tasks remain owned until joined. Source-index rendering remains deterministic while live events follow actual transition order.

## C. Error taxonomy

Usage and malformed input are boundary failures and normally exit 2. A completed run containing domain task failures exits 1. A fully successful run exits 0. Observer failure is recorded or isolated according to event policy and must not erase domain outcomes. Cleanup failure can force nonzero exit even after domain success. Typed errors remain intact until the CLI translates them.

## D. Priority

Priority is validated and defaulted at the manifest boundary. The scheduler ranks only entries already marked ready, then uses source index as a stable tie-breaker. Dependencies and concurrency checks occur before start. Final outcomes remain source ordered. Tests include old manifests, equal-priority stability, high-priority task blocked by a dependency, and a lower-priority ready task running while high priority is not yet ready.

## E. Final transfer

The notification runner uses the same models but a different failure policy. Campaign-level ownership joins every recipient task. Events are observational. Shutdown owns admission and one deadline. A complete defense distinguishes async iteration from streams: Course 4 supplies pull protocols and bounded queues, while Course 5 adds Node’s byte/object stream machinery, pipe topology, high-water marks, and filesystem pipelines.

## F. Temporal and change-review solutions

Temporal invariants require runtime evidence. Controlled executor gates prove no start before validation or dependency success. Event traces prove state-before-observation. Indexed terminal tests prove join before summary. A spawned process proves signal and output behavior. Static types support the structures but cannot establish all execution order.

`maxAttempts` can compile yet reset a task’s timeout, publish `taskFailed` on every retry and then `taskSucceeded`, lose attempt identity, retry non-idempotent effects, or classify dependents too early. The impact matrix forces each surface to agree. Intermediate attempt failure is not a terminal task outcome; events need separate retry semantics.

Streams and workers are deferred because they introduce distinct contracts: byte/object chunking, high-water marks, pipe error propagation, file handles, thread transfer, serialization, and CPU parallelism. Course 4 supplies ownership, cancellation, supervision, time, and lifecycle models those later mechanisms require.

## G. Integrated change answers

Priority changes validation, scheduler selection, reports, and tests, but not dependency legality: only ready tasks compete. A deterministic comparator uses priority first and manifest index second. Completion remains schedule-dependent; final rendering remains manifest ordered. Events may include priority as an immutable fact but do not become scheduling authority.

A retry feature needs attempt identity distinct from task identity, one task-level terminal outcome, an overall deadline, cancellation propagation, and an explicit retryability policy. The attempt commit point belongs to the scheduler when it records an accepted start. Process-local retries can avoid duplicate terminal records, but they cannot resolve ambiguous remote commit; network idempotency belongs to Course 8. The impact matrix is complete only when external format, type surface, lifecycle, diagnostics, and compatibility are considered alongside implementation files.

## H. Mastery-defense answers

A complete explanation begins with JSON validation into an exact manifest, graph validation into a dependency-safe model, and scheduler ownership of ready-set selection and capacity. Lazy task producers begin only after commitment. The supervisor owns every promise and records one terminal outcome. Signals compose through an abort tree; immutable events and diagnostic context observe transitions; source-index reconstruction produces stable output; the lifecycle owner joins work before setting exit status.

Worker execution introduces message serialization, worker lifecycle, CPU isolation, crash recovery, and cross-thread cancellation. Persistent resumability adds durable commit points and recovery. Network submission adds framing, admission, ambiguous commit, authentication, and idempotency. Naming those gaps is stronger than claiming the in-process design already solves them.
