# Module 24 — Mapped Types, Key Remapping, and Template-Literal Types

> **Question:** When should a family of related object contracts be derived from one source type, and when does clever type generation become a second language to maintain?

## Why this comes now

Conditional types choose a type-level branch. Mapped types iterate a key set. Template-literal types construct finite string families. Together they let a library derive related public surfaces from one authority:

- readonly views from mutable records;
- patch types from domain models;
- event names from property names;
- parser outputs from schema shapes;
- getter or command interfaces from a finite declaration;
- route parameter names from a route pattern.

The benefit is not fewer keystrokes. The benefit is removing duplicated relationships. The cost is that generated types can become difficult to read, expensive to instantiate, and easy to detach from runtime code. This module therefore treats every mapped type as a small compiler with an input key set, a transformation rule, and an output contract.

## Outcomes

By the end of the module, you can:

- derive object types by mapping a finite key union;
- add and remove optional and readonly modifiers deliberately;
- filter or rename keys with an `as` clause;
- use template-literal types to build bounded string protocols;
- predict cross-product growth when interpolated positions contain unions;
- preserve required and optional SchemaKit object fields consistently;
- distinguish a type-derived event surface from the runtime registration table that implements it;
- reject type-level DSLs whose generated surface is harder to understand than explicit declarations.

## 1. A mapped type iterates a key union

```ts
interface User {
  readonly id: string;
  name: string;
  age?: number;
}

type Flags<T> = {
  [K in keyof T]: boolean;
};

type UserFlags = Flags<User>;
```

The transformation is:

```text
input keys:  'id' | 'name' | 'age'
for each K:  output property K with value boolean
modifiers:   preserved unless changed
```

Because modifiers are preserved by default, `id` remains readonly and `age` remains optional in `Flags<User>`. This surprises readers who expected a plain required Boolean record.

State modifier policy explicitly.

## 2. Add and remove modifiers

```ts
type MutableRequired<T> = {
  -readonly [K in keyof T]-?: T[K];
};

type ReadonlyOptional<T> = {
  readonly [K in keyof T]?: T[K];
};
```

The `-` form removes a modifier; omitted or `+` adds/preserves according to syntax.

A patch type is often written:

```ts
type Patch<T> = {
  [K in keyof T]?: T[K];
};
```

But a universal patch type can be semantically weak. It may allow updates to identifiers, derived fields, version tags, or mutually dependent fields. A domain patch should filter keys and possibly model related updates as a discriminated union.

Mapped syntax does not supply domain policy.

## 3. Key remapping

TypeScript supports an `as` clause inside a mapped type:

```ts
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

`string & K` filters the interpolation to string-like keys. Symbol keys cannot be converted into template-literal names without losing identity.

For:

```ts
interface Profile {
  name: string;
  active: boolean;
}
```

`Getters<Profile>` becomes:

```ts
{
  getName(): string;
  getActive(): boolean;
}
```

The runtime object still has to implement those methods. Type generation does not create JavaScript members.

## 4. Filter keys by producing `never`

```ts
type FunctionKeys<T> = {
  [K in keyof T]-?: T[K] extends (...args: never[]) => unknown ? K : never;
}[keyof T];
```

The inner mapped type produces one key or `never` per property. Indexed access collects the values into a union, and `never` disappears.

Key remapping can filter directly:

```ts
type DataOnly<T> = {
  [K in keyof T as T[K] extends (...args: never[]) => unknown ? never : K]: T[K];
};
```

Document whether optional function properties, overloaded methods, or unions containing functions should be filtered. The conditional encodes a policy that may need refinement.

## 5. Template-literal types form finite string sets

```ts
type Field = 'name' | 'active';
type EventName = `${Field}Changed`;
// 'nameChanged' | 'activeChanged'
```

Each union in an interpolated position participates in a cross product:

```ts
type Phase = 'before' | 'after';
type Event = `${Phase}:${Field}`;
// four members
```

Three unions of sizes 5, 8, and 4 create 160 strings. This may still be manageable, but the public diagnostics and editor completion surface grow with it. For large or open domains, use a branded string plus runtime validation rather than enumerating every combination.

## 6. Derive event callback values

```ts
type ChangeEvents<T> = {
  [K in keyof T as K extends string ? `${K}Changed` : never]:
    (next: T[K], previous: T[K]) => void;
};
```

The key name and callback value remain related. A runtime event hub can expose:

```ts
type EventName<T> = keyof ChangeEvents<T>;

