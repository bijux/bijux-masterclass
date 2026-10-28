# Module 23 Reasoned Solutions

## A. Distribution

`Flag<'x' | 1 | 'y'>` becomes `{ text: 'x' } | { other: 1 } | { text: 'y' }`. The checked parameter is naked. One wrapper around the whole union uses `[T] extends [string]` or avoids a conditional entirely when the product simply wants `{ value: T }`.

## B. `never`

The function filter keeps only `() => number`; `never` contributes no member. Correct detection is:

```ts
type IsNever<T> = [T] extends [never] ? true : false;
```

The tuple prevents the empty union from distributing to no result.

## C. Extraction

Each helper should return `never` on non-match only when filtering or impossible input is the intended semantics. For a public diagnostic helper, a fallback such as `unknown` may be clearer. `infer` names the element, resolved value, first parameter, schema output, or result error already present in the matched structure.

## D. Return design

The conditional signature is acceptable only if callers gain meaningful precision and the implementation can be kept behind a simple, tested facade. Overloads are often clearer for two finite cases. A lookup map scales better when the command family is the source of truth. An assertion-heavy generic implementation is a warning sign.

## E. Recursive policy

A JSON-only transformation should accept null, string, number, Boolean, readonly arrays, and string-keyed plain objects. It should reject or preserve an explicit error marker for undefined, functions, dates, maps, and class instances. Calling the helper “DeepReadonly” without that domain would overstate its meaning.

## F. Laboratory

One command map should connect each kind to input and output. Conditional or indexed access types derive public relations. Runtime dispatch must switch or index exhaustively, and tests must fail if a new kind lacks a handler.

## G. SchemaKit

`Infer` distributes naturally over a union of schemas, producing a union of outputs. Tuple output should preserve per-index types with a mapped tuple. Optional recognition should match a deliberate `OptionalSchema` contract, not any schema whose output happens to include `undefined`; those semantics differ.

## H. Complexity

A useful review reports actual generated union size and recursive domain. “The checker handles it” is not a design argument. If a caller can state one explicit type more clearly than a recursive public computation, the explicit type may be the better API.

## I. Reconstruction standard

A complete defense connects each type branch to a runtime source of truth and names whether the helper distributes. It also identifies one case where a simpler map or overload should replace a conditional type.

## I. Distribution

`A<'a' | 1>` distributes because the checked side is the naked parameter `T`; the result is `{ text: 'a' } | { other: 1 }`. `B` wraps `T`, so it tests the union as one value and produces `{ other: 'a' | 1 }`. `C` distributes into `readonly ['a'] | readonly [1]`. `D` distributes and extracts only members matching the structural pattern; a nonmatching member contributes `never`, which disappears from the final union.

## J. Result family

The result type should branch on a stable discriminant and keep each branch small. If one command carries a schema, extract the schema output in that branch rather than adding a second free type parameter. A final `never` branch communicates exhaustiveness. If the conditional becomes a nested wall of syntax, named command-to-result helpers are preferable.

## K. Bounded recursion

A predecessor tuple gives the type computation a visible budget. Depth zero returns the input unchanged or a documented terminal representation. Functions should usually remain callable rather than having their members remapped. Arrays require a separate branch from plain objects. The bound is not merely a compiler workaround: it states how much recursive transformation the public API promises to compute.

## L. Extraction limits

`infer` extracts a component from a type that matches a pattern. It does not invent evidence and does not run on values. Overloaded functions are usually observed through their last signature in simple conditional extraction, which can surprise consumers. Unions distribute when the checked parameter is naked. `never` can erase branches; `unknown` often produces an unknown output rather than a useful guess.

## M. Better diagnostics

Naming `CommandByKind<K>` and `OutcomeForCommand<C>` creates smaller declaration fragments and error messages. A caller can see whether the mismatch occurred while selecting a command or computing its result. The public design should optimize for comprehensible relationships, not type-golf density.
