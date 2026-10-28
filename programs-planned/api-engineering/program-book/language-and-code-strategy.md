# Language and Code Strategy

## Why the program uses two languages

Python and TypeScript expose different implementation pressures while sharing the same external contracts. Python makes data and control-flow reasoning explicit and offers a mature scientific and service ecosystem. TypeScript exposes JavaScript number, event-loop, structural typing, and runtime-validation boundaries. Studying both prevents framework-specific behavior from masquerading as an API rule.

## Course 1: symmetric providers

Both providers are first-class because the lesson is that OpenAPI belongs above either framework. The same operation ledger, examples, scenarios, and clients must work across both.

## Courses 2–10: primary and comparison tracks

Choose one primary track for deep labs and repairs. Use the second to inspect one idiomatic implementation and run shared vectors. Do not duplicate every line merely to create visual symmetry.

Parity means:

- the same public messages and statuses;
- the same state-machine and security decisions;
- the same idempotent and concurrency outcomes;
- the same canonical bytes where interoperability depends on bytes;
- the same release classification;
- the same bounded evidence.

Parity does not mean identical classes, packages, exceptions, async primitives, database drivers, middleware hooks, or folder structures.

## Reading code educationally

Before opening an implementation, state the invariant and expected failure. Then inspect the narrow owner of that invariant, its negative test, and its cleanup path. Code without an identified owner and oracle is an example fragment, not evidence.