type EventHandler<T, E extends EventName<T>> = ChangeEvents<T>[E];
```

The implementation needs a runtime mapping from event string back to source property or must receive both explicitly. Avoid parsing generated names with fragile string slicing if an internal table can preserve the relation.

## 7. Exact optionality in mapped output

Consider a schema shape:

```ts
interface OptionalSchema<T> extends Schema<T | undefined> {
  readonly optional: true;
  readonly inner: Schema<T>;
}

type Shape = Readonly<Record<string, Schema<unknown>>>;
```

The output should contain required properties for ordinary schemas and optional properties for `OptionalSchema` entries. First derive the key sets:

```ts
type OptionalKeys<S extends Shape> = {
  [K in keyof S]-?: S[K] extends OptionalSchema<unknown> ? K : never;
}[keyof S];

type RequiredKeys<S extends Shape> = Exclude<keyof S, OptionalKeys<S>>;
```

Then build the output:

```ts
type ObjectOutput<S extends Shape> =
  { readonly [K in RequiredKeys<S>]: Infer<S[K]> } &
  { readonly [K in OptionalKeys<S>]?:
      S[K] extends OptionalSchema<infer T> ? T : never };
```

This reflects the runtime policy: a missing optional key is omitted. It is not emitted as a required property whose value is `undefined`.

Intersections can display poorly in editor hovers. A `Simplify<T>` helper may improve display:

```ts
type Simplify<T> = { [K in keyof T]: T[K] } & {};
```

Use it for readability, not as a claim of exactness.

## 8. Key domains include symbols and numbers

`keyof` may contain string, number, and symbol forms. Template-literal remapping only makes sense for strings or numbers converted deliberately.

```ts
type StringKeys<T> = Extract<keyof T, string>;
```

Do not silently stringify symbol keys. Symbols carry identity, not only descriptions. A public mapped API should state whether it supports:

- string keys only;
- numeric tuple indexes;
- symbols;
- inherited runtime keys;
- open index signatures.

Type-level keys do not by themselves specify runtime enumeration.

## 9. Mapped tuples and arrays

Mapped types preserve tuple structure in many common transformations:

```ts
type Promises<T extends readonly unknown[]> = {
  [I in keyof T]: Promise<T[I]>;
};

type R = Promises<readonly [string, number]>;
// readonly [Promise<string>, Promise<number>]
```

A tuple has additional keys such as `length` and methods, but TypeScript provides tuple-aware behavior for mapped types over `keyof T`. Do not assume every elaborate key remapping preserves tuple identity. Test the exact helper and inspect emitted declarations.

SchemaKit uses mapped tuples to infer tuple-schema output.

## 10. Recursive path types: useful and dangerous

A path helper can derive strings such as `owner.name`:

```ts
type Paths<T> = T extends object ? {
  [K in Extract<keyof T, string>]:
    T[K] extends object ? K | `${K}.${Paths<T[K]>}` : K
}[Extract<keyof T, string>] : never;
```

This simple form mishandles arrays, dates, maps, class instances, cycles, optional values, and large object graphs. It can also create huge unions.

For public validation errors, SchemaKit uses runtime path arrays:

```ts
readonly (string | number)[]
```

The library does not promise a compile-time enumeration of every possible nested path. The runtime path is more general, cheaper, and aligned with unknown input.

A type should not be generated merely because generation is possible.

## 11. Derived public APIs and compatibility

A mapped public type changes when its source changes. Adding a source field may:

- add a required getter;
- add an event name;
- add a patch property;
- enlarge a template-literal union;
- make a downstream exhaustive mapping incomplete.

Therefore, “derived automatically” does not mean “compatible automatically.” The source type becomes an authority whose evolution has multiplied effects.

Document this coupling and test representative downstream uses.

## 12. Runtime implementation of a generated event surface

The laboratory implements a finite change-event API. A sound design keeps one runtime declaration:

```ts
const fields = ['name', 'active'] as const;
```

Then derives:

- the field union;
- event-name union;
- callback argument types;
- runtime registration validation.

However, a heterogeneous model cannot be fully recovered from a runtime string without a table or trusted construction. The implementation may store handlers by original field key and generate public names at the boundary.

Never cast an arbitrary string to the generated event-name type before validating it.

## 13. Type-level string parsing

Template literals can parse finite patterns:

```ts
type RouteParam<S extends string> =
  S extends `${string}:${infer Param}/${infer Rest}`
    ? Param | RouteParam<Rest>
    : S extends `${string}:${infer Param}`
      ? Param
      : never;
