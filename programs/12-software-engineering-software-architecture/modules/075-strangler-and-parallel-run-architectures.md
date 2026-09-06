---
module_id: SARCH-075
program: Software Engineering: Software Architecture
level: 2
module_number: 75
title: Strangler and Parallel-Run Architectures
status: complete
last_verified: 2026-09-06
---

# Strangler and Parallel-Run Architectures

## One-Page Review

### Governing question

How can an organization replace a deeply embedded system slice by slice, route bounded work safely, compare old and new behavior without creating two uncontrolled authorities, and prove when the old path can be retired?

### Essential definitions

- a **strangler fig architecture** gradually places new behavior around an existing system, diverts bounded interactions, and retires displaced legacy behavior;
- an **interception point** is a controlled location where an interaction can be observed, copied, translated, or routed;
- a **transition architecture** is intentionally temporary production structure that enables migration and has explicit ownership and removal conditions;
- **shadow execution** sends equivalent input to a nonauthoritative implementation whose effects are suppressed or isolated;
- a **parallel run** operates old and new implementations over comparable work to gather evidence; it does not imply both are authoritative;
- **canary routing** gives a bounded cohort authoritative service from the candidate path;
- **switchback** assigns authority by a coarse reversible unit such as time window, region, or partition rather than per request;
- a **reconciliation function** classifies acceptable equivalence, explainable difference, and unexplained discrepancy between results;
- **fencing** prevents a superseded writer from committing after authority transfers;
- **retirement evidence** supports removing the legacy route, state, identity, infrastructure, and operational obligations.

### Central model, mechanism, or theorem

For request $r$, let legacy result $L(r)$ and candidate result $N(r)$ be normalized by $\nu$, and let $\approx_c$ be equivalence under comparison policy $c$. Define

$$
d_c(r)=\begin{cases}0,&\nu(L(r))\approx_c\nu(N(r));\\1,&\text{otherwise.}\end{cases}
$$

For a reviewed cohort $Q$, discrepancy rate is $D_c=\sum_{r\in Q}d_c(r)/|Q|$. This is meaningful only when $Q$, pairing, normalization, nondeterminism, missing results, and severity are specified. A low aggregate rate cannot justify authority transfer if one discrepancy violates a noncompensable invariant.

### Critical invariants

- interception covers the intended population and has a tested bypass and failure policy;
- exactly one path has final authority for each mutable fact and cohort;
- shadow effects cannot escape into authoritative state or external actions;
- paired comparisons retain identity, input version, timing, and provenance;
- equivalence is domain-defined rather than raw-byte equality by default;
- missing, late, duplicate, and unpairable results remain visible;
- routing cohorts align with data authority and failure containment;
- rollback or switchback includes state, messages, clients, and external effects;
- transitional components have capacity, security, observability, ownership, and expiry;
- legacy retirement includes rare, batch, support, recovery, and regulatory paths.

### Common failures

Common failures include routing without inventorying hidden entry points; mirroring unsafe writes; calling two writers a parallel run; comparing only successful pairs; ignoring nondeterminism; accepting an average that hides severe cases; letting candidate latency affect the legacy response; sharing a failure domain that defeats the canary; translating protocols lossily; leaving the router as a permanent bottleneck; requiring full feature parity including obsolete behavior; forgetting manual workarounds; permitting rollback after incompatible state; and moving traffic without retiring data, identities, jobs, contracts, and support procedures.

### Compact example

A new credit-decision engine receives shadow copies of applications, but only the legacy engine can commit decisions. Outputs are normalized for order-insensitive reason codes and compared by applicant cohort; missing and late candidate results count separately. One rare protected cohort shows materially different declines despite 99.9% aggregate agreement. Expansion stops, domain and compliance owners investigate, and authority remains legacy. Parallel evidence exposed a consequential semantic mismatch that an aggregate success rate concealed.

### Connections

[SARCH-074](074-incremental-decomposition.md) supplies the seam and responsibility boundary, while [SARCH-073](073-versioned-contracts-and-compatibility.md) supplies coexistence contracts. [SARCH-076](../ROADMAP.md) next develops data migration architecture behind these routing patterns.

## Governing Question

