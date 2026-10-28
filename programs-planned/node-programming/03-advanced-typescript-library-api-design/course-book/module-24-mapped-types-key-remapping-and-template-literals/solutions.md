# Module 24 Reasoned Solutions

## A. Modifiers

Use `-readonly` and `-?` to remove capabilities and `readonly`/`?` to add them. A domain update should omit immutable identifiers, derived values, and fields that require coordinated changes; `Partial<T>` knows none of those rules.

## B. Filtering

A mapped key table can return each key or `never`, then indexed access collects the union. Decide whether `T[K] extends string` means “entirely string” or whether `Extract<T[K], string>` should admit unions. Optional properties include `undefined` when read, so the policy must be explicit.

## C. Events

The mapped type derives callback signatures. Runtime code should preserve the source field key or use a validated event table; it should not parse arbitrary strings and assert the result. Dispatch must supply both values of the exact field type.

## D. Growth

The cross product contains `4 × 5 × 3 = 60` members. That may be acceptable for a fixed operational protocol, but it is excessive if scopes or actions are open-ended. A branded validated string or explicit event object may scale better.

## E. Schema output

Optional keys are those whose schema implements the deliberate `OptionalSchema` contract, not every schema returning a union with `undefined`. Required and optional mapped fragments are intersected and optionally simplified for display. Runtime parsing omits missing optional properties and validates any present property.

## F. Laboratory

A strong solution derives the static surface from the settings model and maintains a runtime field table. It tests wrong callback types, unknown events, listener removal identity, and stable call order.

## G. SchemaKit

The parser checks an own-property record, applies each child schema with an extended path, and handles unknown keys according to declared policy. It does not use the mapped output type as runtime evidence. Declaration tests ensure optional fields remain optional under `exactOptionalPropertyTypes`.

## H. Cleverness review

Keep a generated type only when its source authority and runtime counterpart are obvious. If the helper requires a paragraph of caveats for arrays, classes, cycles, and optional values, a domain-specific explicit type is usually better.

## I. Reconstruction standard

A complete answer names input keys, output keys, modifier changes, runtime source of truth, compatibility effect, and generated size. Syntax alone is not a design explanation.

## I. Modifiers

A draft may remove readonly while preserving requiredness. A persisted snapshot usually preserves readonly and required fields. A patch adds optionality but should not automatically add `undefined` under exact optional semantics. An error map often makes every key optional and changes values to diagnostic collections. Each modifier represents a capability or presence change; it is not cosmetic syntax.

## J. Collision policy

Camel-case normalization is many-to-one. A type that silently unions colliding property values does not tell the runtime which source wins. Rejection is the safest general policy for a configuration or schema boundary. Combining values is valid only when the product defines an associative combination. Last-write-wins is a policy, not a natural consequence of object construction, and should be named and tested if chosen.

## K. Event family

Use `Extract<keyof T, string>` before template interpolation. The mapped union should retain `key: K`, `previous: T[K]`, and `current: T[K]`. That shared `K` is the proof that event name and payload came from one model member. A symbol-keyed internal property remains outside the textual event protocol.

## L. Size budget

The cross product has 384 members. If phases are mainly runtime status, generating all combinations creates noise without meaningful caller safety. Keeping resources and actions static while validating phase at runtime may provide better completion and smaller declarations. The decision should consider consumer use, not only checker capability.

## M. Local assertion

Runtime code cannot directly express the mapped-union correlation while constructing an object from generic `K`. A localized assertion is defensible after reading previous/current from the same `key` and deriving the event name from that exact key. The assertion belongs inside the implementation; callers should never need it.
