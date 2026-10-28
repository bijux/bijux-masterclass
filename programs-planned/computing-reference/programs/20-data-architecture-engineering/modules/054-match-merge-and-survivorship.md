---
module_id: DARCH-054
program: Data Architecture Engineering
level: 2
module_number: 54
title: Match, Merge, and Survivorship
status: complete
last_verified: 2026-09-03
---

# Match, Merge, and Survivorship

## One-Page Review

### Governing question

How should an enterprise turn evidence that records may represent the same entity into controlled match decisions, reversible merge actions, and purpose-qualified surviving values without destroying source history or spreading a bad decision across every consumer?

### Essential definitions

- **matching** compares candidate records and produces evidence or a governed decision such as match, possible match, nonmatch, prohibited, or insufficient evidence.
- A **match policy** binds entity scope, population, purpose, candidate rules, comparison signals, thresholds, negative evidence, decision states, and version.
- An **auto-link threshold** is the evidence boundary above which policy permits an automated link; it is not universal proof of identity.
- A **review band** preserves uncertain cases for adjudication instead of forcing binary output.
- A **merge** is a governed state transition that combines identity membership, identifiers, relationships, or records under declared semantics.
- A **logical merge** links records into one entity while retaining each source record; a **physical merge** collapses or retires records and therefore carries greater reversibility risk.
- A **surviving identifier** is the continuing identifier after a merge; retired identifiers normally remain resolvable aliases or tombstones.
- **unmerge** or **split** reverses or revises a prior merge while preserving lineage and downstream correction semantics.
- **survivorship** selects, composes, or preserves attribute values and relationships for a declared master view after identity membership is decided.
- A **survivorship rule** ranks or filters eligible assertions by authority, verification, effective time, quality, purpose, consent, or another governed criterion.
- An **override** is a scoped, reasoned, approved exception to automated match, merge, or survivorship policy with effective time and expiry.
- **decision provenance** records inputs, transformations, rules or models, versions, thresholds, reviewers, rationale, time, and supersession.

### Central model, mechanism, or theorem

Represent the capability as:

`M = (outcomes, scope, sources, candidates, comparisons, match decisions, merge transitions, assertions, survivorship, publication, protection, service, ownership, evidence, lifecycle)`

The core theorem is separation of decisions. `Match(a,b)` evaluates whether representations belong to one scoped entity. `Merge(E_i,E_j)` changes identity state and identifiers. `Survive(A,k,u)` selects or composes assertions for attribute or relationship `k` and use `u`. A match need not cause an immediate merge; a merge must not delete source evidence; survivorship must not retroactively become match evidence unless an explicit versioned policy allows it. Each stage has its own authority, uncertainty, approval, failure, and correction contract.

### Critical invariants

- Entity type, population, purpose, consequence, and policy version qualify every automated or reviewed match.
- Candidate, comparison, threshold, negative evidence, decision, and reviewer provenance remain reconstructable.
- Match, possible match, nonmatch, prohibited, unresolved, merged, unmerged, split, and retired remain distinct states.
- A merge uses expected prior versions, stable operation identity, idempotency, authorization, and conflict policy.
- Source records and identifiers survive logical consolidation; physical deletion requires separate authority and retained lineage.
- Surviving enterprise identifiers are stable, retired identifiers are not recycled, and alias chains are bounded and resolvable.
- Merge and split transitions preserve prior memberships, relationships, decisions, affected consumers, and reversal evidence.
- Survivorship occurs at attribute or relationship granularity unless whole-record choice is explicitly justified.
- Nonselected assertions remain available according to protection and retention policy with source, time, and decision reason.
- Unknown, disputed, withheld, invalid, expired, not applicable, and source unavailable are not converted into ordinary nulls.
- Publication propagates identity and value changes with ordering, idempotency, correction, reconciliation, and acknowledgement.
- Protection covers comparison values, linkage evidence, clusters, aliases, golden views, histories, review cases, exports, and backups.

### Common failures

Common failures are using one threshold for every consequence; treating a high score as certainty; merging every likely match automatically; using transitive closure without cluster checks; selecting a survivor ID by database convenience; deleting losing records; recycling retired IDs; updating membership without expected-version control; letting late jobs undo steward decisions; choosing an entire winning record; using “latest” without clock and effective-time semantics; ranking sources globally instead of by attribute; treating completeness as correctness; overwriting disputed values; dropping multiplicity; feeding survivorship results back into matching without lineage; applying policy changes directly to live entities; publishing a merge without split correction; measuring only duplicate reduction; and retiring the capability while aliases, cases, and consumers remain.

### Compact example

Two records agree on a verified scoped identifier and normalized email, producing score 9 under match policy 4 and an `auto_link` result above threshold 8. A logical merge creates entity `entity-100`, preserves both source identifiers as cross-references, and records merge operation `merge-501`. Billing has the newer email assertion, but CRM has the verified assertion; contact survivorship policy 3 selects CRM because verification outranks recency. The match evidence, merge state, both assertions, and selected-value rationale remain separate.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-051](051-master-data-and-golden-records.md), [DARCH-052](052-reference-data.md), and [DARCH-053](053-identity-resolution.md) establish time, ownership, product, master, reference, and resolution boundaries. This module deepens action policy; [DARCH-055](../ROADMAP.md) next compares registry, consolidation, and coexistence styles.

