# Module 40 — Integrated Event-Driven Architecture and Independent Change

> **Question:** Can you evolve a complete asynchronous Node.js system while preserving schedule, ownership, cancellation, event, context, boundedness, and shutdown contracts together?

## Why this comes now

Module 39 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- draw an end-to-end async ownership and lifecycle map;
- separate authoritative state from events, diagnostics, and rendered reports;
- validate dependency graphs and produce deterministic source identity;
- combine bounded concurrency, deadlines, cancellation, and blocked dependencies;
- test schedule variation and process shutdown without probabilistic sleeps;
- implement and defend an independent feature across types, runtime, CLI, tests, and compatibility notes;

## 1. Integration begins with authorities

A mature event-driven architecture identifies who owns every decision. The manifest parser owns the transition from unknown JSON to trusted task descriptions. The graph validator owns dependency legality and cycle rejection. The scheduler owns task state and admission. Executors own operation-specific behavior. The EventHub and diagnostic channel observe transitions. The CLI owns process signals, files, and rendering.

If two components can both declare a task complete, the design has competing authorities. If no component owns cancellation cleanup, the design has a gap. Write an authority table before changing code.

## 2. TaskHarbor state model

Each manifest task begins pending. After all dependencies succeed and capacity is available, it becomes running. It reaches exactly one terminal state: succeeded, failed, timed-out, cancelled, or blocked. Blocked means a required dependency did not succeed; it is not a local execution failure. Fail-fast policy may cancel tasks that would otherwise have become ready.

The scheduler records state before emitting the corresponding observation. Final outcome arrays follow manifest order. Live events follow actual transition order. Diagnostic context contains run and task identity but does not authorize transitions.

## 3. Dependency validation precedes execution

The manifest boundary rejects duplicate IDs, unknown dependencies, self-dependencies, and cycles before any executor runs. A deterministic topological analysis reports a stable cycle witness or the set of unresolved tasks. Runtime scheduling then relies on the validated graph rather than repeatedly defending against malformed references.

Validation still has resource bounds: maximum task count, maximum dependency count, identifier length, and payload size. TypeScript cannot prove these properties from JSON. The trusted graph type should be constructed only by the validator.

## 4. Schedule-independent product claims

TaskHarbor does not promise which of two independent jobs finishes first. It promises bounded running count, source-ordered final outcomes, one terminal state per task, no start before dependencies succeed, no new start after fail-fast cancellation, and complete joining before `run` resolves.

Tests vary concurrency and controlled completion order. They assert the invariant set rather than one accidental event trace. Event-order tests focus only on causal relations: started precedes that task’s terminal event; dependency success precedes dependent start; runFinished follows all terminal events.

## 5. Error taxonomy and exit behavior

Manifest syntax, graph validation, task domain failure, timeout, cancellation, observer failure, and internal invariant failure are distinct. The library returns typed aggregate results for expected task outcomes and throws only for configuration or internal execution failures. The CLI maps them to documented exit statuses.

Do not make a failed task throw out of the entire scheduler in continue mode. Do not make malformed input look like a task failure. Error location determines who can repair it.

## 6. Testing the complete system

The evidence stack includes pure graph tests, clock-controlled scheduler tests, EventHub subscription tests, AsyncLocalStorage isolation tests, manifest parsing tests, library integration tests, and real process tests. No single layer proves the others.

Use deferred executors to control completion. Use a manual clock for deadlines. Use temporary directories for manifests. Spawn the CLI for signal and exit-status behavior. After each test, assert that subscriptions and signal handlers return to their baseline counts.

## 7. Independent feature: task priority

The final change adds `priority: low | normal | high` with default `normal`. Priority affects only selection among simultaneously ready tasks. It must not violate dependency order, concurrency bounds, fail-fast cancellation, or source-ordered final reporting.

The change crosses manifest validation, trusted types, scheduler ready-queue policy, event payloads, inspect output, documentation, and tests. Compatibility policy must state that old manifests remain valid and that equal-priority tasks retain source order. A weak implementation sorts the final report by priority or starts a high-priority task before its dependencies; both confuse scheduling policy with identity or legality.

## 8. Mastery standard

You are ready to leave Course 4 when you can inspect an unfamiliar promise-heavy program and answer: which operations have started, who owns them, where they can suspend, how they stop, which queues can grow, which events are observations, how context propagates, what shutdown joins, and which output is deterministic.

The final defense should use concrete invariants and failure paths. “It uses async/await correctly” is not an architectural explanation.

## 9. Authority map for a complete async product

TaskHarbor has several collaborating surfaces, but each fact has one authority:

| Fact | Authority |
|---|---|
| manifest shape | runtime validator |
| dependency legality | graph validator |
| ready/running/terminal state | scheduler |
| task effect | executor |
| cancellation request | run or task controller |
| elapsed time | injected clock |
| live observations | event hub and diagnostics |
| final output order | source-indexed outcome reconstruction |
| process signal ownership | executable boundary |

Most integration defects are authority collisions. An event listener updates scheduler state, a diagnostic context chooses domain behavior, a renderer infers missing outcomes, or the process handler exits before the scheduler joins. The map gives reviewers a direct question: which component was allowed to establish this fact?

