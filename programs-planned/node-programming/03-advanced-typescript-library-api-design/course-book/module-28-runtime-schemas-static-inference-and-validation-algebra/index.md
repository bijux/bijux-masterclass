# Module 28 — Runtime Schemas, Static Inference, and Validation Algebra

> **Question:** How can one runtime description validate unknown data and also produce a precise static type without pretending that either side proves the other?

## Why this comes now

Course 1 introduced runtime validation. Course 3 has now established structural types, generic inference, conditional extraction, mapped object outputs, variance, declarations, and package boundaries. Those mechanisms can be combined into a schema library—but only if runtime truth remains primary at the external boundary.

A schema combinator library has two synchronized products:

```text
runtime parser: unknown → success or issues
static relation: schema value → inferred success type
```

The static relation is useful because callers do not repeat types. The runtime parser is necessary because external values are not checked by TypeScript. Neither surface may be treated as a substitute for the other.

This module completes SchemaKit's core validation algebra.

## Outcomes

By the end of the module, you can:

- define a schema as a runtime validator that produces one static output;
- separate parse success from structured failure;
- carry bounded path context through nested validation;
- implement primitive, literal, optional, nullable, array, tuple, object, record, union, refine, transform, and lazy schemas;
- align optional-property runtime behavior with `exactOptionalPropertyTypes`;
- bound union diagnostics and avoid retaining arbitrary rejected values;
- distinguish validation, refinement, transformation, parsing, and migration;
- prove inferred outputs through type tests and runtime results through adversarial tests;
- recognize when a schema library becomes an unbounded language of its own.

## 1. The schema contract

A minimal public contract is:

```ts
export interface Schema<out T> {
  readonly kind: string;
  safeParse(input: unknown): ParseResult<T>;
  parse(input: unknown): T;
}
```

`safeParse` returns data; `parse` throws a library error on failure. Both operations must use the same internal decoder so their behavior cannot drift.

The internal contract can carry path state:

```ts
type Decode<T> = (
  input: unknown,
  path: readonly PathSegment[],
) => ParseResult<T>;
```

Do not expose `Decode<T>` publicly. It is implementation authority, not consumer capability.

## 2. Results must prevent contradictory states

```ts
export type ParseResult<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly issues: readonly Issue[] };
```

The success branch has no issues. The failure branch has no value. An empty issue list on failure should be impossible by construction.

```ts
function failure(issue: Issue): ParseResult<never> {
  return { ok: false, issues: [issue] };
}
```

A library may choose fail-fast or accumulated issues. SchemaKit accumulates independent object-field issues but bounds union alternatives and collection issue count to avoid diagnostic explosion.

## 3. Paths are runtime evidence

```ts
export type PathSegment = string | number;

export interface Issue {
  readonly path: readonly PathSegment[];
  readonly code: string;
  readonly message: string;
}
```

Nested schemas append a segment:

```ts
const childPath = [...path, key];
```

The public issue contains no complete rejected value. Large input retention and secret exposure are product risks. If a preview is useful, bound its length and redact according to policy.

A runtime path array is more honest than a universal recursive compile-time path union. External data may fail at array indexes or keys not represented by a known domain type.

## 4. Primitive schemas

A string schema checks `typeof input === 'string'`. It should not coerce numbers or objects unless coercion is a separate named combinator.

```ts
export const string = (): Schema<string> =>
  makeSchema('string', (input, path) =>
    typeof input === 'string'
      ? success(input)
      : issue(path, 'type.string', 'expected a string'));
```

The same pattern applies to Boolean. Number validation should decide whether `NaN` and infinities are accepted. SchemaKit's ordinary number schema accepts only finite numbers:

```ts
typeof input === 'number' && Number.isFinite(input)
```

This is product policy, not a TypeScript rule.

## 5. Literal schemas preserve exact values

```ts
export function literal<const V extends string | number | boolean | null>(
  expected: V,
): Schema<V>;
```

The `const` parameter preserves the literal. Runtime validation uses `Object.is` or a documented equality policy.

Literal schemas are building blocks for discriminated models and version tags. They should not accept arbitrary objects because reference identity would make declarations misleading and serialization unstable.

## 6. Optional and nullable are different

`nullable(schema)` accepts `null` as a value. `optional(schema)` describes missing object-property behavior.

A naïve optional schema that simply returns `T | undefined` cannot distinguish:

- property missing;
- property present with `undefined`;
- array element `undefined`;
- top-level `undefined`.

SchemaKit represents optionality with a specific wrapper:

```ts
export interface OptionalSchema<out T> extends Schema<T | undefined> {
  readonly optional: true;
  readonly inner: Schema<T>;
}
```

