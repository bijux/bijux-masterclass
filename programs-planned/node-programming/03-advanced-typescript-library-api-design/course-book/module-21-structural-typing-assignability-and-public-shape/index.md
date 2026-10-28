# Module 21 — Structural Typing, Assignability, and Public Shape

> **Question:** When does one TypeScript value satisfy another contract, and which apparent guarantees disappear when the code reaches JavaScript?

## Why this comes now

Course 2 ended with a runtime object map. You learned to distinguish own properties, inherited properties, descriptors, prototypes, receivers, private brands, plain persistence records, and live objects. TypeScript observes those values through a different lens. Most TypeScript object types are **structural**: compatibility depends mainly on members, not on the declaration that introduced the type.

That difference is productive. A value can satisfy a small capability without extending a shared base class. A test double can satisfy an interface without inheriting from production code. A library can accept any object with the required operations. But the same flexibility creates recurring mistakes:

- treating an interface as runtime validation;
- assuming structural compatibility means exact property equality;
- confusing excess-property checks with a permanent “no extra keys” guarantee;
- widening literals until useful distinctions disappear;
- using assertions to silence the checker before evidence exists;
- introducing brands everywhere and turning structural composition into nominal ceremony.

This module establishes the assignability model used by the rest of Course 3.

## Outcomes

By the end of the module, you can:

- trace assignability from a source type to a target type;
- distinguish required, optional, readonly, index, call, and construct members;
- explain why a fresh object literal can fail when an equivalent variable succeeds;
- use annotations, inference, `as const`, and `satisfies` for different purposes;
- identify widening and contextual typing before they erase literal information;
- distinguish a type assertion from a proof-producing check;
- use private members or unique-symbol brands when domain identity truly requires nominal separation;
- explain why exactness, untrusted-data validation, and runtime object identity remain runtime responsibilities;
- design the first SchemaKit public contracts without claiming more than TypeScript establishes.

## 1. Assignability is directional

Suppose a function requires this capability:

```ts
interface Named {
  readonly name: string;
}

function label(value: Named): string {
  return value.name;
}
```

This value is accepted:

```ts
const account = {
  name: 'Ada',
  balance: 120,
};

label(account);
```

The question is not “Are `account` and `Named` the same type?” They are not. The question is:

> Does the source type of `account` provide every member required by the target type `Named` with compatible member types?

Write an assignability judgment as:

```text
source  ──assignable to──▶  target
```

The direction matters. A larger structural source may satisfy a smaller target. The reverse may fail:

```ts
interface Account extends Named {
  readonly balance: number;
}

const named: Named = { name: 'Ada' };
// const full: Account = named;
// Property 'balance' is missing.
```

When debugging an error, identify source and target explicitly. “These types do not match” is usually too vague to reveal the missing relationship.

## 2. Required members define the minimum surface

For ordinary object types, the target's required members form a minimum capability.

```ts
interface Writer {
  write(text: string): void;
}

const consoleWriter = {
  prefix: '[course]',
  write(text: string): void {
    console.log(this.prefix, text);
  },
};

const writer: Writer = consoleWriter;
```

The extra `prefix` member does not prevent compatibility. That is the central advantage of structural typing: callers can depend on the smallest behavior they need.

But compatibility of method names is not the whole story. The member types must also be compatible. A writer that accepts only one literal is not a safe replacement for a writer that promises to accept every string:

```ts
const narrow = {
  write(text: 'ready'): void {
    console.log(text);
  },
};
```

Function compatibility becomes a full topic in Module 25. For now, record that every member can contain another assignability problem.

## 3. Optional does not mean “present with undefined”

Under `exactOptionalPropertyTypes`, these contracts are different:

```ts
interface A {
  note?: string;
}

interface B {
  note: string | undefined;
}
```

`A` permits the property to be absent. When present, it must contain a string. `B` requires an own or inherited property at the type level whose value may be `undefined`.

