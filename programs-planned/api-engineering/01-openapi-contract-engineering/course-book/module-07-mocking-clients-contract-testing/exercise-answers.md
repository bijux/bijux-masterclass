# Worked Answers — Module 07: Mocks, Clients, and Contract Testing

Use these solutions to audit your reasoning for **Mocks, Clients, and Contract Testing**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What does a successful bundle prove?

That references can be resolved into the chosen output under the bundler’s semantics and the build completed; it does not prove runtime conformance or semantic quality.

The chapter’s decisive distinction is this: A parser proves that a document can be read. A linter applies structural and organizational rules. A bundler resolves references into a publication artifact. A mock simulates responses from examples or schemas. A generator maps the contract into consumer code. A contract tester sends generated requests to a live provider. These claims overlap, but none means “the API is correct.”

## 2. When should a custom lint rule block CI?

When it captures a concrete, recurring interoperability, security, or maintainability risk; has test fixtures; and offers a feasible migration path.

In the cumulative capstone, the rule becomes concrete: Built-in lint rules catch common OpenAPI mistakes. Organizational rules should target defects repeatedly seen in reviews: missing operationId, absent explicit security decision, response without media type, undocumented 4xx classes, weak descriptions, or unstable naming. Rules should not become a prose-style bureaucracy.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 3. Why retain examples when property generation exists?

Examples communicate named domain stories, drive deterministic docs/mocks, and cover intentional cases. Property generation explores broader boundaries; the two are complementary.

A useful way to reason about the boundary is: Examples cover named cases. Property-based contract testing derives many legal and illegal values from constraints: minimum and maximum lengths, numeric bounds, patterns, enums, nested combinations, missing required fields, and unexpected properties. Shrinking reduces a complex failure to a minimal reproducer.

## 4. What should happen when a generator omits callbacks?

Record the unsupported capability, ensure generation does not imply complete coverage, and provide a manual callback consumer/validator test if callbacks matter.

The implementation consequence is: No generator or mock implements every OpenAPI and JSON Schema feature uniformly. A mature toolchain probes support for callbacks, links, multipart encodings, discriminated unions, 3.2 fields, and sequential media. Unsupported features receive a documented fallback, a manual test, or a pinned exclusion with risk.

## 5. How do you test that rejection caused no mutation?

Capture or query relevant state before the invalid request, send it, assert the documented problem, then query state and compare counts/identities.

The important nuance is: A provider that accepts every payload can pass a happy-path suite. Negative tests ask whether malformed identifiers, unknown enums, illegal extra fields, wrong media types, missing credentials, and boundary overflow are rejected with the documented public problem.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 6. What data belongs in a minimized failure report?

Request method/URL/headers/body with secrets redacted, response, seed, contract digest, provider revision, tool and version, and classification.

Under concurrency or failure, the distinction becomes: Randomized testing is useful only when a failure can be replayed. Preserve the minimized request, seed, tool version, contract digest, provider revision, and response. Promote important minimized cases into permanent fixtures rather than relying on the generator to rediscover them.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 7. Why can a schema mock generate an impossible domain state?

JSON Schema constrains representation shape, not all temporal or cross-resource invariants. A completed run without prior dataset may be schema-valid but domain-impossible.

The design remains honest only if: A contract mock lets consumers develop before a provider exists and makes examples executable. Dynamic schema-generated responses broaden coverage, while explicit examples make domain stories legible. Both can be misleading when examples encode impossible lifecycle state or when the mock does not enforce requests.

## 8. Design one stateful invariant for cancellation.

After a run reaches completed, cancellation must return the documented conflict and the run must remain completed with artifacts unchanged.

The consumer-facing consequence is: Many failures appear only after a sequence: update after delete, cancel after completion, retrieve another owner’s artifact, reuse an idempotency key with a changed body, or follow a link using a captured identifier. Stateful tools use explicit links, inferred relationships, or custom state machines to construct these paths.

## 9. What is the client risk of renaming an operationId?

Generated method names and references can change, producing source incompatibility even if method/path remain stable.

The operational consequence is: A generator chooses method names, parameter grouping, nullable conventions, error surfaces, and transport abstractions. Generation success does not mean the resulting client is ergonomic or semantically complete. A change in operationId can be a source-breaking change even when the wire endpoint is unchanged.

**Evidence.** Run the same consumer workflow and provider-neutral scenario against the mock, Python provider, and TypeScript provider.

## 10. Distinguish supported, transformed, and partially supported.

Supported preserves intended behavior directly; transformed maps it to an equivalent tool-specific construct; partially supported handles only a subset or loses semantics.

The strongest engineering interpretation is: The capstone runs the same consumer workflow against Prism and real providers where supported. State-dependent steps are marked when a generic mock cannot persist resource identity. The limitation is reported rather than hidden behind a fabricated all-green workflow.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 11. Practical defect exercise

For **Lint equals correctness**, a valid solution must first reproduce: a perfectly styled contract is assumed to match runtime. The smallest useful starting case is: change provider status while lint remains green. The repair is: Keep live conformance as a separate gate.

The defect-oriented view is: For Linting, Mocking, Clients, and Contract Testing, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

## 12. Cross-language parity exercise

The Linting, Mocking, Clients, and Contract Testing parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: This Linting, Mocking, Clients, and Contract Testing increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.
