# Module 1 Workbook

## A. Predict before using tools

Classify each as `typecheck-pass`, `typecheck-fail`, `run-pass`, or `run-fail`. Some snippets require two classifications.

1. `const value: number = JSON.parse('"5"');` followed by `value + 1`.
2. A package contains `"type": "module"`, but emitted JavaScript imports `./math` rather than `./math.js`.
3. `import type { Config } from './config.js';` where `Config` is used only in an annotation.
4. `import { Config } from './config.js';` when `Config` is a type alias and `verbatimModuleSyntax` is enabled.
5. `node src/main.ts` on a runtime that strips types, where the file contains a TypeScript `enum` requiring transformation.
6. A global `tsc` accepts the project while `npm run typecheck` rejects it.
7. A function parameter is typed `number`, but a JavaScript caller imports the emitted file and passes a string.
8. A test file imports `../src/parser.ts` while the emitted test imports from `dist/tests`.

For each answer, name the decisive phase.

## B. Trace the artifacts

For the following command, list every file and mechanism involved:

```bash
npm test
```

Assume the script runs `npm run build && node --test dist/tests`. Include package metadata, local binaries, source files, emitted modules, the Node resolver, the test runner, and process exit status.

## C. Repair without weakening the contract

A project currently has:

```json
{
  "scripts": { "test": "node src/index.ts" },
  "devDependencies": { "typescript": "*" }
}
```

The source uses assertions to convert `JSON.parse` results into domain types. Repair the tool and execution boundary. Do not solve the problem by changing all inputs to `any` or disabling strict checks.

## D. Focused construction

Create a package named `runtime-card` containing:

- one pure parser for `process.version`;
- a function that returns a structured report from injected inputs;
- a renderer that produces deterministic text;
- a CLI shell that supplies actual process values;
- tests for accepted and rejected versions.

The library must not read `process` directly.

## E. Independent laboratory

Complete [Runtime Report](../../labs/module-01-runtime-report/README.md). Before comparing with the reference, write the source-to-process trace for one test and one CLI invocation.

## F. StudyLedger transfer

Implement `help` and `version` while preserving these boundaries:

- library rendering is pure;
- the binary owns `process.argv`, `stdout`, `stderr`, and `exitCode`;
- ESM imports name emitted `.js` files;
- tests import the public library surface.

## G. Reconstruction

Without notes, explain:

- why TypeScript 7 and Node 24 are separate versioned dependencies;
- why native type stripping is not the same as type checking;
- why a successful `tsc` run cannot validate file contents;
- why `"type": "module"` and NodeNext configuration must agree;
- which evidence proves the CLI’s exit contract.

## H. Extended boundary investigation

A teammate reports: “The editor shows no errors, `node src/main.ts` prints the help page, but `npm test` fails with `ERR_MODULE_NOT_FOUND` for `./command`.” Produce a diagnosis that names every relevant artifact. Your answer must include the local compiler version, the active `tsconfig`, emitted file names, package module mode, and the exact import specifier Node attempts to resolve.

Then repair this miniature package without weakening strictness:

```json
{
  "type": "module",
  "scripts": { "test": "node --test tests" },
  "devDependencies": { "typescript": "*" }
}
```

```ts
// src/main.ts
import { parse } from './parse';
const raw: number = JSON.parse('"7"');
console.log(parse(raw));
```

Your repaired route must separate static checking, emission, and executable tests. Explain why each command exists.

## I. Source-to-process reconstruction

Without notes, draw the path from `capstone/src/main.ts` to a successful `studyledger version` process. Label which stage reads `package.json`, which stage erases types, which stage resolves `.js`, and which stage owns stdout and exit status.

## J. StudyLedger checkpoint

Create the package skeleton and help/version route. Add one process-level test that imports no private helper and observes exact stdout, stderr, and status. Record one claim that this test does **not** establish.
