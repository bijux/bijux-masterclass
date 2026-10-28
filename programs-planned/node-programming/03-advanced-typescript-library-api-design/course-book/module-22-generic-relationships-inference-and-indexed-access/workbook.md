# Module 22 Workbook

For every generic below, write one sentence beginning: “This parameter relates …” If you cannot finish the sentence, simplify the API.

## A. Remove meaningless generics

Review:

```ts
function count<T>(values: readonly T[]): number {
  return values.length;
}

function debug<T>(value: T): string {
  return JSON.stringify(value);
}

function repeat<T>(value: T, count: number): T[] {
  return Array.from({ length: count }, () => value);
}
```

Which parameters preserve useful output information? Rewrite the others with the weakest honest input type.

## B. Trace inference

Predict the inferred types:

```ts
function pair<A, B>(a: A, b: B): readonly [A, B] {
  return [a, b];
}

const p = pair('ready', 3);
```

```ts
function mapOne<T, U>(value: T, f: (value: T) => U): U {
  return f(value);
}

const r = mapOne({ id: 'u1', active: true }, (value) => value.id);
```

```ts
function define<const T extends readonly string[]>(value: T): T {
  return value;
}

const d = define(['a', 'b']);
```

For each parameter, identify the selection site.

## C. Key/value relation

Implement:

```ts
function pluck<T, K extends keyof T>(
  values: readonly T[],
  key: K,
): T[K][];
```

Then explain why this return is weaker:

```ts
T[keyof T][]
```

Add tests for a union-valued field and an optional field.

## D. Ordered tuple projection

Define:

```ts
type ValuesFor<T, Keys extends readonly (keyof T)[]> = ...
```

Required examples:

```ts
const user = { id: 'u1', age: 36, active: true } as const;
const row = valuesFor(user, ['age', 'id'] as const);
// readonly [36, 'u1']
```

Document the implementation assertion and the runtime facts that justify it.

## E. Selection versus checking

Design a `pickDefault` API where the option tuple selects a finite union and the fallback must belong to it. Compare:

- one generic parameter inferred from both positions;
- `NoInfer` on the fallback;
- an explicit type argument;
- runtime membership validation.

Which facts are static, and which remain runtime?

## F. Independent laboratory

Complete [Typed Projection Engine](../../labs/module-22-typed-projection-engine/README.md). Include object projection, ordered tuple values, duplicate-key policy, symbol keys, and declaration tests.

## G. SchemaKit transfer

Add:

- `Schema<out T>`;
- `AnySchema`;
- `Infer<S>`;
- `literal` preserving literal values;
- primitive schema constructors;
- type tests proving exact outputs.

Do not implement object or union schemas yet.

## H. API review

For each proposed signature, decide generic, overload, union, or concrete type:

```ts
function parse<T>(text: string): T;
function length<T extends { length: number }>(value: T): number;
function combine<T>(left: T, right: T): T[];
function decode(value: string | Uint8Array): string;
```

Explain the runtime witness and the relationship preserved.

## I. Reconstruction

Without notes, define inference, constraint, default, explicit argument, indexed access, and `NoInfer`. Give one SchemaKit example for each.

## I. Inference ownership table

For each function, identify which argument should determine `T`, which arguments merely must conform to it, and whether `NoInfer` is justified:

```ts
merge(defaults, override)
choose(value, fallback)
register(handler, example)
compare(left, right)
```

A useful answer explains observable caller behavior. “It fixes inference” is not sufficient.

## J. Projection with symbols and tuples

Extend the projection engine so a const tuple may contain string, number, or symbol keys. Preserve tuple order in `valuesFor` and key identity in `project`. Add a symbol-key test and explain why `Object.keys` is not a complete implementation for `keyof`.

## K. Dynamic key validation

Implement:

```ts
function hasOwnKey<T extends object>(
  value: T,
  key: PropertyKey,
): key is keyof T;
```

Then explain the limits of this predicate. Which keys can exist at runtime but not appear in a useful declared type? What happens when the object is mutated after the check? When should a parser convert an external string into a finite application key instead?

## L. Generic overdesign clinic

Rewrite these signatures so every type parameter communicates a real relationship:

```ts
function label<T>(value: string): string;
function parse<T>(input: unknown): T;
function pair<A, B>(left: A, right: A): readonly [A, B];
function keys<T extends object, K extends keyof T>(value: T): K[];
```

For each removed or repaired parameter, state what false promise the old signature made.

## M. Indexed-access failure audit

With `noUncheckedIndexedAccess`, compare:

- selecting a known `keyof T`;
- reading `Record<string, V>`;
- indexing a tuple with a known literal;
- indexing an array with `number`;
- indexing after a runtime bounds check.

Design return types that preserve uncertainty rather than deleting it with `!`.