## 10. Independent-change impact map

The priority extension looks local but crosses validation, domain types, defaults, inspect output, ready selection, tests, and compatibility. A disciplined change starts with an impact map:

```text
syntax → validator → trusted model → scheduler policy → observations → rendering → tests → compatibility
```

Priority may reorder only simultaneously ready tasks. It cannot bypass dependencies, exceed capacity, or change final source ordering. Equal priorities preserve source order. Old manifests default to normal. This is the sort of cross-layer invariant the final course module must prove.

## 11. Mastery is explanatory compression

A mature explanation does not recite every API. It states the few models that generate the behavior: run-to-completion and queues; owned task trees; cooperative cancellation; synchronous observation; monotonic deadlines; async iterator state; context as diagnostics; finite supervision; lifecycle transitions; and explicit authority. From those models, the reader can predict an unseen variation.

## 12. Temporal invariants across layers

Some invariants are about order rather than shape:

- validation completes before any executor starts;
- state changes before its event is emitted;
- cancellation transition is recorded before dependents are classified;
- all running tasks settle before the run summary is returned;
- final output is rendered only from a complete terminal registry;
- signal listeners are removed after shutdown reaches closed.

TypeScript can encode many shapes but not these temporal relations. Tests need controlled executors, manual clocks, event traces, and process boundaries. A mature architecture names temporal invariants as clearly as data types.

## 13. Change review beyond compilation

A cross-layer feature can compile while breaking semantics. `maxAttempts` may reset a deadline on each attempt, emit duplicate terminal events, or let a dependency observe intermediate failure. A new event may retain large errors. A new CLI option may be parsed but omitted from inspect output and compatibility notes.

Use a change matrix with rows for syntax, validation, domain representation, state transitions, ownership, cancellation, time, observation, persistence if any, rendering, type declarations, tests, and documentation. Mark “not affected” only with a reason.

## 14. Course boundary and next maturity step

TaskHarbor operates on finite in-memory task descriptions and small values. It does not move unbounded byte sequences, coordinate stream backpressure, or model file descriptor lifecycle. Course 5 begins where Course 4 deliberately stops: Node streams, filesystem operations, Buffer ownership, pipeline termination, and bounded data movement. This boundary is part of a coherent program, not missing content.

## 15. The final architecture is a set of cooperating authorities

TaskHarbor is reviewable because no single mechanism owns everything. The manifest codec owns external-data validation. The graph validator owns dependency legality. The scheduler owns readiness, capacity, and terminal state. `AbortSignal` carries cancellation requests. Typed events publish immutable lifecycle facts. `AsyncLocalStorage` carries diagnostic correlation. The process boundary owns signals, output, and exit status. Tests own executable evidence; none of these surfaces should silently become another.

Build an authority map before adding a feature:

| Concern | Single authority | Observable evidence |
|---|---|---|
| task identity and dependency graph | validated manifest | inspection output and graph tests |
| ready-task selection | scheduler | deterministic selection tests |
| maximum running work | supervisor capacity | active-count invariant |
| cancellation request | composed abort signal | cause-aware terminal outcomes |
| terminal result | scheduler outcome table | exactly one result per accepted task |
| diagnostics | event/context adapters | correlation and no-subscriber tests |
| process completion | lifecycle owner | process exit tests |

If two components can author the same state, introduce a command boundary or make one representation derived. If no component owns a terminal path, the architecture leaks work.

## 16. Independent change should be reviewed through impact, not file count

The final priority feature is intentionally cross-cutting. Adding a `priority` field to a TypeScript interface is the smallest part. The manifest validator must reject unknown values and define defaults. The scheduler must select only among ready tasks, preserve dependency legality, and define a deterministic tie-break. Events and reports must expose the chosen policy without making completion order a product guarantee. Persistence or fixtures need a compatibility decision. Tests must cover mixed priorities, equal priorities, dependency blocking, cancellation, and several concurrency widths.

Use an impact matrix with rows for runtime semantics, type surface, external format, scheduling, events, diagnostics, errors, tests, and documentation. For every row, mark **changed**, **unchanged by proof**, or **not applicable**, and justify the mark. This discipline scales to retries, resource classes, task groups, and later worker or network execution. Mastery is not knowing every API; it is being able to predict where a legitimate change must propagate and where it must not.

## 17. Completion standard for the first four Node courses

At this point you should be able to take an untrusted command-line input, validate it into a typed domain model, organize mutable authority behind explicit object and module boundaries, preserve public package contracts, and run asynchronous work with owned promises, bounded concurrency, cancellation, typed observation, deterministic reconstruction, and graceful process termination.

A final defense should explain one complete task from manifest token to process report. Name every state transition, promise owner, cancellation checkpoint, event publication point, context boundary, and cleanup obligation. Then identify one claim that the current course does not establish—such as byte-stream backpressure, worker-thread isolation, distributed commit, or exact production latency—and place it in the correct later course rather than implying that TaskHarbor already solves it.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Event-Driven Job Engine](../../labs/module-40-event-driven-job-engine/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 40 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[TaskHarbor engineering guide](../capstone.md)
