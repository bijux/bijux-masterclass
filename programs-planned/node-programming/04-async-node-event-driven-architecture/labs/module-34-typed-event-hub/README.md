# Typed Event Hub

## Product

Build a typed in-process event hub with explicit synchronous delivery, immutable payloads, observer-failure policy, and subscription ownership. The hub is for observation; it must not become the authoritative store for domain state.

Read [Module 34](../../course-book/module-34-event-emitter-and-typed-event-contracts/index.md).

## Required API

Define an event-map generic whose values are readonly argument tuples. Export `on`, `once`, `emit`, and an idempotent disposer. Keep the underlying `EventEmitter` private. The public type must reject unknown event names and payloads with the wrong arity or type.

## Delivery policy

State whether emission iterates a snapshot of listeners or a live collection. State what happens when a listener throws. The reference isolates observer failures, continues remaining listeners, and reports failures separately; a different policy is acceptable only when the API and tests agree.

Ordinary listener callbacks are synchronous. Async callbacks are prohibited or adapted into an explicitly owned worker. Returning a promise from a listener must not be mistaken for awaited publication.

## Required evidence

Test registration order, `once`, idempotent disposal, self-unsubscription, removing another listener during emission, recursive emission, observer throw, zero listeners, and listener retention after disposal. Include static cases proving event-name-to-tuple relationships.

## `'error'` decision

Do not use the special `'error'` name for ordinary domain failure. Document whether the hub can emit infrastructure errors and who owns the required handler. A domain failure should be represented by a normal typed event such as `taskFailed`.

## Reentrancy and disposal evidence

Add a listener that emits or commands the hub recursively. Define whether recursive emission is legal and prove the selected behavior. Add a listener that removes itself and another that adds a new listener during publication; assert behavior according to the underlying `EventEmitter` contract rather than intuition.

The public API should return an idempotent disposer. Run repeated start/stop cycles and prove listener counts remain stable. Observer failure must follow one documented policy and must not make already-committed domain state ambiguous.

## Payload stability

Freeze or reconstruct event payloads so a listener cannot mutate facts observed by later listeners. Add a test that attempts mutation and proves authoritative state and subsequent observation remain unchanged. Document whether payload freezing is runtime enforcement or only a type-level readonly view.

## Independent transfer

Build an event surface for a stateful cache. Keep cache entries authoritative inside the cache, publish immutable `hit`, `miss`, `filled`, and `evicted` observations, and explain how an async metrics sink is bounded and joined.

## Implementation stages

Define event-map and listener types first. Implement snapshot delivery and idempotent disposal. Add `once` removal-before-invocation. Isolate or aggregate observer errors according to one documented policy. Finally add an async-sequence adapter only if its finite buffer and terminal behavior are explicit.

## Review questions

Can a listener mutate authoritative state? What happens under recursive emission? Does observer throw stop later observers? Are async callbacks permitted? How are retained closures released? What changes when a new event is added?

## Completion evidence

Include static payload tests, listener-mutation tests, recursive `once` evidence, observer failure evidence, and a retention test showing disposed listeners are no longer invoked. Document the difference between synchronous `emit` and any awaitable publication extension.