```

This may be appropriate for a route library whose runtime parser follows the same grammar. It is not validation of an arbitrary runtime route string unless the value remains a literal and the runtime also checks it.

Prefer small grammar helpers with tests. Deep template recursion is difficult to diagnose and will reappear in declarations.

## 14. A transformation ledger

For every mapped/template type, record:

| Question | Record |
|---|---|
| source authority | Which type owns the facts? |
| input keys | Finite union, tuple indexes, open signature? |
| value rule | Preserve, replace, wrap, conditionally transform? |
| modifier rule | Required/optional, readonly/mutable? |
| key rule | Preserve, filter, rename, stringify? |
| union growth | How many generated members? |
| runtime counterpart | What creates/validates the actual keys? |
| compatibility effect | What happens when the source gains a key? |
| declaration quality | Is the emitted type readable? |
| simpler alternative | Explicit interface or runtime map? |

## 15. Common wrong models

### “Mapped types copy runtime objects”

They only compute static object types.

### “`Partial<T>` is a valid update model for every domain”

It often allows forbidden or inconsistent updates.

### “Template-literal unions validate strings”

They check statically known strings. Runtime strings still require validation.

### “Generated fields are automatically compatible additions”

Downstream exhaustive mappings and required implementations can break.

### “Symbols can be treated as string names”

Stringification loses symbol identity.

### “A recursive path type is free documentation”

It can be inaccurate, expensive, and harder to maintain than a runtime path model.

## 16. Use the idea in a complete program

Module 24 adds to SchemaKit:

- `Shape` and object-schema output mapping;
- exact required/optional key derivation;
- tuple-output mapping;
- readonly public results;
- bounded path rendering at runtime rather than recursive path enumeration;
- public helper types that do not expose internal decoder state.

The event-surface lab applies mapped and template types to callbacks instead of schemas.

## Practice sequence

1. Write key and modifier tables for the workbook transformations.
2. Predict the eight Module 24 investigations.
3. Measure one template-literal cross product before implementing it.
4. Complete [Typed Change Event Surface](../../labs/module-24-typed-change-event-surface/README.md).
5. Implement the Module 24 SchemaKit object mapping in [the capstone guide](../capstone.md#module-24--mapped-object-output).
6. Inspect the emitted object-schema declarations for readability.

## Ready to continue

You are ready for Module 25 when you can explain:

- default modifier preservation;
- required/optional key derivation;
- key filtering through `never`;
- why template-literal types create cross products;
- why runtime tables remain necessary;
- how source-type evolution affects generated public APIs;
- why SchemaKit uses runtime issue paths rather than a universal recursive path union.

Next: [Variance, Function Types, and Callback Safety](../module-25-variance-function-types-and-callback-safety/index.md).

## 15. Collision analysis is mandatory

Key remapping can map two source keys to one target key. TypeScript may combine the resulting property types, but the runtime generator still needs an explicit collision policy. Before publishing a remapped family, construct the reverse map:

```text
target name → contributing source keys
```

A target with more than one source requires rejection, disambiguation, or a deliberate combined contract. Ignoring collisions turns a concise mapped type into an ambiguous runtime API.

## 16. Generated families need a size budget

Template-literal unions multiply. If one dimension contains 20 members and another contains 15, the cross product already contains 300 names. That cost appears in declarations, editor completion, diagnostics, and checker work. Prefer runtime validation when the generated space is open, large, or rarely inspected as individual literals. The strongest design is not the one that computes the most names; it is the one that makes the useful finite relationship clear.
