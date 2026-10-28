# Course 3 Final Review — Reasoned Solutions

## Part I

1. Structural compatibility asks whether the source provides the members required by the target. It neither rejects all extra runtime keys nor validates external values.
2. `satisfies` checks compatibility while retaining the expression's more specific inferred type. A broad annotation can replace that specific type with the annotation.
3. Excess-property checking is a special check on fresh object literals. A variable has an already inferred structural type, so ordinary assignability applies.
4. A useful generic parameter connects at least two positions: input and output, key and selected value, schema and inferred result, or container and callback item.
5. `K extends keyof T` limits the key to known keys and allows `T[K]` to preserve the selected property type. `string` loses both facts.
6. A conditional distributes over a union when the checked type is a naked type parameter.
7. `never` represents no possible member; union normalization removes it.
8. `infer` introduces a name for a type already present in the matched structure.
9. Mapped modifiers `+?`, `-?`, `+readonly`, and `-readonly` add or remove capabilities while iterating a key union.
10. Each interpolated union is cross-multiplied. Large generated key sets slow checking and make diagnostics difficult to understand.
11. A covariant type only produces `T`; a contravariant type only consumes `T`; an invariant type requires both directions to remain fixed.
12. TypeScript intentionally permits some method-parameter bivariance for compatibility. A library that treats this as proof can dispatch a broader value into a narrower callback.
13. A declaration proves what the selected checker sees for consumers. It does not prove runtime exports, values, validation, side effects, or behavior.
14. Handwritten or emitted declarations can claim a number while JavaScript returns a string. Only runtime evidence detects the mismatch.
15. `exports` encapsulates paths that were previously reachable by deep import. Consumers of undeclared paths break.
16. The `types` condition directs TypeScript to the declaration file corresponding to a runtime entry point.
17. The schema's job is to turn untrusted input into `T`; accepting `T` would assume the conclusion before validation.
18. The object parser must check own-property presence before invoking the child schema. Missing optional keys are omitted; present values are validated normally.
19. Source, type, declaration, runtime, behavior, package, and data-format compatibility.
20. A downstream exhaustive switch that handled every old member becomes incomplete when the union grows.

## Part II

The assignment through `source` succeeds because its structural type contains `x`; the fresh literal assigned directly to `Point` receives an excess-property error for `y`. The principled repair depends on intent: narrow the construction to the public shape, or validate exactness at runtime. Casting hides the question.

The `string` key is too broad. Preserve a literal (`const key = 'name'`) or accept a generic key constrained to `keyof T`. An assertion to `keyof T` is weak unless another check establishes membership.

`Boxed<'a' | 'b'>` distributes and becomes `{ value: 'a' } | { value: 'b' }`. Wrap the checked parameter in a tuple when one box around the entire union is intended.

Under strict function checking, a listener requiring `Dog` is not safe where an `Animal` listener is required. The caller may supply a non-dog animal. Broaden the callback, narrow before registration, or index handlers by exact event type.

The `declare` statement emits no runtime value. It can describe a nonexistent or incompatible object. Export the actual runtime value with an aligned type or write a declaration adjacent to the JavaScript implementation and test both surfaces.

## Part III

A strong design accepts `unknown`, validates a version discriminator first, and returns one inferred manifest type. The package exports only documented entry points. A declaration test imports exactly as a consumer does. Compatibility fixtures preserve the old version. Adding an optional field can be minor only when runtime defaults and exact-optional semantics are documented. Removing an accepted version or requiring a new field is a major change unless a migration layer preserves old input.

## Part IV

The discriminator must be validated as an own string property. The variant map must reject duplicate static keys by construction and reject missing runtime variants with an issue at the discriminator path. `Infer` should produce the union of variant outputs. The generated declaration must not expose internal parser types. Adding the combinator is additive; changing existing `union` error behavior while implementing it may be breaking and should be reviewed separately.
