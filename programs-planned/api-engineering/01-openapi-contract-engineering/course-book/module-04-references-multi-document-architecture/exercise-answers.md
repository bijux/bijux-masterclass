# Worked Answers — Module 04: References and Multi-Document Architecture

Use these solutions to audit your reasoning for **References and Multi-Document Architecture**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Resolve `../components/schemas/Project.yaml` from `spec/paths/projects.yaml`.

The target is `spec/components/schemas/Project.yaml`; resolution begins at the containing file’s parent `spec/paths`.

The chapter’s decisive distinction is this: $ref: ../components/schemas/Project.yaml identifies a target relative to the base URI of the document containing the reference. It does not paste text relative to the process working directory. Nested references acquire their own document base when resolution continues.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 2. Decode JSON Pointer `/components/schemas/A~1B~0C`.

It selects key `A/B~C` under `components.schemas`; `~1` decodes to `/` and `~0` to `~`.

In the cumulative capstone, the rule becomes concrete: The part before selects a document; the fragment selects a location within it, commonly by JSON Pointer. schemas.yaml /Project and Project.yaml are different organizational choices. $id can establish a base URI inside JSON Schema resources, and anchors can provide stable fragment names.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 3. When should a one-use schema stay inline?

When it is local, short, and has no independent conceptual identity or review lifecycle. Extraction should reduce, not increase, cognitive load.

A useful way to reason about the boundary is: Use these features deliberately. Hidden base changes make references difficult to audit. The capstone prefers one schema per file and straightforward relative paths, reserving IDs and anchors for cases where they add actual portability.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 4. Distinguish bundle and dereference.

A bundle makes external dependencies internal/self-contained, often preserving internal refs. Dereferencing replaces reference occurrences with target values and must handle recursion.

The implementation consequence is: A bundle creates a self-contained description while usually preserving internal references. Dereferencing replaces references with target values and can explode recursive structures. Tools use the words inconsistently, so inspect output rather than inferring behavior from a command name.

**Evidence.** Move the source tree, resolve every reference offline, build twice, and compare the deterministic bundle and operation inventory.

## 5. Why can a recursive schema be valid while a generator fails?

The specification permits recursive instance models, but a generator may have a capability limit. Record the tool limitation rather than declaring the contract invalid.

The important nuance is: A recursive schema such as a tree node can intentionally reference itself. A cycle among files caused by organization can be accidental and unsupported by a generator. The correct question is whether the instance model is recursive, not whether the file graph contains a loop.

## 6. Design a relocation test.

Copy `spec/` to a temporary directory, change `cwd` elsewhere, disable network access, resolve and bundle, then compare the operation ledger and digest behavior.

Under concurrency or failure, the distinction becomes: Copy the source tree to a different absolute path, change the working directory, disconnect the network, and run resolution. If it fails, the source depends on undeclared context. The course’s reference gate resolves every target offline and treats remote dependency as a conscious publication decision.

## 7. What is the risk of `$id` in a nested schema?

It can change the base URI for references below it. That can improve portability but surprises reviewers if hidden.

The design remains honest only if: Claim Category Why it matters Evidence --- --- --- --- Relative references resolve against the base URI of the containing document. URI/JSON Reference semantics Working-directory resolution is incorrect. offline reference gate and relocation exercise JSON Pointer tokens escape ~ as ~0 and / as ~1. RFC 6901 semantics Unescaped component names can point to the wrong location. pointer unit cases Every reusable object has one canonical definition.

## 8. How do you prove bundling preserved meaning?

Compare operation IDs/methods/paths, effective schemas and examples, validate the bundle, and run the same consumer/conformance tests.

The consumer-facing consequence is: For every References and Multi-Document Architecture claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—parse, examples, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 9. Why is editing a bundle forbidden?

It creates an unreproducible fork that will be overwritten and is not traceable to source review.

The operational consequence is: A good split gives a path group, schema, parameter, response, header, or security scheme one clear home. A bad split creates a file for every tiny field, hides local meaning behind long chains, or duplicates nearly identical schemas under different names.

**Evidence.** Move the source tree, resolve every reference offline, build twice, and compare the deterministic bundle and operation inventory.

## 10. Name one intentional and one accidental cycle.

A tree node referencing child nodes is intentional; `Project.yaml` importing `Owner.yaml` while `Owner.yaml` imports `Project.yaml` only for file organization may be accidental.

The strongest engineering interpretation is: A recursive schema such as a tree node can intentionally reference itself. A cycle among files caused by organization can be accidental and unsupported by a generator. The correct question is whether the instance model is recursive, not whether the file graph contains a loop.

## 11. Practical defect exercise

For **Working-directory reference**, a valid solution must first reproduce: resolver joins relative paths to `cwd`. The smallest useful starting case is: run the same command from another directory. The repair is: Resolve from the containing document URI.

The defect-oriented view is: This matters when a source tree is bundled, moved, published, or loaded from a URL. A resolver that accidentally uses the shell directory can appear correct in one checkout and fail everywhere else.

## 12. Cross-language parity exercise

The References and Multi-Document Architecture parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: This References and Multi-Document Architecture increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.
