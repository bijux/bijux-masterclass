# Encapsulated ESM Library Surface

## The product

Publish a small ESM greeting library with exactly two supported entry points:

```text
@bijux-masterclass/encapsulated-esm-library-reference
@bijux-masterclass/encapsulated-esm-library-reference/testing
```

Normalization remains internal. File existence under `dist` does not make a path public.

Read [Module 27](../../course-book/module-27-node-esm-packages-exports-and-consumer-contracts/index.md) before implementation.

## Public contract

The main entry exports `Greeting` and `greet`. The testing subpath exports a helper that consumes the public `Greeting` type. `package.json` must align `types` and `import` targets for both paths. Relative ESM imports use emitted `.js` specifiers.

The package should have no import-time environment reads, I/O, global registration, or mutable singleton initialization.

## Milestones

1. Draw the source module graph and mark public versus private files.
2. Implement the internal normalizer and main facade.
3. Add a testing helper without importing private consumer paths.
4. Configure `exports` with paired declaration and runtime targets.
5. Build and verify every target exists.
6. Create an installation-shaped consumer rather than importing source.
7. Attempt an unsupported deep import and require failure.
8. Inspect emitted declarations for internal path leakage.

## Adversarial cases

Point one `types` condition at the wrong declaration and observe the mismatch. Add an `exports` field to a package whose old consumers deep-imported internals and explain the break. Audit top-level side effects and move avoidable work behind explicit calls.

Do not add CommonJS output merely for completeness. Supporting two module systems is a product commitment involving identity, state, behavior, and declarations.

## Design record

Decide whether to export `./testing`, `./internal`, `./package.json`, and an experimental path. For each, state consumer value, stability, removal cost, and owner. Explain why the package map rather than the directory tree defines the supported surface.

## Independent transfer

Build a formatting or parsing package with one main and one narrow subpath. Test it from a temporary installation-shaped directory.

## Completion standard

A consumer must resolve the same API through TypeScript declarations and Node ESM execution. No test may depend on a private source file that the package does not ship.
