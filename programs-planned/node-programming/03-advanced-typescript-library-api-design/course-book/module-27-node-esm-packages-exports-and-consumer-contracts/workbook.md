# Module 27 Workbook

For each import, trace TypeScript resolution, emitted specifier, package export, declaration target, and Node runtime target.

## A. Repair ESM imports

Given extensionless and type/value-mixed imports, rewrite them for NodeNext ESM and explain the emitted graph.

## B. Design an export map

Create root, `./format`, and `./testing` subpaths. Include `types` and `import` targets, and write one negative deep-import test.

## C. Compatibility inventory

A package currently exposes `dist/parser.js`, `dist/errors.js`, and `package.json` by accident. Plan an `exports` introduction with either aliases or a major-version migration.

## D. Side-effect audit

Classify import-time environment reads, listener registration, prototype patching, cache creation, and constant-table construction. Move inappropriate effects behind explicit operations.

## E. Consumer fixture

Write a fixture that imports the built package by name, checks one inferred type, runs one runtime operation, and proves an internal path is unavailable.

## F. Independent laboratory

Complete [Encapsulated ESM Library Surface](../../labs/module-27-encapsulated-esm-library-surface/README.md). Inspect the packed file list.

## G. SchemaKit transfer

Add root, JSON, and testing exports. Verify declaration/runtime parity, no default export, no import-time effect, and no reachable internal decoder path.

## H. Reconstruction

Explain the roles of `type`, `exports`, `types`, relative `.js` specifiers, type-only imports, and consumer fixtures.

## I. Resolution trace

For each import below, trace package-name lookup, `exports` selection, condition selection, declaration target, emitted JavaScript target, and final runtime URL:

```ts
import { greet } from '@example/greet';
import { helper } from '@example/greet/testing';
import type { Greeting } from '@example/greet';
```

Identify which tool owns each step.

## J. Export-map migration

Start from a package with no `exports` field and consumers deep-importing `dist/internal.js`. Add an export map containing only `.` and `./testing`. Explain why this can be breaking even if the main entry point remains unchanged. Design a staged migration.

## K. Side-effect budget

Audit every top-level statement in the Encapsulated ESM Library. Classify it as declaration, deterministic constant construction, environment read, I/O, registration, or mutation. Move avoidable effects behind explicit functions.

## L. Type/runtime target agreement

Deliberately point the `types` condition for one subpath at the wrong declaration file. Create a consumer call that type-checks but fails at runtime or vice versa. Repair the map and add a package-contract test.

## M. Public-path decision

For each candidate path—`./testing`, `./internal`, `./package.json`, `./format`, and `./experimental`—decide whether to export it. State ownership, compatibility, and removal consequences. “The file exists” is not a reason.

## N. Installation-shape test

Create a temporary directory, copy only files named by the package `files` policy, and import every supported entry point from that installation-shaped directory. This catches tests that accidentally depend on source files or unshipped fixtures.

## O. Conditional export restraint

Sketch separate import and require targets, then list the dual-package hazards they introduce: duplicated module instances, divergent state, declaration mismatch, and inconsistent semantics. Decide whether your current product actually needs both module systems. Supporting fewer conditions can be the more reliable contract.
