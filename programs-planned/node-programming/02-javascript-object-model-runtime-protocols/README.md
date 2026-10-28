# Course 2 — JavaScript Object Model and Runtime Protocols

## Properties, prototypes, classes, iteration, reflection, and object lifecycles

This is the second course in the Node.js Programming program. Course 1 established strict TypeScript, JavaScript values, ESM packages, validation, promises, files, tests, and complete command-line programs. Course 2 goes beneath everyday object syntax and teaches the runtime mechanisms that make JavaScript objects behave as they do.

The course is TypeScript-first for construction and JavaScript-first for semantics. TypeScript can describe a public surface, but it does not replace property descriptors, prototype lookup, receiver binding, private brands, iteration protocols, proxy invariants, cloning behavior, reachability, or cleanup. Those are runtime facts.

> **Governing question:** How do JavaScript objects acquire state and behavior, participate in language protocols, preserve or hide identity, cross persistence boundaries, and remain correct when reflected on, wrapped, cloned, iterated, and disposed?

## Entry standard

Begin after completing Course 1 or proving equivalent ability. You should be able to:

- configure and run a strict TypeScript ESM package;
- distinguish static checks from runtime validation;
- reason about primitive values, functions, closures, object identity, arrays, maps, and promises;
- build a small tested CLI with JSON persistence;
- read a compiler diagnostic and identify the responsible language or host layer.

The course does not reteach those skills. It uses them continuously.

## Course promise

After ten dense modules, you will be able to:

- inspect and define properties through complete descriptors;
- predict own-property, prototype, and receiver behavior;
- explain function callability, constructibility, `this`, `new`, and bound functions;
- use classes and private fields without confusing syntax with semantics;
- choose among inheritance, delegation, forwarding, copying, closures, and capability composition;
- implement and consume symbol-keyed runtime protocols;
- build lawful iterables, iterators, and generators with explicit closing behavior;
- use reflection and proxies without violating target invariants;
- distinguish shallow copying, structured cloning, domain reconstruction, reachability, and deterministic cleanup;
- audit and evolve a complete object-oriented runtime architecture.

## Product structure

```text
02-javascript-object-model-runtime-protocols/
├── course-book/       authoritative chapters, workbooks, solutions, reference, and capstone guide
├── labs/              ten independent products with starter and reference packages
├── compiler-labs/     eighty causal type-check and runtime investigations
├── capstone/          complete ObjectAtlas library and CLI
├── tools/             verification and source-policy routes
├── package.json       pinned toolchain and workspace scripts
└── Makefile           reader-facing commands
```

The course book is the primary product. The laboratories and ObjectAtlas exist to make the explanations executable.

## Main routes

```bash
npm install
npm run verify
```

For exact pinned-toolchain and documentation proof:

```bash
make proof
```

Read [the course-book entry point](course-book/index.md) before opening the laboratories.
