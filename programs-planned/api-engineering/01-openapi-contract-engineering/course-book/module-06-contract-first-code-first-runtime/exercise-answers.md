# Reference Answers — Module 06: Contract-First and Code-First Runtimes

Read after attempting all twelve Contract-First and Code-First Runtimes exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. When is code-first a defensible choice?

When one implementation is intentionally authoritative, framework output covers the required semantics, review occurs on the generated artifact, and consumers are not promised a language-neutral source. It is not inherently inferior; unacknowledged authority is the problem.

## 2. Why not require text-identical generated documents?

Frameworks choose different component names, ordering, defaults, and extension metadata. The useful comparison is semantic surface, with exact review of accepted presentational differences.

## 3. Name four semantic differences that may never be broadly allowlisted.

Method/path identity, parameter location or requiredness, response status/media type, schema admitted set, and security requirements are examples.

## 4. What does response serialization prove that request validation does not?

It constrains outbound data to the public representation and catches invalid or sensitive provider output.

## 5. Why is an imported TestClient insufficient as the only parity proof?

It may bypass deployment configuration and is provider-specific. A base-URL scenario exercises actual HTTP adapters and can target either service.

## 6. How should nondeterministic identifiers be compared?

Validate format and relational use, capture them from one step, and apply them to later requests. Do not expect fresh providers to issue the same literal value.

## 7. What is the risk of exposing framework validation paths?

Consumers become coupled to a framework’s path syntax and wording, making provider changes breaking even when the public schema is unchanged.

## 8. Design a handler-map negative test.

Add or rename one canonical operation without changing one provider, run method/path/operationId set comparison, and assert the report identifies the missing triple.

## 9. Why are TypeScript static types not a boundary validator?

Types are erased at runtime and untrusted network input can violate them. Runtime schemas or validators must inspect actual messages.

## 10. What belongs in a drift report?

Canonical and observed identities, normalized categories, exact differing pointers, classification, rationale for any allowance, tool versions, and command status.

## 11. Practical defect exercise

For **Generated document promoted to canonical**, a valid solution must first reproduce: one provider’s annotations silently redefine the API. The smallest useful starting case is: change a FastAPI default and observe the generated-contract diff. The repair is: keep generated documents as observations and review them against the canonical source.

## 12. Cross-language parity exercise

The Contract-First and Code-First Runtimes parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