Replacing a critical system in one cutover concentrates behavioral, data, operational, and organizational uncertainty at the moment of maximum exposure. A strangler fig approach makes investment, value, and risk visible incrementally by diverting slices around the existing system [1]. It does not make replacement easy, nor does it eliminate transition architecture.

Parallel execution can generate unusually relevant comparative evidence because old and new implementations see related work. It can also duplicate side effects, hide unmatched results, and institutionalize dual systems. The architecture must distinguish observation from authority and define how comparison changes the next decision.

## Why This Matters

Legacy systems often contain behavior absent from documentation: manual corrections, scheduled jobs, partner feeds, operational overrides, compliance reports, and bugs on which consumers rely. Feature-parity projects discover this late and rebuild obsolete complexity. Incremental diversion exposes actual use and lets stakeholders decide what should be preserved, corrected, or retired.

Migration infrastructure is production infrastructure. Routers, interceptors, translation layers, comparison stores, replay tools, flags, and reconciliation pipelines can affect latency, confidentiality, integrity, and recovery. Calling them temporary does not reduce their consequence.

The deepest risk is authority ambiguity. Reading twice is usually manageable; deciding or writing twice can charge, notify, allocate, or authorize twice. A parallel-run architecture is safe only when authoritative effects, cohorts, and fencing are explicit.

## Prerequisites and Retrieval

Retrieve decomposition seam, contract, compatibility window, invariant envelope, authority, system of record, idempotency, retry, replay, duplicate, ordering, interception, proxy, router, facade, adapter, anti-corruption layer, feature flag, canary, shadow traffic, cohort, control group, normalization, reconciliation, threshold, blast radius, fencing token, rollback, roll forward, observability, data lineage, and decommissioning.

SARCH-072 supplies evidence-bearing transitions, SARCH-073 mixed-version compatibility, and SARCH-074 seam creation and single-authority reasoning. This chapter focuses on traffic and execution architectures. It does not replace the data-copy, backfill, consistency, and cutover analysis in SARCH-076.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish strangler fig replacement from proxy installation or wholesale rewrite;
2. select interception points across HTTP, messaging, files, events, UI, and scheduled work;
3. distinguish shadow, parallel comparison, canary, switchback, dual-read, and dual-write modes;
4. preserve one authority and prevent shadow side effects;
5. design pairing, normalization, equivalence, severity, and missing-result treatment;
6. choose cohorts aligned with data and failure boundaries;
7. evaluate routers, translators, comparison stores, and flags as transition architecture;
8. define expansion, stop, reverse, correction, and roll-forward decisions;
9. reject unnecessary feature parity and discover off-system work;
10. assemble complete retirement evidence rather than merely reaching zero normal traffic.

## Core Exposition

**Define the displacement outcome.** Name the capability, population, architecture revision, stakeholder outcome, constraints, and horizon. Decide whether the goal is replacement, capability extraction, supplier exit, risk containment, or product change. A strangler fig is a transition strategy, not a target topology.

Avoid declaring that every legacy feature must exist in the candidate. Some behavior is obsolete, duplicated, unlawful, unsafe, or compensating for another defect. Trace current needs and authoritative policy. Patterns of Legacy Displacement explicitly warn that feature parity can reproduce unwanted behavior [3].

**Inventory every entry and exit.** Map user routes, APIs, events, files, queues, batch schedules, database access, reports, support consoles, identity flows, partner exchanges, backups, replays, and manual work. Identify which interactions can be intercepted and which bypass proposed routing.

Observation should cover failure and recovery paths, not only normal traffic. A reverse proxy does not see a partner writing files or an analyst querying a database. Uncontrolled bypasses undermine both comparison coverage and retirement claims.

**Choose an interception point.** Useful points include edge routing, an API gateway, an application facade, navigation, message subscription, event interception, file intake, database wrapper, or in-process abstraction. Prefer a stable semantic boundary that preserves identity and supports bounded diversion.

The point must have a failure policy. If the router is unavailable, does traffic fail, use legacy, use candidate, or follow a cached decision? Fallback can violate data authority after cutover. Protect routing configuration, audit changes, and test degraded control-plane behavior.

**Define transition modes.** In *shadow* mode, candidate outputs are evidence only and effects are suppressed. In *parallel comparison*, both implementations process comparable input, but authority is still named. In *canary* mode, candidate output becomes authoritative for a bounded cohort. In *switchback*, authority alternates by controlled unit. Dual reads compare state; dual writes attempt state mutation twice and require a far stronger protocol.

