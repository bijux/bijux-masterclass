# Variance-Safe Event Router

## The product

Build a generic event router indexed by an event map. The router stores callbacks, emits typed payloads, returns an idempotent unsubscription function, and defines deterministic behavior when the listener set changes during dispatch.

Read [Module 25](../../course-book/module-25-variance-function-types-and-callback-safety/index.md) first.

## Public contract

```ts
interface Events {
  readonly message: { readonly text: string };
  readonly count: { readonly value: number };
}

const router = new EventRouter<Events>();
router.on('message', event => console.log(event.text));
router.emit('count', { value: 2 });
```

A listener registered for `count` must not demand a narrower payload than the router promises to emit. Function-valued callbacks should receive strict function checking. The internal storage may use a localized cast because a heterogeneous map erases per-key correlation; callers may not be required to cast.

## Milestones

1. Draw producer and consumer arrows for every occurrence of `E[K]`.
2. Define a listener as a function type rather than a method-only interface.
3. Implement key-indexed registration and emission.
4. Snapshot listeners before dispatch.
5. Make unsubscription idempotent and test listener counts.
6. Add rejected tests for wrong keys and payloads.
7. Analyze whether explicit `in` variance improves the public declaration.
8. Document thrown-listener and reentrancy policy.

## Adversarial cases

Test self-removal, removal of another listener, registration during dispatch, repeated unsubscription, empty emission, and a listener that throws. Construct the mutable-array covariance counterexample and explain why the router does not expose mutable listener collections.

Compare method syntax with function-valued properties under strict function types. The more permissive result is not automatically the safer public callback contract.

## Design record

State:

- which positions are covariant, contravariant, or invariant;
- which internal cast exists and how key-indexed operations justify it;
- whether exceptions stop dispatch or are accumulated;
- whether reentrant emission is supported;
- which changes to the event map break exhaustive or implementor consumers.

## Independent transfer

Build a typed hook registry for lifecycle phases or a command middleware table. Preserve callback direction and define mutation-during-dispatch behavior explicitly.

## Completion standard

A reviewer should be able to derive every safe substitution from operations and predict dispatch behavior without reading the chosen collection implementation.
