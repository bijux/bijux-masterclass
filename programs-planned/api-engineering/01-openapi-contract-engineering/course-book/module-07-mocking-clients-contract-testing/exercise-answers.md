# Reference Answers — Module 07: Mocks, Clients, and Contract Testing

Read after attempting all twelve Mocks, Clients, and Contract Testing exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. What does a successful bundle prove?

That references can be resolved into the chosen output under the bundler’s semantics and the build completed; it does not prove runtime conformance or semantic quality.

## 2. When should a custom lint rule block CI?

When it captures a concrete, recurring interoperability, security, or maintainability risk; has test fixtures; and offers a feasible migration path.

## 3. Why retain examples when property generation exists?

Examples communicate named domain stories, drive deterministic docs/mocks, and cover intentional cases. Property generation explores broader boundaries; the two are complementary.

## 4. What should happen when a generator omits callbacks?

Record the unsupported capability, ensure generation does not imply complete coverage, and provide a manual callback consumer/validator test if callbacks matter.

## 5. How do you test that rejection caused no mutation?

Capture or query relevant state before the invalid request, send it, assert the documented problem, then query state and compare counts/identities.

## 6. What data belongs in a minimized failure report?

Request method/URL/headers/body with secrets redacted, response, seed, contract digest, provider revision, tool and version, and classification.

## 7. Why can a schema mock generate an impossible domain state?

JSON Schema constrains representation shape, not all temporal or cross-resource invariants. A completed run without prior dataset may be schema-valid but domain-impossible.

## 8. Design one stateful invariant for cancellation.

After a run reaches completed, cancellation must return the documented conflict and the run must remain completed with artifacts unchanged.

## 9. What is the client risk of renaming an operationId?

Generated method names and references can change, producing source incompatibility even if method/path remain stable.

## 10. Distinguish supported, transformed, and partially supported.

Supported preserves intended behavior directly; transformed maps it to an equivalent tool-specific construct; partially supported handles only a subset or loses semantics.

## 11. Practical defect exercise

For **Lint equals correctness**, a valid solution must first reproduce: a perfectly styled contract is assumed to match runtime. The smallest useful starting case is: change provider status while lint remains green. The repair is: Keep live conformance as a separate gate.

## 12. Cross-language parity exercise

The Linting, Mocking, Clients, and Contract Testing parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
