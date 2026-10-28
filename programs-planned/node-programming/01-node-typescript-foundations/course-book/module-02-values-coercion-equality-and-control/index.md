# Module 2 — Values, Coercion, Equality, Control Flow, and Invariants

> **Question:** Which value actually exists after each operator and branch, and which conversions should the product permit?

## Why this comes now

Module 1 separated static checking from execution. Module 2 studies the values that execution manipulates. JavaScript is not difficult because it has many primitive types; it is difficult because operators can convert values, several “empty” values are distinct, numbers have IEEE-754 edge cases, and concise fallback syntax can erase legitimate data.

The goal is not to memorize trivia. The goal is to replace accidental conversion with explicit product policy.

## Outcomes

You will be able to:

- classify primitives and object values without confusing `typeof` quirks with domain meaning;
- predict truthiness, strict equality, `Object.is`, nullish coalescing, and optional chaining;
- validate numeric text without partial parsing or non-finite results;
- state integer-range and overflow policies for identifiers and durations;
- use guard clauses and branch invariants to make control flow reviewable;
- implement StudyLedger’s ID and duration parsers without accepting accidental coercions.

## 1. Runtime values precede static types

JavaScript primitives are:

```text
undefined
null
boolean
number
bigint
string
symbol
```

Everything else is an object value, including arrays and functions in the broad object model. TypeScript can describe narrower sets, but it cannot change the runtime category.

The historical result `typeof null === "object"` is a language fact, not a useful null check. Use direct equality for nullish cases or a deliberate predicate.

## 2. Number is not an unbounded integer

JavaScript `number` uses IEEE-754 double precision. Important values include:

- finite ordinary numbers;
- `NaN`;
- positive and negative infinity;
- positive and negative zero.

A validation sequence should establish the exact product range:

```ts
export function parsePositiveMinutes(raw: string): number {
  if (!/^[1-9]\d*$/.test(raw)) {
    throw new Error('minutes must be a positive decimal integer');
  }

  const value = Number(raw);
  if (!Number.isSafeInteger(value)) {
    throw new Error('minutes exceed the safe integer range');
  }
  if (value > 24 * 60) {
    throw new Error('minutes must not exceed one day');
  }
  return value;
}
```

The regular expression prevents whitespace, sign, decimal fraction, exponent notation, and partial parsing. `Number.isSafeInteger` prevents integers that cannot be represented exactly. The final bound is StudyLedger policy.

Compare weak alternatives:

```ts
parseInt('12minutes', 10); // 12
Number('');                // 0
Number('   ');             // 0
```

Those conversions may be useful elsewhere. They do not satisfy this parser’s contract.

## 3. `NaN`, equality, and signed zero

Ordinary policy uses strict equality:

```ts
3 === 3;     // true
'3' === 3;   // false
```

`NaN` is unequal to itself under `===`:

```ts
NaN === NaN; // false
```

Use `Number.isNaN` to test it. `Object.is` differs in two notable cases:

```ts
Object.is(NaN, NaN); // true
Object.is(0, -0);    // false
```

Do not replace every equality with `Object.is`. Select it when those distinctions are part of the domain. StudyLedger durations reject non-finite numbers and never need signed-zero identity, so ordinary integer comparisons are sufficient.

## 4. Truthiness is not validity

Falsy values are:

```text
false
0
-0
0n
""
null
undefined
NaN
```

A truthiness check answers “does JavaScript coerce this value to true?” It does not answer “is this a valid duration?”, “was this field supplied?”, or “does this collection exist?”

The distinction appears in defaults:

```ts
const requested = 0;
const withOr = requested || 30;  // 30
const withNullish = requested ?? 30; // 0
```

Use `??` when only `null` or `undefined` means missing. Use `||` when every falsy value should choose the fallback. If zero is invalid, reject zero explicitly rather than relying on `||` to conceal it.

## 5. Optional chaining does not validate the result

```ts
const city = user.profile?.address?.city;
```

The expression prevents property access through `null` or `undefined`. The result remains possibly `undefined`; it does not establish that `city` is nonempty, normalized, or even a string when `user` came from untrusted JavaScript.

