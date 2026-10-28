# Module 23 — Conditional Types, `infer`, and Type-Level Control Flow

> **Question:** How can a public type compute a result from another type while remaining distributively correct, terminating, and readable?

## Why this comes now

Module 22 established generic relationships. Conditional types let one relationship choose among type results. They are powerful because TypeScript libraries often need to answer questions such as:

- What value does this schema produce?
- What payload corresponds to this command?
- What is the resolved value of this promise-like type?
- Which members of a union satisfy one capability?
- What input type does this callback accept?

The danger is that type-level control flow can become detached from runtime behavior. A twenty-line conditional type may impress its author while producing slow checking, unreadable diagnostics, accidental distribution, and a public API no one can explain. This module teaches a small evaluation model and a complexity budget.

## Outcomes

By the end of the module, you can:

- evaluate a conditional type by substituting a concrete checked type;
- predict distributive behavior over unions;
- disable distribution when the whole union is the subject;
- explain how `never`, `unknown`, and `any` interact with conditional types;
- use `infer` to name a type already present in a matched structure;
- design recursive conditional types with an explicit base case and bounded purpose;
- build type-level tests for equality and rejection;
- connect conditional output to a real runtime branch or runtime witness;
- derive SchemaKit output types without duplicating them.

## 1. The basic evaluation rule

A conditional type has the form:

```ts
T extends U ? X : Y
```

Read it as an assignability question in the type system:

```text
if checked type T is assignable to constraint U
    choose X
else
    choose Y
```

Example:

```ts
type IsString<T> = T extends string ? true : false;

type A = IsString<'ready'>; // true
type B = IsString<number>;  // false
```

The result is a type, not a runtime Boolean. No JavaScript branch is emitted.

When debugging, substitute a concrete type before reasoning about generics:

```text
IsString<'ready'>
→ 'ready' extends string ? true : false
→ true
```

## 2. Conditional types describe relationships

A useful conditional type connects a structured input to a related output:

```ts
interface TextCommand {
  readonly kind: 'text';
  readonly text: string;
}

interface CountCommand {
  readonly kind: 'count';
  readonly values: readonly unknown[];
}

type Command = TextCommand | CountCommand;

type CommandOutput<C extends Command> =
  C extends TextCommand ? string :
  C extends CountCommand ? number :
  never;
```

A generic executor can preserve the relationship:

```ts
function execute<C extends Command>(command: C): CommandOutput<C> {
  if (command.kind === 'text') {
    return command.text.trim() as CommandOutput<C>;
  }
  return command.values.length as CommandOutput<C>;
}
```

The assertions expose an important limitation: control-flow narrowing inside a generic function does not always reduce the generic parameter exactly as the conditional return requires. A principled library may instead use overloads, a command-handler table, or a non-generic implementation behind a typed facade. Conditional types can express a relation that the implementation still has to prove.

## 3. Distribution over unions

A conditional type distributes when its checked side is a **naked type parameter**:

```ts
type Box<T> = T extends unknown ? { readonly value: T } : never;

type R = Box<'a' | 'b'>;
// { readonly value: 'a' } | { readonly value: 'b' }
```

Evaluation behaves as if TypeScript mapped the conditional over union members:

```text
Box<'a' | 'b'>
→ Box<'a'> | Box<'b'>
```

This is often exactly what union filtering and variant mapping need.

```ts
type StringsOnly<T> = T extends string ? T : never;
type S = StringsOnly<'a' | 1 | 'b'>; // 'a' | 'b'
```

The `number` branch becomes `never`, and `never` disappears from the union.

## 4. Disable distribution deliberately

Sometimes the question concerns the union as one whole:

```ts
type EveryMemberIsString<T> =
  [T] extends [string] ? true : false;

type A = EveryMemberIsString<'a' | 'b'>; // true
type B = EveryMemberIsString<'a' | 1>;   // false
```

The tuple wrapper prevents the checked type from being naked. It does not create a runtime tuple.

Write the question in English before choosing distribution:

- “For each union member, what is its output?” → distribute.
- “Does the entire union satisfy this constraint?” → do not distribute.

Many difficult conditional-type bugs are question-definition bugs.

## 5. `never` is both empty and distributively special

`never` represents no possible value. In unions it vanishes:

```ts
type A = string | never; // string
```

A distributive conditional given `never` also produces `never` because there are no union members to evaluate:

