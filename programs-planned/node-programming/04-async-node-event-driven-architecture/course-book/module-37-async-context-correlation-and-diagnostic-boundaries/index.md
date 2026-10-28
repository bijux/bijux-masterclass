# Module 37 — Async Context, Correlation, and Diagnostic Boundaries

> **Question:** How can diagnostic context follow an asynchronous operation without turning ambient state into hidden domain authority?

## Why this comes now

Module 36 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- distinguish explicit domain parameters from ambient diagnostic context;
- use AsyncLocalStorage run and getStore with nested restoration;
- identify context-loss boundaries and the role of AsyncResource;
- publish optional diagnostic messages through diagnostics_channel;
- prevent context leakage between concurrent operations and tests;
- avoid using correlation context for authorization or core business decisions;

## 1. Context is useful because async call stacks are fragmented

A request, job, or command may cross dozens of promises and callbacks. Passing a correlation ID through every function can pollute domain signatures whose behavior does not depend on that ID. `AsyncLocalStorage` associates a store with one asynchronous execution lineage so diagnostic code can retrieve context without every intermediate function forwarding it.

This resembles thread-local storage conceptually, but the propagation unit is asynchronous execution context rather than an operating-system thread. Concurrent operations on the same JavaScript thread can observe different stores because their callbacks belong to different async lineages.

Use this power narrowly. Correlation, trace identifiers, and diagnostic tags are appropriate. Authorization decisions, tenant ownership, prices, and other domain inputs should remain explicit because hidden ambient dependencies make tests and reuse unsafe.

## 2. Prefer run-scoped context

`AsyncLocalStorage.run(store, callback)` installs a store for the callback and asynchronous work created within it, then restores the previous store when the callback completes. Nested runs naturally restore the parent. `enterWith` mutates the current synchronous context and can unintentionally affect later handlers in the same turn; prefer `run` unless its broader semantics are specifically required.

Make stores immutable. If every callback receives the same mutable object and changes fields, concurrent nested operations can corrupt each other’s diagnostic view. Create a child store with copied parent data and the deliberate additions.

```ts
const storage = new AsyncLocalStorage<Context>();

function withTask<T>(taskId: string, run: () => Promise<T>): Promise<T> {
  const parent = storage.getStore();
  const next = Object.freeze({ ...parent, taskId });
  return storage.run(next, run);
}
```

## 3. Propagation follows resource creation

Context normally propagates through promises, timers, and many Node callbacks created inside the active run. It can be lost when a library captures a callback in one context and invokes it from an unrelated resource, or when custom thenable/event machinery does not preserve the expected lineage.

`AsyncResource` can bind callbacks to an explicit async resource when building such infrastructure. Do not reach for lower-level `async_hooks` tracing as the default; Node’s documentation recommends `AsyncLocalStorage` for context and notes that raw async hooks are difficult and costly. First confirm that context is actually lost, then place the repair at the adapter boundary.

## 4. Context has a lifetime and retention cost

The store remains reachable while associated async resources remain alive. Capturing large request bodies, mutable service objects, or secrets in the store can extend retention and create accidental exposure. Keep stores small, immutable, and diagnostic.

Call `disable()` only when the AsyncLocalStorage instance itself is no longer needed, such as disposing a dynamically created subsystem. Normal request completion does not require disabling a process-wide storage instance. Tests should ensure no store is visible outside `run` and that nested contexts restore correctly.

## 5. diagnostics_channel separates producers from observers

The `node:diagnostics_channel` module provides named channels for optional diagnostic messages. A library can publish structured lifecycle data without hard-coding a logger. Consumers subscribe by channel name. Publishing code can check `hasSubscribers` before constructing expensive payloads.

Channel names and message shapes are public diagnostic contracts. Use namespaced stable names and document fields, units, and timing. Do not publish raw secrets or unbounded payloads. Diagnostic delivery is synchronous; subscribers must remain fast and should not throw into product code.

A diagnostic channel is not durable messaging. Missing subscribers mean the message is intentionally lost.

## 6. Correlation does not establish causality by itself

A shared correlation ID helps group events, but it does not prove that one operation caused another. Reused IDs, retries, fan-out, and parent/child tasks need explicit fields. A useful context can contain `runId`, `taskId`, and optional `parentTaskId`; event records still include their semantic identity directly.

Never authorize an action solely because the current AsyncLocalStorage store says a tenant name. Any callback invoked under the wrong context would become a security defect. Pass authenticated authority explicitly to domain functions and use context only to annotate evidence.

## 7. Testing concurrent context isolation

Start two operations with different stores, suspend both on controlled promises, resume them in the opposite order, and assert each observes its own context before and after suspension. Add a nested child context and verify parent restoration. After all runs finish, `getStore()` outside them should be undefined.

A test that runs contexts sequentially cannot expose cross-operation leakage. Avoid relying on console logs alone; return observed context snapshots and compare exact immutable values.

## 8. What this changes in TaskHarbor