```ts
const a1: A = {};
const a2: A = { note: 'checked' };
// const a3: A = { note: undefined };

const b1: B = { note: undefined };
```

This distinction matters in object schemas, update payloads, JSON records, and compatibility reviews. A library that changes `field?: T` to `field: T | undefined` has changed construction and presence semantics even though both forms mention `undefined` during reads.

At runtime, TypeScript does not inspect own-property presence. Use `Object.hasOwn` or another deliberate check when the distinction matters.

## 4. `readonly` describes a capability, not frozen runtime memory

A readonly target allows reading but rejects mutation through that reference:

```ts
interface ReadPoint {
  readonly x: number;
}

const mutable = { x: 1 };
const view: ReadPoint = mutable;
mutable.x = 2;
console.log(view.x); // 2
```

The value did not become frozen. Another alias with mutation authority changed it. Therefore:

```text
readonly type
    ≠
Object.freeze
    ≠
deep immutability
    ≠
exclusive ownership
```

Readonly is still useful. It narrows what a particular API surface permits. It also improves variance for collections, as Module 25 explains. But documentation must not claim runtime immutability unless the runtime establishes it.

## 5. Excess-property checking is a construction check

Compare these assignments:

```ts
interface Point {
  x: number;
}

const fromVariable = { x: 1, y: 2 };
const accepted: Point = fromVariable;

// const rejected: Point = { x: 1, y: 2 };
```

The fresh object literal receives an excess-property check because `y` may indicate a misspelled or misunderstood target field. The variable assignment uses ordinary structural compatibility: the source has at least the required `x` member.

Do not describe this as TypeScript having exact object types. The following operations can all introduce extra runtime keys while preserving a `Point` reference:

- assignment through a wider variable;
- object spread;
- mutation through another alias;
- class instances with additional fields;
- values returned from functions;
- external JSON asserted or validated incompletely.

Excess-property checking improves construction feedback. It is not runtime exactness and not a permanent closed-world guarantee.

## 6. Index signatures widen the promised key space

An index signature states a broad relationship:

```ts
interface Scores {
  [name: string]: number;
}
```

Every string-named property visible through that contract must be compatible with `number`. This can conflict with named members:

```ts
interface InvalidScores {
  // label: string;
  [name: string]: number;
}
```

A string index signature also affects reads under `noUncheckedIndexedAccess`:

```ts
const scores: Scores = { Ada: 10 };
const maybeScore = scores['Grace']; // number | undefined
```

The signature promises what values are allowed for possible keys, not that every key exists.

Prefer `Map` when key identity, insertion order, non-string keys, or explicit absence is central. Prefer a finite mapped type when the key set is known. Use an open index signature only when the product genuinely accepts an open string domain.

## 7. Literal widening changes later inference

A `const` variable preserves a primitive literal more often than `let`:

```ts
const fixed = 'ready'; // 'ready'
let changing = 'ready'; // string
```

Object properties are mutable by default, so their literals commonly widen:

```ts
const job = { status: 'ready' };
// job.status is string, because the property could be reassigned.
```

`as const` changes the entire expression:

```ts
const frozenShape = {
  status: 'ready',
  retries: 3,
} as const;
```

The result has readonly properties and literal value types. That can be useful for immutable declarations, but it is too strong when only one literal relationship should be preserved.

TypeScript also supports `const` type parameters for APIs that should infer literal tuples or objects without forcing callers to write `as const`:

```ts
function defineNames<const Names extends readonly string[]>(names: Names): Names {
  return names;
}

const names = defineNames(['parse', 'render']);
// readonly ['parse', 'render']
```

Use literal preservation because later operations need the distinction—not because narrower types look sophisticated.

## 8. Annotation and `satisfies` answer different questions

An annotation chooses the variable's exposed type:

```ts
interface RetryPolicy {
  mode: 'fixed' | 'exponential';
  attempts: number;
}

const annotated: RetryPolicy = {
  mode: 'fixed',
  attempts: 3,
};
```

