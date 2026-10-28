# Reference Answers — Module 04: References and Multi-Document Architecture

Read after attempting all twelve References and Multi-Document Architecture exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Resolve `../components/schemas/Project.yaml` from `spec/paths/projects.yaml`.

The target is `spec/components/schemas/Project.yaml`; resolution begins at the containing file’s parent `spec/paths`.

## 2. Decode JSON Pointer `/components/schemas/A~1B~0C`.

It selects key `A/B~C` under `components.schemas`; `~1` decodes to `/` and `~0` to `~`.

## 3. When should a one-use schema stay inline?

When it is local, short, and has no independent conceptual identity or review lifecycle. Extraction should reduce, not increase, cognitive load.

## 4. Distinguish bundle and dereference.

A bundle makes external dependencies internal/self-contained, often preserving internal refs. Dereferencing replaces reference occurrences with target values and must handle recursion.

## 5. Why can a recursive schema be valid while a generator fails?

The specification permits recursive instance models, but a generator may have a capability limit. Record the tool limitation rather than declaring the contract invalid.

## 6. Design a relocation test.

Copy `spec/` to a temporary directory, change `cwd` elsewhere, disable network access, resolve and bundle, then compare the operation ledger and digest behavior.

## 7. What is the risk of `$id` in a nested schema?

It can change the base URI for references below it. That can improve portability but surprises reviewers if hidden.

## 8. How do you prove bundling preserved meaning?

Compare operation IDs/methods/paths, effective schemas and examples, validate the bundle, and run the same consumer/conformance tests.

## 9. Why is editing a bundle forbidden?

It creates an unreproducible fork that will be overwritten and is not traceable to source review.

## 10. Name one intentional and one accidental cycle.

A tree node referencing child nodes is intentional; `Project.yaml` importing `Owner.yaml` while `Owner.yaml` imports `Project.yaml` only for file organization may be accidental.

## 11. Practical defect exercise

For **Working-directory reference**, a valid solution must first reproduce: resolver joins relative paths to `cwd`. The smallest useful starting case is: run the same command from another directory. The repair is: Resolve from the containing document URI.

## 12. Cross-language parity exercise

The References and Multi-Document Architecture parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