```ts
type IsNeverWrong<T> = T extends never ? true : false;
type N = IsNeverWrong<never>; // never, not true
```

Detect `never` non-distributively:

```ts
type IsNever<T> = [T] extends [never] ? true : false;
```

This is not trivia. Recursive transformations and filtering helpers often accidentally erase all members, after which a downstream type becomes `never` and diagnostics point far from the original cause.

## 6. `unknown` is the safe top type

Every type is assignable to `unknown`, so:

```ts
type Always<T> = T extends unknown ? 'yes' : 'no';
```

This helper distributes and returns `'yes'` for every union member. `unknown` itself is not assignable to an arbitrary narrower type without checking.

Use `unknown` in schema and declaration helpers when the concrete type is intentionally unconstrained. It preserves type safety because operations require narrowing.

## 7. `any` contaminates type-level reasoning

`any` suppresses ordinary checking and can make conditionals produce a union of both branches or otherwise lose useful certainty:

```ts
type MaybeString<T> = T extends string ? 'string' : 'other';
type A = MaybeString<any>; // effectively both possibilities
```

A public helper that behaves differently for `any` should document or reject that boundary if possible. Usually the better strategy is to prevent `any` from entering the package through explicit source policy and use `unknown` for external values.

Do not write elaborate `IsAny` tricks unless the product genuinely needs them. They increase complexity and rarely repair an upstream `any` leak.

## 8. `infer` names evidence inside a match

```ts
type ElementOf<T> = T extends readonly (infer Item)[] ? Item : never;

type A = ElementOf<readonly string[]>; // string
```

`infer Item` does not invent the element type. It names the type found where the pattern matched.

Function examples:

```ts
type ReturnOf<T> = T extends (...args: never[]) => infer R ? R : never;

type ParametersOf<T> =
  T extends (...args: infer P) => unknown ? P : never;
```

For overloaded function types, inference generally reflects the last signature used as the implementation-facing catch-all, not an overload-resolution process for every call. Public APIs should not depend on a conditional type magically reconstructing overload selection.

## 9. Extract multiple relationships

```ts
type PairParts<T> =
  T extends readonly [infer A, infer B]
    ? { readonly first: A; readonly second: B }
    : never;
```

The pattern can contain constraints:

```ts
type StringHead<T> =
  T extends readonly [infer H extends string, ...readonly unknown[]]
    ? H
    : never;
```

Constrained inference improves local precision, but nested patterns can become hard to read. Name intermediate helpers rather than embedding every extraction into one public alias.

## 10. Schema output inference

SchemaKit uses a small relationship:

```ts
export interface Schema<out T> {
  parse(input: unknown): T;
}

export type Infer<S extends Schema<unknown>> =
  S extends Schema<infer Output> ? Output : never;
```

The type parameter is in a known location, so `infer` extracts it. This is better than adding a public phantom property solely for indexing:

```ts
// Avoid exposing implementation-shaped public fields just for type extraction.
interface WeakSchema<T> {
  readonly _output: T;
}
```

A private or `declare`-only brand can be useful when necessary, but method return positions already carry the relation.

## 11. Conditional return types and implementation burden

This looks attractive:

```ts
function normalize<T extends string | readonly string[]>(
  value: T,
): T extends string ? string : readonly string[] {
  // ...
}
```

The implementation often needs assertions because generic control flow does not perfectly correlate `T` with each branch. Before accepting that burden, compare:

- overloads;
- a union return;
- two named functions;
- a discriminated input object;
- a conditional type used only by consumers, with a simpler internal implementation signature.

A narrower caller type is not automatically worth a more fragile implementation.

## 12. Recursive conditional types

Recursive types can transform nested structures:

```ts
type DeepReadonly<T> =
  T extends (...args: never[]) => unknown ? T :
  T extends readonly (infer Item)[] ? readonly DeepReadonly<Item>[] :
  T extends object ? { readonly [K in keyof T]: DeepReadonly<T[K]> } :
  T;
```

This helper encodes policy choices:

- functions remain callable;
- arrays lose tuple precision in this version;
- dates, maps, sets, branded objects, and class instances are treated as generic objects;
- recursive/cyclic types may stress the checker;
- runtime values are not frozen.

A utility type that works for one plain-data model may be wrong as a universal public utility. Prefer domain-specific recursion with a documented input universe.

## 13. Termination and compiler work are design concerns

Type-level recursion needs a base case. It also needs a bounded reason to exist. Warning signs include:

