# Laboratory 16 — Protocol-Aware Value Object

## Product

Build a `Distance` value object that participates deliberately in primitive conversion, runtime tagging, iteration, JSON serialization, and Node custom inspection. Each protocol must have a separate product purpose.

The laboratory rejects the vague idea that adding `toString` makes an object “work everywhere.” Different operations ask different protocols, use different hints, and need different representations.

## Contract

A distance stores an integer number of millimetres. It can be constructed from millimetres or metres. It exposes no mutable state.

- numeric conversion yields millimetres;
- string/default conversion yields a stable human-readable value;
- `Object.prototype.toString.call(value)` reports `[object Distance]`;
- iteration yields a labelled unit decomposition used only by the laboratory;
- `toJSON` emits a plain versioned record;
- Node custom inspection emits bounded debug text;
- equality is an explicit method, not an accidental coercion trick.

## Required reasoning

Build a table for `String(value)`, template interpolation, unary `+`, comparison, concatenation, `Object.prototype.toString`, spread, `JSON.stringify`, and `util.inspect`. State which protocol is requested and which fallback would occur without it.

## Invariants

- millimetres are finite safe integers;
- protocol methods return permitted result categories;
- debug output and JSON are not interchangeable;
- symbols are discoverable and are not used as secrets;
- iteration creates a fresh iterator per traversal.

## Transfer

Add `Symbol.match`-like behavior only as a written design exercise. Decide whether pretending a distance is a regular-expression protocol participant would clarify or distort the domain. The expected answer may be “do not implement it.”
