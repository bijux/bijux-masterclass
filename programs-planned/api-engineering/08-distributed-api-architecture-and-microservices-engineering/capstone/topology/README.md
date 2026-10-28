# Topology evidence

This directory contains two different evidence classes.

## Executable Compose laboratory

`compose.yaml` builds the dependency-light Python network laboratory. It starts four real processes in separate containers and exercises the same boundaries as `make network-lab-proof`. The laboratory intentionally uses in-memory state so that service interaction, delegated authority, and failure behavior remain inspectable.

It is not evidence of durable storage or production capacity. Those claims require the service-owned PostgreSQL migration trees, environment-backed database tests, and representative load evidence.

## Kubernetes declarations

`kubernetes/` records the intended deployment, Service, and NetworkPolicy structure. The files are static architecture evidence unless they are applied to a real cluster and subjected to readiness, identity, routing, policy, and failure tests.

Neither Compose nor Kubernetes decides business ownership. The service catalogue, data-ownership map, dependency graph, and architecture decisions remain authoritative.
