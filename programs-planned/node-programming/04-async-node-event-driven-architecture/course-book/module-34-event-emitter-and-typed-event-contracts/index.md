# Module 34 — EventEmitter and Typed Event Contracts

> **Question:** How can events expose meaningful observations without becoming an untyped second state machine or a source of listener leaks and hidden failures?

## Why this comes now

Module 33 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- explain EventEmitter synchronous delivery and listener order;
- distinguish commands, state transitions, results, and observational events;
- model event names and argument tuples with TypeScript generics;
- handle the special error event and async-listener rejection policy deliberately;
- return explicit subscription disposers and prevent listener retention;
- use once and async event iteration with cancellation and cleanup;

## 1. EventEmitter delivery is synchronous

`EventEmitter.emit` calls registered listeners synchronously in registration order unless listeners themselves schedule later work. The emitter does not await returned promises. The emitting function therefore does not finish until every synchronous listener returns, and one throwing listener can interrupt the remaining delivery unless the emitter or caller catches it.

This surprises developers who equate “event-driven” with “asynchronous.” Events describe a communication style, not a scheduling guarantee. Synchronous delivery can be useful: an observer sees the transition before the command returns. It can also create reentrancy. A listener may call back into the emitter while the original emission is still on the stack.

Define whether reentrancy is permitted. If not, publish an immutable event after the authoritative transition and keep listener code unable to mutate internal state. Do not add `setImmediate` casually to “fix” reentrancy; that changes ordering and failure propagation and must be a deliberate protocol.

## 2. Events should report state, not secretly own it

A command asks the system to do something. A state transition changes authoritative data. A result tells the caller what happened. An event reports a fact that observers may care about. Collapsing these concepts produces fragile systems where the only record of state is that some listener probably ran.

TaskHarbor’s scheduler owns task state. After it changes a task from ready to running, it emits `taskStarted`. If no listener exists, the task is still running. If a metrics listener fails, that failure should not silently revert the scheduler state. The event is observation, not the transaction log.

Events that are required for correctness need stronger delivery and acknowledgement semantics than a local EventEmitter. Those concerns belong to messaging systems later in the program. Course 4 uses events for in-process observation with explicit synchronous semantics.

## 3. Typed event maps preserve argument relationships

A useful TypeScript wrapper maps each event name to one tuple of arguments:

```ts
interface HarborEvents {
  taskStarted: readonly [taskId: string, index: number];
  taskSucceeded: readonly [taskId: string, value: string];
  taskFailed: readonly [taskId: string, error: unknown];
}
```

The listener type for key `K` becomes `(...args: HarborEvents[K]) => void`. This preserves name-to-payload relationships and rejects misspelled names or incorrect listener parameters. The wrapper should not expose the raw emitter where callers can bypass the map.

Type safety does not validate runtime values from an untrusted plugin. It only connects code compiled under the same declarations. When events cross a package or process boundary, runtime validation remains necessary.

## 4. The error event is exceptional

Node gives the string event name `'error'` special behavior. Emitting an error without a listener throws and can terminate the process. That convention is useful for stream-like and resource-like objects, but it should not be copied into every domain event hub without understanding the consequence.

If a public EventEmitter can emit `'error'`, document who installs the listener and what an error means. `errorMonitor` can observe errors without consuming the fatal behavior. `captureRejections` can route rejected promises returned by async listeners, but it does not make event delivery awaitable and it introduces another error path. Node’s documentation specifically warns against async `'error'` handlers because rejection there can loop.

A typed domain hub may instead represent task failure as an ordinary `taskFailed` event and reserve `'error'` for emitter infrastructure failure. The names should reflect the distinction.

## 5. Subscription ownership prevents leaks

Every listener creates a lifetime relation: the emitter retains the listener, and the listener’s closure retains its captured values. If the subscriber’s lifetime ends without removal, memory and behavior remain. Max-listener warnings are a diagnostic, not a garbage collector.

Return an idempotent disposer from every subscription method. Use `once` for one terminal observation. When converting an event to a promise, remove the event listener and abort listener on every terminal path. When exposing an async iterator over events, define what early `break` does and whether buffered events are discarded.

Subscription ownership should be visible in code:

```ts
const unsubscribe = hub.on('taskStarted', onStart);
try {
  await run();
} finally {
  unsubscribe();
}
```

Course 2’s deterministic-disposal discipline remains active here.

## 6. Async listeners need an explicit policy

Because `emit` ignores returned promises, an `async` listener begins work that the emitter does not own. Rejection can become unhandled unless `captureRejections` or local handling is configured. Completion order becomes detached from emission order.

Use synchronous listeners for quick observation, or wrap async work in a component that owns it. An event consumer that must persist every audit record may need a bounded queue and a joined worker, not an async listener attached directly to the emitter. If emission itself must await all listeners, design a different abstraction—perhaps an explicit `publish` method returning a promise—rather than pretending EventEmitter does that.

The event contract should state whether listener failures are isolated, propagated, logged, or fatal. “Listeners should not throw” is not a policy unless the boundary enforces or tests it.

## 7. Waiting for one event and iterating many events

Node’s events utilities can turn one event into a promise or a sequence into an async iterator. Those adapters are useful when cancellation and cleanup are included. A one-shot wait should reject on abort and remove all listeners. An async event sequence needs bounded buffering or a clearly documented risk when producers can outrun consumers.

EventEmitter is push-based: the producer emits whether the consumer is ready. Async iteration is pull-based at the consumption surface, but an adapter may still buffer pushed events internally. Module 36 builds a bounded bridge and makes that hidden queue explicit.

