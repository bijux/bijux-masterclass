# OpenAPI Contract Engineering

**Course 1 of 10 — Specify the public promise**

## Course promise

Define a precise, reviewable, executable HTTP API contract without confusing a description, a framework, and a running provider.

> **Governing question:** What exactly does the API promise, and how can providers and consumers verify that promise?

## Place in the program

**Incoming boundary:** Basic programming ability, command-line familiarity, and no assumed OpenAPI experience.

**Outgoing boundary:** A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflow description, compatibility policy, and provider-neutral behavioral scenarios.

Course 1 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the specify the public promise mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- a canonical multi-document OpenAPI description;
- precise JSON Schema models and examples;
- Python and TypeScript provider parity;
- generated and authored consumer evidence;
- compatibility, security, Overlay, and Arazzo artifacts;

## Course-level learning outcomes

- Read requests and responses as protocol messages.
- Model path, query, header, cookie, and body input deliberately.
- Distinguish missing, null, empty, and default.
- Resolve relative references from the correct document base.
- Use `202 Accepted` with a status resource.
- Keep the canonical contract authoritative.
- Distinguish syntax, semantic linting, conformance, and consumer tests.
- Model API-key and bearer security schemes.
- Analyze compatibility in the correct message direction.
- Maintain a broadly executable OpenAPI 3.1 baseline.

## Module map

| Day | Chapter | Governing question | Capstone increment |
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

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- durable persistence;
- production identity infrastructure;
- operated deployment;
- performance or reliability claims;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 1, read each chapter around the question **What exactly does the API promise, and how can providers and consumers verify that promise?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
