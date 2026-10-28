# Module 34 Workbook — EventEmitter and Typed Event Contracts

## A. Trace synchronous delivery

An emitter registers listeners `A`, `B`, and `C`. `B` emits the same event recursively once. `C` throws.

1. Draw the call stack and delivery order.
2. Which listeners in the outer and inner emission run before the throw?
3. What state can be reentered halfway through the outer transition?
4. Propose a reentrancy policy and evidence for it.

## B. Separate authority from observation

A shopping cart emits `itemAdded` and relies on a listener to update the total.

5. Explain why the cart has two state authorities.
6. Move the total update into the authoritative transition and redesign the event as immutable observation.
7. Decide what happens if a metrics listener throws after the cart transition commits.

## C. Design a typed hub

Create an event map whose values are readonly argument tuples. Implement `on`, `once`, `off`, and `emit` without exposing the raw emitter. Return an idempotent disposer from `on`.

8. Preserve event-name-to-payload relationships.
9. Decide whether observer failures propagate, are isolated, or are collected.
10. State how async listeners are handled; do not pretend ordinary `emit` awaits them.

## D. The special `'error'` event

11. Explain the behavior of unhandled `'error'` emission.
12. Distinguish a domain `taskFailed` event from emitter infrastructure failure.
13. Explain why an async `'error'` handler can create a rejection loop under capture policies.

## E. Independent laboratory

Complete [Typed Event Hub](../../labs/module-34-typed-event-hub/README.md). Add a listener that unsubscribes itself and another listener during emission; document whether the current emission uses a snapshot or live listener set.

## F. TaskHarbor transfer

Publish immutable lifecycle events only after scheduler transitions. An observer failure must not erase an outcome or stop later observers unless the documented event policy says so. Add listener cleanup and bounded async-event buffering tests.

## G. Unseen transfer

Design a typed event surface for a configuration reloader. Include `reloadStarted`, `reloadSucceeded`, and `reloadRejected`; decide what data is safe to expose, which state owns the active configuration, and what a slow async audit consumer requires beyond EventEmitter.

## I. Listener mutation matrix

For snapshot and live delivery policies, predict behavior when a listener:

- removes itself;
- removes the next listener;
- adds a new listener;
- emits recursively;
- is registered with `once`.

Choose one policy for the laboratory and write tests that distinguish it.

## J. Design an awaitable publisher

Define a separate `publish` API for three async validators. Decide whether validators run sequentially or concurrently, how failures aggregate, what cancellation does, and whether one slow validator blocks all commands. Explain why this should not be hidden in `EventEmitter.emit`.

## K. Compatibility review

TaskHarbor adds a `taskRetrying` event. Map the change through event type, timing, payload, async sequence adapter, old observers, and documentation. State whether old exhaustive consumers require a versioned event union.

## L. Reentrancy and observer-failure drill

A `taskSucceeded` listener immediately submits another task; a second listener throws; a third records an audit event. Trace the exact synchronous call stack and state visible to each listener. Decide whether the command path should propagate the observer failure, isolate it, or use an awaited hook abstraction instead.

Design immutable payloads for `taskStarted`, `taskSucceeded`, `taskFailed`, and `schedulerIdle`. State which revision or sequence fields prevent listeners from confusing an old event with current state.

## M. Event versioning exercise

Version a public `taskFailed` event from `{ id, message }` to a richer payload containing a stable code, causal category, attempt, and revision. Compare four migration strategies: mutate the existing payload, add optional fields, publish a second event name, or wrap payloads in a versioned envelope. Evaluate source compatibility, runtime compatibility, listener assumptions, and observability cost.

Write a listener ownership test that creates and disposes one thousand short-lived subscribers. The test should prove stable listener count and absence of duplicate delivery without inspecting private fields.

## H. Defense

Explain why “event-driven” does not imply asynchronous delivery, why events should not be a transaction log by accident, and why max-listener warnings do not replace subscription ownership.
