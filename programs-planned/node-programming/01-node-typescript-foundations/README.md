# Course 1 — Node.js and TypeScript Foundations

## JavaScript Semantics, Strict Types, ESM, Async Effects, and Complete Programs

This course is the first ten-day stage of the Node.js program. It is written for a programmer who is new to JavaScript, TypeScript, and Node.js but already understands basic programming ideas.

The course is TypeScript-first for construction and JavaScript-first for explanation. TypeScript improves static reasoning; JavaScript still determines runtime values, object identity, coercion, exceptions, promises, module execution, and I/O behavior.

> **Governing question:** How do JavaScript runtime behavior, TypeScript contracts, ESM packages, failures, asynchronous effects, and tests combine into a complete Node.js program you can explain end to end?

## Outcomes

By the end you can:

- distinguish Node.js, ECMAScript, TypeScript, npm, ESM, compilation, type checking, and execution;
- predict JavaScript primitive, coercion, equality, truthiness, and control-flow behavior;
- reason about lexical scope, closures, callback invocation, and `this`;
- track object and array identity, aliases, mutation, and shallow copies;
- model closed domain alternatives with discriminated unions and exhaustive handling;
- accept external values as `unknown` and establish trusted data through runtime validation;
- build deterministic collection transformations with arrays, maps, sets, and basic generics;
- organize an ESM package with explicit public and private boundaries;
- preserve causal errors across parsing, domain, persistence, and process layers;
- own promises and asynchronous file operations rather than leaving work unobserved;
- test pure rules, public modules, persistence, and real CLI behavior;
- build and independently extend StudyLedger.

## Course surfaces

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Reference desk](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [StudyLedger engineering guide](course-book/capstone.md)
- [Independent laboratories](labs/)
- [Compiler and runtime investigations](compiler-labs/README.md)
- [Complete capstone](capstone/README.md)

## Toolchain

```text
Node.js 24.19.0 LTS
npm 11.17.0
TypeScript 7.0.2
ECMAScript modules
strict type checking
Node built-in test runner
```

Install dependencies, then run the pinned-baseline proof:

```bash
npm install
make proof
```

`make proof` requires the exact Node.js, npm, and TypeScript versions above and a working MkDocs installation. It fails rather than silently downgrading an unavailable check. While porting or inspecting the course on another maintained toolchain, use:

```bash
make verify
```

`make verify` executes every available audit, investigation, type check, and test, but labels version differences and unavailable documentation rendering instead of claiming the pinned release baseline.