Every TaskHarbor run receives a generated or injected run ID. Each task execution occurs inside a child context containing run ID, task ID, and manifest index. Event records include those identifiers explicitly, while diagnostic subscribers can retrieve the same context without changing executor signatures.

TaskHarbor publishes optional `taskharbor.task.start`, `.end`, and `.error` diagnostic messages. The domain scheduler does not read them back, and disabling every subscriber leaves behavior unchanged.

## 9. Deep case study: context as hidden authorization

A service stores both `requestId` and `currentUser` in AsyncLocalStorage. Deep domain code reads `currentUser` to authorize an operation. A background task inherits the context accidentally and performs work under a user that no longer owns the lifecycle. Diagnostic convenience has become hidden security authority.

Keep ambient context small and observational: correlation IDs, trace IDs, task IDs, and perhaps immutable sampling metadata. Pass security capabilities and domain authority explicitly. AsyncLocalStorage propagation follows async resource creation, not business ownership. A context value surviving across an `await` does not prove the current operation is authorized.

## 10. Propagation boundaries and retention

A context store remains reachable while async resources created inside its scope remain alive. Long timers, leaked promises, or retained callbacks can retain context and captured values. Store compact immutable identifiers, not request bodies or large user objects. Prefer `run`-scoped context over broad `enterWith` mutation because `run` restores the prior store when the callback scope exits.

## 11. Diagnostics as optional observation

A diagnostics channel is named observation infrastructure. Publishing must not mutate product state or become required for correctness. Decide whether subscriber failure propagates, is isolated, or is prevented by subscriber discipline. High-cardinality identifiers belong in event fields, not channel names. Channel names should remain stable and bounded.

## 12. Context snapshots and mutable stores

AsyncLocalStorage returns the store object by reference. If callers mutate one shared store, concurrent descendants may observe changes that resemble context corruption. Freeze or otherwise treat stores as immutable snapshots. Derive a child by creating a new object rather than editing the parent.

This does not mean every diagnostic field should be copied at every function. Establish context at operation boundaries—run, request, task, attempt—and read it only for diagnostics. Domain code that requires a value for correctness should still accept it explicitly.

## 13. Bridging unusual async resources

Most built-in promises, timers, and Node APIs preserve AsyncLocalStorage context. Custom callback integration or third-party native resources may break propagation. The first repair should be to locate the boundary and wrap it using supported context APIs, not to adopt raw `async_hooks` globally. Raw hooks are low level, performance sensitive, and harder to use safely; AsyncLocalStorage is the intended high-level mechanism for context propagation.

Tests for a boundary should create context, cross the suspect resource, and assert the same immutable identifiers afterward. Do not infer propagation from one log line in a larger application.

## 14. Diagnostic cardinality and cost

Context fields often become log or metric dimensions. A run ID is useful in structured events but dangerous as a metric label because it creates unbounded cardinality. Decide separately what is logged, traced, counted, or sampled. Diagnostics are optional observation, yet their allocation and subscriber work still occur on the event loop and can affect performance.

## 15. Context propagation is not context validation

`AsyncLocalStorage` can make a value available through asynchronous descendants, but availability does not establish authenticity, authorization, or freshness. A request ID placed in a store is diagnostic context. A tenant permission copied there becomes dangerous if downstream code treats presence as proof. Security-relevant decisions should receive explicit validated capabilities or arguments whose provenance is reviewable.

Define context fields by purpose:

| Field | Appropriate role | Inappropriate role |
|---|---|---|
| correlation ID | connect logs from one operation | prove caller identity |
| task ID | label diagnostics and metrics | authorize mutation of that task |
| attempt number | explain retry behavior | decide whether retry is legal without explicit policy |
| deadline label | enrich events | replace the actual `AbortSignal` or deadline value |

Store values should normally be immutable snapshots. Mutating one shared object during nested work makes log interpretation schedule-dependent: a child can change what its parent later observes. Create a fresh store for a new logical operation and keep high-cardinality or sensitive payloads out of ambient context.

## 16. Diagnostic publication must remain optional and bounded

`diagnostics_channel` allows instrumented code to publish structured messages without depending on a concrete logger. That decoupling is useful only when publication is cheap, payloads are bounded, and correctness does not depend on a subscriber. The producer should behave correctly when no channel has subscribers and when an observer is slow or defective according to the chosen boundary policy.

Design each channel with a small schema and a timing point. A `task.start` message should be published after capacity is committed and before user work begins. A `task.finish` message should be published after the terminal result is recorded. Publishing “completed” before report construction or cleanup finishes creates a false lifecycle claim. Include stable identifiers, state transitions, and durations; do not include entire input documents or mutable domain objects.

Testing should run multiple concurrent contexts with deliberately interleaved completions, then assert that every event retains the correct correlation identity. Add a no-subscriber test and a subscriber-removal test. If an adapter breaks propagation, isolate it behind one wrapper rather than spreading manual context rebinding throughout the application.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Correlation Context](../../labs/module-37-correlation-context/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 37 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 38](../module-38-task-supervision-failure-policies-and-bounded-concurrency/index.md)
