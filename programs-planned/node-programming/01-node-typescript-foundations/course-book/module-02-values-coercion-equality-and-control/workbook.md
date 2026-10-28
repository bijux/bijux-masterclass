# Module 2 Workbook

## A. Predict the value

Without running code, record the value and type of each expression:

1. `'' || 'fallback'`
2. `'' ?? 'fallback'`
3. `0 || 20`
4. `0 ?? 20`
5. `Number('')`
6. `Number.isNaN(Number('abc'))`
7. `parseInt('12px', 10)`
8. `Object.is(0, -0)`
9. `NaN === NaN`
10. `'😀'.length`, `[...'😀'].length`, and `Buffer.byteLength('😀')`

For every surprising result, state whether the product should permit the conversion.

## B. Diagnose a weak parser

```ts
function parseMinutes(raw: string | undefined): number {
  return parseInt(raw || '30', 10);
}
```

Find at least eight inputs whose treatment is ambiguous or wrong. Design a contract before writing a replacement.

## C. Branch invariants

Write a function that accepts `string | number | null` and returns a normalized nonnegative safe integer. Strings must use decimal digits only. `null`, empty strings, fractions, exponents, whitespace-padded text, negative values, and unsafe integers must fail.

Explain which branch establishes each fact.

## D. Equality policy

For each domain, choose `===`, `Object.is`, normalized text comparison, or a different explicit relation:

- session IDs;
- case-insensitive topic search;
- detecting `NaN` in a calculation;
- distinguishing signed zero in a numeric-analysis tool;
- determining whether two configuration objects are “the same”.

## E. Independent laboratory

Complete [Usage Quote Policy](../../labs/module-02-usage-quote-policy/README.md). The quotation must distinguish malformed input, unsupported plans, and valid zero-cost tiers.

## F. StudyLedger transfer

Implement and test parsers for ID, planned minutes, actual minutes, topic, and optional note. Include Unicode and boundary cases. The domain model must not contain raw command tokens.

## G. Reconstruction

Explain from memory:

- why `number` is not an integer type;
- why `??` and `||` express different policies;
- why optional chaining does not prove validity;
- why string bounds require a named unit;
- why a canonical parser is an authority rather than a convenience helper.

## H. Conversion clinic

For each token below, predict `Number(token)`, `Boolean(token)`, `token || 'fallback'`, and `token ?? 'fallback'`. Then state whether the StudyLedger minutes grammar accepts it: `''`, `' '`, `'0'`, `'00'`, `'+5'`, `'5.0'`, `'5e1'`, `'5'`.

Repair this parser:

```ts
function minutes(raw: string | undefined): number {
  return Number(raw || 30);
}
```

The product contract is: the option is required; decimal digits only; range 1–1,440; no fallback for malformed input. Your solution must produce different errors for missing syntax and out-of-range domain values.

## I. Unicode and equality review

Explain why `text.length <= 20` is not a promise of twenty user-perceived characters. Decide whether StudyLedger should normalize topics in Course 1. Defend the decision and identify one domain in which the opposite choice would be safer.

## J. StudyLedger checkpoint

Implement exact ID and minutes parsing. Add a table-driven test covering zero, unsafe integers, signs, decimals, exponents, whitespace, and a valid maximum. The test should reveal the accepted textual language, not only numeric conversion.