After annotation, the variable is viewed as `RetryPolicy`. In contrast, `satisfies` checks compatibility while preserving the expression's inferred type:

```ts
const checked = {
  mode: 'fixed',
  attempts: 3,
} satisfies RetryPolicy;

// checked.mode remains the literal 'fixed'.
```

Use an annotation when callers should see the declared abstraction. Use `satisfies` when you want to validate a declaration without discarding useful literal information.

A common library pattern is:

```ts
const codecs = {
  json: { extension: '.json' },
  text: { extension: '.txt' },
} satisfies Record<string, { extension: string }>;

type CodecName = keyof typeof codecs; // 'json' | 'text'
```

An annotation as `Record<string, ...>` would widen the key set to `string` and destroy the finite-name relationship.

## 9. Assertions spend trust

A type assertion tells the checker to adopt a type relation that it could not establish normally:

```ts
const input: unknown = JSON.parse(source);
const project = input as { name: string };
```

Nothing validated `name`. The assertion only changed the static view.

Assertions are appropriate at narrow boundaries where another mechanism has already established the fact and the checker cannot express it. Examples include:

- a carefully audited low-level helper;
- an API whose runtime contract is stronger than its declarations;
- a test fixture intentionally constructing an invalid value;
- a parser implementation after explicit checks.

For each assertion, write the missing proof in one sentence. If no proof exists, the assertion is a defect.

`as unknown as T` is not a repair. It erases the source relationship and invents the target relationship.

## 10. `unknown`, `object`, `{}`, and `Record` are not interchangeable

These broad types answer different questions:

- `unknown` — any value may arrive; no operation is allowed before narrowing;
- `object` — any non-primitive value;
- `{}` — historically, any non-nullish value under strict null checking;
- `Record<PropertyKey, unknown>` — an object assumed to support arbitrary own or inherited property reads by property key, often broader than the runtime evidence;
- `Record<string, unknown>` — a string-keyed dictionary model, not every object.

A runtime schema should accept `unknown` because external input can be any JavaScript value. A function requiring an object identity may use `object`. A dictionary validator should establish a plain-object or null-prototype policy before treating a value as a record.

## 11. Structural typing and nominal islands

Sometimes two structurally identical values must not be interchangeable. A user ID and an order ID may both be strings, but mixing them is a domain error.

A unique-symbol brand creates a nominal island:

```ts
declare const userIdBrand: unique symbol;

export type UserId = string & {
  readonly [userIdBrand]: 'UserId';
};

export function parseUserId(raw: string): UserId {
  const value = raw.trim();
  if (!/^usr_[a-z0-9]+$/.test(value)) {
    throw new Error('invalid user id');
  }
  return value as UserId;
}
```

The assertion is justified by the validation immediately before it. The brand has no runtime property; it prevents accidental static interchange.

JavaScript private fields also affect structural compatibility for class types. Classes with different private declarations are not structurally interchangeable even when their public members match. This is useful for true class identity, but it is a poor reason to turn every data value into a class.

Use a brand when:

- validation creates a domain identity;
- accidental interchange would be costly;
- the creation function can be centralized;
- consumers benefit from preserving the distinction.

Do not brand values merely to make simple types look “enterprise.” Brands increase API friction and require migration thought.

## 12. Exactness is a runtime product policy

Suppose an API accepts this configuration:

```ts
interface ServerConfig {
  port: number;
  host?: string;
}
```

A runtime exactness policy must answer:

- are unknown keys rejected, ignored, or preserved?
- are inherited keys considered?
- are symbol keys relevant?
- is a class instance accepted?
- is a null-prototype object accepted?
- is `{ host: undefined }` different from missing `host`?
- are getters invoked?
- is the result copied, frozen, or retained?

An interface answers none of these questions. A schema or validator must implement them.

This distinction becomes the foundation of SchemaKit:

```text
Schema<T>
  accepts unknown runtime input
  validates a documented policy
  returns T only after success
```

The static output type must describe the successful runtime result, not the unchecked input.

## 13. Public shape is a compatibility promise

Every exported type creates downstream expectations. Consider:

```ts
export interface Result<T> {
  ok: boolean;
  value?: T;
  error?: string;
}
```

This type permits contradictory states: `ok: true` with an error, `ok: false` with a value, or neither field. A discriminated union states a stronger relation:

```ts
export type Result<T, E> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: E };
```

The second design improves narrowing and prevents invalid combinations. It also creates a public union. Adding a third member later may break exhaustive consumers. Type precision and compatibility must be reviewed together.

SchemaKit begins with these public concepts:

```ts
export type PathSegment = string | number;

export interface Issue {
  readonly path: readonly PathSegment[];
  readonly code: string;
  readonly message: string;
}

export type ParseResult<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly issues: readonly Issue[] };
```

The issue does not retain the entire rejected input. That avoids accidental memory retention and secret exposure. The result is discriminated and immutable through the public view.

## 14. An assignability ledger

For every important assignment or call, write:

| Question | Record |
|---|---|
| source type | What does the expression currently have? |
| target type | What does the context require? |
| required members | Which target members must exist? |
| member compatibility | Do nested types and call signatures align? |
| optionality | Missing versus present-undefined? |
| readonly | Which mutation capability is removed? |
| freshness | Is an object literal receiving an excess-property check? |
| literal state | Which names or values widened? |
| assertion | Is trust being spent? What proves it? |
| runtime policy | What remains to validate or enforce? |

This ledger is more effective than experimenting with random annotations until an error disappears.

## 15. Common wrong models

### “An interface validates an object”

Interfaces are erased. Validate external values at runtime.

### “No compiler error means no extra keys”

Structural compatibility allows extra members. Excess-property checking is limited.

### “Readonly means immutable”

Readonly removes mutation through one static view. Other aliases and runtime operations may mutate.

### “`satisfies` casts the value”

It checks assignability and preserves inferred type. It emits no runtime conversion.

### “A brand validates the string”

The brand exists only in the type system. The constructor or parser must validate.

### “Assertions fix difficult inference”

Assertions suppress a proof obligation. Improve the relationship or add the missing runtime check.

## 16. Use the idea in a complete program

In SchemaKit, Module 21 establishes:

- immutable `Issue` and `ParseResult` public shapes;
- a branded `SchemaName` constructed only after validation;
- a runtime plain-object predicate that does not equate `object` with dictionary;
- exact own-key policy for the project-manifest example;
- type tests proving that success and failure states narrow correctly;
- no assertion at a public boundary without a named runtime proof.

The corresponding laboratory uses a feature catalog because it exposes the same problem in a different product: preserve literal feature names, accept a small structural contract, reject duplicate runtime identities, and avoid pretending that `satisfies` performs validation.

## Practice sequence

1. Complete the source/target predictions in the workbook.
2. Run the eight Module 21 investigations.
3. Repair each assertion by supplying evidence or deleting the unsupported claim.
4. Build [Structural Contract Catalog](../../labs/module-21-structural-contract-catalog/README.md).
5. Add the Module 21 SchemaKit contracts from [the capstone guide](../capstone.md#module-21--public-shape-and-result-contracts).
6. Reconstruct the assignability ledger without looking at this chapter.

## Ready to continue

You are ready for Module 22 when you can explain all of the following without notes:

- why assignability is directional;
- why a fresh literal and a variable may receive different diagnostics;
- the difference among annotation, `as const`, `satisfies`, and assertion;
- why optional presence and `undefined` are distinct;
- what readonly does and does not promise;
- when a brand is justified;
- which exactness and validation facts remain runtime responsibilities.

Next: [Generic Relationships, Inference, and Indexed Access](../module-22-generic-relationships-inference-and-indexed-access/index.md).