## Governing Question

Finding similar records is only the beginning. An organization must decide when evidence permits automatic linkage, when people must review, what state changes after approval, which identifier continues, which values appear in each master view, how conflicting assertions remain visible, and how every affected consumer recovers from a mistake.

The governing question is which policy and operational architecture makes matching useful without turning probabilistic or incomplete evidence into irreversible identity and value loss. The answer must connect error consequence, review capacity, atomic state transitions, attribute authority, propagation, protection, recovery, and lifecycle evidence.

## Why This Matters

The U.S. Census Bureau [Statistical Quality Standard C4](https://www.census.gov/about/policies/quality/standards/standardc4.html) requires accurate linking, documented procedures, evaluation, review, protection, and corrective action. Its [Overview of Record Linkage and Current Research Directions](https://www.census.gov/library/working-papers/2006/adrm/rrs2006-02.html) discusses comparison-based record linkage. These mechanisms support matching; they do not decide an enterprise's merge authority or surviving representation.

IBM's [Matching Algorithms in Master Data Management](https://www.ibm.com/docs/en/ws-and-kc?topic=data-matching-algorithms-in-match-360) separates standardization, candidate bucketing, comparison, and entity formation and describes how additions, changes, and deletions can merge or split entities. IBM [Survivorship](https://www.ibm.com/docs/en/imdm/14.0.0?topic=data-survivorship) distinguishes duplicate identification from later action and value composition. Its guidance on [Deciding on Criteria for Data Survivorship](https://www.ibm.com/docs/en/imdm/12.0.0?topic=data-deciding-criteria-survivorship) discusses source, standards, quality, and recency, while [Merging Records](https://www.ibm.com/docs/en/imdm/12.0.0?topic=assignment-merging-records) shows that merge can involve staged coordination with sources. Product mechanisms require locally justified semantics and controls.

W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) supplies a provenance vocabulary. The NIST [Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework) addresses privacy risk, the NIST [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) addresses risk in AI systems, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames lifecycle engineering of trustworthy systems. Match, merge, and survivorship combine classification, sensitive linkability, distributed state change, and durable consequence.

## Prerequisites and Retrieval

You should understand identity resolution, master and reference data, identifiers, assertions, namespaces, source authority, temporal modeling, probability and classification basics, APIs, events, transactions, concurrency, lineage, privacy, security, reliability, recovery, and governance.

Retrieve candidate, comparison, feature, score, calibration, match, possible match, nonmatch, negative evidence, threshold, margin, abstention, clerical review, entity cluster, link, merge, collapse, logical merge, physical merge, surviving ID, obsolete ID, alias, tombstone, split, unmerge, survivorship, eligible assertion, source priority, verification, recency, multiplicity, override, provenance, propagation, reconciliation, and retirement.

As a retrieval test, inspect “automatically merge duplicates and keep the best data.” Ask which entity and population, evidence and thresholds, error losses, review bands, merge type, identifier survivor, source write authority, attribute semantics, clocks, multiplicity, consent, correction, consumers, propagation time, rollback, protection, and retirement conditions apply. “Duplicate” and “best” hide several independent decisions.

## Learning Objectives

After completing this module, you should be able to:

1. separate candidate generation, comparison, match decision, merge action, and attribute or relationship survivorship;
2. define match policies using evidence, negative constraints, thresholds, margins, decision states, consequence, and review capacity;
3. compare logical linking, physical merging, consolidation, aliasing, tombstoning, unmerge, and split semantics;
4. design stable surviving identifiers and temporal cross-references without destroying source identity;
5. construct attribute-level survivorship using authority, verification, time, quality, purpose, consent, and multiplicity;
6. preserve assertions, rule and model versions, overrides, approvals, decision provenance, and historical master generations;
7. control concurrency, idempotency, staged source coordination, out-of-order work, replay, and reconciliation;
8. publish merge, split, and value-change contracts with downstream correction and acknowledgement;
9. evaluate accuracy, calibration, slice effects, queue health, false-link and missed-link harm, propagation, and value; and
10. protect, recover, migrate, and retire the whole decision system with accountable evidence.

## Core Exposition

**Separate the pipeline.** Candidate generation retrieves plausible comparisons. A comparator produces signals or scores. Match policy creates a decision. Merge changes identity state. Survivorship creates a view.

These steps can share data but not implicit authority. A comparator must not mutate the master, and a merge function must not silently invent value precedence.

**Start from scoped identity.** Reuse the entity type, population, purpose, time, and consequence definition established by identity-resolution architecture.

A party match policy must not merge household membership, account ownership, and legal personhood. Different scopes require different entity graphs and master views.

**Define decision states.** At minimum distinguish match, possible match or review, nonmatch, insufficient evidence, prohibited, and superseded.

Binary decisions force uncertainty into unsafe links or missed links. Each downstream process needs declared behavior for every state.

**Treat scores as evidence, not truth.** A score has meaning only with comparator version, population, features, transformations, missingness, and evaluation.

If a score is called a probability, verify calibration on representative independent data. A monotonic ranking score can still support policy without probabilistic language.

**Use more than one threshold when needed.** An upper boundary can permit auto-link, a lower boundary can permit nonmatch, and the interval between can abstain or route to review.

