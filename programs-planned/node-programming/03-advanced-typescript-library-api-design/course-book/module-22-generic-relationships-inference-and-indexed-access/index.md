# Module 22 — Generic Relationships, Inference, and Indexed Access

> **Question:** How do you preserve a relationship among inputs and outputs without inventing a generic parameter that communicates nothing?

## Why this comes now

Module 21 taught you to read assignability from source to target. A generic API extends that question across several uses of the same operation. Instead of describing one concrete source and target, a generic declaration says:

> For every type that satisfies these requirements, these positions remain related in this way.

That sentence is more important than angle-bracket syntax. Weak generic APIs often contain a type parameter merely because the author wants the API to look reusable. The parameter appears once, is immediately widened by a constraint, or forces callers to supply a type argument that the implementation cannot verify. Strong generic APIs preserve a relationship that would otherwise be lost:

- a selected key determines a selected value type;
- a tuple of keys determines a projected object type;
- a schema determines its validated output;
- a function stage determines the next stage's input;
- a constructor determines the instance it creates.

This module develops a disciplined inference model used by conditional types, schema combinators, and public package APIs later in the course.

## Outcomes

By the end of the module, you can:

- state the relationship represented by every type parameter;
- distinguish inference from constraints, defaults, and explicit arguments;
- trace inference from argument, contextual, return, and callback positions;
- preserve literal tuples with `const` type parameters;
- use `keyof` and indexed access to connect keys with property types;
- choose among a generic, an overload set, a union, and an ordinary concrete function;
- use `NoInfer` to prevent one argument from changing an already selected type;
- recognize generic parameters that add no information;
- design `Schema<T>` and `Infer<S>` as relationships rather than decorative abstractions.

## 1. A type parameter is a named relationship

Consider three functions:

```ts
function identity<T>(value: T): T {
  return value;
}

function logAndReturn<T>(value: T): T {
  console.log(value);
  return value;
}

function stringify<T>(value: T): string {
  return String(value);
}
```

The first two use `T` to relate input and output. The third uses `T` only once in a meaningful public position. It gains almost nothing from being generic:

```ts
function stringify(value: unknown): string {
  return String(value);
}
```

A useful review question is:

> If I replace this type parameter with its constraint, what relationship disappears?

If the answer is “none,” remove the parameter.

## 2. Inference selects a candidate; a constraint checks it

```ts
function lengthOf<T extends { length: number }>(value: T): number {
  return value.length;
}
```

For `lengthOf('abc')`, inference chooses `string` for `T`. The constraint then checks whether `string` has a numeric `length`. The constraint does not replace `T` with `{ length: number }`; it establishes which operations the implementation may perform.

That distinction matters when returning the input:

```ts
function keep<T extends { length: number }>(value: T): T {
  return value;
}

const kept = keep({ length: 2, label: 'pair' });
// label remains present in the inferred type.
```

A common weak repair changes `T` to the constraint in the return type and loses information:

```ts
function weak(value: { length: number }): { length: number } {
  return value;
}
```

Both functions run, but only the generic one preserves the caller's specific shape.

## 3. Inference sites

TypeScript can gather candidates from several places.

### Direct arguments

```ts
function first<T>(values: readonly T[]): T | undefined {
  return values[0];
}

const result = first([1, 2, 3]); // number | undefined
```

### Multiple arguments

```ts
function pair<T>(left: T, right: T): readonly [T, T] {
  return [left, right];
}
```

Both arguments contribute candidates. Depending on context and literal widening, the inferred type may be a common supertype or a union. If the arguments are semantically allowed to differ, use two parameters:

```ts
function pair<A, B>(left: A, right: B): readonly [A, B] {
  return [left, right];
}
```

One type parameter means “same relationship,” not “two arbitrary unknown things.”

### Callback positions

```ts
function mapOne<T, U>(value: T, transform: (value: T) => U): U {
  return transform(value);
}

const count = mapOne('rust', (text) => text.length);
```

`T` is inferred from the first argument and contextualizes the callback parameter. `U` is inferred from the callback return.

### Contextual return position

A surrounding target can influence inference in some APIs:

```ts
function empty<T>(): T[] {
  return [];
}

const names: string[] = empty();
```

Do not rely on subtle contextual inference when a public API can state a clearer argument relationship. An argument such as a schema or constructor usually produces better evidence than an unconstrained explicit type argument.

## 4. Explicit type arguments are instructions, not validation

```ts
function parseUnsafe<T>(text: string): T {
  return JSON.parse(text) as T;
}

const user = parseUnsafe<{ name: string }>('42');
```

The caller selected `T`; no runtime operation established it. A generic return type without an input witness is often a disguised assertion.

Compare a schema-guided parser:

```ts
interface Schema<T> {
  parse(input: unknown): T;
}

function parseWith<T>(schema: Schema<T>, input: unknown): T {
  return schema.parse(input);
}
```

Here `T` is inferred from a runtime object whose contract promises how validation occurs. The implementation still has to make that promise true, but the public relationship is meaningful.

