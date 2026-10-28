# Module 7 — Modules, Packages, Resolution, and Public API Boundaries

> **Question:** Which import causes which module to execute, and which paths are intentionally part of the package contract?

## Why this comes now

You have enough domain code to need structure. Splitting files too early creates navigation without architecture; keeping everything in one file now hides authority. ESM modules are executable units with live bindings, cached evaluation, and a resolution algorithm. A package adds metadata and an intentional import surface.

The objective is not “one file per class.” It is a dependency graph whose direction can be explained.

## Outcomes

You can:

- distinguish file, module, package, dependency, and public entry point;
- trace ESM resolution and evaluation from one import;
- use `.js` relative specifiers correctly in TypeScript NodeNext source;
- explain live bindings, one-time module evaluation, and cycle risks;
- keep top-level effects narrow and visible;
- classify dependencies, development tools, and built-in modules;
- design StudyLedger’s domain, command, storage, application, and process boundaries.

## 1. A module is an executable boundary

Every ESM file has its own scope and explicit imports/exports. Importing a module can execute its top-level code once per module instance:

```ts
console.log('configuration loaded');
export const mode = 'strict';
```

A caller importing `mode` also triggers the log. This is why module top level should primarily establish declarations. Hidden file reads, environment parsing, timers, and network connections make import order observable and tests difficult.

## 2. Static imports create a graph

```ts
import { execute } from './app.js';
```

Node resolves the specifier, loads dependencies, instantiates module bindings, and evaluates the graph in dependency order subject to cycle rules. Imports are not textual inclusion.

Bindings are live. If a module exports a mutable binding and changes it, importers observe the updated value. The course avoids public mutable bindings because they create a hidden shared-state authority.

## 3. Cycles are not automatically safe

ESM supports cycles, but evaluation timing can expose uninitialized bindings or create architecture that is difficult to explain:

```text
app -> storage -> model -> app
```

The better repair is usually dependency direction, not rearranging imports until the cycle happens to run.

StudyLedger uses:

```text
main
  ↓
app ─────> command
  ↓           ↓
storage ───> domain
```

`domain` imports no process or filesystem module. `storage` knows domain validation. `app` orchestrates a typed command over a ledger and dependencies. `main` owns the process.

## 4. Public surface versus file reachability

An application package can still benefit from one public library entry:

```ts
// src/index.ts
export { executeCommand } from './app.js';
export { parseCommand } from './command.js';
export type { Command } from './command.js';
```

Tests of public behavior import `index.js`. Unit tests may live beside private modules when the implementation detail itself needs focused evidence.

For published packages, `exports` defines reachable package subpaths. Introducing it can be a breaking change if consumers previously deep-imported internal files. Course 3 treats public package evolution deeply; Course 1 establishes the boundary.

## 5. Type-only imports

```ts
import type { StudySession } from './domain.js';
```

A type-only import makes it explicit that no runtime dependency is needed. Under verbatim module syntax, this protects the emitted graph from accidental imports and clarifies cycle analysis.

Do not mechanically convert every import. Values such as classes, constants, validators, and functions need runtime imports.

## 6. Package metadata

Important fields include:

```json
{
  "name": "study-ledger",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "main": "./dist/src/main.js",
  "bin": { "study-ledger": "./dist/src/main.js" },
  "scripts": { "build": "tsc -p tsconfig.json" }
}
```

`private` prevents accidental publication. `bin` describes a command entry point after installation. Scripts name canonical operations. Runtime dependencies belong in `dependencies`; compilers and type declarations belong in `devDependencies` for an application build.

Avoid dependency installation for trivial functions that the standard library or a small local function already provides. The cost of a package includes transitive code, maintenance, license, update, and supply-chain surface.

## 7. Configuration is not a global singleton

Reading environment variables at module top level couples import to process state:

```ts
export const DATA_FILE = process.env['STUDY_LEDGER_FILE'] ?? 'study-ledger.json';
```

A better process boundary reads configuration and passes it inward:

```ts
function readDataPath(environment: NodeJS.ProcessEnv): string {
  return environment['STUDY_LEDGER_FILE'] ?? 'study-ledger.json';
}
```

Tests can supply a plain object. Importing the domain does not inspect the environment.

## 8. Module errors need context

A module should translate failures only when it adds meaningful boundary information:

```ts
try {
  return await readFile(path, 'utf8');
} catch (error: unknown) {
  throw new Error(`cannot read StudyLedger file ${path}`, { cause: error });
}
```

The storage module adds operation and path. The application can then decide how to render a storage failure. Do not catch only to throw a message that discards the cause.

## 9. Side-effect budget

For each module, record permitted top-level effects:

| Module | Permitted top-level work |
|---|---|
| domain | declarations only |
| command | declarations only |
| storage | declarations only |
| app | declarations only |
| main | process start through an explicit `main()` call |

