# Course 3 — Advanced TypeScript and Library API Design

## Structural typing, generic relationships, type transformations, declarations, package boundaries, runtime schemas, and compatibility

This is the third course in the Node.js Programming program. Course 1 established strict TypeScript, JavaScript values, ESM execution, runtime validation, promises, files, and complete small programs. Course 2 established the JavaScript object model: descriptors, prototypes, receivers, private brands, protocols, proxies, identity, cloning, and lifecycle.

Course 3 turns those foundations into a library-design discipline. The subject is not “advanced syntax.” The subject is the agreement among five surfaces:

```text
runtime JavaScript behavior
        ↕
TypeScript relationships
        ↕
emitted declaration files
        ↕
Node.js package entry points
        ↕
downstream compatibility
```

> **Governing question:** How do you design a TypeScript library whose runtime behavior, inferred types, declarations, package exports, and evolution policy tell the same story?

## Entry standard

Begin after Course 2 or equivalent experience. You should be able to:

- build and test a strict ESM TypeScript package;
- distinguish runtime values from erased type contracts;
- reason about object identity, descriptors, prototypes, receivers, classes, and private brands;
- validate `unknown` data before treating it as domain data;
- separate live objects, persistence records, diagnostics, and process representations;
- explain a type-check failure and a runtime failure as different events.

The course does not repeat basic unions, classes, object syntax, or package setup. It uses them as prerequisites.

## Course promise

After ten dense modules, you will be able to:

- reason about structural assignability without confusing it with exact runtime shape;
- design generic APIs that preserve real relationships and support useful inference;
- derive conditional, mapped, and template-literal types without losing control of distribution or complexity;
- review variance and callback safety instead of trusting apparent assignability;
- emit, inspect, and test declaration files as a public artifact;
- publish a restrained ESM package surface through `exports` and declaration entry points;
- create runtime schemas whose inferred types agree with validated output;
- distinguish source, type, runtime, behavior, package, and data-format compatibility;
- evolve a public library through explicit deprecation and migration policy;
- complete and defend SchemaKit, an ESM schema-combinator library with a real downstream contract.

## Product structure

```text
03-advanced-typescript-library-api-design/
├── course-book/       authoritative chapters, workbooks, solutions, reference, and SchemaKit guide
├── labs/              ten independent products with starter and reference packages
├── compiler-labs/     eighty causal type-check and runtime investigations
├── capstone/          complete SchemaKit package and example CLI
├── tools/             verification and source-policy routes
├── package.json       pinned toolchain and workspace scripts
└── Makefile           reader-facing commands
```

The course book is the primary product. The labs and SchemaKit exist to make its claims executable.

## Main routes

```bash
npm install
npm run verify
```

For exact pinned-toolchain and documentation proof:

```bash
make proof
```

Begin with [the course-book entry point](course-book/index.md).