Thresholds should reflect false-link and missed-link loss, label uncertainty, review capacity, latency, and downstream reversibility. One global number rarely fits every use.

**Use margin and contradiction policy.** A high leading score can remain ambiguous when a runner-up is nearly equal or strong negative evidence exists.

Require a score margin, evidence minimum, or cluster constraint. Do not let a threshold override mutually exclusive verified identifiers without an explicit exception.

**Define deterministic rules precisely.** Exact source cross-reference, trusted issued identifier, or combination of stable attributes can create strong rules.

Qualify namespace, issuer, status, entity type, time, and source authority. Preserve which rule fired and prevent overlapping rules from producing contradictory actions.

**Control probabilistic decisions.** Record training or estimation data, labels, sampling, model, features, transformations, calibration, thresholds, slices, limitations, and approvals.

Monitor population and feature drift. Model updates are policy migrations because they can change identity membership at scale.

**Evaluate candidate coverage.** Match evaluation over admitted candidates can appear excellent while blocking excludes difficult true pairs.

Measure retrieval recall, block sizes, truncated candidates, common-value behavior, latency, and slices separately from comparison and decision quality.

**Evaluate decision quality by consequence.** Estimate false links, missed links, precision, recall, abstention, calibration where relevant, and review disagreement.

Weight high-consequence cases and inspect languages, scripts, regions, sources, sparsity, entity types, and other lawful slices. Aggregate duplicate reduction is not assurance.

**Preserve negative evidence.** Confirmed separate entities, incompatible types, temporal impossibility, revoked identifiers, and reviewed nonmatches can constrain future clustering.

Version negative evidence, scope, authority, reason, and expiry. It can become stale after source correction and therefore must remain reviewable.

**Validate clusters, not only pairs.** A set of individually acceptable edges can create an impossible cluster through transitivity or a glue record.

Check unique-identifier constraints, entity-type compatibility, maximum plausible cardinality, time, relationships, source duplication, and protected business rules before union.

**Control glue records.** A new record that connects two existing entities can merge a large component and amplify one bad signal.

Require stronger evidence, bounded component growth, human approval, or shadow analysis for high-impact merges. Record the causal edge and affected memberships.

**Design review bands from capacity.** A broad review band can improve safety only if qualified reviewers can handle volume within decision deadlines.

Forecast arrival, service time, priority, rework, and incident surge. When queues overload, degrade by abstaining or narrowing automation—not by silently lowering evidence requirements.

**Make review reproducible.** Show permitted original assertions, transformations, comparison signals, contradictions, policy, candidate context, and source provenance.

Capture outcome, rationale, reviewer, approvals, effective interval, confidence if used, and appeal. Sample decisions for quality and disagreement.

**Use overrides as governed assertions.** An override names match edge, cluster, attribute, or source; decision; reason; evidence; requester; approver; scope; effective time; expiry; and precedence.

Expired and unexplained overrides must not live forever. Analyze recurring exceptions as evidence that policy or source contracts need change.

**Distinguish link from merge.** Linking can group records under an entity while retaining each record unchanged. Merge may redirect identifiers, collapse records, change source state, or publish a new master generation.

Choose the least destructive operation that satisfies the decision. Logical linkage is usually easier to reverse and audit than physical consolidation.

**Specify merge semantics.** Define preconditions, targeted entities or records, expected versions, surviving enterprise ID, source identifiers, membership, relationships, assertions, aliases, events, and consumer effects.

“Merge A into B” is insufficient. It must state what becomes authoritative, what remains readable, which writes are allowed, and how correction works.

**Choose surviving identifiers deliberately.** Prefer an existing stable enterprise ID according to policy, or issue a new one when neither prior ID can safely represent the combined history.

Do not choose by smallest number, oldest database row, or arbitrary request order unless that is an intentional stable rule with acceptable consequences.

**Never recycle obsolete IDs.** Retired IDs should resolve to the surviving ID or a typed split or tombstone result during the support period.

Record alias direction, merge operation, effective time, status, and chain. Compress lookup paths without erasing historical transitions.

**Bound alias chains.** Repeated mergers can create long, cyclic, or ambiguous aliases. Validate acyclicity, resolve to current state, and preserve original history.

A split can make one old alias point to several new entities. Return a typed ambiguous result with context rather than choosing one silently.

**Prefer atomic logical merge.** Update cluster membership, current entity pointer, alias map, version, and outbox record in one durable boundary when one store owns them.

External source updates and consumer propagation remain distributed. Use staged workflows, idempotency, reconciliation, and explicit completion instead of claiming global atomicity.

**Use expected-version concurrency.** A merge approved against entity generations 7 and 4 should fail or re-evaluate if either changed before commit.

Otherwise a late merge can erase a split, correction, new member, or steward decision. Return conflict state with refreshed evidence.

**Give every operation stable identity.** `merge_id`, `split_id`, request ID, initiator, policy, target versions, and idempotency key support safe retry and audit.

On unknown outcome, query the operation before resubmitting. A duplicate merge command must not emit a second semantic change.

**Stage cross-system merges.** When source systems must merge their own records, use requested, accepted, applied, confirmed, failed, compensated, and reconciled states.

The master should not claim source completion before acknowledgement. Define timeout, retry, disagreement, manual repair, and cancellation semantics.

**Preserve source records.** Logical consolidation retains each source namespace, ID, version, assertions, and lifecycle even when a master view presents one entity.

