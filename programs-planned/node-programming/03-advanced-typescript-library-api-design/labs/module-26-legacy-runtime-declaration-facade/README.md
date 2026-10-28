# Legacy Runtime Declaration Facade

## The product

Place a precise TypeScript facade in front of a JavaScript counter module. The JavaScript implementation is the runtime source of truth; the declaration file is the consumer contract. The exercise proves they agree.

Read [Module 26](../../course-book/module-26-declaration-files-emission-and-type-tests/index.md) before beginning.

## Runtime behavior

`createCounter(initial?)` returns an object with:

- `increment(step?)` using safe integers;
- `value()` returning the current integer;
- `close()` making later reads and writes fail.

The runtime rejects `NaN`, infinities, unsafe integers, invalid steps, and post-close operations. These invariants are narrower than TypeScript's broad `number` type and therefore require runtime tests.

## Declaration contract

Write a `.d.ts` file exposing the callable surface without inventing fields, mutability, or failure guarantees not present at runtime. Re-export the public type and function through `index.ts`, then inspect emitted declarations.

## Milestones

1. Run the JavaScript module without TypeScript and record observed behavior.
2. Write the smallest `Counter` declaration that matches it.
3. Add a TypeScript consumer test for optional arguments and return types.
4. Add rejected type tests for unsupported static calls.
5. Add runtime tests for safe-integer and lifecycle failures.
6. Deliberately make one declaration dishonest and observe the evidence gap.
7. Restore alignment and create a separate built-consumer check.
8. Compare runtime namespace exports with declaration value exports.

## Adversarial cases

Test `NaN`, `Infinity`, a fractional value, a step string, repeated close, and use after close. Distinguish which are rejected statically and which only at runtime. Do not broaden the declaration to `unknown` merely to avoid modeling the actual contract.

## Design record

Explain:

- which names exist only in the type namespace;
- which names must exist at runtime;
- why a successful `.d.ts` type check does not prove implementation alignment;
- how overload order or generic defaults could create declaration compatibility changes;
- whether errors are part of the stable public behavior.

## Independent transfer

Create a facade for an untyped date parser, checksum module, or callback API. Include at least one runtime invariant that cannot be expressed by the TypeScript primitive type alone.

## Completion standard

The built JavaScript, declaration file, consumer fixture, and runtime failure tests must all describe the same module. Source-relative shortcuts do not count as package evidence.
