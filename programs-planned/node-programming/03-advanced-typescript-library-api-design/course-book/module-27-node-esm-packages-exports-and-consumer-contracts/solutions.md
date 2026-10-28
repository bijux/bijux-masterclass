# Module 27 Reasoned Solutions

## A. Imports

Node ESM executes emitted `.js` files, so relative source specifiers use `.js` under NodeNext. Type-only imports are marked explicitly and disappear from the runtime graph.

## B. Export map

Every subpath needs matching declaration and runtime targets. Internal paths remain absent. Conditions should stay simple and specific. A negative test should import as a consumer, not merely inspect a file.

## C. Compatibility

Introducing `exports` closes undeclared paths. Preserve historical paths temporarily or release a major version with migration instructions. `package.json` access must also be exported if it remains supported.

## D. Side effects

Pure constant construction is usually acceptable. Environment reads, handlers, prototype mutation, and external resource acquisition should be explicit. Caches may be safe only when identity, lifetime, and test isolation are documented.

## E. Consumer fixture

The fixture must resolve built package metadata. Source aliases or relative imports bypass the contract. It should test both static inference and actual ESM execution.

## F. Laboratory

The reference package exposes only documented root, formatting, and testing surfaces. Internal helpers are available to source modules but unavailable to package consumers.

## G. SchemaKit

The main entry contains production combinators, JSON owns text decoding, and testing owns assertions/formatting. The declaration condition and import condition for each path describe the same exports.

## H. Reconstruction standard

A complete explanation follows one specifier from consumer source to declaration and runtime file, then identifies side effects, packaged files, and compatibility promises.

## I. Resolution

Node resolves the package and selects an import target from `exports`; TypeScript in NodeNext mode mirrors the package contract while selecting declaration information. A type-only import still requires declaration resolution but creates no runtime edge. Relative imports inside emitted ESM use their emitted `.js` names. The trace should end at both one `.d.ts` contract and one JavaScript URL.

## J. Adding exports

An export map encapsulates all undeclared subpaths. Consumers relying on deep imports will fail even though those files remain in the tarball. A staged migration can publish supported replacement subpaths, deprecate old documented paths, add consumer fixtures, and reserve the strict encapsulation change for a major release when necessary.

## K. Effects

Declarations and immutable tables are usually safe top-level work. Environment reads, file access, network access, process mutation, and global registration make import itself observable and harder to test. Libraries should expose explicit initialization when the effect has failure, ordering, or cleanup semantics.

## L. Conditions

The `types` target and runtime `import` target must describe the same API. A wrong type target can make a missing runtime export appear valid or hide a real export. A consumer fixture importing each supported subpath and executing representative behavior is stronger than inspecting JSON alone.

## M. Path ownership

`./testing` is reasonable when consumers need stable test helpers. `./internal` is contradictory unless those internals become supported. Package metadata may be exported deliberately, but doing so creates a contract. A focused `./format` can be useful if it represents a separable capability. Experimental paths need an explicit stability policy; the name alone does not exempt them from consumer reliance.

## N. Installation shape

Tests run inside the repository can accidentally import files that are absent from the published package. An installation-shaped test reproduces the consumer artifact: built JavaScript, declarations, package metadata, and documented assets only. Supported imports must resolve there. Fixtures, source maps, or internal modules should appear only when deliberately shipped.

## O. Conditions

Separate ESM and CommonJS implementations can be loaded as different module instances, producing duplicated singleton state and identity. Their behavior and declarations can drift. Conditional exports are justified only when the product truly supports both environments and tests cross-mode semantics. An ESM-only package is often the clearer modern Node contract.
