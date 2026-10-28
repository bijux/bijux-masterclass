# Course 3 Outcomes

By the end of Course 3, you can produce evidence for the following abilities.

## Structural reasoning

- Trace assignability from a source type to a target type.
- Explain required, optional, readonly, literal, index, and call-signature effects.
- Distinguish excess-property checking from exact object typing.
- Choose among annotation, inference, `as const`, `satisfies`, validation, and assertion.
- Introduce nominal identity only where structural interchangeability would violate the domain.

## Generic and type-level design

- Name the relationship represented by every type parameter.
- Predict inference from arguments, contextual positions, constraints, defaults, and `const` type parameters.
- Use `keyof` and indexed access to preserve key/value relationships.
- Control conditional-type distribution and `never` behavior.
- Use `infer` to extract rather than duplicate related types.
- Build mapped and template-literal types with bounded output and readable helper names.
- Recognize recursive type computations that are difficult to explain or expensive to instantiate.

## Variance and callback contracts

- Classify producer, consumer, and mutable positions.
- Review function parameters under strict function checking.
- Explain method bivariance and other deliberate TypeScript unsoundness.
- Prefer readonly views when covariance is intended.
- Design callback registration and dispatch surfaces that do not rely on unsafe narrowing.

## Library artifacts

- Inspect emitted `.d.ts` files as deliverables.
- Write or repair ambient declarations for JavaScript runtimes.
- Distinguish external modules, globals, augmentation, and declaration merging.
- Create type tests that assert both supported and rejected usage.
- Align ESM source imports, emitted JavaScript, declaration paths, and package `exports`.
- Prevent accidental deep-import compatibility promises.

## Runtime/static agreement

- Build schema combinators that validate `unknown` input and infer the validated output type.
- Preserve path-aware errors without retaining arbitrary external values.
- Model required and optional object properties consistently at runtime and in types.
- Separate parsing, validation, refinement, transformation, and migration.

## Compatibility and evolution

- Review source, type, declaration, runtime, behavioral, package, and data-format compatibility separately.
- Identify breaking changes caused by unions, overloads, constraints, optionality, readonly, exports, and error behavior.
- Use deprecation, adapters, versioned records, and compatibility fixtures deliberately.
- Implement an unseen SchemaKit feature across runtime, type inference, declarations, package exports, tests, and documentation.
