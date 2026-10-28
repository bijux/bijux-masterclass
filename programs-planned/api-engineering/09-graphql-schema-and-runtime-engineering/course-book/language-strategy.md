# Language strategy

GraphQL semantics are language-neutral; implementations are not. The program therefore separates **behavioral parity** from **syntactic mirroring**.

## TypeScript track

The TypeScript reference uses strict types for global identifiers, parsed operations, budgets, loaders, compatibility decisions, and the graph gateway. An optional GraphQL Yoga adapter shows how these policies attach to a complete GraphQL.js-based server. The dependency-light core compiles without registry access and is tested with Node's built-in test runner.

## Python track

The Python reference uses dataclasses, explicit exceptions, request-scoped loaders, a persisted-operation registry, and service clients. An optional Strawberry/FastAPI adapter demonstrates complete-framework integration. The dependency-light core uses the standard library so the course can prove its engineering mechanisms in constrained environments.

## What must match

Both tracks must agree on:

- global identifier and cursor decoding;
- operation identity;
- query-budget outcomes;
- authorization decisions;
- batch key collapse and request-scope isolation;
- mutation replay and conflict behavior;
- subscription gap and duplicate behavior;
- compatibility classification;
- externally visible data and error semantics.

They do not need identical class names, folder structures, async primitives, or middleware APIs.

## Recommended workflow

Implement the primary track. Before moving on, read the equivalent mechanism in the comparative track and answer: “Which guarantee is the same, and which implementation choice is idiomatic to this language?” This develops transferable engineering judgment rather than framework memorization.