Physical deletion belongs to source, retention, privacy, and records policy. “Losing the merge” is not sufficient authority to erase evidence.

**Design unmerge before merge.** Record pre-merge memberships, identifiers, relationships, master versions, selected assertions, consumer generations, and source positions.

Unmerge is not simply deleting an edge after subsequent changes. It may require repartitioning, issuing IDs, remapping facts, and preserving actions legitimately taken while merged.

**Treat split as a correction product.** State which records and relationships move to which entities, which old ID becomes ambiguous or remains with one, and which facts require reassignment.

Publish prior and new versions, reason, effective and correction time, severity, aliases, and affected consumers. Verify downstream completion.

**Separate survivorship from match evidence.** Matching decides membership. Survivorship evaluates eligible assertions after membership for a specific view.

Do not conclude that records match because a golden view selected similar values. If selected outputs become later signals, preserve lineage and guard against self-reinforcing feedback.

**Select at attribute level.** Legal name, delivery address, risk status, contact preference, classification, and relationship can have different authorities and purposes.

Whole-record winner simplifies storage but discards valid assertions and imports one source's weaknesses into unrelated fields.

**Define eligibility before ranking.** Filter assertions by entity membership, attribute semantics, purpose, consent, authorization, effective time, validity, status, and required evidence.

A highly trusted source is not eligible when its value is expired, outside purpose, for a different relationship type, or legally restricted.

**Rank authority before convenience.** Some attributes have a business or legal authority; others are observed, verified, self-asserted, derived, or curated.

Document who may originate, validate, correct, override, expire, and delete each attribute. Central storage does not grant semantic authority.

**Use recency with explicit clocks.** Source modification, observation, verification, effective, ingestion, and processing time answer different questions.

Latest arrival can be an old replay. Latest source timestamp can come from a skewed clock. Select the time dimension that matches attribute meaning and break ties deterministically.

**Use quality with provenance.** Validity, completeness, accuracy estimates, verification, and confidence can inform selection when their definitions and evidence are comparable.

Do not turn a generic quality score into universal precedence. Preserve component evidence and policy version.

**Handle multiplicity.** Addresses, names, roles, classifications, contacts, identifiers, and relationships can have several simultaneous valid values with types and intervals.

Survivorship may return a governed set plus a preferred member for one purpose. It need not reduce every attribute to a scalar.

**Preserve exceptional states.** Unknown, not collected, withheld, disputed, invalid, expired, source unavailable, and not applicable affect eligibility and consumer meaning differently.

A missing high-priority assertion does not automatically authorize a lower-priority value. Policy must state fallback and whether the result is provisional.

**Compose only with semantics.** Concatenation, union, average, minimum, maximum, or frequency can be legitimate for specific fields, not generic survivorship recipes.

Never average identifiers, choose a frequent false value, concatenate incompatible classifications, or union relationships without deduplication and authorization.

**Keep nonselected assertions.** Record source, original value, normalization, time, quality, status, purpose, policy, and selection or exclusion reason.

Retention and access rules may limit availability, but logical survivorship alone should not erase disagreement or evidence needed for correction.

**Version golden views.** A master view version binds identity generation, eligible assertion set, reference-data versions, survivorship policy, overrides, and selected or composed results.

Changing selection rules can change outputs even when no source changes. Publish a new generation and preserve the old explanation.

**Publish match and merge events carefully.** Candidate-created, reviewed, linked, merged, split, alias-changed, and corrected events have different meanings and audiences.

Include operation and entity versions, prior and new IDs, effective time, cause, ordering key, idempotency key, schema, and protection classification.

**Publish survivorship changes separately when useful.** Identity membership can remain stable while a preferred value changes, and a merge can occur without changing a consumer's projected attributes.

Separate event types reduce false coupling. Consumers subscribe to identity, attribute, or relationship changes they actually require.

**Define consumer write behavior.** A source correction should update its assertion, not overwrite the golden field directly unless that source owns it.

Commands target source or master authority with expected versions. Prevent a consumer from turning a purpose-specific view into a new authoritative source.

**Prevent feedback loops.** Tag published values with origin entity generation, survivorship version, and propagation purpose.

If a source re-emits a master-selected value, do not count it as independent corroboration or newer authority. Detect and suppress echoes.

**Control out-of-order work.** Delayed source changes, match jobs, review cases, merges, and events can arrive after newer decisions.

Compare expected entity and policy versions, source positions, and effective time. Re-evaluate or supersede stale work rather than applying it blindly.

**Pin reprocessing inputs.** Reproduction requires source assertions, transformations, candidate rules, reference data, model, thresholds, match policy, overrides, merge history, and survivorship rules.

A current-policy replay is a proposed migration. Run it in isolation, compare clusters and views, and plan review capacity before cutover.

**Reconcile state at several layers.** Check source coverage, candidate jobs, decision counts, cluster membership, alias resolution, operation states, selected values, event positions, consumer acknowledgements, and derived products.

Use keyed evidence to localize drift. A matching row count can hide swapped identities or different surviving assertions.

**Contain bad merges quickly.** Freeze unsafe fan-out, preserve evidence, identify affected identities, attributes, decisions, and consumers, and route critical operations to safe alternatives.

