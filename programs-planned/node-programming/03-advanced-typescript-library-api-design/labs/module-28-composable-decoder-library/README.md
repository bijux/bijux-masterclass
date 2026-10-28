# Composable Decoder Library

## The product

Build a small validation algebra independent of SchemaKit. Each `Decoder<T>` accepts `unknown`, produces either a trusted `T` or a nonempty path-aware issue list, and composes without requiring callers to repeat output types.

Read [Module 28](../../course-book/module-28-runtime-schemas-static-inference-and-validation-algebra/index.md) first.

## Required decoders

Implement:

- text;
- finite number;
- array of another decoder;
- one required object field.

Derive `Output<D>` from a decoder. Array output must be a new readonly collection. Field decoding must require an own property and append the field key to the issue path.

## Milestones

1. Define a result union that cannot represent success and failure simultaneously.
2. Define `Decoder<out T>` and `Output<D>`.
3. Implement primitive decoders from `unknown` without coercion.
4. Implement array traversal with deterministic issue order and a finite issue limit.
5. Implement field decoding with own-property semantics.
6. Add nested path tests.
7. Add type tests for inferred array and field outputs.
8. Compare runtime and declaration surfaces.

## Adversarial cases

Test `NaN`, arrays containing multiple bad elements, inherited fields, present `undefined`, getter-backed properties, large arrays, and an assertion-based parser that lies. Decide whether the product reads getters and state that policy.

A localized assertion inside fixed construction may be justified. An assertion at the unknown-input boundary is not validation.

## Design record

Record for every decoder:

- accepted runtime domain;
- output ownership;
- inferred type;
- issue path;
- resource limit;
- construction-time and parse-time failures;
- compatibility effect of changing acceptance.

Explain why a type test and a runtime rejection test prove different contracts.

## Independent transfer

Add a tuple or optional-field decoder without copying SchemaKit. Preserve exact optional-property behavior and define whether present `undefined` is accepted.

## Completion standard

An external value becomes trusted only through runtime evidence. The output type must be extracted from the same decoder value that performs validation, and failures must identify the nested location without retaining the complete rejected object.
