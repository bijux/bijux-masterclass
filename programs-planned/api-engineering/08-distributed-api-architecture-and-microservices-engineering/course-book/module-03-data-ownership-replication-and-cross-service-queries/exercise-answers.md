# Worked Answers — Module 03: Data Ownership, Replication, and Cross-Service Query Design

Use these solutions to audit your reasoning for **Data Ownership, Replication, and Cross-Service Query Design**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a separate schema not sufficient for database-per-service?

Authority is the key property. If another service queries or writes the schema directly, the owner cannot evolve or secure it independently even when the schema name differs.

**Decisive evidence:** database access and migration ownership audit

The chapter’s decisive distinction is this: “Database per service” is frequently reduced to “different connection strings.” The important rule is authority: only the owning service may write the canonical fact. Separate schemas in one PostgreSQL cluster can be a valid transitional deployment, but application code still must not query across them as if the network boundary did not exist.

## 2. A projection receives version 8 after version 6. What should happen?

Record a gap, stop treating that key as complete, and request replay or reconciliation. Applying version 8 silently would hide missing business history.

**Decisive evidence:** projection gap test

In the cumulative capstone, the rule becomes concrete: Notification Service may use its run view to select a template, but it cannot change the run state. If its projection is missing version 14 after receiving version 15, it pauses the subject and requests replay. It never “fixes” the source by writing to Control’s database.

## 3. When is gateway composition preferable to a local projection?

When freshness is required, fan-out is bounded, and the caller can tolerate dependency availability or explicit partial response. A projection is better when synchronous coupling would be too costly and bounded staleness is acceptable.

**Decisive evidence:** query decision record

A useful way to reason about the boundary is: The gateway requests authoritative parts from several services and composes the response. This is useful when freshness matters and fan-out is bounded. The response must disclose partial results rather than silently omit unavailable parts.

## 4. Why must a partial response be explicit?

An empty field can mean no data or unavailable data. Silent omission converts dependency failure into false business information.

**Decisive evidence:** public response oracle

The implementation consequence is: If a query is central to one invariant and cannot tolerate remote or stale data, the proposed boundary may be wrong. Architecture is allowed to move the boundary rather than invent increasingly complex synchronization.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 5. What makes a replicated view non-authoritative?

It has a named source, source version, rebuild path, staleness policy, and no write path for canonical facts.

**Decisive evidence:** projection metadata proof

The important nuance is: A service consumes events into a local read model. This removes synchronous dependency but introduces staleness. Notification Service keeps a run view for delivery policy. The view records run version and pauses on gaps.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 6. Why is a global migration head incompatible with independent service release?

It forces unrelated schemas into one ordering and release process. Service-owned histories let each owner expand and contract independently while the legacy line remains historical evidence.

**Decisive evidence:** migration-head inventory

Under concurrency or failure, the distinction becomes: Reconciliation reads each authority through a safe administrative interface or controlled snapshot, compares stable identifiers, and produces findings. Repair remains owner-specific. A reconciliation job must not become a super-service that writes every database.

## 7. How should Notification Service react to an old duplicate event?

Recognize the version or event id as duplicate/stale and avoid a second effect. The source owner remains unchanged.

**Decisive evidence:** inbox and projection vector

The design remains honest only if: Course 8 first asks whether the invariant should remain within one service. Analysis Control keeps run, idempotency, lease, and event outbox together for this reason. Cross-service workflows use durable state, idempotent effects, and compensation when true independent ownership exists.

## 8. What is wrong with bilateral table synchronization?

Both sides become writers and conflict resolution becomes implicit. Replication should have a clear authoritative direction.

**Decisive evidence:** single-writer proof

The consumer-facing consequence is: Two services must not “keep tables in sync” through bilateral updates. Replication has direction: owner to consumer. If Artifact Service needs tenant and run identifiers, the upload capability or command supplies them under an authenticated contract. It does not update Control’s tables. Artifact Service publishes its fact; Control records an artifact reference under its own transaction.

## 9. When is a reporting data product preferable to an API join?

For large cross-domain history, aggregates, or queries that do not need transaction-time freshness. It can publish snapshot and completeness metadata.

**Decisive evidence:** query workload classification

The operational consequence is: A delivery dashboard may tolerate a 30-second run view. Authorization for an artifact download should not depend on a 30-second replica unless the capability itself encodes the current decision and expires quickly.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 10. How can an artifact be orphaned without data corruption?

Artifact Service validly committed its owned object, but Analysis Control later rejected attachment. The system records the orphan and applies retention/compensation instead of pretending the commit never happened.

**Decisive evidence:** reconciliation finding and compensation

The strongest engineering interpretation is: A coordinator can provide atomic commit across participants in some environments, but it does not remove ownership, availability, latency, or recovery costs. It can also make a local failure block multiple services.

## 11. Why must TypeScript reject unsafe integer versions even though Python can represent them?

The cross-language contract must preserve identity and ordering in every supported runtime. Python’s larger integer range cannot redefine the portable boundary.

**Decisive evidence:** shared version vectors

The defect-oriented view is: Both tracks implement a versioned projection with identical classifications. TypeScript rejects versions outside the safe-integer range; Python’s arbitrary-size integers do not excuse accepting values that the cross-language contract cannot preserve. Shared vectors define the portable boundary.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 12. What is the safe alternative to uncontrolled dual writes during extraction?

Backfill history, shadow reads, move write authority through one controlled path, and use stable idempotent import identities with reconciliation.

**Decisive evidence:** extraction phase report

Across the Python and TypeScript tracks, the invariant is: The classification determines recovery. An authoritative fact requires backup, migration, and controlled mutation. A projection requires replay or backfill. A cache can be dropped. Treating all tables alike produces dangerous recovery plans.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.