Never use “parallel run” without the mode. Two calculators with one committing path differ fundamentally from two payment writers. Document authority for decisions, persistent data, emitted messages, external calls, audit, and user-visible response.

**Isolate shadow side effects.** Candidate code may send email, charge a card, reserve inventory, alter a cache, consume a one-time token, advance a cursor, or trigger a downstream workflow. Replace effectful dependencies with governed sinks, simulations, or idempotent observation interfaces.

Isolation must be end-to-end. Pointing the candidate at a copied database does not prevent calls to a production partner. Use scoped identities, network policy, test accounts, explicit dry-run capabilities, and alerts for attempted forbidden effects.

**Preserve input equivalence.** Comparison needs paired inputs with stable identity, version, and provenance. Copying after legacy mutation can give the candidate different state. Asynchronous delivery can reorder messages. Personal or sensitive data copying may require additional authority and minimization.

Record interception time, payload digest where appropriate, configuration, model or rule versions, and relevant dependencies. Do not log secrets or create an ungoverned shadow data store. Define retention and deletion.

**Define semantic equivalence.** Raw output equality is sometimes correct for deterministic hashes or exact ledger totals. Often it is wrong: identifiers, timestamps, ordering, formatting, probabilistic ranks, and explanatory text may differ while the business result is equivalent.

Build a domain-owned normalization $\nu$ and comparison relation $\approx_c$. State tolerances, units, rounding, ignored fields, set ordering, and acceptable nondeterminism. Never normalize away a field merely because it produces failures; justify why it is noncontractual.

**Classify discrepancies by consequence.** Separate exact match, acceptable equivalence, known intentional change, legacy defect, candidate defect, input mismatch, missing result, late result, and unexplained difference. Attach severity to the affected invariant and cohort.

An aggregate rate can conceal a catastrophic case. Review maximum loss, protected populations, safety or compliance rules, and tail behavior. Some discrepancies are noncompensable gates regardless of frequency.

**Count missing and unpairable work.** Comparing only requests that produced two successful outputs creates survivor bias. Report legacy-only, candidate-only, both-failed, timed-out, duplicate, and unpairable cases. Define denominator before execution.

Candidate latency in shadow mode should not delay authoritative legacy response unless that consequence is explicitly accepted. Measure lag separately. Provide backpressure and shedding so comparison cannot exhaust production resources.

**Treat old behavior as evidence, not oracle.** Agreement proves similarity, not correctness. The legacy result may contain a defect; both implementations may share a faulty upstream input; the candidate may deliberately implement a corrected policy.

Use specifications, stakeholder decisions, independent calculations, curated cases, invariants, and incident history to adjudicate. Fowler's legacy-displacement material recommends returning to source requirements where inherited reports or workarounds are misleading [4].

**Select a cohort that contains risk.** Cohorts may be tenants, accounts, regions, products, operations, devices, or stable hashed identities. A per-request split can break session, workflow, cache, or data consistency. Align routing with the unit of authority and state.

A 1% cohort is not automatically safe. It may include critical users, share a global ledger, or corrupt state read by everyone. Map failure domains and dependencies. Exclude no population without understanding whether that exclusion hides the hard cases.

**Gate progress with evidence.** Before each expansion define required duration, workload and failure coverage, discrepancy thresholds, quality measures, manual review, and decision authority. Include latency, availability, capacity, security, cost, support, recovery, and business outcome.

Possible decisions are expand, hold, correct and repeat, revise equivalence, isolate a cohort, reverse, roll forward, or stop. If every result expands traffic, measurement is decorative. Preserve dissent and reasons.

**Fence authority transfer.** When the candidate becomes authoritative, routing alone may not stop an in-flight or partitioned legacy writer. Use epoch or ownership tokens, conditional writes, leases with safe assumptions, access revocation, or another domain-appropriate fencing mechanism.

Define the exact transfer point and audit it. Ensure recovery does not resurrect an old snapshot with authority. If rollback after transfer is unsafe, specify roll-forward and compensation instead.

**Understand dual writes.** A caller writing old then new can fail between writes; retry can duplicate one side; order can reverse; both can accept incompatible values. A transaction spanning both may reduce some ambiguity while increasing coupling and availability dependency.

