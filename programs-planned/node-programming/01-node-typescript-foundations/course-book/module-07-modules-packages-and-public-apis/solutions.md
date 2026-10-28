# Module 7 Solutions

## A. Cycle

`model -> app` violates the intended stable center. Move the needed rule into `model` or pass a capability from `app`; the domain should not import orchestration.

## B. Effects

Pure declaration and regex construction are normally safe. Environment reads belong in process/configuration adapters. File open and timers belong in explicit effect functions. Signal handlers belong in the executable lifecycle. A logger object is safe only if construction itself has no external effect.

## C. Surface

Export stable domain types/constructors and the application facade. Keep caches and concrete filesystem implementation private unless extension is a product requirement. The CLI should be a binary, not a library export.

## D. ESM

Declare `type: module`, use NodeNext, include `.js` in relative imports, replace `require`/`module.exports`, and mark type-only imports. Do not fix runtime resolution with a bundler in a course intended to teach Node’s own graph.

## E–F. Design notes

Package-boundary tests should import by the documented entry point. StudyLedger’s `main` supplies environment and path. Public imports should instantiate no files, timers, or handlers.

## G. Readiness answer

ESM loads and evaluates a graph once per module identity and exposes live bindings. Type-only imports disappear. Package metadata controls `.js` interpretation. Relative ESM paths are explicit. The public entry point limits contract surface. Import-time effects make order and environment observable before the caller asks for behavior.

## Extended solution

The runtime graph uses main → app, app → domain/render types and storage interface, main → command/storage/render, and public index → selected library symbols. Type-only edges should use `import type`. Domain must not import main or storage; that would create policy cycles.

`Ledger` is imported with `import type { Ledger } from './domain.js'`. `parseCommand` is imported as a named value from `./command.js`. Changing resolver mode to conceal extensionless imports would misdescribe direct Node execution.

The public entry includes commands, domain operations, error categories, codec, and repository functions useful to tests and callers. Temporary naming and environment path selection remain private because exposing them would make implementation details compatibility promises. A source audit can enforce the absence of `node:` imports from domain files.
