# Module 34 Reasoned Solutions — EventEmitter and Typed Event Contracts

## A. Synchronous and reentrant delivery

Listeners run synchronously in registration order. When `B` recursively emits, the inner emission completes before outer `B` returns. A throw interrupts the current call unless caught. The exact list of later listeners depends on where the throw occurs. The important model is nested stacks, not a later asynchronous queue.

A component can permit reentrancy and make transitions robust, reject calls while a transition flag is active, queue commands for later processing, or remove observer authority. The chosen policy must be visible in tests.

## B. Authority

If a listener updates the cart total, absence, duplication, or failure of that listener changes domain correctness. The cart transition should update items and total together. The event carries immutable facts derived from the committed state. Metrics failure can be isolated or surfaced as a separate observation failure, but should not silently rewrite committed cart state.

## C. Typed hub

A generic event map links each key to one tuple. `on<K>` accepts `(...args: Events[K]) => void`; `emit<K>` accepts the same tuple. A disposer closes the retention edge. Listener failure policy is explicit. If failures are isolated, continue through a snapshot and return or publish a list of observer errors. Async work requires a separate owned queue or an explicit awaitable publisher because EventEmitter ignores returned promises.

## D. Error event

Unhandled `'error'` is special and may terminate the process. A domain task failure is ordinary product data and should have a domain event name. Rejected async error handlers can recursively trigger error handling under capture policies, so Node warns against that design.

## E. TaskHarbor and transfer

TaskHarbor emits after state mutation, with frozen or immutable payloads. The scheduler record remains authoritative. An async sequence over events requires finite capacity and a terminal close/failure policy. For configuration reload, the active configuration belongs to the reloader, not listeners. A slow mandatory audit consumer needs a bounded joined queue or durable messaging rather than a fire-and-forget async listener.

## F. Listener mutation and publication solutions

Under snapshot delivery, removals and additions do not alter the current copied listener sequence, while future emissions see the change. A correct `once` wrapper unregisters before user code so recursive emission cannot invoke it again. A live policy can skip removed listeners and requires more complicated index handling; either can work if specified.

An awaitable publisher owns subscriber promises. Concurrent validation reduces latency but requires complete settlement and deterministic error ordering. Sequential validation establishes a clear first-failure order but increases latency. Cancellation must be propagated and every started validator joined. This is a supervised operation and deserves a promise-returning name.

Adding `taskRetrying` may be source-compatible for observers that subscribe by name, but a public discriminated event union used exhaustively can break. Emission timing and meaning are behavioral contracts even when payload types remain assignable.

## G. Reentrancy and publication answers

`emit` invokes the first listener before moving to the second. A listener that submits another task can therefore re-enter scheduler code while the outer publication stack is active. The scheduler must have committed its authoritative transition before emission, and it must either tolerate that command reentrancy or queue commands explicitly. The immutable event should carry task ID, scheduler revision, source index, and terminal fact, not the mutable task record.

A thrown observational listener should not retroactively undo committed state. Either isolate observer failures and report them through a separate diagnostic boundary, or replace the event with an awaited hook when listener success is required by the command. Catching every error silently is the weak repair: it hides defects without defining ownership. Subscription disposers belong to the subscriber’s lifecycle and should be idempotent.

## H. Event-evolution answers

Changing the existing payload can break listeners that validate exact shape or assume `message` is the only field. Optional additions are source-compatible for many TypeScript consumers but still require runtime policy and can create partially populated states. A new event name gives the clearest contract but temporarily duplicates publication. A versioned envelope supports long-lived extension at the cost of branching in every listener. The correct choice depends on public compatibility commitments.

Listener-leak evidence should use the public disposer and observable delivery. Register, dispose, publish, and repeat; assert one delivery to live listeners and none to disposed listeners. Private listener arrays are implementation details and do not establish the public lifecycle contract.