Prefer one authoritative write plus replication, change capture, or derived comparison where it preserves the requirement. When dual writes are unavoidable, define idempotency, ordering, durable intent, reconciliation, repair authority, and exit conditions. SARCH-076 provides the fuller data treatment.

**Use switchbacks carefully.** Time- or region-based switches can expose candidate behavior under real load while keeping cohorts coherent. They complicate comparison because conditions differ across periods and carryover state can contaminate results.

Randomized assignment can improve causal comparison for eligible low-consequence changes, but many migrations cannot ethically or technically randomize. Account for time, population, workload, and learning effects. Never claim causal proof from an uncontrolled before-after comparison.

**Engineer the router.** The router must handle protocol semantics, identity, authorization, request bodies, streaming, retries, timeout budgets, affinity, observability, and configuration consistency. It may need to translate, but lossy translation should be visible and tested.

Keep routing rules understandable and bounded. Conflicting flags and nested cohort rules create unreachable or unintended states. Maintain a decision table, test it, record the chosen route, and remove rules after completion.

**Operate transition architecture.** Size shadow compute and comparison storage. Prevent candidate overload from consuming legacy capacity. Secure copied inputs and discrepancy records. Give dashboards and alerts owners, runbooks, retention, and recovery procedures.

Fowler's transitional-architecture pattern treats migration elements as installed specifically to enable legacy displacement and intended for removal [5]. “Temporary” should mean governed lifecycle, not reduced engineering quality.

**Find manual and off-system behavior.** Observe operators, spreadsheets, exports, email, phone approvals, and corrections. The visible application may not produce the real business outcome. Migrating only its code can remove a critical control or reproduce an avoidable workaround.

Decide which manual work is a required control, usability failure, exception, or obsolete process. Include affected people in design; automation is not automatically improvement.

**Plan rollback and roll forward.** Before authoritative canary, identify whether the old path can read candidate-produced state and whether external effects can be undone. Test the route switch under control-plane failure. Define compensation for irreversible effects.

After an authority or schema boundary, roll forward may be safer. A kill switch that stops new candidate work is still useful even when completed work cannot revert. State these different controls precisely.

**Avoid permanent comparison.** Long parallel runs double cost, expand data exposure, and create pressure to treat both systems as required. Set a learning horizon and retirement conditions. If continuous independent checking has durable value, redesign it as an owned control rather than leaving migration machinery accidentally.

Unexplained discrepancies are not resolved by lowering thresholds. Investigate, change the comparison, correct behavior, or accept a difference through accountable policy. Preserve sampled evidence for audit within privacy and retention constraints.

**Retire from the edges inward.** Stop legacy authority, remove routes and bypasses, wait for or disposition in-flight work, revoke identities, remove data replication and jobs, migrate support and recovery, archive required records and decoders, decommission infrastructure, and delete transition code.

Observe after removal and define response to unexpected callers. Retirement completes the economic and security benefit. Zero primary traffic alone is not enough.

## Definitions and Notation

Let:

- $Q$ be the reviewed set of paired interactions;
- $L(r)$ and $N(r)$ be legacy and candidate results for request $r$;
- $\nu$ be a declared normalization function;
- $\approx_c$ be domain equivalence under comparison policy $c$;
- $d_c(r)$ be 0 for equivalent results and 1 otherwise;
- $D_c=|Q|^{-1}\sum_{r\in Q}d_c(r)$ be aggregate discrepancy rate for $|Q|>0$;
- $U$ be unpaired, missing, late, or duplicate observations excluded from $Q$ but reported separately;
- $S_k$ be severity class $k$, with $D_{c,k}$ the discrepancy rate within that class or cohort;
- $a(r)\in\{L,N\}$ identify the authoritative path for $r$;
- $g(r)$ be the stable routing cohort;
- $e$ be an authority epoch or fencing token;
- $T$ be the transition architecture and $\tau(T)$ its removal conditions.

The formula requires paired observations and does not account for severity by itself. If $Q$ is empty, $D_c$ is undefined. Missing results must not be silently omitted from readiness evidence.

## Mechanisms, Invariants, or Proof Structure

**Single-authority invariant.** For every mutable fact and cohort, exactly one path may commit the final decision in a transition state. Shadow output has no authority. If both paths can commit independently, reconciliation after the fact cannot guarantee that external consequences were not duplicated.

