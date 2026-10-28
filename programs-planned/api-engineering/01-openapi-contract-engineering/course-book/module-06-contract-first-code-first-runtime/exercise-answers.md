# Worked Answers — Module 06: Contract-First and Code-First Runtimes

Use these solutions to audit your reasoning for **Contract-First and Code-First Runtimes**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. When is code-first a defensible choice?

When one implementation is intentionally authoritative, framework output covers the required semantics, review occurs on the generated artifact, and consumers are not promised a language-neutral source. It is not inherently inferior; unacknowledged authority is the problem.

The chapter’s decisive distinction is this: A design-first system begins with a reviewed contract and asks providers and consumers to conform. A code-first system derives a description from runtime declarations. A schema-first system may begin with shared data schemas but still needs explicit HTTP decisions. None is universally correct, but mixing them without naming authority guarantees drift.

## 2. Why not require text-identical generated documents?

Frameworks choose different component names, ordering, defaults, and extension metadata. The useful comparison is semantic surface, with exact review of accepted presentational differences.

In the cumulative capstone, the rule becomes concrete: Normalize before comparison. Ignore ordering, generated server URLs, and harmless documentation text only when an allowlist names the exact path and reason. Never normalize away a changed status, parameter location, required property, media type, or security requirement.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 3. Name four semantic differences that may never be broadly allowlisted.

Method/path identity, parameter location or requiredness, response status/media type, schema admitted set, and security requirements are examples.

A useful way to reason about the boundary is: Request validation rejects messages outside the admitted input set. Response serialization restricts what the provider releases and confirms that output satisfies the public representation. A service can validate input rigorously while leaking internal ownership, idempotency fingerprints, or database fields in its response.

## 4. What does response serialization prove that request validation does not?

It constrains outbound data to the public representation and catches invalid or sensitive provider output.

The implementation consequence is: Request validation rejects messages outside the admitted input set. Response serialization restricts what the provider releases and confirms that output satisfies the public representation. A service can validate input rigorously while leaking internal ownership, idempotency fingerprints, or database fields in its response.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 5. Why is an imported TestClient insufficient as the only parity proof?

It may bypass deployment configuration and is provider-specific. A base-URL scenario exercises actual HTTP adapters and can target either service.

The important nuance is: Scenarios should remain provider-neutral. They receive a base URL and credentials, not an imported application object. Provider unit tests can be faster and more diagnostic, but only a black-box suite proves that deployment adapters expose the same boundary.

**Evidence.** Run the same consumer workflow and provider-neutral scenario against the mock, Python provider, and TypeScript provider.

## 6. How should nondeterministic identifiers be compared?

Validate format and relational use, capture them from one step, and apply them to later requests. Do not expect fresh providers to issue the same literal value.

Under concurrency or failure, the distinction becomes: Some nondeterminism must be normalized carefully. Identifiers and timestamps can differ across fresh runs, but their formats and relationships must match. A shared scenario should capture an identifier from one response and use it later rather than compare hard-coded values across providers.

## 7. What is the risk of exposing framework validation paths?

Consumers become coupled to a framework’s path syntax and wording, making provider changes breaking even when the public schema is unchanged.

The design remains honest only if: FastAPI and Fastify have different default validation shapes, status choices, field paths, and wording. Exposing either default makes consumers framework-dependent and destroys provider parity. The adapter must translate native failures into the canonical application/problem+json representation.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 8. Design a handler-map negative test.

Add or rename one canonical operation without changing one provider, run method/path/operationId set comparison, and assert the report identifies the missing triple.

The consumer-facing consequence is: A parsed contract can contain an operation no provider implements. A provider can expose an undocumented route. The operation ledger extracts method, path, and operationId from the canonical bundle; language-specific maps extract the same identity from route declarations. The checkpoint compares both sets in both directions.

## 9. Why are TypeScript static types not a boundary validator?

Types are erased at runtime and untrusted network input can violate them. Runtime schemas or validators must inspect actual messages.

The operational consequence is: Some generated differences are inevitable: title wording, schema component names, generated documentation routes, or order. An allowlist can suppress these only by exact JSON Pointer or comparison category, with rationale and owner. A wildcard over responses or schemas is equivalent to disabling the gate.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 10. What belongs in a drift report?

Canonical and observed identities, normalized categories, exact differing pointers, classification, rationale for any allowance, tool versions, and command status.

The strongest engineering interpretation is: Each allowlisted item should be reviewed when framework versions change. The capstone keeps an intentionally small observation report rather than claiming semantic equality from a textual diff of two very different generated documents.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 11. Practical defect exercise

For **Generated document promoted to canonical**, a valid solution must first reproduce: one provider’s annotations silently redefine the API. The smallest useful starting case is: change a FastAPI default and observe the generated-contract diff. The repair is: keep generated documents as observations and review them against the canonical source.

The defect-oriented view is: The capstone uses a hand-authored, multi-document contract as the normative source. FastAPI and Fastify can each emit an OpenAPI document, but those documents are observations of framework configuration. They are compared to the canonical contract; they do not overwrite it. This preserves language neutrality and prevents one provider's defaults from becoming accidental public policy.

## 12. Cross-language parity exercise

The Contract-First and Code-First Runtimes parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: This Contract-First and Code-First Runtimes increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.
