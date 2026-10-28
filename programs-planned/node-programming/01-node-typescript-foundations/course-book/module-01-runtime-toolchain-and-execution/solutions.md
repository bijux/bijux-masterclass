# Module 1 Solutions

## A. Prediction reasoning

1. **Typecheck-pass and surprising runtime value.** The historical `JSON.parse` declaration is permissive, so the assignment may be accepted. The runtime value is the string `"5"`; `value + 1` performs string concatenation and produces `"51"`. The principled repair is to receive the parsed value as `unknown` and validate it.
2. **Build may pass; run-fail at ESM resolution.** Node does not perform extension searching for a relative ESM import. The repair is `./math.js` in TypeScript source under NodeNext.
3. **Typecheck-pass.** `import type` states that no runtime import is required.
4. **Typecheck-fail.** With verbatim module syntax, a type-only symbol must use a type-only import. Removing the option would hide the mismatch rather than express the intended graph.
5. **Run-fail.** Type stripping handles erasable syntax, not every syntax requiring JavaScript transformation. The canonical build emits supported JavaScript.
6. Both outcomes are possible because the commands may use different compiler versions or configurations. The package-local command is authoritative for the project.
7. The TypeScript caller contract does not constrain arbitrary JavaScript callers at runtime. The emitted function receives a string. Public runtime boundaries need validation when JavaScript or external data can call them.
8. The source import describes a path that does not exist in the emitted runtime graph. The repair is the emitted `.js` specifier.

## B. Artifact trace

npm reads `package.json`, resolves the local `tsc`, reads `tsconfig.json` and source modules, emits JavaScript and source maps into `dist`, then starts Node with the test flag. Node reads package type metadata, resolves each `.js` import, evaluates modules, registers tests, executes them, reports results, and exits. A failure at any step produces a nonzero command result, but the causal owner differs.

## C. Repair

Pin the supported runtime and compiler, declare ESM, add a strict TypeScript configuration, separate `typecheck`, `build`, and `test`, and replace assertions at the JSON boundary with validation. Changing `typescript` from `*` to a known line prevents unreviewed checker changes from arriving silently.

## D–F. Design notes

The report library should receive `{ version, platform, arch }` rather than importing `process`. That makes the static and runtime contracts testable with ordinary values. The CLI is a thin adapter. StudyLedger uses the same pattern: pure help/version behavior inside the library; process ownership only in `main.ts`.

## G. Readiness answer

Node versions the host APIs and runtime semantics; TypeScript versions static analysis and emission. Type stripping removes syntax but does not prove type relationships. File validity is a runtime claim. ESM metadata and compiler resolution must describe the same graph. Only a process-level test can directly observe arguments, streams, and exit status together.

## Extended solution

The editor can use a different TypeScript version or resolver from the package command. Direct source execution can strip types and resolve the entry while the emitted test graph still contains `./command` without an extension. The diagnosis begins by printing `node --version`, `npm --version`, and the package-local compiler version, then inspecting the effective configuration and `dist` imports. The principled import is `./command.js` in TypeScript source under NodeNext.

A repaired package pins a reviewed compiler line, declares ESM, adds `typecheck`, `build`, and `test`, and runs tests against emitted files. The JSON result begins as unknown; a runtime parser establishes number validity. A cast would repair only the static symptom.

For `studyledger version`, npm is not involved once the emitted binary is started. Node reads package metadata to interpret `.js` as ESM, resolves `main.js` and its imports, evaluates the module, the process adapter parses the command, the application returns version text, and main writes stdout and sets status. The process test does not prove JSON persistence or other commands.
