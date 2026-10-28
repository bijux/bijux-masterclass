# OpenAPI Contract Engineering

**Course 1 of 6 — Specify the promise**

Define and verify the public HTTP contract.

> What exactly does the API promise, and how can providers and consumers verify that promise?

## Begin with the course book

1. Read [Course introduction](course-book/index.md).
2. Complete [Start here](course-book/start-here.md) and [orientation](course-book/module-00-orientation/index.md).
3. Follow the ten modules in order.
4. Use the capstone and implementation tracks only through the reading routes named in each chapter.
5. Preserve checkpoint evidence before progressing.

## Modules

01. [HTTP and OpenAPI Foundations](course-book/module-01-http-openapi-foundations/index.md)
02. [Operations, Parameters, and Messages](course-book/module-02-operations-parameters-messages/index.md)
03. [JSON Schema Contract Modeling](course-book/module-03-json-schema-contract-modeling/index.md)
04. [References and Multi-Document Architecture](course-book/module-04-references-multi-document-architecture/index.md)
05. [Production HTTP API Design](course-book/module-05-production-http-api-design/index.md)
06. [Contract-First and Code-First Runtimes](course-book/module-06-contract-first-code-first-runtime/index.md)
07. [Mocks, Clients, and Contract Testing](course-book/module-07-mocking-clients-contract-testing/index.md)
08. [Security in the Public Contract](course-book/module-08-security-authentication-authorization/index.md)
09. [Evolution, Compatibility, and Audience Views](course-book/module-09-evolution-compatibility-overlays-ci/index.md)
10. [OpenAPI 3.2, Streaming, Webhooks, and Workflows](course-book/module-10-openapi-32-workflows-advanced/index.md)

## Program boundary

**Incoming:** Basic programming ability and no assumed OpenAPI experience.

**Outgoing:** A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflows, and provider-neutral behavioral scenarios.

## Implementation strategy

Both Python/FastAPI and TypeScript/Fastify are used symmetrically to prove that the contract is language-neutral.

## Verification

```bash
make doctor
make core-proof
make manifest-proof
```

Environment-dependent routes are reported separately. Missing infrastructure is never represented as a passing live proof.
