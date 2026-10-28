# Module 28 Workbook

For each combinator, write its runtime input domain, output ownership, inferred type, failure path, and resource bound.

## A. Primitive policy

Specify string, finite number, Boolean, and literal semantics. Decide coercion, `NaN`, infinities, negative zero, and object-wrapped primitives.

## B. Optional object fields

Trace missing, present valid, present `undefined`, inherited, getter-backed, and unknown fields. Ensure static optionality matches runtime own-property policy.

## C. Collection bounds

Design array validation with maximum length, maximum issues, deterministic order, and copied output. Add nested path tests.

## D. Union diagnostics

Compare fail-fast, all-member, and bounded-summary strategies for an overlapping three-member union. State compatibility effects of reordering members.

## E. Recursive schema

Build a tree schema with a depth limit. Test a deep chain and a cyclic JavaScript object. State whether cycles are unsupported input or a separate graph feature.

## F. Independent laboratory

Complete [Composable Decoder Library](../../labs/module-28-composable-decoder-library/README.md). Do not import SchemaKit.

## G. SchemaKit transfer

Complete all combinators, JSON subpath, example project schema, CLI, and runtime/static agreement tests.

## H. Reconstruction

Explain the complete path from unknown input to inferred trusted output, including where TypeScript ends and runtime evidence begins.

## I. Algebra table

For every SchemaKit combinator, record input domain, output type, output ownership, path behavior, issue bound, construction-time failure, parse-time failure, and compatibility risk. Include optional, nullable, array, tuple, object, record, union, refine, transform, and lazy.

## J. Optionality proof

Write tests for property missing, own property present with valid value, own property present with `undefined`, inherited property, accessor property, and unknown property. Align runtime behavior with the inferred output under exact optional properties.

## K. Union policy

Construct two overlapping schemas and demonstrate how declaration order changes first-success behavior. Define when reordering is breaking. Design a bounded failure summary that remains useful without retaining the complete rejected value.

## L. Recursive data

Create a recursive tree schema, a value deeper than the configured limit, and a cyclic JavaScript object. Trace where depth and cycle evidence is recorded. Explain why ordinary JSON data cannot contain an object-reference cycle even though JavaScript input can.

## M. Resource review

Set explicit limits for array length, object keys, recursive depth, accumulated issues, union-member details, identifier length, and diagnostic previews. For each limit, decide whether rejection occurs before allocation or after partial work.

## N. Static/runtime agreement

Add one type test and one runtime test for every public combinator. Type tests should prove inferred output; runtime tests should prove acceptance and rejection. Neither test category may stand in for the other.

## O. Getter and proxy policy

Create an object whose property getter increments a counter and a proxy that records `get`, `ownKeys`, and `getOwnPropertyDescriptor` traps. Run the object schema against each. Document which user code may execute during validation. Decide whether SchemaKit validates ordinary data-shaped objects or claims to sandbox hostile JavaScript objects.

## P. Canonical output

Validate two inputs with different property insertion orders and render their trusted outputs canonically. Prove that semantically equivalent validated values produce the same text. Explain why canonical rendering is separate from validation and why it matters for fixtures and compatibility.
