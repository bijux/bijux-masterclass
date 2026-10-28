# Worked answers — Data Ownership, Replication, and Cross-Service Query Design

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why is a separate schema not sufficient for database-per-service?

Authority is the key property. If another service queries or writes the schema directly, the owner cannot evolve or secure it independently even when the schema name differs.

**Decisive evidence:** database access and migration ownership audit

## 2. A projection receives version 8 after version 6. What should happen?

Record a gap, stop treating that key as complete, and request replay or reconciliation. Applying version 8 silently would hide missing business history.

**Decisive evidence:** projection gap test

## 3. When is gateway composition preferable to a local projection?

When freshness is required, fan-out is bounded, and the caller can tolerate dependency availability or explicit partial response. A projection is better when synchronous coupling would be too costly and bounded staleness is acceptable.

**Decisive evidence:** query decision record

## 4. Why must a partial response be explicit?

An empty field can mean no data or unavailable data. Silent omission converts dependency failure into false business information.

**Decisive evidence:** public response oracle

## 5. What makes a replicated view non-authoritative?

It has a named source, source version, rebuild path, staleness policy, and no write path for canonical facts.

**Decisive evidence:** projection metadata proof

## 6. Why is a global migration head incompatible with independent service release?

It forces unrelated schemas into one ordering and release process. Service-owned histories let each owner expand and contract independently while the legacy line remains historical evidence.

**Decisive evidence:** migration-head inventory

## 7. How should Notification Service react to an old duplicate event?

Recognize the version or event id as duplicate/stale and avoid a second effect. The source owner remains unchanged.

**Decisive evidence:** inbox and projection vector

## 8. What is wrong with bilateral table synchronization?

Both sides become writers and conflict resolution becomes implicit. Replication should have a clear authoritative direction.

**Decisive evidence:** single-writer proof

## 9. When is a reporting data product preferable to an API join?

For large cross-domain history, aggregates, or queries that do not need transaction-time freshness. It can publish snapshot and completeness metadata.

**Decisive evidence:** query workload classification

## 10. How can an artifact be orphaned without data corruption?

Artifact Service validly committed its owned object, but Analysis Control later rejected attachment. The system records the orphan and applies retention/compensation instead of pretending the commit never happened.

**Decisive evidence:** reconciliation finding and compensation

## 11. Why must TypeScript reject unsafe integer versions even though Python can represent them?

The cross-language contract must preserve identity and ordering in every supported runtime. Python’s larger integer range cannot redefine the portable boundary.

**Decisive evidence:** shared version vectors

## 12. What is the safe alternative to uncontrolled dual writes during extraction?

Backfill history, shadow reads, move write authority through one controlled path, and use stable idempotent import identities with reconciliation.

**Decisive evidence:** extraction phase report
