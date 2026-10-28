# Laboratory 1 — Runtime Report

## Product and purpose

The runtime report is a controlled first product. It lets you prove the complete TypeScript-to-Node route without hiding a failure inside a large domain. The library receives environment facts as ordinary input; only a thin executable adapter may read `process`.

## Entry standard

Reconstruct the source → checker → emitted ESM → Node process chain before opening the starter. Predict all eight Module 1 investigations and write which authority owns each result. Run the starter tests once to verify the package route, then inspect the emitted import specifiers. The starter proves only that the baseline builds; version grammar, policy, rendering, and process binding remain your responsibility.

## Public contract

The accepted version grammar is exactly `vMAJOR.MINOR.PATCH`. Each component is a canonical nonnegative decimal safe integer. The report preserves platform, architecture, executable path, and ESM mode as opaque values; it does not reject an unfamiliar platform name. Support policy is derived from the parsed major version and kept separate from parsing.

## Required construction sequence

Implement version parsing, report construction, deterministic rendering, and a CLI adapter. Begin with failing tests for missing prefix, missing component, suffix text, negative or fractional components, whitespace, and unsafe integers. Add a structural assertion that the library source has no `process` or `node:` dependency.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Test empty strings, missing `v`, missing or extra components, leading plus/minus, whitespace, suffix text, leading-zero policy, values beyond the safe-integer range, and unfamiliar platform/architecture strings. Also run the executable with controlled facts so a renderer defect is not confused with a version-parser defect. Every rejection should identify the violated grammar rather than fail later in arithmetic.

## Prohibited shortcuts

Do not use `split` without validating the complete grammar, do not allow `Number` to turn empty components into zero, and do not read process globals inside the reusable function. A type annotation on the version string is not validation.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when the complete version grammar has table-driven tests, report construction is independent of `process`, rendering is byte-for-byte stable, the CLI adapter alone reads runtime facts, and emitted ESM runs through Node. Explain one failure that TypeScript catches, one that Node catches, and one that only a product test catches before comparing with the reference.

## Independent transfer

Extend support classification to `older`, `baseline`, and `newer`. The parser must remain unchanged; only policy and rendering should grow.

Before coding, state which type and policy table change, which renderer line changes, and which tests prove that parsing remained untouched. The transfer fails if the version grammar is broadened merely to support the new classification.
