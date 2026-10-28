# ADR 0003: separate executable baseline and current frontier

**Status:** accepted

## Context

OpenAPI 3.2 introduces useful constructs, while client generators and renderers expose uneven support.

## Decision

Maintain an OpenAPI 3.1.2 baseline for broad execution and a 3.2.0 frontier that adds current features without contaminating baseline proof.

## Consequences

Learners see the current specification and the practical ecosystem simultaneously. Capability gaps become measured engineering data rather than reasons to teach an obsolete standard or make unsupported claims.