The object parser inspects own-property presence. If missing, it omits the property. If present, it validates with `inner`; present `undefined` therefore fails unless the inner schema accepts it deliberately.

Outside object shapes, calling an optional schema directly may accept `undefined`; the documentation distinguishes these contexts.

## 7. Arrays validate incrementally and bound issues

```ts
export function array<S extends Schema<unknown>>(
  item: S,
  options?: { readonly maxLength?: number },
): Schema<readonly Infer<S>[]>;
```

Runtime procedure:

1. require an array;
2. validate length before allocating output;
3. iterate indexes in source order;
4. validate each item with path `[..., index]`;
5. accumulate issues up to a configured bound;
6. return a new readonly view/copy on success.

Do not retain the external array as trusted output. Copying separates later mutation by the caller from the validated result.

## 8. Tuple schemas preserve position

```ts
type TupleOutput<S extends readonly Schema<unknown>[]> = {
  readonly [I in keyof S]: Infer<S[I]>;
};

export function tuple<const S extends readonly Schema<unknown>[]>(
  items: S,
): Schema<TupleOutput<S>>;
```

Runtime validation requires exact length unless the product explicitly supports rest elements. Each position has its own schema and path index.

The internal implementation may require a localized assertion because ordinary array accumulation loses per-index correlation. The proof is the exact one-to-one traversal over the fixed schema tuple.

## 9. Object schemas need an unknown-key policy

```ts
type Shape = Readonly<Record<string, Schema<unknown>>>;

type UnknownKeys = 'reject' | 'strip';
```

SchemaKit checks that input is a supported plain record, then:

- validates required own properties;
- omits missing optional properties;
- validates present optional properties with their inner schema;
- rejects or strips unknown own string keys;
- ignores inherited properties;
- returns a new result object;
- exposes readonly output types.

The library does not silently preserve unknown keys because the output type would not describe them. A future `passthrough` mode would require an explicit output model.

## 10. Plain-object policy

`typeof value === 'object' && value !== null` also accepts arrays, dates, maps, class instances, proxies, and many host objects.

SchemaKit's plain-record check accepts objects whose prototype is `Object.prototype` or `null`. It rejects arrays and branded class instances. This keeps enumeration and persistence behavior predictable.

Even a plain-object check can trigger proxy traps. The library is not a sandbox against hostile JavaScript objects; it validates data-shaped values. Security boundaries should parse serialized formats or isolate untrusted code.

## 11. Records and open key domains

```ts
export function record<S extends Schema<unknown>>(
  valueSchema: S,
): Schema<Readonly<Record<string, Infer<S>>>>;
```

A record schema accepts an open string key domain under a key policy. It should reject dangerous keys if the result uses ordinary objects, or construct a null-prototype result.

SchemaKit returns a frozen/null-prototype dictionary view and validates own enumerable string keys in deterministic order. It does not claim every possible key exists; reads remain potentially undefined under strict indexed access.

## 12. Union schemas are runtime search

```ts
export function union<const S extends readonly [Schema<unknown>, ...Schema<unknown>[]]>(
  members: S,
): Schema<Infer<S[number]>>;
```

Runtime behavior must be defined:

- try members in declaration order;
- return the first success;
- on total failure, report a union issue and a bounded summary of member issues;
- avoid exposing implementation order as semantic preference unless documented;
- reject an empty union at construction.

For overlapping schemas, “first success” can change behavior when a new member is inserted. Discriminated unions are more predictable and become the final independent extension.

## 13. Refinement validates domain predicates

```ts
export function refine<T>(
  schema: Schema<T>,
  predicate: (value: T) => boolean,
  options: { readonly code: string; readonly message: string },
): Schema<T>;
```

The base schema establishes `T`. The predicate checks an additional invariant such as non-empty text or a numeric range.

If the predicate throws, SchemaKit converts it into a bounded refinement issue rather than allowing arbitrary exceptions to escape from `safeParse`. The throwing `parse` method still throws `SchemaError` containing issues, not the original arbitrary value.

Document whether a predicate is pure. Re-running it should not produce inconsistent validation.

## 14. Transform changes the output authority

```ts
export function transform<Input, Output>(
  schema: Schema<Input>,
  map: (value: Input) => Output,
): Schema<Output>;
```

A transform is not validation unless it also checks the output. It creates a new trusted output through library code. If `map` throws, the failure policy must be explicit.

Use transform for deterministic conversions such as trimming or parsing a date only when the result invariant is fully established. Do not hide lossy coercion inside primitive schemas.

A safer alternative for fallible transformation accepts a function returning `ParseResult<Output>`.