**Aggregate-rate counterexample.** Suppose 9,999 of 10,000 comparisons agree and the one difference creates an unauthorized payment. Then $D_c=1/10{,}000=0.0001=0.01\%$. A threshold of 0.1% passes, yet the integrity invariant fails. Therefore an aggregate discrepancy threshold is insufficient without severity gates.

**Executable reconciliation.** This toy ledger reports matched, mismatched, and missing pairs rather than dropping incomplete work.

<!-- bijux-verify: {"id":"reconcile-parallel-results","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"paired=3\nmatched=2\nmismatched=1\nlegacy_only=1\ncandidate_only=1\ndiscrepancy_rate=0.333\nready=false\n","stderr":""}} -->
```python
legacy = {"a": 100, "b": 200, "c": 300, "d": 400}
candidate = {"a": 100, "b": 201, "c": 300, "e": 500}
paired_ids = legacy.keys() & candidate.keys()
matched = {key for key in paired_ids if legacy[key] == candidate[key]}
mismatched = paired_ids - matched
legacy_only = legacy.keys() - candidate.keys()
candidate_only = candidate.keys() - legacy.keys()
rate = len(mismatched) / len(paired_ids)
print(f"paired={len(paired_ids)}")
print(f"matched={len(matched)}")
print(f"mismatched={len(mismatched)}")
print(f"legacy_only={len(legacy_only)}")
print(f"candidate_only={len(candidate_only)}")
print(f"discrepancy_rate={rate:.3f}")
print(f"ready={str(not mismatched and not legacy_only and not candidate_only).lower()}")
```

Execution verifies one finite comparison. It does not define valid equivalence, severity, population representativeness, or production readiness.

**Fencing invariant.** After authority epoch advances to $e+1$, a writer holding $e$ must be unable to commit. Routing without storage or decision fencing does not satisfy this invariant because delayed work can arrive after the route changes.

**Denominator invariant.** Every intercepted interaction receives a terminal comparison classification. If incomplete interactions disappear from both numerator and denominator, the measured rate is biased toward work both systems complete.

**Retirement proposition.** Removing the primary route is insufficient when any legacy authority, bypass, scheduled caller, replay, credential, recovery dependency, or obligated support remains. Retirement is a conjunction over these surfaces, so failure of one condition keeps the legacy obligation active.

## Alternatives and Trade-Offs

**Edge proxy versus internal interception.** Edge routing covers external traffic visibly but misses internal, batch, and data paths. Internal interception reaches behavior close to the seam but requires legacy change. Often both are needed with one routing authority.

**Shadow versus canary.** Shadowing reduces consequence and enables paired comparison but cannot test authoritative effects fully. Canary routing tests real behavior but exposes a cohort. Use shadow evidence before authority where it answers the risk, then bounded canary for mechanisms shadowing omits.

**Request split versus cohort split.** Per-request assignment improves sample mixing but can violate state and workflow consistency. Cohort assignment preserves authority but may confound tenant or regional traits. Match allocation to invariant and analysis.

**Raw equality versus semantic comparison.** Raw equality is simple and auditable but overreacts to irrelevant nondeterminism. Semantic normalization reduces noise but can hide defects. Version and review normalization as contract logic.

**Fail open to legacy versus fail closed.** Legacy fallback preserves availability before authority transfer but can bypass new security or data decisions afterward. Fail closed protects integrity but reduces availability. Define policy per transition state and test it.

**Full parity versus outcome replacement.** Parity lowers apparent change but reproduces unused features and bugs. Outcome replacement requires stakeholder decisions and may change workflows. Preserve obligations, not accidental implementation.

**Temporary router versus durable gateway.** Reusing a durable gateway can reduce infrastructure, but migration rules can pollute its ownership. A temporary router is removable but adds operations. Name the lifecycle either way.

## Failure Modes and Misconceptions

1. **“A proxy implements the strangler fig.”** It is only one possible interception mechanism.
2. **“Parallel means both paths write.”** Parallel observation should normally retain one authority.
3. **“Shadow is side-effect free.”** Candidate dependencies may still emit or mutate unless isolated.
4. **“Same input means comparable state.”** timing, mutation, configuration, and dependency versions can differ.
5. **“Byte equality is correctness.”** Some differences are irrelevant and identical outputs can share one error.
6. **“Low discrepancy means ready.”** One severe invariant violation can dominate the aggregate.
7. **“Only paired successes matter.”** Omitting missing and failed results creates survivor bias.
8. **“One percent traffic means one percent risk.”** shared state and control planes can spread consequences.
9. **“Random routing is always scientific.”** workflows, ethics, dependence, and nonstationarity can invalidate comparison.
10. **“The old system is the oracle.”** Legacy behavior may be wrong, obsolete, or workaround-laden.
11. **“Routing transfers authority.”** In-flight and partitioned writers require fencing.
12. **“Dual writes keep stores synchronized.”** partial failure, retry, and ordering create divergence.
13. **“Fallback is always safe.”** Old code may not understand new state or policy.
14. **“Feature parity is the acceptance criterion.”** It can rebuild unused or harmful behavior.
15. **“Temporary infrastructure can be underengineered.”** It carries production traffic and sensitive evidence.
16. **“Zero traffic proves retirement.”** rare, recovery, batch, and bypass paths can remain.
17. **“Longer parallel run always improves confidence.”** exposure, cost, drift, and duplicated obligations also grow.
18. **“Migration ends at cutover.”** retirement and post-removal observation complete the architecture.

## Worked Examples

### Example 1

**Situation.** A reverse proxy diverts `/catalog` to a new service, but nightly imports still write legacy tables directly.

**Reasoning.** HTTP traffic is intercepted, yet batch writes determine catalog state and bypass comparison. The team inventories entry points, places file intake behind an owned adapter, and keeps legacy authority until both interactive and batch paths are governed.

**Conclusion.** A strangler boundary is only as complete as its hidden entry and exit paths.

### Example 2

**Situation.** A shadow payment implementation uses production credentials “so results are realistic.”

**Reasoning.** It can create real authorizations even though its response is ignored. The team replaces the effectful gateway with a governed simulator and tokenized test accounts, denies production payment network access, and alerts on attempted effects.

**Conclusion.** Suppressing a response does not suppress side effects; shadow authority must be technically constrained.

### Example 3

**Situation.** Old and new search results differ only in identifier order.

**Reasoning.** Product semantics define the top three as an unordered set but preserve rank afterward. Raw equality overreports disagreement; sorting every result would hide meaningful ranks. Normalization sorts only the top-three set and retains remaining order, with the rule versioned and reviewed.

**Conclusion.** Comparison equivalence must encode actual semantics narrowly.

### Example 4

**Situation.** Of 1,000 intercepted requests, 900 produce paired results with nine mismatches; 100 candidate calls time out.

**Reasoning.** Reporting 9/900=1% alone hides a 10% missing-candidate rate. All interactions need terminal categories: 891 matched, 9 mismatched, 100 legacy-only/timeouts. Readiness must assess both correctness and completion behavior.

**Conclusion.** Missing pairs belong in migration evidence, not outside the denominator story.

### Example 5

**Situation.** A candidate has 0.01% discrepancy over 10,000 credit decisions.

**Reasoning.** The sole mismatch affects a protected cohort and reverses an eligibility decision. Aggregate threshold passes, but a noncompensable policy gate fails. Qualified owners investigate model, input, and rule versions; traffic does not expand.

**Conclusion.** Severity and cohort review prevent averages from hiding consequential errors.

### Example 6

**Situation.** A 5% per-request checkout canary reads and writes customer carts.

**Reasoning.** A customer's requests can alternate implementations with incompatible cart versions. The team assigns by stable customer cohort and version-compatible cart state, or isolates a separate store partition. Routing is recorded for support and reconciliation.

**Conclusion.** Cohort granularity must match workflow and data authority.

### Example 7

**Situation.** Traffic switches to a new order writer, but a delayed legacy worker commits afterward.

**Reasoning.** The router changed, yet the queued job retained database access. An authority epoch is stored with the order; conditional writes reject the old epoch, legacy identity is revoked after drain, and rejected attempts alert operators.

**Conclusion.** Fencing, not routing alone, completes authority transfer.

### Example 8

**Situation.** A report replacement never matches the legacy spreadsheet exactly.

**Reasoning.** Investigation finds manual exchange-rate edits and an obsolete category adjustment. Finance owners return to authoritative policy, classify the old adjustments, approve a corrected definition, and compare both systems to curated cases. Intentional differences are recorded rather than normalized away.

**Conclusion.** Legacy output is evidence; authoritative meaning decides whether difference is defect or correction.

### Example 9

**Situation.** A canary is isolated by region but shares a global identity issuer and queue.

**Reasoning.** Candidate overload exhausts queue partitions and its malformed claims affect issuer caches globally. Regional request routing does not contain these mechanisms. The team isolates queue namespace and test authority or reduces candidate privileges before resuming.

**Conclusion.** Blast-radius claims must follow shared data and control dependencies.

### Example 10

**Situation.** Normal legacy traffic is zero after migration.

**Reasoning.** Inventory still finds annual replay, support impersonation, an old disaster runbook, replication, credentials, and a contractual decoder obligation. Each is migrated, retired, or explicitly retained with ownership; identifiers are reserved and infrastructure removal is monitored.

**Conclusion.** Complete retirement spans authority, rare use, data, identity, operations, and obligations—not just routing.

## Cross-Program Connections

- [CONPAR](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies ordering, atomicity, and interference reasoning for parallel execution.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) develops canary delivery, flags, observability, rollback, and incident response.
- [DBE](../../18-database-engineering/ROADMAP.md) develops fencing, transactions, replication, reconciliation, and recovery for state transfer.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) supplies lineage, semantic comparison, retention, and downstream consumer discovery.
- [SEC](../../25-security-engineering/ROADMAP.md) develops scoped identities, network isolation, audit, and downgrade or bypass controls.
- [DIST](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, duplicate, timing, partition, and authority models.
- [API](../../28-api-and-service-engineering/ROADMAP.md) develops gateway, routing, idempotency, version, and deprecation mechanics.
- [PLAT](../../29-platform-engineering/ROADMAP.md) provides governed routing, shadow environments, telemetry, policy, and safe self-service rollout capabilities.

## References

1. Martin Fowler. “Strangler Fig.” 22 August 2024. Checked 2026-09-06. https://martinfowler.com/bliki/StranglerFigApplication.html
2. Martin Fowler. “Original Strangler Fig Application.” 29 June 2004, revised 29 April 2019. https://martinfowler.com/bliki/OriginalStranglerFigApplication.html
3. Ian Cartwright, Rob Horn, and James Lewis. “Patterns of Legacy Displacement.” MartinFowler.com, maintained catalog checked 2026-09-06. https://martinfowler.com/articles/patterns-legacy-displacement/
4. Ian Cartwright, Rob Horn, and James Lewis. “Divert the Flow.” 9 June 2022. Checked 2026-09-06. https://martinfowler.com/articles/patterns-legacy-displacement/divert-the-flow.html
5. Ian Cartwright, Rob Horn, and James Lewis. “Transitional Architecture.” 28 March 2022. Checked 2026-09-06. https://martinfowler.com/articles/patterns-legacy-displacement/transitional-architecture.html
6. Sam Newman. *Monolith to Microservices: Evolutionary Patterns to Transform Your Monolith*. O'Reilly Media, 2019.
7. Michael Feathers. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
8. Jez Humble and David Farley. *Continuous Delivery*. Addison-Wesley, 2010.
9. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage. *Building Evolutionary Architectures*. 2nd ed. O'Reilly Media, 2022.
10. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.

## Exercises

### Exercise 1

Define strangler fig architecture, interception point, transition architecture, shadow execution, parallel run, canary, switchback, reconciliation, fencing, and retirement evidence.

### Exercise 2

A run intercepts 2,000 requests: 1,920 paired, 1,900 equivalent, 20 mismatched, 60 legacy-only, and 20 candidate-only. Compute paired discrepancy rate and all-category proportions. Explain why the paired rate is insufficient.

### Exercise 3

A new fulfillment service shadows production but reserves inventory and emits events. Diagnose the architecture and design safe shadow evidence.

### Exercise 4

Design strangler and parallel-run states for replacing a billing calculator. Include interception, authority, cohorts, normalization, missing results, severe gates, fencing, rollback or roll forward, and retirement.

### Exercise 5

A public-health reporting system combines clinical feeds, manual corrections, statutory reports, privacy-sensitive records, and emergency dashboards. Propose a governed replacement architecture without claiming that parallel agreement establishes clinical, legal, privacy, accessibility, or public-health approval.

## Answers to the Exercises

### Answer 1

A strangler fig architecture gradually surrounds, diverts, and retires legacy behavior. An interception point controls an interaction for observation, copying, translation, or routing. Transition architecture is intentionally temporary production structure with an owner and removal conditions. Shadow execution runs a nonauthoritative candidate with effects isolated. Parallel run processes comparable work in both paths while authority remains explicit. Canary makes the candidate authoritative for a bounded cohort. Switchback alternates authority by a controlled coarse unit. Reconciliation classifies equivalence and discrepancy. Fencing rejects stale writers after authority transfer. Retirement evidence supports removing every legacy obligation, not only normal traffic.

### Answer 2

The paired discrepancy rate is $20/1920=0.010416\ldots$, about 1.042%. Relative to all 2,000 intercepted requests, equivalent pairs are 95%, mismatches 1%, legacy-only 3%, and candidate-only 1%. These categories sum to 100%.

The paired rate excludes 80 unpaired interactions and says nothing about severity, cohort, representativeness, or shared defects. If timeouts disproportionately affect one population or one mismatch violates an integrity invariant, even a low rate cannot authorize expansion. Evidence should report terminal categories, reasons, latency, severity, and cohort-specific results.

### Answer 3

The candidate is not a safe shadow: reservations mutate authoritative capacity and emitted events can trigger external effects. Ignoring its response does not remove authority. Give the candidate a scoped identity denied production writes and event publication. Feed it immutable input copies or governed replay, replace inventory and event dependencies with simulators or quarantine sinks, and alert on attempted forbidden effects.

Pair inputs and configuration, compare proposed reservations and events semantically, and record missing or late results. If real contention must be tested, advance to an explicitly authorized canary with one authoritative owner, bounded inventory cohort, idempotency, fencing, recovery, and downstream isolation. Do not blur that higher-consequence state into shadow terminology.

### Answer 4

Intercept billable usage at a stable account or ledger boundary and preserve a durable correlation identity. Legacy remains the only committing calculator while the candidate shadows into an isolated evidence store. Normalize irrelevant ordering and formatting but compare totals, currency, rounding, line provenance, tax treatment, and terminal errors exactly where required. Report unmatched, late, and duplicate cases.

Segment by product, currency, account type, boundary values, billing cycle, and protected or regulated cohort. Gate on zero duplicate charges and unauthorized adjustments, domain-approved tolerances, representative peak and full-cycle evidence, and recovery. After shadow acceptance, route a fenced account cohort authoritatively to the candidate; never split one account's cycle across authorities. Stop, hold, reverse, or roll forward according to predeclared state compatibility.

Transfer authority with an epoch or equivalent conditional mechanism, revoke old write paths after drain, and reconcile the ledger. Retirement includes re-rating, annual jobs, credits, support tools, exports, identities, contracts, recovery, records, and infrastructure. A strong answer treats the router and comparator as secured capacity-bearing transition architecture with expiry.

### Answer 5

Establish accountable public-health, clinical, epidemiology, privacy, security, accessibility, legal, records, operations, and emergency-management authorities. Inventory clinical and laboratory feeds, manual correction, statutory transformations, late data, identity resolution, dashboards, exports, replays, audit, and emergency procedures. Define nonnegotiable authority, provenance, correction, confidentiality, accessibility, timeliness, and statutory-report invariants.

Intercept one bounded report or feed after authorization, initially shadowing the candidate with effects and external publication disabled. Minimize copied sensitive data, preserve lineage, and secure comparison retention. Pair records and versions; distinguish expected policy changes, legacy defects, candidate defects, missing and late results. Compare domain semantics and cohort completeness, not raw rows alone. Qualified authorities adjudicate differences.

Advance only through authorized cohorts aligned with reporting authority and data jurisdiction. Fence publication so exactly one path issues each statutory or emergency result. Test failure, delayed feeds, manual correction, replay, and recovery. Define rollback before incompatible state; otherwise use controlled roll forward. Retire old feeds, identities, correction tools, archives, reports, contracts, and runbooks only with evidence. Parallel agreement is technical evidence, not proof of clinical validity, legal compliance, privacy, accessibility, or public-health readiness; those conclusions require the responsible processes and people.