Correct cluster state, aliases, golden views, caches, indexes, events, models, reports, and source coordination. Confirm consumer repair rather than closing on publisher success.

**Protect all derived surfaces.** Comparison values, scores, negative edges, duplicate candidates, merge history, alias maps, source linkage, golden records, reviewer notes, and audit can reveal sensitive facts.

Apply purpose, minimization, access, encryption, isolation, export limits, retention, deletion, and monitoring by consequence. Review tools need special attention because they assemble broad evidence.

**Threat-model automation and workflow.** Attackers may create glue records, reuse identifiers, poison values or labels, manipulate clocks, enumerate candidates, trigger merges, steal review access, or exploit retries.

Authenticate sources and commands, validate inputs, rate-limit, separate duties, protect secrets and models, monitor component growth and anomaly, and rehearse correction.

**Engineer service objectives.** Define match throughput, decision latency, review age, merge completion, propagation, correction time, alias lookup, freshness, availability, and recovery.

Observe by domain, source, policy, score band, decision state, operation state, component size, survivorship reason, consumer, and slice. Aggregate uptime hides unsafe queues.

**Design degraded behavior by risk.** If comparison features are stale, a workflow may abstain, use strong deterministic evidence only, queue review, or stop.

Do not lower thresholds or reuse an old golden view silently to maintain nominal availability. Expose degraded state and reconcile after recovery.

**Recover policy and evidence.** Restore source positions, assertions, transformations, candidate indexes, models and rules, decisions, cluster generations, aliases, merge and split operations, overrides, survivorship, queues, events, permissions, and audit.

Test restoration in isolation and compare representative identities and values. A backup of the current golden table cannot explain or reverse prior decisions.

**Assign ownership at each decision.** Domain owners define entity and attribute meaning; match-policy owners approve evidence and thresholds; merge owners approve state transitions; attribute owners define survivorship.

Stewards, source owners, platform, privacy, security, legal, records, reliability, consumers, incident commanders, and retirement owners retain their accountable parts.

**Measure outcome, harm, and cost.** Track false-link and missed-link consequences, abstention, candidate coverage, review disagreement, queue age, merge and split frequency, overrides, corrections, propagation, consumer outcomes, incidents, and cost.

Duplicate reduction and field completeness are intermediate signals. A wrong complete golden record can be worse than an unresolved honest one.

**Plan migration and retirement.** Inventory policies, models, thresholds, source assertions, decisions, clusters, IDs, aliases, operations, views, APIs, events, files, consumers, cases, credentials, histories, backups, and duties.

Transfer authority and resolution behavior before stopping work. Verify that old jobs, delayed reviews, caches, packages, and restore procedures cannot recreate retired merges or survivorship outputs.

## Definitions and Notation

For candidate records $r_i,r_j$, let match evidence $\gamma_{ij}$ contain versioned comparison signals, negative constraints, provenance, and missingness. Match policy produces:

$$
d_{ij}=Match(\gamma_{ij},scope,purpose,policy)\in\{match,review,nonmatch,insufficient,prohibited\}.
$$

Let merge transition $\mu=(op,E_a^p,E_b^q,E_c^{q+1},A,H,t)$ contain stable operation ID, expected prior entity versions, resulting entity version, alias mapping $A$, transition history $H$, and effective time $t$.

For attribute or relationship $k$ and use $u$, survivorship operates on eligible assertions:

$$
G(k,u)=Survive(Eligible(A,k,u,t),Authority,Verification,Time,Quality,Policy).
$$

The result can be a selected assertion, governed set, composed value with lineage, or typed unresolved state. Nonselected assertions remain outside $G$ but inside retained evidence according to policy.

Let expected decision loss be $L=c_{FL}N_{FL}+c_{ML}N_{ML}+c_RN_R+c_CC$, covering false links, missed links, reviews, and delayed or blocked cases. Costs require empirical and accountable justification.

Define `FitMerge(M,u,t)` as a review predicate requiring scoped and evaluated matching, authorized and reversible transitions, stable identifiers, assertion-preserving survivorship, protected publication, reliable correction, accountable outcomes, and lifecycle closure for use $u$ at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Name entity decisions, population, purpose, false-link and missed-link harms, deadlines, fallback, value, and assurance depth.

**2. Match gate.** Define candidates, signals, negative evidence, model or rules, thresholds, margins, states, evaluation, review band, and version.

**3. Cluster gate.** Validate pair interactions, glue records, transitivity, unique constraints, component growth, entity type, time, and negative edges.

**4. Merge gate.** Define authority, preconditions, expected versions, operation identity, surviving ID, memberships, relationships, aliases, source coordination, and idempotency.

**5. Reversal gate.** Preserve prior state, unmerge and split semantics, tombstones, affected facts, correction events, consumer impact, and acknowledgement.

**6. Survivorship gate.** Separate eligibility and ranking; define attribute authority, time, verification, quality, purpose, consent, multiplicity, fallback, and unresolved states.

**7. Evidence gate.** Retain source assertions, transformations, comparisons, policies, decisions, overrides, selection reasons, history, provenance, and audit.

**8. Publication gate.** Contract APIs, events, snapshots, consistency, ordering, replay, feedback suppression, reconciliation, correction, and consumer writes.

**9. Protection and service gate.** Bound linkability, access, integrity, queue and component capacity, degraded behavior, incidents, recovery, retention, and deletion.

