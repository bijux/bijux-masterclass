# ADR 0001: canonical contract is independent of providers

**Status:** accepted

## Context

FastAPI and Fastify can generate OpenAPI descriptions from registered routes and schemas. Their output reflects framework capabilities and defaults, which differ.

## Decision

The multi-document OpenAPI source under `spec/` is canonical. Framework-generated descriptions are observations used for drift analysis. Provider code must map to the canonical operation IDs and pass shared behavior tests.

## Consequences

The course carries some intentional duplication between contract schemas and implementation schemas. That cost is accepted because it makes drift visible and teaches source-of-truth decisions. Generation can reduce duplication in production, but it does not remove the need to review runtime behavior.
