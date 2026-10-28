# Laboratory 11 — Descriptor-Safe Settings

## Product

Build a settings object whose ordinary data, hidden provenance, accessor behavior, debug inspection, and persistence snapshot are intentionally different surfaces.

The laboratory exists because many object utilities silently assume that an object is a string-keyed bag of values. That assumption causes accessors to run during copying, symbol metadata to disappear, non-enumerable state to be ignored, and descriptor restrictions to be weakened. Your product must inspect and copy by contract rather than by habit.

## Public behavior

The reference package exposes operations equivalent to:

```ts
createSettings(values, source)
describeOwnProperties(settings)
snapshotSettings(settings)
settingsSource(settings)
```

`createSettings` accepts a plain record of primitive setting values. Each setting becomes an own enumerable writable configurable data property. The source is stored under a module-local symbol as a non-enumerable, non-writable, non-configurable property. A non-enumerable accessor named `summary` may compute a human-readable description, but persistence must never invoke it.

`describeOwnProperties` reports keys and complete descriptor facts without reading property values. `snapshotSettings` copies only approved own enumerable string-keyed data properties. Encountering an enumerable accessor is a contract error, not an invitation to execute it.

## Invariants

- setting keys are non-empty and cannot be `__proto__`, `prototype`, or `constructor`;
- the provenance symbol does not appear in `Object.keys`, object spread, or JSON;
- descriptor inspection invokes no getters;
- snapshots contain no symbols, accessors, methods, or inherited state;
- source metadata cannot be overwritten or deleted;
- snapshot order follows the product's validated insertion order.

## Work sequence

1. Record the descriptor produced by ordinary assignment.
2. Define the provenance symbol with a complete descriptor.
3. Add the non-enumerable summary accessor.
4. Implement descriptor-only inspection using `Reflect.ownKeys` and `Object.getOwnPropertyDescriptor`.
5. Implement the data-only snapshot and make accessor rejection causal.
6. Add adversarial tests for symbol keys, inherited properties, forbidden names, deletion, and a getter that throws.

## Prohibited shortcuts

Do not use spread or `Object.assign` as the snapshot implementation. Do not stringify the live object and parse it back. Do not read every property and hope accessors are harmless. Do not make metadata enumerable merely to simplify tests.

## Completion evidence

Your tests must demonstrate the exact descriptor of each surface, zero getter invocations during inspection and snapshot rejection, stable source metadata, and a plain snapshot suitable for validation and persistence.

## Transfer

Add a second hidden symbol for a revision number. Explain whether that symbol should be writable, whether the live object or a separate authority may update it, and why persistence should or should not contain it.
