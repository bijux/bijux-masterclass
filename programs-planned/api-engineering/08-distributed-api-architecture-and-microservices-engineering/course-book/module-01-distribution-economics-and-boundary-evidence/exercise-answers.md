# Worked answers — Distribution Economics, Boundary Evidence, and Architecture Fitness Functions

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. A team proposes splitting ProjectService because the projects table has grown. What evidence is missing?

Table size is not boundary evidence. The proposal needs an independently owned capability, canonical data authority, distinct change or scale pressure, failure-isolation value, and an operator. If project rules still participate in run creation transactions, the split converts local invariants into network calls.

**Decisive evidence:** boundary scorecard and transaction map

## 2. Why can an independently deployed worker process still be part of the same service boundary?

Deployment independence concerns process lifecycle and scaling. Service ownership concerns business decisions and data authority. Worker Plane may deploy separately while Analysis Control retains lease, attempt, and completion authority.

**Decisive evidence:** service classification and state-ownership map

## 3. Notification Delivery has moderate traffic but a separate retry and retention policy. Is low traffic a reason to keep it inside Control?

No. Scale is only one criterion. Event-fed temporal decoupling, failure isolation, separate retention, and accountable ownership can justify extraction even at modest traffic, provided operational cost is accepted.

**Decisive evidence:** notification boundary decision record

## 4. What is wrong with using number of services as an architecture KPI?

It rewards fragmentation without measuring ownership, release independence, user outcomes, or coordination cost. A system can gain services while becoming more coupled and less reliable.

**Decisive evidence:** architecture fitness functions

## 5. How does a modular monolith reduce extraction risk?

It lets the team establish cohesive modules, local contracts, tests, and change evidence before introducing network failure. Extraction can preserve a tested seam rather than invent one while migrating.

**Decisive evidence:** module dependency and change-coupling report

## 6. A candidate scores highly but has no team willing to own its incidents. What is the decision?

Reject or defer. Ownership is non-compensable; a numerical score cannot create operational accountability.

**Decisive evidence:** named owner and on-call acceptance

## 7. Why is operational cost a negative score rather than a footnote?

Every service adds patching, release, backup, monitoring, credentials, capacity, and incident work. Ignoring those costs systematically biases decisions toward fragmentation.

**Decisive evidence:** operational cost ledger

## 8. What evidence could reverse the decision to keep Analysis Control cohesive?

A stable independent owner, a true data authority that can commit without cross-service transactions, measured scale or release pressure, and an extraction plan with lower synchronous coupling could justify review.

**Decisive evidence:** reversal criteria in ADR 0001

## 9. Why is Artifact Delivery only conditionally approved at first?

It has distinct storage and egress value, but extraction is unsafe until authorization can work without shared database reads and orphan effects can be reconciled after ambiguous completion.

**Decisive evidence:** artifact prerequisite checklist

## 10. Name one fitness function that protects the architecture after release.

`one authoritative writer per fact` prevents future convenience writes from recreating a shared database. It can be checked from catalogue and migration ownership.

**Decisive evidence:** single-writer ownership proof

## 11. What does failure isolation mean for Notification Service?

Notification delay or failure must not block run completion. Durable events preserve the fact and the consumer catches up independently.

**Decisive evidence:** critical-path and event-retention test

## 12. When should a service be merged back?

When ownership collapses, releases remain coordinated, synchronous coupling increases, independent scaling is unused, and operational cost exceeds isolation value. Merge-back is an architectural correction, not failure.

**Decisive evidence:** merge-back review
