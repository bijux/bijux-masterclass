# Glossary — Distributed API Architecture and Microservices Engineering

These terms have precise meanings in Course 8. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## modular monolith

One deployable system with explicit internal ownership and dependency boundaries, often the safest baseline before remote extraction.

## service boundary

A remote ownership boundary with its own contract, data authority, deployment, failure behavior, security identity, and operational responsibility.

## bounded context

A domain boundary within which terms and rules have one coherent meaning; it is evidence for, not automatic proof of, a microservice boundary.

## authoritative writer

The single capability permitted to decide and persist a particular business fact.

## projection

A derived read model built from owner-published facts and governed by staleness, gap, replay, and reconciliation rules.

## staleness budget

The maximum acceptable age or version lag for derived data before the caller must wait, fail, or use another path.

## API composition

Combining results from service-owned APIs without taking ownership of their facts or directly joining their private databases.

## dependency depth

The longest synchronous call chain required for a request, which affects latency, availability, and failure amplification.

## saga

A durable multi-step workflow across owners in which each local transaction commits independently and failures require forward recovery or compensation.

## compensation

A semantic action that counteracts an earlier committed effect; it is not a database rollback across services.

## process manager

A durable coordinator that observes workflow events, records progress, and issues idempotent commands without becoming owner of domain facts.

## workload identity

The cryptographically established identity of a service instance or workload used for service-to-service authentication and policy.

## delegated capability

A narrowly scoped, time-bounded authority allowing one service to perform a specific action on behalf of a caller or workflow.

## service discovery

The mechanism mapping a logical service identity to healthy network endpoints.

## version skew

The period during deployment when callers, providers, schemas, and projections run different supported versions.

## shadow traffic

A copy of real or representative calls sent to a candidate path for comparison without making it authoritative.

## canary

A bounded fraction of authoritative traffic routed to a candidate release with explicit promotion and rollback criteria.

## strangler migration

Incremental replacement in which selected capabilities move behind controlled routing while the legacy path remains available.

## distributed monolith

Multiple deployables that remain tightly coupled through shared data, synchronous release ordering, cycles, or hidden workflow ownership.

## merge-back

A deliberate reversal that returns an unjustified service boundary to a simpler ownership and deployment model.
