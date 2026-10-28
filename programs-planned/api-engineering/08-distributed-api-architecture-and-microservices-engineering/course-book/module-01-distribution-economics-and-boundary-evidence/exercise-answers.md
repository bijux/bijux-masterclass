# Worked Answers — Module 01: Distribution Economics, Boundary Evidence, and Architecture Fitness Functions

Use these solutions to audit your reasoning for **Distribution Economics, Boundary Evidence, and Architecture Fitness Functions**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. A team proposes splitting ProjectService because the projects table has grown. What evidence is missing?

Table size is not boundary evidence. The proposal needs an independently owned capability, canonical data authority, distinct change or scale pressure, failure-isolation value, and an operator. If project rules still participate in run creation transactions, the split converts local invariants into network calls.

**Decisive evidence:** boundary scorecard and transaction map

The chapter’s decisive distinction is this: Notification unavailability should not prevent run completion. Extracting notification can improve failure isolation because the event boundary already exists. Splitting run state from idempotency would reduce isolation because every mutation would require another dependency.

## 2. Why can an independently deployed worker process still be part of the same service boundary?

Deployment independence concerns process lifecycle and scaling. Service ownership concerns business decisions and data authority. Worker Plane may deploy separately while Analysis Control retains lease, attempt, and completion authority.

**Decisive evidence:** service classification and state-ownership map

In the cumulative capstone, the rule becomes concrete: A business service must own its writes. If two services update the same tables, or one service reaches into another database for a join, deployment independence is fictional. Some components—gateway and worker plane—may be legitimate non-data services, but their lack of data authority must be explicit.

## 3. Notification Delivery has moderate traffic but a separate retry and retention policy. Is low traffic a reason to keep it inside Control?

No. Scale is only one criterion. Event-fed temporal decoupling, failure isolation, separate retention, and accountable ownership can justify extraction even at modest traffic, provided operational cost is accepted.

**Decisive evidence:** notification boundary decision record

A useful way to reason about the boundary is: Proposal Value created New coupling Decision --- --- --- --- Extract Notification Delivery independent retry, retention, receiver policy, and on-call ownership event lag, consumer recovery, separate data store approve first Extract Artifact Delivery isolated storage and egress scaling, retention and integrity policy capability issuance, event-fed references, reconciliation approve conditionally Extract Idempotency none outside the owning mutation remote transaction on every command reject

## 4. What is wrong with using number of services as an architecture KPI?

It rewards fragmentation without measuring ownership, release independence, user outcomes, or coordination cost. A system can gain services while becoming more coupled and less reliable.

**Decisive evidence:** architecture fitness functions

The implementation consequence is: The Course 8 proof suite checks the declared graph for cycles and maximum depth. It also verifies that rejected candidates remain rejected. This matters because architecture degradation is often incremental: one “temporary” callback, one shared table, one gateway rule. A scorecard without a failing proof becomes historical prose.

## 5. How does a modular monolith reduce extraction risk?

It lets the team establish cohesive modules, local contracts, tests, and change evidence before introducing network failure. Extraction can preserve a tested seam rather than invent one while migrating.

**Decisive evidence:** module dependency and change-coupling report

The important nuance is: Study real change history. If two capabilities always change in one release because one rule spans them, splitting increases coordination. If they change for distinct reasons and can evolve under contracts, separation may help.

## 6. A candidate scores highly but has no team willing to own its incidents. What is the decision?

Reject or defer. Ownership is non-compensable; a numerical score cannot create operational accountability.

**Decisive evidence:** named owner and on-call acceptance

Under concurrency or failure, the distinction becomes: Scores do not make architecture objective. They make assumptions visible. Weight ownership and data autonomy highly; subtract operational and synchronous coupling. Then require narrative evidence for each score. A boundary with a high score but no team owner remains invalid. A boundary with a moderate score may remain a module until a real workload or compliance need appears.

## 7. Why is operational cost a negative score rather than a footnote?

Every service adds patching, release, backup, monitoring, credentials, capacity, and incident work. Ignoring those costs systematically biases decisions toward fragmentation.

**Decisive evidence:** operational cost ledger

The design remains honest only if: Suppose a public request currently has a 700 ms objective. A proposed decomposition adds two sequential remote calls with 120 ms and 180 ms p95 latency. Ignoring processing variance, the budget left for the original work becomes:

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 8. What evidence could reverse the decision to keep Analysis Control cohesive?

A stable independent owner, a true data authority that can commit without cross-service transactions, measured scale or release pressure, and an extraction plan with lower synchronous coupling could justify review.

**Decisive evidence:** reversal criteria in ADR 0001

The consumer-facing consequence is: A boundary review should begin with the current transaction and failure model, not with a proposed service diagram. In the Course 7 baseline, run completion and notification delivery are already separated by a durable event. Analysis Control commits the terminal run state and the corresponding event record under one authority. Delivery can happen later, can be retried, and can fail without changing whether the analysis completed.

## 9. Why is Artifact Delivery only conditionally approved at first?

It has distinct storage and egress value, but extraction is unsafe until authorization can work without shared database reads and orphan effects can be reconciled after ambiguous completion.

**Decisive evidence:** artifact prerequisite checklist

The operational consequence is: Artifact bytes, checksums, object storage, retention, and egress have a distinct scaling profile. The extraction is conditional because authorization and completion currently depend on run state. Course 8 first designs narrow capabilities, event-fed references, and orphan reconciliation.

## 10. Name one fitness function that protects the architecture after release.

`one authoritative writer per fact` prevents future convenience writes from recreating a shared database. It can be checked from catalogue and migration ownership.

**Decisive evidence:** single-writer ownership proof

The strongest engineering interpretation is: The capstone service catalogue requires one owner for every service and one writer for every authoritative fact. The gateway is owned as an edge component, but it owns no business facts. The worker plane has an operational owner, but Analysis Control remains the writer of leases and run state. These distinctions prevent “ownership” from becoming a label attached to a deployment.

## 11. What does failure isolation mean for Notification Service?

Notification delay or failure must not block run completion. Durable events preserve the fact and the consumer catches up independently.

**Decisive evidence:** critical-path and event-retention test

The defect-oriented view is: Notification is already event-driven. It owns retry timing, destination handling, delivery history, and operational concerns distinct from Analysis Control. Its failure need not block the core workflow. The extraction adds consumer lag and another database, but not a synchronous critical-path call.

## 12. When should a service be merged back?

When ownership collapses, releases remain coordinated, synchronous coupling increases, independent scaling is unused, and operational cost exceeds isolation value. Merge-back is an architectural correction, not failure.

**Decisive evidence:** merge-back review

Across the Python and TypeScript tracks, the invariant is: or about 99.70%, before considering shared failures and network paths. This calculation is not a complete reliability model, but it exposes the cost of required synchronous edges. An extraction justified by “independent scaling” may still be unacceptable if it consumes the public SLO.