- recursion over arbitrary object graphs;
- repeated distribution inside mapped types;
- template-literal cross products at each level;
- error messages that expose dozens of internal aliases;
- a public type whose result cannot be explained without compiler experimentation;
- editor latency or excessive instantiation errors.

Simplify by:

- restricting the input domain;
- splitting helpers;
- precomputing a named public type;
- moving validation to runtime;
- asking callers for one explicit annotation;
- avoiding recursive exactness utilities.

Type-level computation is part of the package's performance and maintenance budget.

## 14. Equality tests for types

Runtime tests cannot observe erased types. Use compile-time assertions:

```ts
type Equal<A, B> =
  (<T>() => T extends A ? 1 : 2) extends
  (<T>() => T extends B ? 1 : 2)
    ? true
    : false;

type Expect<T extends true> = T;

type _Check = Expect<Equal<Infer<typeof stringSchema>, string>>;
```

This equality helper has subtleties around `any`, intersections, and normalization. Use it for controlled course types, not as a formal theorem prover.

Negative tests use `@ts-expect-error` next to one intentional failure. A negative test that compiles after an API change should fail because the expected error disappeared.

## 15. Type-level and runtime exhaustiveness

A conditional type may cover every current union member:

```ts
type Output<C extends Command> =
  C extends TextCommand ? string :
  C extends CountCommand ? number :
  never;
```

If a new command is added, the type returns `never` for it, but that may not create an obvious error at every use. Pair the type with a runtime exhaustive dispatch and explicit tests.

A handler map can make the relation more visible:

```ts
interface CommandMap {
  text: { readonly input: TextCommand; readonly output: string };
  count: { readonly input: CountCommand; readonly output: number };
}
```

Then indexed access may be clearer than nested conditionals. Choose the representation that keeps the source of truth obvious.

## 16. A conditional-type ledger

For every helper, record:

| Question | Record |
|---|---|
| checked type | Which parameter or concrete type is tested? |
| constraint | What shape or capability is matched? |
| branch relation | What output corresponds to each branch? |
| distribution | Per union member or whole union? |
| inferred parts | Which existing types are named with `infer`? |
| `never` behavior | Filter, error signal, or accidental erasure? |
| recursion | Base case and maximum intended depth/domain? |
| runtime counterpart | Which branch or witness makes the relation true? |
| tests | Positive equality and negative usage? |
| public cost | Diagnostic and checker complexity? |

## 17. Common wrong models

### “Conditional types run at runtime”

They are erased. Runtime code must implement the same relationship independently.

### “Union input means union output in one wrapper”

A naked type parameter distributes. Wrap it when the entire union is the subject.

### “`infer` chooses any convenient type”

It names a type found in a matched position.

### “`never` means an error will always be shown”

`never` can disappear silently through unions and inference.

### “Recursive utility types are universally reusable”

They encode domain assumptions and consume checker resources.

### “A clever conditional return is better than overloads”

Only if the runtime implementation and consumer diagnostics remain clear.

## 18. Use the idea in a complete program

Module 23 adds to SchemaKit:

- `Infer<S>` and `OutputOf<S>` aliases;
- union schema output as the union of member outputs;
- tuple schema output by mapped extraction;
- optional-schema recognition through a specific interface marker;
- compile-time equality tests;
- no recursive conditional type broader than the runtime schema domain.

The Command Outcome Matrix lab uses a different domain to prove that type-level dispatch and runtime dispatch remain aligned.

## Practice sequence

1. Evaluate every conditional in the workbook by substitution.
2. Predict the eight Module 23 investigations.
3. Rewrite one accidental distributive helper non-distributively.
4. Complete [Command Outcome Matrix](../../labs/module-23-command-outcome-matrix/README.md).
5. Implement the Module 23 SchemaKit increment in [the capstone guide](../capstone.md#module-23--conditional-output-derivation).
6. Inspect one difficult diagnostic and simplify the helper that produced it.

## Ready to continue

You are ready for Module 24 when you can explain:

- naked-parameter distribution;
- tuple-wrapped non-distribution;
- why `never` vanishes from unions;
- what `infer` can and cannot do;
- why conditional return types burden implementations;
- the base case and domain of one recursive helper;
- how SchemaKit derives output without repeating it.

Next: [Mapped Types, Key Remapping, and Template-Literal Types](../module-24-mapped-types-key-remapping-and-template-literals/index.md).
