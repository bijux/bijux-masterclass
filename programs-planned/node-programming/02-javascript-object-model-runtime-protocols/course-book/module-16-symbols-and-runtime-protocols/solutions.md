# Module 16 Reasoned Solutions

## A. Symbol identity

`a === b` is false because direct `Symbol` calls create distinct identities. `c === d` is true because `Symbol.for` resolves the same global-registry key. `Symbol.keyFor(a)` is `undefined`; `Symbol.keyFor(c)` returns the registry key.

Persisting descriptions cannot restore unique identity. Persisting a registry key is possible only when the global-registry protocol is itself the intended contract.

## B. Enumeration surface

String-key operations and symbol-key operations must be analyzed separately. `Object.keys` reports enumerable own strings. `Object.getOwnPropertySymbols` reports all own symbols. `Reflect.ownKeys` reports both. Spread copies enumerable own strings and symbols. JSON ignores symbols.

A debugger may use `Reflect.ownKeys` and descriptors. A persistence codec should use an explicit schema. A protocol registry should use the exact imported or registry symbol identities, not enumeration order.

## C. Primitive conversion policy

Temperature has unit semantics, so implicit numeric conversion is risky unless the type has one canonical unit documented everywhere. A safer design makes `format(unit)` and `toCelsius()` explicit and uses `Symbol.toPrimitive` only for string/default display or throws on numeric conversion.

A weak design returns Celsius for `number` but displays Fahrenheit without making the unit distinction visible. That allows arithmetic to appear correct while mixing domains.

## D. Diagnostic tag counterfeit

Any object can define the same `Symbol.toStringTag`; the resulting diagnostic label is not a brand. A validator must check actual domain evidence. Controlled class code may expose a private-brand predicate, while external records require runtime field validation.

## E. Custom inspection

The custom method should read already-owned stable data and return a bounded redacted string. It should not invoke arbitrary accessors or perform I/O. Tests can assert the redaction and stable payload, but should avoid depending on unrelated Node formatting that documentation does not guarantee.

JSON persistence must call an explicit snapshot method. Custom inspection can change without a storage migration.

## F. Protocol decision table

Persistence and transaction commit should be named methods because they are consequential domain operations. Default traversal fits `Symbol.iterator`; alternate traversal should be named. Debug summary fits `util.inspect.custom`. A module-owned cache may use an unexported symbol or private field. Validation should be a named predicate or parser. Duration numeric conversion may use `Symbol.toPrimitive` only if one canonical numeric meaning is indisputable.

## G. Laboratory

A complete value object keeps conversion pure, distinguishes string and numeric hints, exports one deliberate symbol capability, redacts custom inspection, and proves that copied tags do not establish validity.

## H. ObjectAtlas transfer

ObjectAtlas should keep protocol output separate from persisted data. Its metadata symbol can be reflective but non-enumerable. The custom inspector must report only bounded summaries. Counterfeit objects with the same tag or conversion method remain invalid.

## I. Reconstruction standard

A complete answer states what triggers a protocol and what identity coordinates it. It does not describe symbols as secrets or debugging output as a stable serialization surface.
