# OpenAPI Contract Engineering

**Course 1 of 6 — Specify the promise**

> **Central question:** What exactly does the API promise, and how can providers and consumers verify that promise?

## Course responsibility

Define and verify the public HTTP contract. The course inherits earlier guarantees rather than restating them as new work. Its purpose is to add one mature engineering responsibility to the same Analysis Runs Platform.

## Incoming and outgoing boundaries

**Incoming boundary:** Basic programming ability and no assumed OpenAPI experience.

**Outgoing boundary:** A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflows, and provider-neutral behavioral scenarios.

## What you will be able to do

After completing the course, you can:

- establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior.
- complete project and dataset messages, including pagination inputs, creation responses, and problem representations.
- define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus.
- split the contract into owned documents, resolve every reference offline, and produce deterministic bundles.
- add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details.
- map every operation to both providers and compare generated observations with the canonical contract.
- build the consumer and contract-test ladder against the mock and both real providers.
- describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures.
- create compatible and rejected release candidates, compatibility gates, and public/partner audience views.
- publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow.

## Ten-module learning path

| Day | Module | Governing question | Capstone result |
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


## How the book is organized

Each numbered module has five learner-facing files:

1. `index.md` — the complete explanation, worked designs, implementation reading, failure analysis, and transition;
2. `exercises.md` — twelve transfer questions;
3. `exercise-answers.md` — matching reasoned reference answers;
4. `lab.md` — one controlled failure, pressure, or release experiment;
5. `checkpoint.md` — the evidence required before progression.

The course book is authoritative. Capstone source, fixtures, reports, and proof scripts make the material executable; they do not replace the explanation.

## Completion standard

You complete the course only when every module checkpoint, the capstone proof, and the final defense pass. A strong result states not only what worked but which claim was established, which evidence class supports it, and what remains unexecuted.

Continue with [Start here](start-here.md).