## 8. What this changes in TaskHarbor

TaskHarbor gains a typed `HarborEventHub`. Scheduler transitions happen first; immutable observations are emitted afterward. The CLI subscribes to render optional live progress. Tests subscribe to assert event order and then dispose. The final report comes from scheduler outcomes, not from replaying the event list.

The capstone must prove that removing all listeners does not change task correctness, that listener registration order is respected, and that a throwing observer cannot corrupt the scheduler’s authoritative state.

## 9. Deep case study: the observer that mutates authority

A scheduler emits a mutable task object after setting its status to running. A listener changes the object to failed before the scheduler continues. Another listener sees the mutated value and writes a misleading audit record. The event layer has become a second write authority.

The repair is not merely `Object.freeze` at the emitter boundary. Define an immutable event value containing only observational fields, keep the authoritative task record private, and emit after the state transition. If observers need to request actions, give them an explicit command interface with its own validation. Observation and command are different protocols.

## 10. Reentrancy analysis

Because listener invocation is synchronous, an observer can call back into the component before the original `emit` returns. Mark the component’s reentrancy policy:

- permitted and tested;
- prohibited through a state guard;
- deferred through an explicit queue;
- impossible because observers receive no authority.

Deferring every event with `setImmediate` is not a neutral repair. It changes error propagation, listener order relative to subsequent state changes, and process-liveness behavior.

## 11. Event contract table

For every public event, record event name, payload tuple, emission point, authoritative preceding transition, listener failure policy, buffering policy, and subscription lifetime. If the table cannot identify an authoritative preceding transition, the event may be trying to own state rather than report it.

## 12. Listener-set mutation during emission

Node’s EventEmitter has defined behavior when listeners are added or removed during an emission: the current call operates on its internal listener snapshot in ways that can surprise readers who imagine a live loop over one array. Rather than depending on undocumented details in a custom wrapper, choose and test a policy. A snapshot policy gives every listener present at emission start one opportunity. A live policy reflects removals immediately but is harder to reason about under reentrancy.

For a public typed hub, snapshot delivery is often easier to explain. The hub copies the current listener list, then calls it. Unsubscription affects future emissions. A `once` wrapper removes itself before invoking the user callback so recursive emission cannot call it twice. These details belong in the contract because they change observable behavior.

## 13. Awaitable publication is a different abstraction

Some systems require every subscriber to acknowledge before the command completes. This is not ordinary EventEmitter semantics. An awaitable publisher can accept async listeners and return a promise, but then it must define sequential versus concurrent invocation, failure aggregation, cancellation, timeout, and backpressure. It becomes a supervised fan-out operation.

Do not retrofit this behavior invisibly behind an `emit` method whose users expect synchronous delivery. Name it `publish` or `notifyAndWait`, make its promise ownership obvious, and use the Course 4 supervisor model. A mandatory audit listener is a dependency, not an optional observer.

## 14. Event evolution and compatibility

Typed events are public APIs. Adding an optional event is usually compatible for emitters, but a consumer that claims exhaustive handling may need a nonbreaking extension strategy. Changing payload position, meaning, or emission timing can break code even when TypeScript still compiles. Document whether event order is causal, total, or unspecified among independent operations.

## 15. Event streams, state queries, and command methods are different APIs

A mature event-driven component usually needs three distinct surfaces. A **command** asks the component to attempt a transition. A **query** returns authoritative current state. An **event** reports that a transition or observation already occurred. Collapsing those surfaces creates ambiguity. A listener that must call `getState()` after every event may receive a newer state than the event describes. A query implemented by waiting for the next event can hang when no transition occurs. A command represented as an event leaves authority unclear because any listener might appear able to cause the transition.

For every proposed event, write a four-column contract:

| Question | Example answer |
|---|---|
| What fact has already become true? | task `A` entered `running` at revision 7 |
| Which component was authoritative? | the scheduler, after reserving capacity |
| What immutable data is carried? | task ID, revision, start timestamp |
| What may listeners do? | observe, record, or trigger independent follow-up work |

This contract also exposes payload design errors. Passing a mutable domain object gives listeners accidental write authority. Passing only an ID may force a racy query. Prefer immutable event facts that identify the transition precisely. When payloads are large, include a stable identity and revision plus the small facts required for ordinary observers; document when a separate query is necessary.

## 16. Listener failure, cleanup, and publication ownership

Synchronous `EventEmitter.emit` returns after listeners have been invoked, but it does not define a transaction across listener effects. If the third listener throws, earlier listeners have already run. Catching that exception and continuing can conceal an observer defect; letting it escape can make an observational concern fail the command path. The component must choose deliberately.

A useful default for domain events is: commit authoritative state first, publish an immutable fact second, and isolate observer failure through an explicit reporting policy. Critical in-process hooks that must participate in success should not be disguised as ordinary events; model them as awaited collaborators with typed failure. This distinction keeps “notification” from silently becoming “distributed transaction.”

Subscription cleanup is part of the same contract. Returning a disposer from `on` gives ownership a concrete shape. The owner of the subscription stores that disposer and calls it during its own terminal transition. Tests should prove that disposal is idempotent, removed listeners no longer run, and listener counts do not grow across repeated start/stop cycles.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Typed Event Hub](../../labs/module-34-typed-event-hub/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 34 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 35](../module-35-timers-clocks-rate-control-and-deterministic-time/index.md)