Optional chaining is an access policy, not a validation system.

## 6. Strings and Unicode boundaries

JavaScript strings are sequences of UTF-16 code units. Several lengths can matter:

```ts
'😀'.length;             // 2 code units
[...'😀'].length;        // 1 Unicode code point
Buffer.byteLength('😀'); // 4 UTF-8 bytes in Node
```

A product must name the unit. StudyLedger limits topics by Unicode code points for a reader-facing bound and separately rejects control characters required by its display/storage policy. Later courses address grapheme clusters and streaming encodings in depth.

A simple code-point count is:

```ts
function codePointLength(value: string): number {
  return Array.from(value).length;
}
```

This still does not count user-perceived grapheme clusters. The course names that non-contract instead of pretending “character” has one universal meaning.

## 7. Branches should establish invariants

Use guard clauses to turn a broad input into a narrower trusted value:

```ts
function normalizeTopic(raw: string): string {
  const topic = raw.trim();
  if (topic.length === 0) {
    throw new Error('topic must not be empty');
  }
  if (Array.from(topic).length > 120) {
    throw new Error('topic is too long');
  }
  if (/\p{Cc}/u.test(topic)) {
    throw new Error('topic contains a control character');
  }
  return topic;
}
```

After the function returns, callers can rely on the invariant. A function named `isTopicValid` that returns only `boolean` may force each caller to normalize independently. Prefer one authority that returns the canonical value or a structured failure.

## 8. Control flow and exhaustive reasoning

JavaScript `if`, `switch`, loops, and conditional expressions are ordinary control constructs. TypeScript performs control-flow analysis across them. Keep runtime and static effects distinct:

```ts
function describe(value: string | number): string {
  if (typeof value === 'number') {
    return Number.isFinite(value) ? `number:${value}` : 'non-finite';
  }
  return `text:${value}`;
}
```

The `typeof` check both controls runtime behavior and narrows the static type. A truthiness check would narrow differently and could accidentally reject an empty string or zero.

## 9. StudyLedger increment

Implement canonical parsers for:

- positive session IDs;
- planned minutes in the range 1–1440;
- actual minutes in the range 1–10080;
- nonempty normalized topics;
- optional notes whose absence differs from an empty supplied value.

Do not expose `Number(raw)` or `parseInt` directly to the rest of the application. The command parser owns textual conversion. Domain functions receive validated values.

## 10. Common wrong models

### “TypeScript says number, so it is a valid integer”

`number` includes fractions, infinities, `NaN`, and unsafe integers.

### “Falsy means missing”

Falsy is a language conversion category. Missing is a product concept.

### “`==` is convenient input parsing”

Abstract equality has conversion rules; it does not document the accepted grammar.

### “String length means characters”

State whether the unit is UTF-16 code units, code points, graphemes, or encoded bytes.

### “A default repairs invalid input”

A default is appropriate for absence when the product allows it. Invalid supplied data should normally fail visibly.

## 11. The acceptance–conversion–domain pipeline

External text should cross three distinct steps:

```text
raw token
   ↓ syntax acceptance
convertible representation
   ↓ conversion
JavaScript number
   ↓ domain validation
planned minutes
```

For StudyLedger, `--minutes 30` is valid, while these strings are not equivalent:

```text
" 30"   leading whitespace
"+30"   explicit sign
"3e1"   exponent notation
"30.0"  decimal notation
""      empty text
```

`Number` converts all or most of them. That is why conversion is not validation. The parser first chooses the accepted textual language:

```ts
function parsePositiveDecimal(raw: string): number {
  if (!/^(0|[1-9]\d*)$/u.test(raw)) {
    throw new Error('expected decimal digits');
  }
  const value = Number(raw);
  if (!Number.isSafeInteger(value) || value <= 0) {
    throw new Error('outside the supported range');
  }
  return value;
}
```

The domain layer may apply a narrower maximum, such as 1,440 planned minutes. Keeping syntax and domain rules separate allows another command to reuse decimal parsing while enforcing a different range.

### Numbers have several validity dimensions

A value typed `number` can still be:

- `NaN`;
- positive or negative infinity;
- non-integral;
- outside the safe integer range;
- negative when a count must be nonnegative;
- zero when a quantity must be positive.

