# Language and Code Strategy

## Why the program uses Python and TypeScript

The program is about API engineering rather than one framework. Python/FastAPI and TypeScript/Fastify provide two mature but different ecosystems in which to test whether an invariant is truly architectural or merely an implementation habit.

## Course 1: symmetric tracks

In the contract course, both providers are first-class because the learner must see that methods, parameters, schemas, status codes, security requirements, examples, and compatibility belong to the public boundary. A contract that only one framework can express is suspect. Shared black-box scenarios are more important than matching controller syntax.

## Courses 2–6: primary and comparative tracks

Choose one primary track for the full implementation and laboratory work. Use the second track for focused comparative review. A good comparison names:

1. the shared externally observable or durable invariant;
2. the Python mechanism that enforces it;
3. the TypeScript mechanism that enforces it;
4. one deliberate ecosystem difference;
5. one source-shape difference that must not become a parity requirement;
6. the shared vector or black-box proof that decides equivalence.

## What should remain the same

The tracks must agree on:

- public HTTP and event behavior;
- canonical identities and bytes where cross-language equality is required;
- transaction and idempotency outcomes;
- authorization decisions;
- bounded-resource and failure classifications;
- metric and SLI populations;
- release decisions;
- replay and consumer-effect semantics.

## What may differ

They may use different:

- dependency-injection styles;
- model and validation libraries;
- asynchronous primitives;
- transaction APIs;
- file organization;
- error classes;
- test frameworks;
- profiling tools;
- middleware and plugin hooks.

Forcing identical structure usually produces unidiomatic code and hides the real invariant.

## How to read examples

Every non-trivial example should answer four questions: where does it live, which guarantee does it enforce, which failure does it prevent, and which proof would fail if it were removed? Short excerpts are explanatory views of complete source files; they are not alternate implementations to copy blindly.

## When to translate code

Translate only after you can state the invariant without language vocabulary. If the only explanation is “this decorator does it” or “this Promise fixes it,” the concept is not yet understood. The comparison track is a test of abstraction quality, not extra typing work.