Even `main.ts` benefits from an explicit function because tests and import analysis can distinguish declaration from execution. A common ESM entry guard is based on `import.meta.url` and the invoked file URL, but the course’s binary file is not imported by tests; tests exercise the library and process separately.

## 10. StudyLedger increment

Split the package into:

```text
src/
├── domain.ts
├── query.ts
├── command.ts
├── storage.ts
├── app.ts
├── index.ts
└── main.ts
```

State why each module changes. Keep `main.ts` thin. Use type-only imports. Ensure no domain module imports `node:` APIs. Add a public-behavior test through `index.ts`.

## Common wrong models

### “A module is just a file organization feature”

It is also a scope, runtime evaluation unit, dependency node, and public boundary.

### “Imports copy exported values”

ESM imports are live bindings.

### “Cycles work, so the architecture is fine”

Legal cycles can still produce fragile evaluation and competing authority.

### “An index file should re-export everything”

A public entry point is a curated contract, not a directory listing.

### “Reading environment at import time is convenient”

It creates hidden process coupling and test-order sensitivity.

## 11. ESM has linking and evaluation phases

An ESM graph is not equivalent to concatenating files. The host resolves specifiers, links import/export relationships, instantiates module environments, and evaluates modules in dependency order. Exports are live bindings:

```ts
// state.ts
export let count = 0;
export function increment(): void { count += 1; }

// consumer.ts
import { count, increment } from './state.js';
increment();
console.log(count); // 1
```

The imported binding observes updates. It is not a copied snapshot and cannot be reassigned by the importer.

Cycles can expose partially initialized bindings or create order-sensitive side effects. A cycle that happens to run is not evidence of a healthy boundary. Break cycles by moving shared primitives downward or by separating construction from use.

## 12. Public reachability and supported API differ

A file may exist on disk without being a supported package import. The `exports` field can define the public surface:

```json
{
  "name": "@example/conversion",
  "type": "module",
  "exports": {
    ".": "./dist/index.js",
    "./format": "./dist/format.js"
  }
}
```

Callers should not depend on `./dist/internal.js` merely because a path currently works. Internal layout can then change without becoming an accidental compatibility promise.

A course application marked `private` does not need a published package export map for every internal crate-like package, but the design habit still matters: one entry file curates reusable behavior; tests import that entry when they claim to protect public behavior.

## 13. Barrels can erase architecture

An `index.ts` that wildcard-exports every sibling makes discovery easy but can flatten intentional boundaries:

```ts
export * from './domain.js';
export * from './storage.js';
export * from './internal-cache.js';
```

The caller can no longer tell which modules are supported. Name exports deliberately. Avoid re-export chains that create cycles or collisions.

Type-only exports should be marked:

```ts
export type { Ledger, Session } from './domain.js';
export { planSession } from './domain.js';
```

This keeps the emitted runtime graph accurate under verbatim module syntax.

## 14. Top-level side effects create hidden lifecycle

Import-time environment reads, filesystem access, logging, timers, and registration mutate global process behavior before the application has selected policy or error handling.

Prefer factories or explicit startup functions:

```ts
export function createRepository(path: string): Repository {
  return { /* methods capture path */ };
}
```

The process adapter decides which path to supply. Tests can import the module without touching a real home directory.

Some modules legitimately perform top-level setup, especially executable entries. The requirement is not “zero side effects everywhere”; it is “side effects have one visible owner and a deliberate lifecycle.”

## 15. Package metadata is part of the source contract

These fields influence behavior:

- `type` — interpretation of `.js` files;
- `exports` — supported import paths;
- `main` — legacy package entry behavior;
- `types` — declaration entry for consumers;
- `bin` — executable command mapping;
- `engines` — supported runtime range;
- `files` — publish inclusion;
- `sideEffects` — bundler-facing information, not a Node execution guarantee.

A library’s declarations and JavaScript must describe the same surface. A type-only export that has no runtime value must not be imported as one.

## 16. Module-boundary error context

Low-level errors should acquire context when crossing an authority boundary:

```ts
try {
  return await readFile(path, 'utf8');
} catch (error: unknown) {
  throw new StorageError(`cannot read configuration at ${path}`, { cause: error });
}
```

Do not wrap at every line. Add context where the operation gains product meaning. Preserve `cause` so diagnostics can still reach the original filesystem failure.

StudyLedger follows a one-way dependency direction: process → application → domain/storage. Domain code imports no Node APIs. Storage knows files but not CLI grammar. The binary binds both and owns exit status.

## Practice sequence

Complete the [workbook](workbook.md), then [Package Boundary](../../labs/module-07-package-boundary/README.md). Refactor StudyLedger and draw the resulting import graph.

## Ready to continue

Continue when every import direction has a reason and importing a library module performs no unrequested external effect.

Next: [Module 8 — Errors, JSON, Runtime Validation, and Persistence Contracts](../module-08-errors-json-validation-and-persistence/index.md)
