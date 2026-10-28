# Module 23 Workbook

Evaluate each type by substitution. Do not rely on editor hover until the written derivation is complete.

## A. Distribution table

Derive:

```ts
type Flag<T> = T extends string ? { text: T } : { other: T };
type A = Flag<'x' | 1 | 'y'>;
```

Then change the helper so the result is one object containing the entire union.

## B. `never` behavior

Predict:

```ts
type OnlyFunctions<T> = T extends (...args: never[]) => unknown ? T : never;
type F = OnlyFunctions<string | (() => number) | never>;
```

Implement `IsNever<T>` and explain why the naïve form fails.

## C. Extraction

Write helpers for:

- element of a readonly array;
- success value of `PromiseLike<T>`;
- first argument of a function;
- value type of `Schema<T>`;
- error type of `Result<T, E>`.

For each, state what happens when the input does not match.

## D. Conditional return review

Review:

```ts
function create<T extends 'text' | 'count'>(
  kind: T,
): T extends 'text' ? string : number;
```

Compare a conditional implementation with overloads and a lookup-map design. Choose one and justify diagnostics, implementation clarity, and compatibility.

## E. Recursive policy

Design a domain-specific `JsonReadonly<T>` for a JSON-only model. State explicitly how it treats arrays, objects, primitives, `undefined`, dates, maps, and functions. Reject unsupported types rather than pretending to transform them.

## F. Independent laboratory

Complete [Command Outcome Matrix](../../labs/module-23-command-outcome-matrix/README.md). Keep one authoritative command map and derive both input/output relations. Add a runtime exhaustive dispatcher and a compile-time equality suite.

## G. SchemaKit transfer

Add:

- union output derivation;
- tuple output derivation;
- optional-schema identification;
- type equality helpers in tests;
- negative tests for unsupported schema values.

Document every assertion required by the runtime implementation.

## H. Complexity review

For one helper in your codebase, record:

- distribution count;
- recursion depth/domain;
- number of generated union members;
- public diagnostic surface;
- simpler alternative.

## I. Reconstruction

Explain conditional types, distribution, `infer`, `never`, recursion, and runtime alignment using one SchemaKit example and one laboratory example.

## I. Distribution ledger

For each type below, compute the result manually before using the checker:

```ts
type A<T> = T extends string ? { text: T } : { other: T };
type B<T> = [T] extends [string] ? { text: T } : { other: T };
type C<T> = T extends unknown ? readonly [T] : never;
type D<T> = T extends { value: infer V } ? V : never;
```

Evaluate each with `T = 'a' | 1`. State exactly where distribution occurs and why.

## J. Conditional type contract

Design `ResultOf<C>` for a five-command union. One command has a union result and one command is generic over a payload schema. Keep the conditional readable enough that a consumer can diagnose a wrong assignment from the declaration alone.

## K. Recursion and termination

Implement a bounded `DeepReadonly<T, Depth>` using a finite predecessor tuple. Test arrays, functions, records, and a depth of zero. Explain why an unbounded recursive type may be correct for small inputs yet unusable for a public library.

## L. `infer` extraction limits

Write extraction helpers for function parameters, return values, promises, array elements, and schema outputs. For each, state what happens for overloads, unions, `never`, and `unknown`. Do not claim that `infer` inspects runtime values.

## M. Diagnostic simplification

Take one type-level computation from the Command Outcome Matrix and expose a named intermediate alias. Compare the declaration error before and after. The goal is not the shortest source; it is a public failure message a caller can act on.

## N. Failure-message exercise

Create two equivalent helpers: one expressed as a single nested conditional type and one decomposed into three named aliases. Trigger the same invalid assignment against both. Copy the resulting diagnostics into your notes and judge them by three questions: Can the caller identify the selected branch? Can the caller see the expected relation? Can the caller repair the call without reading implementation source?

## O. Type-computation budget

For one recursive conditional in your design, record maximum intended depth, union width, distribution points, and fallback behavior. Add a type test at the supported boundary and one just beyond it. A public helper that works only for the author’s tiny example has no honest support envelope.