## 15. Lazy schemas support recursion

```ts
export function lazy<T>(factory: () => Schema<T>): Schema<T>;
```

The factory is evaluated lazily and cached. It supports recursive models:

```ts
interface Tree {
  readonly value: string;
  readonly children: readonly Tree[];
}

const tree: Schema<Tree> = lazy(() => object({
  value: string(),
  children: array(tree),
}));
```

Recursion creates runtime risks:

- cyclic input objects;
- excessive depth;
- stack exhaustion;
- large issue trees.

SchemaKit documents an input-depth limit in the parser context. It validates data trees, not arbitrary cyclic object graphs.

## 16. Parse JSON separately

JSON text parsing and schema validation are distinct phases:

```ts
export function safeParseJson<S extends Schema<unknown>>(
  schema: S,
  text: string,
): ParseResult<Infer<S>>;
```

First `JSON.parse` converts text to an unknown JavaScript value or throws syntax error. Then the schema validates structure and domain rules. The error model should distinguish JSON syntax from schema issues.

Do not accept a type parameter as a substitute for a schema:

```ts
// Unsafe: no runtime validation.
// JSON.parse(text) as T
```

## 17. Schema construction can validate configuration

A schema factory can reject invalid schema configuration immediately:

- negative max length;
- empty union;
- duplicate literal variants;
- unsafe or empty issue code;
- object shape keys that are invalid for the selected policy.

Construction-time errors are programmer errors, distinct from parse failures on external data. Keep the two error categories separate.

## 18. Error quality is part of the API

Useful issues include:

- path;
- stable code;
- concise message;
- expected category where helpful;
- no unbounded raw value;
- deterministic order.

Avoid messages built from full `JSON.stringify(input)` because cycles can throw, large inputs can explode output, and secrets can leak.

Stable error codes are more compatible than exact English text. Tests should assert codes and paths; message snapshots can be narrower.

## 19. Runtime/static agreement tests

For every combinator, test both surfaces:

| Claim | Evidence |
|---|---|
| string output inferred | type equality test |
| wrong literal rejected | runtime test |
| optional key omitted | runtime own-key assertion |
| optional key type optional | negative/positive type test |
| tuple positions preserved | type equality + runtime order |
| union output union | type equality |
| union member order behavior | runtime test |
| issue path exact | runtime issue assertion |
| internal decoder hidden | declaration inspection |

No single test category proves the whole combinator.

## 20. A schema-design ledger

For each combinator, record:

- accepted runtime input domain;
- successful output ownership/copying;
- inferred output type;
- failure codes and path behavior;
- issue accumulation bound;
- optional/nullable semantics;
- callback purity and error behavior;
- recursion/depth policy;
- declaration surface;
- compatibility risks.

## 21. Common wrong models

### “The inferred type proves the input is valid”

Only runtime parsing validates external data.

### “The runtime schema makes TypeScript unnecessary”

Static inference prevents callers from repeating and drifting successful output types.

### “Optional means `T | undefined` everywhere”

Object-property absence is a separate runtime operation.

### “Union validation should return every nested issue”

Unbounded alternatives can create unusable diagnostics and memory cost.

### “Transform is validation”

It creates output; its function must establish any promised invariant.

### “Recursive schemas handle arbitrary graphs”

Depth, cycles, and resource bounds need explicit policy.

## 22. Use the idea in a complete program

Module 28 completes SchemaKit's runtime core and the example project-manifest schema. The CLI reads JSON, validates it, prints canonical summary output, and returns distinct exit statuses for usage, I/O, syntax, and schema failure.

The independent decoder lab implements a smaller algebra from scratch so you can transfer the model without relying on SchemaKit internals.

## Practice sequence

1. Trace one nested invalid value through path construction.
2. Predict the eight Module 28 investigations.
3. Implement primitive and array schemas before object/union.
4. Complete [Composable Decoder Library](../../labs/module-28-composable-decoder-library/README.md).
5. Finish SchemaKit core using [the capstone guide](../capstone.md#module-28--runtime-validation-algebra).
6. Add adversarial tests for depth, issue bounds, getters, unknown keys, mutation after parse, and overlapping unions.

## Ready to continue

You are ready for Module 29 when you can explain:

- why schema input is `unknown`;
- how static output is inferred;
- optional absence versus `undefined`;
- object unknown-key policy;
- union search and bounded diagnostics;
- validation versus transform;
- recursive depth/cycle limits;
- which tests prove runtime/static agreement.

Next: [API Compatibility, Semantic Versioning, and Migration](../module-29-api-compatibility-semver-and-migration/index.md).
