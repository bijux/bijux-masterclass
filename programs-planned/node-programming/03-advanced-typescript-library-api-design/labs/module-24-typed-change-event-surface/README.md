# Typed Change Event Surface

## The product

Build a state container that derives its event family from one model type. For a model key `name`, the public event is `nameChanged` and its payload contains `key: 'name'`, the previous `string`, and the current `string`.

Read [Module 24](../../course-book/module-24-mapped-types-key-remapping-and-template-literals/index.md) before beginning.

## Public contract

The library should expose a mapped event union and operations similar to:

```ts
store.on('nameChanged', event => {
  event.previous; // string
  event.current;  // string
});

store.set('name', 'Grace');
```

Only string keys participate in the textual protocol. Symbol-keyed internal state must be excluded explicitly rather than accidentally converted with `String(symbol)`.

Dispatch uses registration order and a listener snapshot. Removing or adding listeners during an emission affects future emissions, not the active snapshot. Unsubscription is idempotent.

## Milestones

1. Derive `StringKey<T>` from `keyof T`.
2. Derive one event object per key and collapse the mapped object to a union.
3. Derive `EventFor<T, K>` from that union.
4. Connect template-literal event names to listener payloads.
5. Implement immutable top-level state replacement in `set`.
6. Derive the runtime event name and payload from the same key.
7. Test removal during dispatch and wrong payload rejection.
8. Inspect declarations for readable event aliases.

## Adversarial cases

Test Boolean and numeric fields, symbol keys, a listener removed during dispatch, a listener registered during dispatch, and two source keys that a proposed normalization would map to the same event name. If you support remapping, define a collision policy before coding.

Do not replace the event family with `Record<string, unknown>`. That removes the relation the lab exists to teach.

## Design record

Explain:

- why the event object includes both `type` and `key`;
- where one localized assertion is required by generic runtime construction;
- why that assertion is justified by one shared key;
- how large template-literal cross products would affect declarations and editor use;
- whether adding a model field is compatible for exhaustive event consumers.

## Independent transfer

Derive property-specific validation errors or command option names from another model. Keep the key set finite and estimate generated declaration size before deciding to use template-literal types.

## Completion standard

The model must remain the sole source of truth for event names and payload types. Runtime dispatch policy must be explicit and tested rather than inherited accidentally from `Set` iteration.
