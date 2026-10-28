# Module 2 Solutions

## A. Values

1. `'fallback'` because the empty string is falsy.
2. `''` because it is neither `null` nor `undefined`.
3. `20` because zero is falsy.
4. `0` because zero is present.
5. `0`; this is why direct numeric conversion is not a grammar.
6. `true`.
7. `12`; `parseInt` accepts a prefix.
8. `false`.
9. `false`.
10. `2`, `1`, and `4`, measuring UTF-16 code units, code points, and UTF-8 bytes.

## B. Weak parser

Problematic inputs include `undefined`, `''`, `'0'`, `'  '`, `'12px'`, `'1.5'`, `'-3'`, `'1e3'`, and values beyond the safe integer range. The contract should name absence behavior, accepted grammar, integer/range policy, and error representation before implementation.

## C. Branch design

Handle `null` first as failure. For a number, require `Number.isSafeInteger(value) && value >= 0`. For a string, require `/^(0|[1-9]\d*)$/`, then convert and repeat the safe-integer bound. The returned number is trusted because every successful branch establishes the same invariant.

## D. Equality

Session IDs use `===` after parsing. Search compares normalized strings. `NaN` uses `Number.isNaN`. Signed-zero analysis uses `Object.is`. Object semantic equality requires a domain-specific comparison; reference equality or JSON text is not automatically correct.

## E–F. Design notes

The lab should never treat an unsupported plan as a numeric default. StudyLedger parsers should return canonical values or throw/return structured parse failures. An empty optional note may be normalized to absence only if the command contract says so; that policy must be tested.

## G. Readiness answer

JavaScript’s `number` represents more than integers. `??` selects on nullish absence; `||` selects on all falsy values. Optional chaining only prevents nullish property traversal. String length depends on the chosen representation unit. A canonical parser centralizes the only route from raw syntax to trusted domain value.

## Extended solution

`Number('')` and `Number(' ')` are zero; `Number('00')` is zero; `Number('+5')`, `Number('5.0')`, and `Number('5e1')` all produce numbers. Boolean conversion treats every nonempty string as true, including `'0'`. `||` returns the fallback for an empty string but not for a whitespace string. `??` uses the fallback only for nullish values, so none of these string tokens trigger it.

The accepted minutes grammar includes only canonical decimal digits with no leading zero except the single token `0`, followed by domain rejection of zero and values above 1,440. Missing option and malformed text are command errors; a syntactically valid but out-of-range number is a domain error.

StudyLedger does not normalize Unicode topics in Course 1. It trims outer whitespace, rejects control characters, and preserves authored text. Silent normalization could change identifiers or search behavior. A display-name directory might deliberately normalize for matching; a password system should not casually transform secrets.