Use the predicate that expresses the actual invariant. `Number.isFinite`, `Number.isInteger`, and `Number.isSafeInteger` answer different questions. An ID allocator needs safe integer arithmetic; a temperature may legitimately be fractional; a ratio may allow zero but reject infinity.

`bigint` is not a transparent upgrade. It uses different operators and does not mix implicitly with `number`:

```ts
const exact = 9_007_199_254_740_993n;
// exact + 1 // type and runtime error: bigint and number do not mix
```

Choose `bigint` when the product requires exact integers outside the safe-number range, then carry that choice through parsing, JSON policy, persistence, and APIs. Course 1 keeps IDs within safe `number` bounds.

## 12. Logical operators return operands

JavaScript’s `&&`, `||`, and `??` do not necessarily return booleans.

```ts
const retries = 0;
const withOr = retries || 3;  // 3
const withNullish = retries ?? 3; // 0
```

The first treats every falsy value as absence. The second treats only `null` and `undefined` as absence. Neither validates that the remaining value is an acceptable retry count.

A useful decision table is:

| Requirement | Operation |
|---|---|
| choose default only for missing value | `??` after type validation |
| require nonempty string | trim and compare length |
| require positive number | explicit numeric predicate |
| convert any value to boolean | `Boolean(value)` when that is truly the contract |
| select one of several domain alternatives | explicit branch or discriminated union |

Optional chaining has the same limitation. `config.output?.directory` safely avoids a property access on nullish `output`; it does not prove the resulting directory exists, is nonempty, or is usable.

## 13. Equality is a policy choice

Use `===` for ordinary exact comparisons, but know its numeric edge cases:

```ts
NaN === NaN       // false
Object.is(NaN, NaN) // true
0 === -0          // true
Object.is(0, -0)  // false
```

`Map` and `Set` use SameValueZero equality: `NaN` keys match each other, and `0` and `-0` are treated as equal. Object equality is identity equality, not structural equality.

Do not select loose equality as an input-conversion shortcut. The expression `raw == 0` accepts values through coercion that the product may never have intended. Parse once, validate once, then compare values of the intended runtime category.

## 14. Strings, code points, and user-visible text

JavaScript string indices and `.length` count UTF-16 code units. They do not directly count Unicode code points or grapheme clusters. For example, one visible symbol can occupy multiple code units, and a letter plus a combining mark can be visually equivalent to a precomposed character.

Course 1 uses bounded text rules for topics, notes, and reasons. The length limit is a storage and abuse-control policy, not a claim about displayed characters. When user-visible character limits matter, the product must define normalization and segmentation explicitly.

Normalization can affect equality:

```ts
const composed = 'é';
const decomposed = 'e\u0301';
composed === decomposed; // false
composed.normalize('NFC') === decomposed.normalize('NFC'); // true
```

Do not normalize silently unless the domain owns that policy. Identifiers, passwords, file names, and display text have different requirements.

## 15. Branches establish invariants

A branch should leave the rest of the function with stronger knowledge:

```ts
function requireNonempty(value: string | undefined): string {
  if (value === undefined) throw new Error('missing value');
  const trimmed = value.trim();
  if (trimmed.length === 0) throw new Error('empty value');
  return trimmed;
}
```

After each guard, both runtime and static uncertainty decrease. By contrast, nested truthiness checks often mix missing, empty, zero, and invalid cases.

For closed alternatives, use total control flow. A `switch` over a discriminant is not merely formatting; it is a place where the compiler can reveal a newly added case. Course 1 begins this practice with command and session states and deepens it in Module 5.

## Practice sequence

Complete the [workbook](workbook.md), then [Usage Quote Policy](../../labs/module-02-usage-quote-policy/README.md). Apply the parsers to StudyLedger and keep raw command strings out of the domain model.

## Ready to continue

Continue when you can explain why each accepted textual form is accepted, why every rejected form is rejected, and which unit and range each numeric or string bound uses.

Next: [Module 3 — Functions, Scope, Closures, Callbacks, and `this`](../module-03-functions-scope-closures-and-this/index.md)
