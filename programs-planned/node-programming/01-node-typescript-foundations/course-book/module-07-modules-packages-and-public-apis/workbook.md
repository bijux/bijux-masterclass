# Module 7 Workbook

## A. Import graph

Draw the graph and find the cycle:

```text
main -> app -> storage -> model
app -> command -> model
model -> app
```

Move responsibility rather than hiding the cycle with dynamic import.

## B. Side-effect audit

Classify these top-level operations: defining a constant, parsing `process.env`, opening a file, registering a signal handler, constructing a regex, starting a timer, creating a logger object. Decide which module should own each effect.

## C. Public surface

Design an `index.ts` for a package with domain constructors, an internal cache, a file repository, and a CLI. Expose only what another module genuinely needs.

## D. ESM repair

Repair imports, type-only imports, and package metadata in a project that emits ESM but uses extensionless relative specifiers and CommonJS assumptions.

## E. Independent laboratory

Complete [Package Boundary](../../labs/module-07-package-boundary/README.md). Its tests import the public entry point and verify that a private module cannot be reached through package exports.

## F. StudyLedger transfer

Split modules by authority. Add an import-graph note to the capstone documentation. Prove importing the public library does not inspect the environment or filesystem.

## G. Reconstruction

Explain module evaluation, live bindings, type-only imports, package type, relative `.js` specifiers, public exports, and why side effects at import time damage testability.

## H. Module graph review

Draw the graph for `main`, `app`, `command`, `domain`, `storage`, and `render`. For every arrow, state whether it is a runtime import or a type-only import. Identify one cycle that would be easy to introduce and refactor it away.

Repair these imports under NodeNext ESM:

```ts
import { Ledger } from './domain';
import parser from './command.js';
```

Assume `Ledger` is an interface and `command.ts` exports only a named `parseCommand`.

## I. Public surface decision

Choose which StudyLedger symbols belong in `src/index.ts`. Defend why temporary-file naming, JSON helper internals, and process environment selection remain private.

## J. StudyLedger checkpoint

Add a structural test or source audit proving domain code imports no `node:` modules and import-time execution performs no file access.
