# Async Node.js and Event-Driven Architecture

**Course 4 of the Node.js Programming program — Modules 31–40**

Course 4 turns promises from syntax into architecture. It teaches when asynchronous work runs, who owns it, how it stops, what remains after cancellation, how observations are published, where demand accumulates, how diagnostic context propagates, and how a Node.js process proves that every accepted operation is terminal before exit.

The course remains framework-free and standard-library-only. That restriction is pedagogical: event-loop behavior, `AbortSignal`, EventEmitter, timers, AsyncLocalStorage, diagnostics channels, async iteration, and process lifecycle are easier to evaluate when a framework is not silently choosing policies.

## Entry standard

You should already be able to build a strict TypeScript ESM package, validate unknown input, reason about JavaScript object identity and lifecycle, design generic library APIs, inspect declarations, and maintain package exports. Courses 1–3 establish those prerequisites.

## Course promise

After ten dense days, you can:

- predict documented partial orders without relying on incidental traces;
- keep the event loop responsive through bounded synchronous work;
- give every started promise a lifecycle owner;
- compose cancellation, deadlines, and shutdown while preserving cause;
- design typed synchronous event contracts and dispose subscriptions;
- build bounded async iterable bridges with complete terminal semantics;
- use small immutable async context for diagnostics without hiding authority;
- supervise finite task trees under explicit failure policy and capacity;
- implement transactional startup and graceful process shutdown;
- evolve a complete event-driven system through a cross-layer impact map.

## Ten-module path

| Module | Subject | Product proof |
|---:|---|---|
| 31 | Event loop, scheduling, fairness, and blocking | Event Loop Observatory |
| 32 | Promises, async functions, and task ownership | Owned Promise Nursery |
| 33 | Cancellation, abort signals, deadlines, and budgets | Deadline Budget |
| 34 | EventEmitter and typed event contracts | Typed Event Hub |
| 35 | Timers, clocks, rate control, and deterministic time | Deterministic Scheduler |
| 36 | Async iterables, generators, and pull sequences | Bounded Async Queue |
| 37 | Async context, correlation, and diagnostics | Correlation Context |
| 38 | Supervision, failure policies, and bounded concurrency | Supervised Task Group |
| 39 | Process lifecycle and graceful shutdown | Graceful Lifecycle Harness |
| 40 | Integrated event-driven architecture | Event-Driven Job Engine |

## Primary learning surfaces

Start with the [course book](course-book/index.md). Each module contains one authoritative chapter, a workbook, and reasoned solutions. Build the independent laboratory before inspecting `reference/`. Transfer the mechanism into [TaskHarbor](course-book/capstone.md), then complete the [final review](course-book/final-review.md).

The [compiler and runtime investigations](compiler-labs/README.md) separate checker failures from runtime failures. Predict each result before running the investigation suite.

## Course boundaries

This course does not yet teach Node streams, filesystem data pipelines, HTTP servers, databases, worker threads, or production observability systems. It builds the scheduling, ownership, cancellation, and lifecycle models those later courses require.

## Verification

```bash
make verify
```

The compatibility route runs the static course audit, links, TypeScript source policy, 80 investigations, and all 21 executable packages. `make proof` additionally requires the exact pinned Node.js, npm, TypeScript, and MkDocs baseline.
