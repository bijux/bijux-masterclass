# Module 26 Workbook

Treat declarations as if implementation source were unavailable.

## A. Runtime/declaration mismatch

Given a JavaScript runtime and three candidate `.d.ts` files, identify mismatches in export kind, return type, optionality, callback behavior, and thrown errors. Write runtime tests capable of falsifying each claim.

## B. Ambient scope

Classify each declaration as external module, global, ambient module, or augmentation. Explain what import or runtime side effect must exist.

## C. Emission review

Build a small TypeScript library with declaration emission. Find:

- one anonymous public shape worth naming;
- one internal helper leaked through inference;
- one broad type caused by widening;
- one declaration import path that must remain resolvable.

Repair the public source, not the emitted file.

## D. Type tests

Write:

- three positive inferred-type assertions;
- three `@ts-expect-error` cases, each isolating one rule;
- one consumer test that imports the package entry point;
- one test proving an internal deep import is unsupported.

## E. Augmentation review

Design a hypothetical module augmentation. List the static declaration, runtime installation, import side effect, collision risk, and removal/migration strategy. Then decide whether an explicit wrapper is clearer.

## F. Independent laboratory

Complete [Legacy Runtime Declaration Facade](../../labs/module-26-legacy-runtime-declaration-facade/README.md). Both runtime and consumer type tests are mandatory.

## G. SchemaKit transfer

Emit and inspect declarations. Create a parity table for main, JSON, and testing surfaces. Ensure internal decoders, mutable contexts, and source paths are absent.

## H. Reconstruction

Explain what a declaration proves, how it can lie, how a consumer test differs from an implementation test, and why package metadata is the next part of the proof.

## I. Artifact inspection

Build one laboratory package, then inspect the emitted `.js`, `.d.ts`, `.d.ts.map`, and package metadata. For every exported declaration, locate the runtime binding that supports it. For every runtime export, decide whether it is intentionally public.

## J. Wrong declaration experiment

Change the legacy counter declaration so `increment` returns `string` while runtime still returns `number`. Show that a consumer can type-check and then fail or behave incorrectly. Restore alignment and add a runtime contract test that would detect the drift.

## K. Type-only boundary

Create a module exporting one class, one interface, one const enum alternative, and one type alias. Import each correctly under verbatim module syntax. Explain which names survive emission and which cannot be used at runtime.

## L. Consumer fixture

Create a separate consumer package that imports only supported entry points from the built laboratory. Type-check it against emitted declarations and execute it against emitted JavaScript. Do not let the consumer import source files.

## M. Declaration review

Audit for leaked private helper types, inferred anonymous object explosions, accidental overload order, widened literals, missing readonly guarantees, and dependencies on internal file paths. Propose one explicit public alias that improves the declaration without duplicating runtime logic.

## N. Declaration compatibility fixture

Copy the emitted declaration surface into a small consumer fixture that represents version 1 usage. Make one candidate source change at a time—rename a type, reorder overloads, change a generic default, narrow an input, or expose a concrete internal class. Rebuild declarations and identify which old uses fail.

## O. Runtime export census

Use `Reflect.ownKeys` on each public module namespace after build. Compare the observed runtime exports with the names in the declaration file and package documentation. Explain every intentional type-only name and treat every unexplained mismatch as a release defect.