**10. Lifecycle gate.** Assign ownership, measure outcome and harm, manage policy migration, transfer authority, migrate consumers, and verify retirement.

Passing these gates supports a declared decision context. It does not make a score certain, a merge irreversible, a selected value universally true, or a policy safe for another population or purpose.

### Executable evidence

The executable example keeps match, logical merge, and contact survivorship as separate versioned decisions while preserving both source assertions.

<!-- bijux-verify: {"id":"match-merge-survivorship-separation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"match_score=9\nmatch_decision=auto_link\nmatch_policy=4\nmerge_id=merge-501\nsurviving_entity=entity-100\nsource_identifiers=2\nselected_email=verified@example.test\nselected_source=crm\nassertions_preserved=2\nsurvivorship_policy=3\n","stderr":""}} -->
```python
records = [
    {
        "source_id": "crm:17",
        "email": "verified@example.test",
        "verified": True,
        "observed_day": 5,
    },
    {
        "source_id": "billing:82",
        "email": "newer@example.test",
        "verified": False,
        "observed_day": 8,
    },
]

match_score = 6 + 3  # scoped verified identifier plus normalized email evidence
match_decision = "auto_link" if match_score >= 8 else "review"
source_identifiers = {record["source_id"] for record in records}
selected = max(records, key=lambda record: (record["verified"], record["observed_day"]))

print(f"match_score={match_score}")
print(f"match_decision={match_decision}")
print("match_policy=4")
print("merge_id=merge-501")
print("surviving_entity=entity-100")
print(f"source_identifiers={len(source_identifiers)}")
print(f"selected_email={selected['email']}")
print(f"selected_source={selected['source_id'].split(':')[0]}")
print(f"assertions_preserved={len(records)}")
print("survivorship_policy=3")
```

The result proves only the declared arithmetic, threshold branch, identifier count, ordering, and assertion count for two in-memory records. It does not prove identity, identifier validity, source authority, email ownership, score calibration, merge authorization, survivorship fitness, consent, production atomicity, propagation, protection, recovery, or consumer safety.

## Alternatives and Trade-Offs

**Link without physical merge.** Source records remain independent under one entity, improving reversibility and provenance while increasing query and storage complexity.

**Physical merge.** One stored record simplifies some systems but risks lost evidence, source disagreement, difficult unmerge, and ambiguous correction.

**Automatic high-confidence match.** Low latency and scale improve when evidence is strong; a small false-link rate can still create severe harm and wide propagation.

**Human-approved merge.** Judgment and extra evidence can reduce some errors, but queues, inconsistency, privacy exposure, fatigue, and cost limit use.

**Survive one whole record.** Implementation is simple and internally consistent, but good values in other sources disappear and one source's authority is overstated.

**Attribute-level survivorship.** Authority and purpose fit improve, at the cost of more metadata, rules, provenance, testing, and consumer explanation.

**Persist a golden copy.** Reads are fast and coherent; invalidation, history, correction, and replay need robust operation.

**Compose a virtual view.** Current source values and lineage remain visible; availability, latency, consistency, and repeated rule execution become dependencies.

**Use source priority.** Rules are understandable and stable but can ignore attribute-specific expertise and source quality changes.

**Use verification and quality.** Evidence-sensitive choice can improve fitness, but quality definitions, comparability, gaming, and missingness require governance.

**Use recency.** Fresh values win simply when clocks match semantics; replay, skew, observation differences, and expired assertions can make it unsafe.

**Immediate propagation.** Consumers converge quickly, but failures amplify and rollback after new facts may be impossible. Versioned cohort adoption contains risk while extending inconsistency.

Choose by consequence, evidence, reversibility, source authority, temporal semantics, multiplicity, consumer needs, latency, protection, review capacity, economics, and exit.

## Failure Modes and Misconceptions

1. **Match, merge, and survivorship are one operation.** They answer different questions under different authority.
2. **A score above threshold proves sameness.** It triggers a scoped policy action under bounded evidence.
3. **One threshold fits every use.** Error losses, populations, and reversibility differ.
4. **Pairwise matches guarantee a valid cluster.** Transitivity and glue records can create contradictions.
5. **Review means safe.** Reviewers face evidence, policy, bias, fatigue, access, and capacity limits.
6. **Merge means delete the loser.** Logical linkage can preserve every source representation.
7. **The oldest or smallest ID should survive.** Identifier continuity needs explicit consumer and lifecycle policy.
8. **Aliases can be forgotten after cutover.** Historical facts and late consumers may still use them.
9. **Unmerge restores the past automatically.** Later facts and decisions require explicit repartition and correction.
10. **One source is best for every field.** Authority and quality vary by attribute, purpose, and time.
11. **Latest means most accurate.** Clock, observation, verification, effective time, and replay matter.
12. **Completeness means correctness.** A complete value can be invalid or unauthorized.
13. **Survivorship needs one scalar.** Valid multiplicity and unresolved states can be the correct result.
14. **Nonselected values can be discarded.** They support explanation, correction, and new policies.
15. **Golden values are safe matching labels.** Feedback can make earlier policy appear self-confirming.
16. **A successful merge request means all systems merged.** Distributed source and consumer completion requires acknowledgement.
17. **Replay reproduces the master.** Changed inputs, policies, models, overrides, and order can change results.
18. **Duplicate reduction proves value.** Outcome, harm, correction, adoption, and cost determine value.
19. **Turning off matching retires the capability.** IDs, aliases, histories, views, cases, consumers, and duties remain.

## Worked Examples

### Example 1

Scores above 0.90 auto-link low-consequence newsletter profiles, while benefit accounts require verified identifier evidence and review. **Conclusion:** threshold policy follows decision harm, not one model scale.

### Example 2

A new record links two clusters of fifty records through one shared office phone. Component-growth and common-value rules block automatic union. **Conclusion:** cluster impact constrains pair evidence.

### Example 3

A steward approves a match, but one entity changed before commit. Expected-version control returns conflict and refreshes the case rather than applying stale membership. **Conclusion:** review approval does not suspend concurrency.

### Example 4

Two records link logically under `entity-100`; both source IDs remain active and no source row is deleted. **Conclusion:** identity consolidation need not be physical destruction.

### Example 5

After repeated mergers, three obsolete IDs resolve through one bounded alias index to the surviving ID while the full operation chain remains in history. **Conclusion:** fast current resolution and detailed provenance can coexist.

### Example 6

A false merge is split after orders were placed using the combined ID. The correction partitions memberships, flags ambiguous historical orders for review, publishes new IDs, and verifies consumer repair. **Conclusion:** unmerge includes downstream facts, not only edges.

### Example 7

CRM provides a verified older email and billing a newer unverified one. Contact policy selects CRM while retaining billing for investigation. **Conclusion:** verification can outrank recency without erasing disagreement.

### Example 8

A person has simultaneous residence and correspondence addresses. The master retains both with type and interval; a mailing view prefers correspondence. **Conclusion:** survivorship can return a set plus a purpose-specific preference.

### Example 9

A coexistence source echoes a golden phone value back to the hub. Origin and generation metadata prevent the echo from counting as independent confirmation. **Conclusion:** feedback suppression protects evidence quality.

### Example 10

The matching service has no live requests, yet unresolved cases, alias lookups, annual bulk files, model features, and backup restores remain. **Conclusion:** lifecycle closure requires more than traffic cessation.

## Cross-Program Connections

- **Data engineering:** source contracts, standardization, candidate generation, incremental joins, cluster state, assertion histories, events, snapshots, reconciliation, replay, and deletion implement the pipeline.
- **Platform engineering:** search, graph, workflow, model serving, transaction boundaries, outbox delivery, policy, observability, recovery, and safe deployment support operation.
- **API and service engineering:** expected versions, idempotency, operation resources, typed states, aliases, events, correction, pagination, and deprecation shape contracts.
- **Security engineering:** source and command authenticity, identifier abuse, glue records, reviewer privilege, enumeration, integrity, secret protection, and incident containment affect trust.
- **Privacy engineering:** linkability, purpose, minimization, derived sensitivity, consent, access, explanation, retention, deletion, and split correction constrain processing.
- **Machine learning:** retrieval, comparison, labels, calibration, thresholds, slice evaluation, drift, abstention, feedback loops, and human review require evidence.
- **Organizational design:** domain, match, merge, attribute, source, steward, consumer, and incident decision rights determine real authority.
- **Reliability engineering:** hot blocks, queues, concurrency, stale work, fan-out, backpressure, unknown outcomes, recovery, replay, and correction time define service.
- **Economics and decision science:** asymmetric errors, review capacity, delay, reversibility, value of information, propagation cost, and exit cost guide policy.
- **Systems engineering:** stakeholder outcomes, boundaries, hazards, configuration control, assurance, change impact, lifecycle, and verification connect the whole system.

## References

1. U.S. Census Bureau, *Statistical Quality Standard C4: Linking Data Records*. <https://www.census.gov/about/policies/quality/standards/standardc4.html>
2. U.S. Census Bureau, *Overview of Record Linkage and Current Research Directions*. <https://www.census.gov/library/working-papers/2006/adrm/rrs2006-02.html>
3. IBM, *Matching Algorithms in IBM Master Data Management*. <https://www.ibm.com/docs/en/ws-and-kc?topic=data-matching-algorithms-in-match-360>
4. IBM, *Survivorship*. <https://www.ibm.com/docs/en/imdm/14.0.0?topic=data-survivorship>
5. IBM, *Deciding on Criteria for Data Survivorship*. <https://www.ibm.com/docs/en/imdm/12.0.0?topic=data-deciding-criteria-survivorship>
6. IBM, *Merging Records*. <https://www.ibm.com/docs/en/imdm/12.0.0?topic=assignment-merging-records>
7. W3C, *PROV-O: The PROV Ontology*. <https://www.w3.org/TR/2013/REC-prov-o-20130430/>
8. NIST, *Privacy Framework*. <https://www.nist.gov/privacy-framework/privacy-framework>
9. NIST, *Artificial Intelligence Risk Management Framework*. <https://www.nist.gov/itl/ai-risk-management-framework>
10. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design match, merge, and survivorship architecture for a party, supplier, product, device, or organization domain. Define policies, states, thresholds, review, merge semantics, identifiers, reversal, attribute selection, publication, protection, operation, ownership, and lifecycle.

### Exercise 2

A match system has good pairwise precision, but one glue record would merge two clusters containing 40 and 70 records. Design the automatic and reviewed decision controls.

### Exercise 3

CRM, billing, fulfillment, and compliance disagree on legal name, shipping address, contact preference, and risk status. Design eligibility and survivorship without one global source priority.

### Exercise 4

A policy replay proposes 18,000 merges and 4,000 splits while live source updates and steward decisions continue. Design containment, comparison, cutover, correction, and rollback.

### Exercise 5

An organization plans to retire its centralized matching and survivorship capability after moving master products to domains. Define evidence that all functions and obligations transferred or ended.

## Answers to the Exercises

### Answer 1

Define entity type, population, purpose, source coverage, time, consumers, and false-link and missed-link consequences. Separate candidate generation, comparison, policy decision, merge transition, and survivorship. Specify deterministic and statistical evidence, negative constraints, upper and lower thresholds, margins, typed states, evaluation slices, review capacity, reviewer evidence, overrides, and versioning. Validate cluster constraints and large-component effects before automatic union.

Prefer logical linkage unless physical merge has explicit source, retention, and reversal authority. Use stable operation IDs, expected entity versions, idempotency, a deliberate surviving ID, nonrecycled aliases, temporal memberships, and designed split semantics. Define attribute-level eligibility and ranking by authority, verification, effective time, quality, purpose, consent, multiplicity, and fallback while preserving every permitted assertion. Publish versioned APIs, events, and snapshots with feedback suppression, reconciliation, correction, and acknowledgement. Protect every linkage and review surface, recover policy and evidence, assign accountable owners, measure outcome and harm, and verify retirement dependencies.

### Answer 2

Treat component growth as part of policy, not a side effect of pairwise scoring. Inspect which edge makes the connection, its signals, common values, source provenance, negative constraints, entity types, time, and unique identifiers. Recompute pair evidence and validate the proposed 110-record cluster for contradictions, duplicate source identities, implausible cardinality, and protected business constraints. A shared office phone, address, or default value should not establish identity merely because it connects many pairs.

Set lower automatic size limits or require stronger evidence and margin as impact grows. Run the proposed membership change in shadow state, calculate affected source records, master views, consumers, and false-link loss, and send a focused case to a qualified reviewer with dual approval if consequence warrants it. Use expected cluster versions so live changes invalidate stale approval. If accepted, publish one idempotent versioned merge with aliases and monitor propagation. If unresolved, preserve separate clusters and the candidate edge. Record the decision and sample it in ongoing evaluation.

### Answer 3

Define semantics and authoring authority per attribute. Compliance or a legal registry may originate verified legal name and risk status; fulfillment may own the effective shipping address for an order; the subject's consent workflow may own contact preference; billing may own invoice address but not general residence. Filter first by entity membership, purpose, consent, attribute type, effective interval, validity, and evidence. Then rank eligible assertions by declared authority, verification, relevant time, and quality—not arrival order.

Retain original and normalized assertions, source and observation time, verification, dispute state, policy, and exclusion reason. Legal name may select one verified assertion with an unresolved state during conflict. Addresses remain a typed temporal set with purpose-specific preference. Contact preference may return prohibited or withheld when consent is absent. Risk status can fail closed when its authoritative feed is stale rather than fall back to CRM. Publish a purpose-limited view with identity and survivorship generation, provenance, freshness, and correction channel. Never use the golden output as independent match evidence without explicit lineage and feedback control.

### Answer 4

Pin source snapshots and positions, transformations, candidate rules, reference data, model and features, thresholds, match policy, negative edges, overrides, prior cluster generations, merge history, and survivorship rules. Run reprocessing in an isolated namespace. Compare candidate coverage, score distributions, false-link and missed-link estimates, slices, membership and alias changes, golden attributes, review volume, high-consequence consumers, resource demand, and protection impact. Blind-review representative and risky changes.

Capture live source and review changes at a declared boundary and apply or reconcile them to the candidate generation with expected versions. Cut over by atomic generation or controlled cohorts with stable operation IDs, idempotent events, old-to-new aliases, rate-limited propagation, monitoring, and consumer acknowledgement. Preserve the old read path and exact evidence. Rollback must account for facts created under new identities; some cases require forward split or merge corrections rather than reverting a pointer. Block delayed jobs and stale approvals from overwriting the chosen generation, and close after keyed membership and attribute reconciliation.

### Answer 5

Inventory every entity domain, source, assertion history, transformation, candidate index, rule, model, threshold, negative decision, override, cluster, merge and split operation, stable ID, alias, tombstone, survivorship rule, golden view, API, event, snapshot, cache, consumer, report, model feature, review and appeal case, credential, backup, retention and deletion path, and incident duty. Map each semantic and operational capability to a receiving domain service with verified authority, contract, protection, service objective, recovery, funding, and escalation—or prove it is no longer required.

Run old and new capabilities in bounded comparison, migrate consumers by cohort, preserve historical identity resolution, and reconcile memberships, aliases, selected values, corrections, and downstream decisions. Include seasonal, offline, manual, and disaster-recovery dependencies. Stop new matches and merges only after authority transfer; close or move queues and appeals; revoke access; remove prohibited linkage copies; retain required provenance under named custody; and exercise correction and recovery without the old platform. Test that delayed reviews, old jobs, packages, caches, and backup restoration cannot recreate retired identity or survivorship state before accountable closure.
