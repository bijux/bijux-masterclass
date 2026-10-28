# Ten-Day Study Plan — OpenAPI Contract Engineering

This is a dense two-week course with one numbered module per weekday. Orientation is required before Day 1 and is not counted as a teaching module. The middle weekend contains no hidden new curriculum.

| Day | Module | Main intellectual move | Required result |
|---:|---|---|---|
| 1 | [HTTP and OpenAPI Foundations](module-01-http-openapi-foundations/index.md) | How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior? | Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior. |
| 2 | [Operations, Parameters, and Messages](module-02-operations-parameters-messages/index.md) | How are parameters, request bodies, media types, status codes, and headers modeled without ambiguity? | Complete project and dataset messages, including pagination inputs, creation responses, and problem representations. |
| 3 | [JSON Schema Contract Modeling](module-03-json-schema-contract-modeling/index.md) | How do schemas reject invalid states while remaining usable for providers, clients, and future evolution? | Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus. |
| 4 | [References and Multi-Document Architecture](module-04-references-multi-document-architecture/index.md) | How can a multi-document contract remain understandable, relocatable, and deterministically buildable? | Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles. |
| 5 | [Production HTTP API Design](module-05-production-http-api-design/index.md) | How should an HTTP API express asynchronous work, retries, conflicts, conditional updates, and machine-readable failures? | Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details. |
| 6 | [Contract-First and Code-First Runtimes](module-06-contract-first-code-first-runtime/index.md) | How do design-first and code-first descriptions relate, and how is semantic drift detected? | Map every operation to both providers and compare generated observations with the canonical contract. |
| 7 | [Mocks, Clients, and Contract Testing](module-07-mocking-clients-contract-testing/index.md) | How do mocks, generated clients, examples, property tests, and stateful tests provide different evidence? | Build the consumer and contract-test ladder against the mock and both real providers. |
| 8 | [Security in the Public Contract](module-08-security-authentication-authorization/index.md) | What can the public contract say about authentication and authorization, and what remains a runtime responsibility? | Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures. |
| 9 | [Evolution, Compatibility, and Audience Views](module-09-evolution-compatibility-overlays-ci/index.md) | How can a published API evolve without silently breaking request writers or response readers? | Create compatible and rejected release candidates, compatibility gates, and public/partner audience views. |
| 10 | [OpenAPI 3.2, Streaming, Webhooks, and Workflows](module-10-openapi-32-workflows-advanced/index.md) | How do current OpenAPI features express streaming, webhooks, links, query methods, and multi-step workflows? | Publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow. |


## Daily rhythm

A productive day uses four blocks:

- **Model:** read the chapter and reconstruct the governing diagram or state machine;
- **Transfer:** answer the exercises and compare with the reasoned answers;
- **Experiment:** perform the lab, including the failure or pressure condition;
- **Defense:** complete the checkpoint and preserve evidence.

Do not treat “morning to night” as uninterrupted screen time. Use deliberate breaks. Stop blind copying when fatigue removes your ability to predict outcomes.

## Middle weekend

Use Saturday for at most one focused repair cycle per failed checkpoint and for a cross-module synthesis note. Sunday contains no required implementation. Rerun predecessor and accumulated course proofs before Week 2.

## Recovery rule

When behind, reduce breadth before reducing evidence. Complete one language track deeply, keep the comparison focused, and do not skip the failure experiment. A copied second implementation is less valuable than one defended invariant.