## 5. `keyof` creates a finite key domain

```ts
interface User {
  readonly id: string;
  readonly age: number;
}

type UserKey = keyof User; // 'id' | 'age'
```

A generic selector can connect a key to its value:

```ts
function get<T, K extends keyof T>(value: T, key: K): T[K] {
  return value[key];
}

const user: User = { id: 'u1', age: 36 };
const id = get(user, 'id');   // string
const age = get(user, 'age'); // number
```

Replacing `K` with `keyof T` weakens the return:

```ts
function weakGet<T>(value: T, key: keyof T): T[keyof T] {
  return value[key];
}
```

For `User`, the return becomes `string | number` because the key/value correlation is lost. `K` exists to preserve that correlation.

## 6. Indexed access is a projection, not a runtime read

`T[K]` computes the property type associated with a type-level key. It does not perform a JavaScript lookup and does not prove an own property exists.

```ts
type UserId = User['id']; // string
```

When `K` is a union, the result is the union of selected property types:

```ts
type UserField = User['id' | 'age']; // string | number
```

For arrays and tuples:

```ts
type Element<T extends readonly unknown[]> = T[number];
type Names = Element<readonly ['Ada', 'Grace']>; // 'Ada' | 'Grace'
```

This pattern becomes central when a tuple of keys should determine a projected object.

## 7. Preserve key tuples, not only key unions

Suppose a query API accepts ordered fields:

```ts
function project<T, K extends keyof T>(
  value: T,
  keys: readonly K[],
): Pick<T, K> {
  // implementation omitted
  throw new Error('not implemented');
}
```

The result preserves the selected key set, but the type does not preserve tuple order or duplicates. If the product needs an ordered row, return a tuple:

```ts
type ValuesFor<T, Keys extends readonly (keyof T)[]> = {
  readonly [I in keyof Keys]: Keys[I] extends keyof T ? T[Keys[I]] : never;
};

function valuesFor<T, const Keys extends readonly (keyof T)[]>(
  value: T,
  keys: Keys,
): ValuesFor<T, Keys> {
  return keys.map((key) => value[key]) as ValuesFor<T, Keys>;
}
```

The assertion is localized around an implementation limitation: ordinary `map` does not preserve tuple length and per-index correlation. The public type is justified by the iteration over exactly the supplied keys. The lab requires you to document and test that proof.

Do not return a tuple when order has no product meaning. `Pick<T, K[number]>` is simpler for unordered projection.

## 8. `const` type parameters preserve declaration intent

Without a `const` type parameter, array literals may widen:

```ts
function names<Names extends readonly string[]>(values: Names): Names {
  return values;
}
```

Modern TypeScript lets the API request literal-style inference:

```ts
function names<const Names extends readonly string[]>(values: Names): Names {
  return values;
}

const declared = names(['parse', 'render']);
// readonly ['parse', 'render']
```

Use `const` parameters for declaration-like APIs: route tables, command catalogs, schema tuples, or finite registries. Avoid them when callers expect mutable general collections or when preserving every literal creates enormous public types.

## 9. Generic defaults are fallback selections

```ts
interface Result<T, E = Error> {
  readonly value?: T;
  readonly error?: E;
}
```

A default is used when inference and explicit arguments do not select the parameter. It does not mean the parameter is optional at runtime. Defaults can improve ergonomics, but they also become public compatibility commitments. Changing a default can change downstream inferred types without changing source syntax.

Place required parameters before defaulted parameters. A default should represent the common case, not hide an underspecified relationship.

## 10. `NoInfer` separates selection from checking

Sometimes one argument should select a type and another should merely be checked against it.

```ts
function choose<C extends string>(
  options: readonly C[],
  fallback: NoInfer<C>,
): C {
  return options.includes(fallback) ? fallback : options[0]!;
}

choose(['red', 'green'] as const, 'red');
// choose(['red', 'green'] as const, 'blue'); // rejected
```

Without `NoInfer`, the fallback might contribute a wider candidate and make `C` include `'blue'`. The utility says: infer `C` elsewhere, then check this position.

Use it sparingly. If readers cannot identify the selecting argument and the checked argument, the API may be too implicit.

## 11. Constraints should grant only required operations

This is overconstrained:

```ts
function findById<T extends { id: string; name: string; createdAt: Date }>(
  values: readonly T[],
  id: string,
): T | undefined {
  return values.find((value) => value.id === id);
}
```

The implementation uses only `id`. The additional requirements reject valid callers and create accidental compatibility commitments.

Prefer:

```ts
function findById<T extends { id: string }>(
  values: readonly T[],
  id: string,
): T | undefined {
  return values.find((value) => value.id === id);
}
```

The weakest sufficient constraint improves reuse and documents actual dependence.

## 12. Overloads, unions, and generics solve different problems

Use a generic when one relationship works uniformly:

```ts
function wrap<T>(value: T): { value: T };
```

Use overloads when a finite set of call shapes has distinct externally visible results and one implementation can safely handle them:

