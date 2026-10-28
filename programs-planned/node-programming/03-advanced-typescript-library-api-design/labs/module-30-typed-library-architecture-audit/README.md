# Typed Library Architecture Audit

## The product

Build an independent field-spec library whose one shape value owns runtime parsing, inferred output, deterministic formatting, declarations, and public package behavior. This is the transfer assessment for Course 3; it must not depend on SchemaKit.

Read [Module 30](../../course-book/module-30-integrated-library-architecture-and-independent-change/index.md) first.

## Public contract

A field spec parses unknown input and renders its accepted value. `defineLibrary(shape)` returns a library whose output is derived from the field specs:

```ts
const Score = defineLibrary({
  id: textField(),
  score: numberField(),
});

const value = Score.parse({ id: 'a', score: 2 });
Score.format(value); // id=a;score=2
```

Formatting order is canonical and independent of source object insertion order. Implementation helpers and mutable shape state are private.

## Milestones

1. Write the complete surface-agreement table before implementation.
2. Define `FieldSpec<T>` and output extraction.
3. Implement strict runtime parsing from `unknown`.
4. Freeze or copy construction inputs so later mutation cannot change library behavior unexpectedly.
5. Define deterministic key order.
6. Emit and inspect declarations.
7. Add package-path and consumer tests.
8. Create a compatibility fixture and one independent cross-layer change proposal.

## Adversarial cases

Test an invalid field, missing property, extra property under your chosen policy, shape mutation after construction, a wrong declaration path, unsupported deep import, and a field renderer that throws. Identify which verification layer owns each defect.

Do not expose internal shape maps to simplify tests. Verify behavior through the public facade.

## Design record

Produce an impact map with columns for:

- runtime behavior;
- inferred type;
- declaration artifact;
- package export;
- errors;
- compatibility;
- stored or serialized representation;
- tests and documentation.

Name the one localized assertion, if any, and prove it from traversal over the same sorted key set.

## Independent transfer

Add a Boolean field, an optional field, or a renamed public subpath. Before coding, classify whether the change is additive, behaviorally breaking, or package-breaking. Implement it only after the impact map is complete.

## Completion standard

A release-candidate rehearsal must build the installation shape, execute consumers, inspect declarations, test unsupported paths, and preserve old fixtures. The lab is complete when every public claim has evidence at the phase where it could fail.
