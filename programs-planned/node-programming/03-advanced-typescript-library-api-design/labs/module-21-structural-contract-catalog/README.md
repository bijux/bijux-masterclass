# Structural Contract Catalog

## The product

Build a small library that declares a closed catalog of product features. Each feature has a literal `id`, a human label, and a stability state. The resulting catalog exposes ordered IDs and a key-safe lookup whose return type remains connected to the selected ID.

This is not a configuration parser and not a demonstration of `as const`. It is an exercise in separating three ideas that are often collapsed:

- structural assignability between source and target types;
- runtime validation of catalog invariants;
- nominal identity when two structurally identical strings belong to different domains.

Read [Module 21](../../course-book/module-21-structural-typing-assignability-and-public-shape/index.md) before beginning.

## Public contract

The finished library should support a call shaped like:

```ts
const catalog = defineCatalog(
  { id: 'search', label: 'Search', stability: 'stable' },
  { id: 'export', label: 'Export', stability: 'experimental' },
);

catalog.ids();
catalog.get('search');
```

The ID tuple must remain a finite literal union. `catalog.get('missing')` must be rejected statically. Runtime construction must reject empty IDs and duplicates before the catalog becomes visible.

The catalog owns an internal lookup map. Consumers must not receive that map or any mutable staging array. Returned feature values and ID collections should be readonly views or frozen snapshots according to one documented policy.

## Milestones

1. Define the public feature and stability contracts without using a broad index signature.
2. Preserve literal IDs through a `const` generic construction boundary.
3. Derive `FeatureId<F>` from the feature tuple rather than maintaining a second union.
4. Derive the selected feature type with `Extract` or an equivalent relationship.
5. Validate empty and duplicate IDs before publishing the catalog.
6. Emit declarations and inspect whether literal IDs and readonly members survived.
7. Add a compile-time rejection for an unknown ID and runtime tests for duplicate construction.

## Adversarial cases

Test two features with the same ID but different labels, an empty ID, and a source object containing extra fields. Record which cases TypeScript notices and which only runtime code can reject. Also test that a readonly catalog view does not imply deep runtime immutability for nested objects unless you enforce it.

Do not “solve” the unknown-ID case with a broad `string` overload. That removes the central relationship.

## Design record

Write one page answering:

- Is the catalog exact at runtime, or may features contain extra fields?
- Does adding a feature break exhaustive consumers of `FeatureId<F>`?
- Where would a branded `FeatureId` be useful, and where would it obscure the literal catalog relationship?
- Which assertion, if any, remains inside the implementation, and what preceding invariant justifies it?

## Independent transfer

Rebuild the mechanism for a command registry or database-column catalog. Change the domain and at least one policy—such as duplicate handling or catalog ordering—while preserving literal lookup precision.

## Completion standard

The lab is complete when runtime construction, static lookup, emitted declarations, and the compatibility note all describe the same catalog. Compare with `reference/` only after your own package type-checks and tests pass.
