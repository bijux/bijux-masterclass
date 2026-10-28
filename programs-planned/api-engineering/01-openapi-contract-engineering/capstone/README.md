# Analysis Runs API capstone

Prism is excluded from the installable toolchain because its dependency chain
has unresolved security advisories. Mock/proxy lessons and fixtures remain as
reference material. `make prism-mock` and `make prism-smoke` stop with an explicit
error; `npm run mock` and `npm run proxy:python` are unavailable. Full course
qualification remains blocked until a maintained replacement is qualified.

This directory is the executable spine of **OpenAPI Contract Engineering**. It is deliberately larger than a toy CRUD example and smaller than a production platform: enough protocol depth to expose real contract failures, without hiding the contract behind databases, message brokers, cloud accounts, or framework magic.

## Outcome under test

A consumer must be able to:

1. create a project;
2. register a local dataset;
3. upload bounded multipart content;
4. submit an idempotent asynchronous analysis;
5. observe progress through polling or a sequential representation;
6. retrieve the resulting artifact;
7. request completion delivery through a callback or registered webhook.

The same externally observable behavior is implemented by FastAPI/Pydantic and Fastify/TypeBox. One provider-neutral live suite judges both.

## Canonical artifacts

| Artifact | Role |
|---|---|
| `spec/openapi.yaml` | Multi-document OpenAPI 3.1.2 source of truth. |
| `spec/openapi-3.2.yaml` | Current-standard frontier with enhanced tags, `QUERY`, `querystring`, and stream item schemas. |
| `spec/dist/openapi.bundle.yaml` | Deterministic self-contained baseline bundle. |
| `spec/overlays/*.overlay.yaml` | Public and partner derived views. |
| `spec/workflows/analysis-run.arazzo.yaml` | Arazzo 1.1 outcome workflow. |
| `services/python-fastapi/` | Python provider. |
| `services/typescript-fastify/` | TypeScript provider. |
| `clients/python/` | Handwritten Python consumer plus generator-owned output location. |
| `clients/typescript/` | Handwritten TypeScript consumer plus generated type output. |
| `tests/` | Shared fixtures, live scenarios, security matrix, and compatibility cases. |
| `releases/` | Safe and intentionally unsafe contract evolution fixtures. |
| `reports/` | Generated proof evidence; no report is accepted merely because a command existed. |

## First execution

From the program root:

```bash
make doctor
make setup
make capstone-tour
make capstone-confirm
```

Setup installs Python and Node dependencies plus a checksum-verified course-local `oasdiff` binary. The tour uses the Python provider in-process and prints the concrete resource IDs and status transition. Confirmation runs deterministic contract gates plus both implementation and client test suites.

## Providers

Python:

```bash
make python-run
# http://127.0.0.1:8000
```

TypeScript:

```bash
make typescript-run
# http://127.0.0.1:3000
```

Both providers expose framework-generated documentation for comparison, but those generated descriptions are observations—not the canonical contract.

## Deterministic credentials

| Header | Principal | Effective authority |
|---|---|---|
| `Authorization: Bearer learner-read` | `learner` | all read scopes |
| `Authorization: Bearer learner-write` | `learner` | normal read and write scopes |
| `Authorization: Bearer other-owner` | `other` | same scopes, different ownership boundary |
| `Authorization: Bearer admin` | `admin` | all scopes plus internal diagnostics |
| `X-API-Key: demo-api-key` | `learner` | alternative security-scheme branch |

These are training credentials, not an OAuth implementation. They make authorization evidence reproducible while preserving the distinction between authentication, scope checks, and object ownership.

## Fast proof routes

```bash
make core-proof        # no vendor CLI required
make python-test       # provider, client, fixture, and contract tests
make typescript        # strict type checks and Vitest suites
make live-conformance  # one suite against both running providers
make lint-contract     # Redocly + Spectral
make clients-generate  # pinned Python and TypeScript generators
make prism-smoke       # mock and invalid-request evidence
make schemathesis      # deterministic generated tests
make oasdiff           # external compatibility gate
make proof             # all of the above plus strict docs
```

A missing full-toolchain dependency is a failure with a direct message. The course does not print “skipped” and then call the result proven.

## Behavioral depth

The contract includes:

- cursor pagination and filtering;
- precise JSON Schema unions and closed objects;
- multipart upload and bounded content;
- `201`, `202`, `204`, `409`, `412`, `413`, `415`, `422`, and `428` behavior;
- `Location`, `ETag`, `If-Match`, `Retry-After`, idempotency, and request-correlation headers;
- RFC 9457-style Problem Details and validation extensions;
- OAuth-scope and API-key alternatives;
- ownership concealment;
- callback and root-level webhook descriptions;
- SSE and NDJSON progress;
- deterministic public and partner overlays;
- compatibility fixtures with a rejected minor release;
- Arazzo value flow across the complete outcome.

## What is intentionally absent

The state is in-memory and reset when a provider restarts. The project does not implement a database, real OAuth authorization server, durable queue, webhook delivery worker, TLS termination, cloud deployment, or observability backend. Those concerns are documented at their contract boundaries but excluded from the ten-day learning objective.

Read [architecture.md](docs/architecture.md), [contract-decisions.md](docs/contract-decisions.md), and verification.md before changing the capstone.
