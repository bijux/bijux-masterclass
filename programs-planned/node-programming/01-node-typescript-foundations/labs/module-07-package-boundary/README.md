# Laboratory 7 — Package Boundary

## Product and purpose

The conversion package makes ESM architecture observable. Public imports, private implementation, initialization effects, and package metadata must agree. The domain is intentionally small so module behavior cannot hide behind business logic.

## Entry standard

Draw two graphs: runtime imports and type-only imports. Mark the supported package entry, internal files, initialization side effects, and any cycle. Predict the Module 7 resolution cases and inspect the package metadata before running the starter. A file that can be imported relatively is not automatically supported public API.

## Public contract

The public entry exposes conversion and formatting only. Calibration data and audit counters remain private. Relative imports name emitted `.js` files. Importing the package performs declarations only: no environment read, file access, logging, timer, or mutable registration.

## Required construction sequence

Create the dependency graph, implement named exports, and add behavior tests through the public entry. Inspect package metadata or attempt unsupported subpath imports to prove internal files are not promised. Verify import order does not alter output.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Attempt the supported import, an undocumented deep import, a missing named export, a type-only value use, a dependency-renamed consumer, and an initialization cycle. Add a process-level import that proves no file or environment read occurs merely by loading the package. Diagnose resolver, linker, evaluator, and product-boundary defects separately.

## Prohibited shortcuts

Do not wildcard-export every file, add synthetic default imports to conceal mismatches, read environment at module top level, or introduce a cycle between formatting and conversion. Do not claim a file is private only because its name says internal.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when the documented entry imports successfully from a consumer package, unsupported internals are not part of the declared surface, type-only edges emit no runtime import, top-level evaluation performs no hidden effects, and the graph contains no hazardous cycle. Explain the linking/evaluation sequence for one import before viewing the reference.

## Independent transfer

Add a `./format` public subpath without exposing calibration or creating a cycle. Explain how the export map and declaration output must change together.

Write the supported import examples before editing exports. Confirm the new subpath exposes only the intended symbols, emits declarations, performs no top-level calibration, and does not create a cycle back into the main entry.


Test the consumer from emitted JavaScript, not only from TypeScript source. This distinguishes declaration correctness from Node’s actual package-resolution behavior.