```ts
function parse(value: string): string;
function parse(value: Uint8Array): string;
function parse(value: string | Uint8Array): string {
  return typeof value === 'string' ? value : new TextDecoder().decode(value);
}
```

Use a union when the implementation and caller should handle the alternatives directly:

```ts
function length(value: string | readonly unknown[]): number {
  return value.length;
}
```

Do not replace a simple union with a conditional generic merely to produce a narrower return if the runtime branches are not meaningfully related.

## 13. Generic classes and interfaces carry long-lived relationships

```ts
interface Repository<Entity, Id> {
  get(id: Id): Entity | undefined;
  save(entity: Entity): void;
}
```

The two parameters are justified because operations repeatedly connect them. But a public repository type also raises variance and mutation questions: it consumes and produces `Entity`, so it is not safely covariant. Module 25 returns to this.

SchemaKit's central contract is simpler:

```ts
export interface Schema<out T> {
  readonly kind: string;
  safeParse(input: unknown): ParseResult<T>;
  parse(input: unknown): T;
}
```

The schema consumes `unknown`, not `T`, and produces `T`, so covariance is the intended direction. The implementation's internal decoder can remain private.

## 14. Derive, do not repeat

A poor schema API asks callers to state the type twice:

```ts
const userSchema: Schema<User> = object({
  id: string(),
  age: number(),
});
```

If the schema and `User` drift, an assertion or broad structural match may hide the inconsistency. Instead derive the output:

```ts
type Infer<S extends Schema<unknown>> =
  S extends Schema<infer T> ? T : never;

const userSchema = object({
  id: string(),
  age: number(),
});

type User = Infer<typeof userSchema>;
```

The runtime schema becomes the source of truth for external validation. This does not mean every internal domain type must be schema-derived. Choose one authority per fact.

## 15. Inference failure is information

When inference produces `unknown`, `never`, or an unexpectedly broad union, do not immediately add explicit type arguments. Ask:

- Which input was supposed to select the parameter?
- Did a broad annotation erase a literal?
- Are two arguments competing to infer one parameter?
- Is the parameter used only in a return position?
- Did a callback lack contextual typing?
- Is an overload a clearer surface?
- Is the desired relationship actually valid?

An explicit type argument can be legitimate, but it should not conceal a missing runtime witness or a poorly expressed relation.

## 16. A generic relationship ledger

For each parameter, record:

| Question | Example |
|---|---|
| name | `T`, `K`, `Output` |
| semantic role | record type, selected key, parsed result |
| selection sites | first argument, schema argument, callback return |
| checking-only sites | fallback, default, comparator |
| constraint | operations implementation requires |
| default | common fallback selection |
| output positions | return, property, callback argument |
| literal preservation | `const` parameter needed? |
| runtime witness | schema, constructor, key lookup, or none |
| compatibility risk | constraint/default/inference change |

If the semantic role cannot be stated, redesign before adding more type machinery.

## 17. Common wrong models

### “Generic means accepts anything”

A generic preserves a relation across many allowed types. `unknown` accepts anything without preserving a caller-specific type.

### “A constraint is the inferred type”

The candidate remains specific; the constraint only checks required capability.

### “Explicit `T` validates the return”

Callers can select unsupported types unless a runtime witness proves the relation.

### “`keyof T` and `K extends keyof T` are equivalent”

The separate `K` preserves the chosen key and therefore `T[K]`.

### “More parameters make an API more precise”

Each parameter increases inference and compatibility complexity. Keep only real relationships.

### “A tuple-preserving assertion is automatically safe”

The implementation must iterate exactly the supplied tuple without reordering, dropping, or inserting values.

## 18. Use the idea in a complete program

Module 22 adds to SchemaKit:

- covariant `Schema<T>`;
- `AnySchema`;
- `Infer<S>`;
- `safeParse` and `parse` relation;
- literal-preserving `literal<const V extends ...>(value: V)`;
- tuple schema declarations that preserve element positions;
- type tests showing that one schema selects one output type.

The independent projection lab requires a different relation: a tuple of keys determines both a projected object and an ordered value tuple.

## Practice sequence

1. Name the relationship in every workbook generic before writing syntax.
2. Predict the eight Module 22 investigations.
3. Remove one meaningless type parameter from an existing helper.
4. Complete [Typed Projection Engine](../../labs/module-22-typed-projection-engine/README.md).
5. Implement the Module 22 SchemaKit increment in [the capstone guide](../capstone.md#module-22--schema-and-inference).
6. Inspect the emitted declaration and confirm that internal decoder details are absent.

## Ready to continue

You are ready for Module 23 when you can explain:

- inference candidate versus constraint;
- why a type parameter should appear in a real relation;
- how `K extends keyof T` preserves a selected value type;
- when `const` type parameters are useful;
- why a generic return without an input witness is suspicious;
- how `NoInfer` separates selection from checking;
- why `Infer<S>` should derive rather than duplicate a schema output.

Next: [Conditional Types, infer, and Type-Level Control Flow](../module-23-conditional-types-infer-and-type-level-control-flow/index.md).
