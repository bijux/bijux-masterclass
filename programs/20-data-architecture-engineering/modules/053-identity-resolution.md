---
module_id: DARCH-053
program: Data Architecture Engineering
level: 2
module_number: 53
title: Identity Resolution
status: complete
last_verified: 2026-09-03
---

# Identity Resolution

## One-Page Review

### Governing question

How should an enterprise decide whether records, identifiers, claims, accounts, devices, organizations, products, locations, or other representations refer to the same scoped entity while preserving uncertainty, provenance, privacy, correction, and accountability?

### Essential definitions

- **identity resolution** is the governed process of deciding whether two or more representations correspond to the same entity within a declared population, entity type, purpose, time, and evidence policy.
- An **entity** is the scoped subject the architecture intends to distinguish, such as a legal person, customer account, organization, product, device, household, or facility.
- A **record** is one source's representation or assertion about an entity; it is not the entity itself.
- An **identifier** is a value issued in a namespace to refer to a subject; possession of the same string does not prove common identity outside that namespace and lifecycle.
- A **source identity** is the identifier and record history maintained under one source system's authority.
- A **candidate pair** is a pair of records admitted for comparison; candidate generation reduces work but can exclude true matches.
- A **comparison signal** is an observed agreement, disagreement, relationship, or evidence feature used by a resolution policy.
- A **link decision** states linked, not linked, unresolved, or another governed state with scope, policy, evidence, version, time, and decision provenance.
- An **identity cluster** is a versioned set of source records currently judged to represent one scoped entity.
- A **cross-reference** maps an enterprise entity identifier to source namespace and identifier over a declared interval.
- A **false link** joins different entities; a **missed link** leaves the same entity separated. Their harms are context-dependent and asymmetric.
- **identity proofing** establishes assurance about a claimed identity; **authentication** confirms control of an authenticator; **authorization** decides permitted action. None is interchangeable with enterprise record linkage.

### Central model, mechanism, or theorem

Represent identity-resolution architecture as:

`I = (outcomes, scope, entities, sources, assertions, identifiers, candidates, signals, policy, decisions, graph, publication, protection, service, ownership, evidence, lifecycle)`

Resolution is a versioned decision under bounded evidence, not discovery of an unqualified natural identity. A person can legitimately have separate customer, employee, patient, beneficiary, household, and digital-persona identities. The same records can be linked for fraud investigation and kept separate for marketing because purpose, authority, protection, error cost, and population differ. Preserve source records, candidate evidence, policy version, decisions, reviews, and corrections so a cluster can be explained and reversed.

### Critical invariants

- Every resolution domain states entity type, population, purpose, excluded uses, time, consumers, consequences, and accountable owner.
- Source identifiers remain qualified by namespace, issuer, entity type, status, and lifecycle; they are not treated as global proof.
- Original assertions and transformation provenance survive normalization, comparison, linking, unlinking, merge, split, and retirement.
- Candidate generation is evaluated for missed-link risk, scale, skew, and protected-group effects, not only runtime.
- Signals have declared semantics, provenance, availability, quality, time, and permitted use.
- Decisions expose policy or model version, evidence, confidence where meaningful, threshold or rule, outcome, reviewer, and effective interval.
- Linked, not linked, unresolved, pending review, prohibited, and insufficient evidence remain distinct.
- Enterprise entity identifiers are stable within scope, never recycled, and maintain temporal source cross-references.
- False-link and missed-link harms, review capacity, correction time, and downstream propagation shape policy.
- Linkage keys, graphs, features, clusters, review cases, exports, histories, and backups receive protection proportional to linkability and consequence.
- Publication covers APIs, events, bulk, cache, aliases, consistency, correction, reconciliation, recovery, and consumer acknowledgement.
- Retirement closes decisions, feeds, identifiers, cross-references, models, indexes, queues, consumers, retained evidence, and obligations.

### Common failures

Common failures are defining identity as a name and birth date; using one customer ID across unrelated scopes; assuming shared government identifiers are infallible; treating authentication as proof that two source records are the same person; normalizing away cultural or source meaning; blocking only on exact values without measuring excluded matches; training on convenient labels; interpreting a score as probability without calibration; optimizing aggregate accuracy despite catastrophic false links; forcing ambiguous pairs into match or nonmatch; taking transitive closure without checking contradictions; silently merging clusters; recycling entity IDs; discarding negative and unresolved evidence; exposing linkage graphs broadly; using production outcomes as unbiased ground truth; replaying with new rules into live identity; measuring only match rate; and shutting down the resolver while consumers, aliases, or retained link decisions remain.

### Compact example

Two candidates are compared with a source record. Initially the leading candidate scores 5 and the runner-up scores 4, so the one-point margin is insufficient and policy returns `review`. A verified source-identifier assertion raises the leading candidate to 9 without changing the runner-up, so the governed result becomes `linked`. Both candidates, signals, scores, policy version, and the before-and-after decisions remain preserved. The example demonstrates bounded policy behavior, not that the records concern the same real entity.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-051](051-master-data-and-golden-records.md), and [DARCH-052](052-reference-data.md) establish time, ownership, product, master, and reference boundaries. This module establishes resolution architecture; [DARCH-054](../ROADMAP.md) next deepens match, merge, and survivorship policy.

## Governing Question

Organizations accumulate separate representations because systems serve different processes, identifiers are local, attributes change, values are missing or erroneous, and people or organizations legitimately present different identities in different contexts. Joining every similar record creates dangerous false links; keeping every record separate produces duplicated service, fraud blind spots, fragmented compliance, and contradictory analysis.

The governing question is not “which tool finds duplicates?” It is which scoped decision process produces enough evidence to link or separate representations for a named use, contains harms when evidence is weak, protects the increased linkability it creates, and remains correctable through change, failure, migration, and retirement.

## Why This Matters

The U.S. Census Bureau's [Overview of Record Linkage and Current Research Directions](https://www.census.gov/library/working-papers/2006/adrm/rrs2006-02.html) describes record linkage as associating records from different files with the same entity. Its [Statistical Quality Standard C4](https://www.census.gov/about/policies/quality/standards/standardc4.html) requires accurate linkage processes, documentation, evaluation, review, and protection. The Census paper [Methods for Record Linkage and Bayesian Networks](https://www.census.gov/content/dam/Census/library/working-papers/2002/adrm/rrs2002-05.pdf) develops comparison-based statistical reasoning. These sources inform mechanisms; local architecture must still define entity, population, purpose, loss, and evidence.

NIST [SP 800-63A](https://pages.nist.gov/800-63-4/sp800-63a.html) separates identity resolution, evidence validation, and verification within identity proofing and requires risk-based evidence and process records. That usage concerns digital identity proofing. Enterprise data architecture often resolves records for parties, products, suppliers, or devices without enrolling a digital subscriber, so terminology and assurance claims must remain scoped.

W3C [Decentralized Identifiers](https://www.w3.org/TR/did-core/) distinguishes identifier, subject, controller, document, resolution, and correlation risk. W3C's [Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/) distinguishes issuer, holder, verifier, subject, and claims and warns that verifying credential integrity does not by itself establish the truth of every claim. Identifier control, credential integrity, real-world identity, and record linkage are different judgments.

W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) supplies a provenance vocabulary. The NIST [Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework) addresses privacy risk, the NIST [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) addresses trustworthy risk management for AI systems, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames lifecycle engineering of trustworthy systems. Identity resolution combines evidence, decision systems, sensitive linkability, and long-lived operational consequence.

## Prerequisites and Retrieval

You should understand data models, identifiers, namespaces, source authority, temporal modeling, master and reference data, data quality, APIs, events, graphs, probability basics, classification errors, privacy, security, lineage, reliability, recovery, and governance.

Retrieve entity, representation, record, assertion, identifier, namespace, issuer, population, entity type, purpose, source identity, cross-reference, normalization, candidate generation, blocking, comparison, signal, feature, deterministic rule, probabilistic score, threshold, margin, calibration, candidate pair, linked, not linked, unresolved, cluster, graph, false link, missed link, review, override, merge, split, provenance, propagation, reconciliation, and retirement.

As a retrieval test, inspect “deduplicate all customers.” Ask what customer means, which legal and account boundaries apply, the population and time window, sources and identifiers, permitted purpose, evidence and missingness, false-link and missed-link harms, protected groups, decision states, review capacity, downstream consumers, correction deadline, protection, recovery, and exit conditions. Without those answers, a duplicate count has no stable interpretation.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish entity identity, source record, identifier, claim, credential, account, proofing, authentication, authorization, and master representation;
2. frame resolution from entity type, population, purpose, time, authority, consequences, and consumer decisions;
3. model source assertions, qualified identifiers, transformations, candidates, signals, decisions, clusters, and provenance;
4. compare deterministic, probabilistic, graph-assisted, human-reviewed, and privacy-preserving approaches without overstating assurance;
5. design candidate generation, decision states, thresholds, review queues, stable IDs, and reversible correction boundaries;
6. evaluate false links, missed links, abstention, calibration, slice behavior, temporal drift, and downstream decision cost;
7. publish identity and cross-reference products through APIs, events, and bulk contracts with compatible correction semantics;
8. control linkability, access, purpose, minimization, retention, deletion, abuse, and incident scope;
9. operate resolution through change capture, replay, reconciliation, monitoring, recovery, migration, and degraded modes; and
10. assign accountable ownership and measure decision value, harm, queue health, adoption, cost, and closure.

## Core Exposition

**Start with an entity question.** State what kind of thing the system intends to distinguish and why. “Person,” “customer,” and “organization” are not sufficiently precise without institutional scope.

A legal person can hold several accounts; a household can contain several people; an organization can have subsidiaries and establishments. A resolution domain must not collapse these types for convenience.

**Define the population.** Specify geography, jurisdiction, source systems, time interval, eligibility, lifecycle states, and expected scale.

Attributes that are distinctive in one population may be common in another. Thresholds and candidate strategies learned on current active customers may fail for historical, international, or sparse records.

**Declare purpose and prohibited reuse.** Resolution for benefit delivery, fraud investigation, customer support, research, marketing, and safety can justify different evidence and error tradeoffs.

A link approved for one purpose is not automatically authorized or fit for another. Store purpose and policy with the decision rather than treating the cluster as universal fact.

**Distinguish entity from record.** A source record is a versioned representation produced by a process. The same entity can have several records, and one record can contain mixed, stale, or disputed assertions.

Do not use a preferred record as the definition of the entity. Preserve source identity and history even after linking.

**Qualify identifiers.** Model namespace, issuer, entity type, value, creation event, status, aliases, effective interval, revocation, and non-reuse.

Equal strings from different namespaces need not identify the same subject. Different identifiers can legitimately identify the same entity, different roles of one entity, or related but distinct entities.

**Separate identifier control from subject identity.** A user may authenticate control of an account or cryptographic key. That evidence does not by itself prove another account, record, or real-world person is identical.

Conversely, records can be resolved to one organization without any actor authenticating. Record linkage, proofing, authentication, and authorization need explicit boundaries.

**Treat claims as assertions.** Record who asserted an attribute, about which subject identifier, under which process, at what effective and observation time, with what validation and provenance.

A signed credential can establish integrity and issuer but the relying decision still evaluates issuer authority, subject binding, status, meaning, time, and fitness.

**Inventory identity sources.** Include systems of record, operational accounts, registries, credentials, documents, events, directories, partner feeds, vendor data, derived features, manual cases, and consumer corrections.

For each source, record population coverage, authority, identifiers, collection process, time, quality, errors, missingness, protection, permitted use, availability, correction, and deletion behavior.

**Model source assertions before standardizing.** Keep original value, source record, field meaning, locale, script, formatting, effective time, observation time, and status.

Normalization produces a derived comparison value with a transformation version. It does not silently replace the assertion from which it came.

**Normalize cautiously.** Case folding, whitespace removal, transliteration, address parsing, phone formatting, nickname expansion, and reference mapping can improve comparison.

They can also erase cultural, linguistic, geographic, or temporal distinctions. Retain originals and record errors, ambiguity, locale, and rule version.

**Separate candidate generation from decision.** Candidate generation identifies plausible pairs or groups so comparison remains computationally feasible. The decision policy evaluates admitted candidates.

If blocking excludes a true counterpart, even a perfect matcher cannot recover it. Evaluate candidate recall and slice behavior separately from decision accuracy.

**Design blocking keys by evidence.** Exact email, phonetic name plus region, address token, source identifier, time window, or learned retrieval may create candidate sets.

Use multiple passes when one key is brittle. Monitor common-value blocks, adversarial collisions, missing keys, skew, cost, and protected or underrepresented populations.

**Control candidate explosion.** Common surnames, shared addresses, default phone numbers, business contact points, or corrupted identifiers can create huge blocks.

Cap, partition, or reroute pathological cases without silently declaring nonmatches. Record truncation as insufficient evidence and expose queue or recall effects.

**Define comparison signals.** Signals can cover exact identifiers, edit similarity, token overlap, dates, addresses, geospatial proximity, relationships, source compatibility, temporal consistency, and contradictions.

Each signal needs semantic meaning, transformation, provenance, availability, time, reliability, permitted purpose, and known failure modes.

**Preserve disagreement.** Exact name agreement can be weak in a common-name population. Birth-date disagreement can reflect error, approximation, calendar conversion, or different people.

Do not turn every missing or disagreeing value into negative evidence. Model missing, invalid, withheld, not applicable, and contradictory states separately.

**Use deterministic rules deliberately.** Rules such as exact trusted source identifier plus compatible entity type can be transparent, fast, and easy to audit.

Rules can become brittle across sources and populations. Version them, test overlaps and precedence, preserve which clause fired, and route exceptions rather than accumulating undocumented patches.

**Use probabilistic methods deliberately.** Statistical approaches combine evidence based on how agreements behave among matches and nonmatches. Scores support ranking or decisions only under the population and evaluation for which they are valid.

A raw score is not automatically a calibrated probability. Record model, training and label provenance, feature versions, population, threshold, and evaluation evidence.

**Use learned embeddings cautiously.** Representations can retrieve candidates or compare complex text and images, but introduce training dependence, opacity, drift, scale, and adversarial risk.

Do not treat semantic similarity as identity. Test languages, scripts, sparsity, common names, rare entities, image conditions, and manipulated inputs.

**Use graphs carefully.** Records and identifiers can form nodes connected by evidence-bearing link decisions. Graphs support relationships, cluster inspection, and incremental change.

Transitive closure is not universally valid. If A links B and B links C weakly, A and C may contradict. Preserve edge evidence and apply cluster-level constraints before union.

**Model negative evidence.** Mutually exclusive identifiers, incompatible entity types, impossible time overlap, confirmed separate subjects, or steward decisions can prohibit a link.

Negative decisions need provenance, scope, expiry, and review because future corrections may change the evidence. A permanent exclusion should be an accountable claim.

**Keep an unresolved state.** When evidence is insufficient, conflicting, prohibited, or too close between candidates, abstain or request review.

Forcing binary output inflates apparent coverage and hides risk. Design downstream behavior for unresolved identity before launch.

**Set policy from consequences.** A false link can expose records, deny service, corrupt history, or combine balances; a missed link can duplicate service or hide aggregate risk.

Estimate losses by decision, not only pair count. Different use cases can require different thresholds, margins, evidence minima, or manual confirmation.

**Evaluate the full decision system.** Measure candidate recall, pairwise precision and recall, cluster quality, calibration where applicable, abstention, review outcomes, correction time, and downstream harm.

Report by source, time, geography, language, script, entity type, sparsity, evidence pattern, protected or vulnerable population where lawful, and consequence tier. Aggregate accuracy hides unsafe slices.

**Build evaluation data carefully.** Labels can come from authoritative cross-references, adjudication, controlled tests, historical decisions, or synthetic data, each with bias and limitations.

Separate training, threshold tuning, and evaluation. Preserve label provenance, disagreement, sampling, blind review, uncertainty, and leakage controls.

**Do not learn blindly from operations.** Prior system links, successful transactions, or unchallenged clusters are not unbiased truth. People harmed by false links may be less visible than satisfied users.

Audit feedback routes and sample noncomplaints. Use production outcomes as evidence with selection effects, not automatic labels.

**Design human review as a system.** Cases need candidate records, relevant evidence, source and transformation context, policy, uncertainty, prohibited fields, and a clear decision vocabulary.

Define reviewer qualification, workload, service levels, dual control, blind review, escalation, quality sampling, conflict of interest, rationale, and appeals.

**Protect reviewers and subjects.** Minimize sensitive fields and avoid showing irrelevant protected characteristics. Log access and decisions without making broad identity graphs discoverable.

Support accessibility, language, and safe escalation. Manual review can reproduce bias and error; it is not a correctness oracle.

**Version every decision.** A link decision records record pair or cluster, scope, purpose, outcome, policy or model, thresholds, signals, evidence versions, time, reviewer, and supersession.

New data or rules can change a decision without erasing the old basis. Historical consumers may need the cluster version used at a past time.

**Issue stable enterprise IDs after policy.** An enterprise entity identifier labels a governed cluster within a domain. It does not prove natural identity outside that scope.

Never recycle it. Preserve source cross-references, aliases, merges, splits, tombstones, and resolution behavior so consumers can follow correction without guessing.

**Represent clusters as versions.** A cluster version binds member source records, edge or decision evidence, excluded candidates, policy, and effective time.

Avoid one mutable `master_id` column as the only history. Cluster changes affect every downstream fact joined through that identity.

**Make merge and split reversible.** Preserve pre-change IDs, memberships, relationships, source assertions, versions, aliases, and affected consumers.

A false merge can become a privacy or safety incident. Splitting requires correction propagation, cache invalidation, recomputation, and confirmation that consumers separated data and decisions.

**Separate identity from survivorship.** Resolution decides which records represent one entity. Survivorship decides which assertions appear in a preferred representation.

A source can be strong evidence for identity yet weak authority for address or preference. DARCH-054 develops match, merge, and survivorship mechanics.

**Publish purpose-specific identity products.** Consumers may need source-ID translation, cluster membership, duplicate candidates, a stable entity key, or a minimized derived view.

Do not publish the entire linkage graph by convenience. Define allowed uses, fields, confidence semantics, staleness, correction, and consumer duties.

**Design lookup APIs explicitly.** A resolution request declares entity domain, source namespace, identifier or permitted attributes, purpose, as-of time, policy, and requested evidence level.

Responses declare resolved entity ID or typed state, decision version, source cross-reference, effective time, freshness, and correction channel. Avoid a bare ID that hides ambiguity.

**Use events for identity changes.** Link, unlink, merge, split, alias, tombstone, review, and correction events need stable IDs, prior and new versions, cause, time, idempotency, ordering, and protection.

Events notify change but do not replace snapshots. Consumers need bootstrap, replay bounds, gap detection, and reconciliation.

**Provide bulk snapshots for repair and analysis.** Publish versioned cluster membership and cross-reference extracts with schemas, manifests, digests, effective intervals, and access controls.

Make activation atomic and prevent mixing cluster versions. Bulk consumers must record which identity generation they used.

**Control consistency expectations.** Source changes, candidate indexes, review decisions, master views, APIs, events, and analytical snapshots may converge at different times.

Define maximum lag and visible provisional states. Consumers should not infer that every channel reflects one instantaneous cluster graph unless the architecture supplies that guarantee.

**Handle incremental change.** A new or corrected source record can affect its candidate set, neighboring clusters, negative decisions, and downstream views.

Record source position and identity generation. Avoid recomputing only the changed row when graph constraints or shared identifiers can affect a wider component.

**Pin replay inputs.** Reproducible replay requires source versions, transformations, reference data, candidate indexes or rules, model, thresholds, overrides, and code.

Running old data through current policy creates a new counterfactual generation. Do so in isolation and compare before publication.

**Prevent stale overwrite.** A delayed batch or review result must not replace a newer cluster version without explicit conflict handling.

Use expected version, idempotency keys, source positions, and monotonic publication generations. Unknown outcomes require query and reconciliation before retry.

**Reconcile by identity and membership.** Compare source coverage, record counts, unresolved counts, membership keyed digests, aliases, merge and split chains, events, and consumer acknowledgements.

Whole-file equality can detect drift; localized membership evidence is needed to repair it and assess impact.

**Plan incidents around harm.** Contain unsafe publication, preserve evidence, identify affected subjects and consumers, stop amplification, and route high-consequence decisions to safe alternatives.

Correction includes unlinking or relinking, republishing identities, invalidating caches, recomputing derived data, notifying consumers, and verifying acknowledgement.

**Protect linkage as sensitive derived data.** Combining benign records can reveal relationships, behavior, households, locations, risk, or protected status.

Apply purpose limitation, minimization, role and attribute controls, encryption, isolation, query limits, export controls, monitoring, retention, deletion, and audit to identifiers, features, graphs, decisions, and histories.

**Reduce correlation where possible.** Pairwise or domain-specific identifiers can limit cross-context linkage. Tokenization and privacy-preserving linkage can reduce raw-value sharing.

These mechanisms move trust and attack surfaces; they do not eliminate false linkage, frequency attacks, auxiliary-data inference, key compromise, governance, or correction needs.

**Threat-model the resolver.** Attackers may inject records, claim shared identifiers, poison training or feedback, enumerate identities, exploit common values, steal linkage keys, manipulate reviewers, or trigger denial of service.

Use source authentication, input validation, rate limits, anomaly detection, separation of duties, signed or verified artifacts, secret rotation, case controls, and incident exercises.

**Honor correction and deletion duties.** Determine which assertions, derived features, clusters, decisions, exports, models, logs, and backups must be corrected, retained, restricted, or deleted.

Do not erase required provenance indiscriminately or retain every linked copy forever. Record legal and policy basis and test propagation.

**Engineer service objectives.** Define freshness, availability, latency, throughput, candidate-index lag, review time, correction time, event delivery, reconciliation, and recovery.

Observe by domain, source, policy, decision state, evidence pattern, slice, queue, consumer, and consequence. Healthy API latency can hide a stalled source or biased unresolved queue.

**Design degraded behavior.** A consumer may use a pinned mapping, return unresolved, require fresh proofing, queue a decision, or stop safely when identity evidence is stale.

The correct behavior follows consequence and purpose. Never broaden links merely to preserve service availability.

**Recover the decision system.** Restore source positions, normalized assertions, candidate indexes, models and rules, cluster generations, negative decisions, overrides, queues, cross-references, aliases, events, permissions, and audit.

Exercise restoration in isolation, verify representative decisions and keyed membership, then reconcile consumers. Backing up a current master table is insufficient.

**Assign accountability.** Domain owners define entity and purpose; source owners own assertions; resolution-product owners own contracts; model and rule owners own decision behavior; stewards own governed reviews.

Platform, privacy, security, legal, records, reliability, consumer, incident, and retirement owners retain their decisions. A vendor score does not absorb institutional accountability.

**Measure decision value and harm.** Track false-link and missed-link loss, candidate recall, abstention, correction, appeals, review capacity, downstream outcomes, protection incidents, adoption, cost, and avoided duplication.

Match count, cluster count, or model accuracy is supporting context. Continue only when improved outcomes justify linkage and its ongoing risk.

**Plan migration and retirement.** Inventory sources, identifiers, indexes, rules, models, clusters, cross-references, consumers, exports, cases, corrections, credentials, histories, backups, and duties.

Transfer authority and stable resolution before stopping feeds. Retire only after consumers migrate, retained evidence has custody, access is revoked, prohibited copies are removed, and restoration cannot resurrect unsupported identities.

## Definitions and Notation

Let source assertion $a=(s,r,n,k,v,t_e,t_o,q,p)$ contain source $s$, record $r$, namespace $n$, attribute key $k$, original value $v$, effective time $t_e$, observation time $t_o$, quality or evidence state $q$, and provenance $p$.

For records $r_i,r_j$, candidate function $C_B(r_i,r_j)$ declares whether blocking policy $B$ admits comparison. A signal vector $\gamma_{ij}=Compare(T(a_i),T(a_j),x)$ binds versioned transformations $T$, source assertions, context $x$, and comparison outputs.

Decision policy produces a typed outcome:

$$
d_{ij}=Decide(\gamma_{ij},scope,purpose,cost,policy) \in \{linked,not\_linked,unresolved,prohibited\}.
$$

Let entity generation $E_g=(id_g,R_g,D_g,N_g,P_g)$ bind stable enterprise identity, member source records $R_g$, supporting link decisions $D_g$, negative or excluded evidence $N_g$, and policy and provenance $P_g$.

For a decision population, expected loss can be framed as:

$$
L = c_{FL}N_{FL} + c_{ML}N_{ML} + c_RN_R + c_DD,
$$

where false links, missed links, reviews, and delayed decisions have context-specific costs. The expression disciplines tradeoffs; its coefficients require evidence and accountable judgment.

Define `FitResolution(I,u,t)` as a review predicate requiring justified use, scoped identity, qualified sources and identifiers, retained evidence, evaluated candidates and decisions, reversible clusters, protected publication, reliable operation, accountable outcomes, and lifecycle closure for use $u$ at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Name entity-dependent decisions, actors, population, purpose, deadlines, false-link and missed-link harms, fallback, and value.

**2. Scope gate.** Define entity type, legal and institutional boundary, time, source coverage, included and excluded relationships, and prohibited reuse.

**3. Evidence gate.** Preserve source assertions, qualified identifiers, authority, transformations, quality, temporal meaning, provenance, and correction.

**4. Candidate gate.** Evaluate blocking coverage, cost, skew, truncation, adversarial values, slice behavior, and typed insufficient evidence.

**5. Decision gate.** Define signals, rules or models, thresholds, margins, calibration, decision states, negative evidence, review, and versioning.

**6. Cluster gate.** Maintain stable IDs, temporal membership, edge evidence, constraints, aliases, merge, split, reversal, and consumer impact.

**7. Publication gate.** Contract APIs, events, snapshots, generations, consistency, freshness, corrections, replay, reconciliation, and acknowledgement.

**8. Protection gate.** Control purpose, linkability, minimization, access, keys, features, graphs, exports, retention, deletion, abuse, and audit.

**9. Service gate.** Bound capacity, index lag, queues, degraded behavior, incidents, recovery, monitoring, source failure, and stale overwrite.

**10. Lifecycle gate.** Assign authority, evaluate outcomes and fairness, manage policy change, migrate consumers, transfer custody, and verify retirement.

Passing the gates supports one scoped resolution use. It does not prove natural identity, universal correctness, credential truth, lawful reuse, absence of bias, or safety for another population or decision.

### Executable evidence

The executable example requires a minimum score and margin, then records how one verified identifier assertion changes a review outcome.

<!-- bijux-verify: {"id":"identity-resolution-evidence-margin","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_count=2\ninitial_best=loyalty:l-9\ninitial_score=5\ninitial_margin=1\ninitial_decision=review\nafter_verified_evidence_score=9\nafter_verified_evidence=linked\nprovenance_preserved=true\npolicy_version=3\n","stderr":""}} -->
```python
candidates = [
    {"id": "loyalty:l-9", "score": 5, "signals": ["email", "birth_date"]},
    {"id": "support:s-4", "score": 4, "signals": ["email", "postal_code"]},
]


def decide(items):
    ranked = sorted(items, key=lambda item: item["score"], reverse=True)
    margin = ranked[0]["score"] - ranked[1]["score"]
    outcome = "linked" if ranked[0]["score"] >= 8 and margin >= 3 else "review"
    return ranked[0], margin, outcome


before, initial_margin, initial_decision = decide(candidates)
candidates[0]["signals"].append("verified_source_identifier")
candidates[0]["score"] += 4
after, _, after_decision = decide(candidates)

print(f"candidate_count={len(candidates)}")
print(f"initial_best={before['id']}")
print(f"initial_score={before['score'] - 4}")
print(f"initial_margin={initial_margin}")
print(f"initial_decision={initial_decision}")
print(f"after_verified_evidence_score={after['score']}")
print(f"after_verified_evidence={after_decision}")
print(f"provenance_preserved={str(len(after['signals']) == 3).lower()}")
print("policy_version=3")
```

The result proves only arithmetic and branching for two in-memory candidates under the declared policy. It does not prove the records concern the same entity, that the identifier is valid or authoritative, that scores are calibrated, that features are fair or permitted, or that production linkage, review, protection, propagation, recovery, and downstream decisions are safe.

## Alternatives and Trade-Offs

**No enterprise resolution.** Domains retain separate identities and consumers integrate when needed. This limits central linkability but duplicates effort and can leave cross-domain decisions fragmented.

**Deterministic rules.** Transparent rules can fit strong identifiers and constrained populations. Coverage and maintenance suffer when sources, formats, and exceptions vary.

**Probabilistic linkage.** Weighted evidence handles noise and missingness but requires trustworthy labels or assumptions, calibration, threshold governance, monitoring, and explanation.

**Graph-assisted resolution.** Relationships and clusters reveal multi-record structure, while transitive errors and large-component failures can amplify harm.

**Manual resolution.** Expert judgment handles exceptional evidence but is slow, costly, variable, privacy-sensitive, and capacity-limited.

**Central identity graph.** Shared resolution and stable IDs reduce duplicated matching, while concentration increases coupling, correlation, incident blast radius, and contested authority.

**Federated resolvers.** Domains keep authority and purpose boundaries, but cross-domain consumers must combine identities and understand incompatible evidence policies.

**Universal identifier.** Strong shared identifiers simplify joins where legitimate and accurate, but coverage, issuance, reuse, fraud, lifecycle, and surveillance risks remain.

**Pairwise identifiers.** Context-specific identifiers reduce unauthorized correlation while making approved cross-context resolution and recovery more complex.

**Real-time resolution.** Supports interactive decisions with current evidence, but source latency, capacity, unknown outcomes, and outage policy become critical.

**Scheduled identity generations.** Coherent snapshots aid audit and analytics, but lag can miss urgent correction or create temporary inconsistency.

**Automatic low-confidence linking.** Coverage rises and review cost falls, but hidden false links can dominate value. Abstention preserves safety at the cost of unresolved work.

Choose by entity scope, purpose, evidence, source authority, population, error consequence, latency, correction need, privacy, adversarial pressure, review capacity, economics, and exit.

## Failure Modes and Misconceptions

1. **Identity is an intrinsic row property.** It is a scoped correspondence decision about representations and an entity.
2. **One person should have one enterprise identity.** Roles, legal boundaries, purposes, and privacy can require separation.
3. **Matching identifiers prove identity.** Namespace, issuance, status, reuse, theft, error, and time matter.
4. **Authentication proves record linkage.** It proves control of an authenticator under a protocol, not universal entity sameness.
5. **Normalization is harmless.** It can erase source, language, cultural, geographic, and temporal meaning.
6. **A strong matcher fixes weak blocking.** Excluded candidates are never compared.
7. **A score is a probability.** Calibration and population evidence are required.
8. **High aggregate accuracy means safety.** Rare catastrophic false links and unsafe slices can remain.
9. **Every pair needs a binary answer.** Unresolved, prohibited, and insufficient evidence are valid states.
10. **Transitive closure always forms entities.** Edge evidence can be incompatible at cluster scale.
11. **Manual review guarantees truth.** Review has evidence, bias, fatigue, capacity, and policy limits.
12. **A master ID is proof of natural identity.** It identifies a governed cluster within scope.
13. **Merge and split are table updates.** They are versioned decisions with downstream correction consequences.
14. **Historical links can be overwritten.** Audits and past decisions require as-of identity generations.
15. **More attributes always improve resolution.** They can add noise, prohibited use, bias, attack surface, and privacy risk.
16. **A tokenized graph is anonymous.** Link structure and auxiliary information can remain identifying.
17. **Replay reproduces identity.** Changed data, transformations, indexes, models, rules, and overrides change results.
18. **Match rate proves value.** Outcomes, harms, abstention, correction, adoption, and cost determine value.
19. **Stopping the resolver retires identity.** IDs, clusters, copies, aliases, cases, models, histories, and duties remain.

## Worked Examples

### Example 1

A bank account, mobile-app user, legal customer, and household are modeled as related but distinct entity types. Resolution policies cannot merge them merely because a person participates in each. **Conclusion:** scope precedes similarity.

### Example 2

Two source systems issue identifier `1842`; their namespaces and entity types differ. A qualified cross-reference prevents an accidental link. **Conclusion:** identifier values are not globally self-describing.

### Example 3

Exact email blocking retrieves most domestic candidates but misses shared inboxes and transliterated international records. A second address-and-phone pass improves candidate coverage, while ambiguous common values route to review. **Conclusion:** candidate recall is a separate quality dimension.

### Example 4

A model gives two candidates scores 0.82 and 0.81. Despite a nominal 0.80 threshold, margin policy abstains because evidence does not distinguish them safely. **Conclusion:** threshold crossing need not resolve ambiguity.

### Example 5

Three pairwise links form A–B–C, but A and C carry mutually exclusive verified organization identifiers. Cluster validation blocks transitive union and opens a case. **Conclusion:** graph connectivity is not sufficient identity evidence.

### Example 6

A customer authenticates both accounts during an attended recovery process. The evidence supports a scoped account-link claim, but marketing reuse remains prohibited and the two account histories stay traceable. **Conclusion:** evidence and permission are purpose-bound.

### Example 7

A false merge exposes one patient's appointment history to another. The incident restores prior cluster versions, publishes split and alias corrections, invalidates caches, and verifies every consumer acknowledgement. **Conclusion:** reversible identity and impact lineage are safety properties.

### Example 8

A replay using current nickname rules changes 6% of historical clusters. It runs in an isolated generation, compares memberships and slice outcomes, and cannot publish until owners accept the change. **Conclusion:** policy replay is a governed migration, not reproduction.

### Example 9

An analytical team receives pairwise domain tokens rather than raw national identifiers. The design reduces direct exposure but still protects mapping keys, graph structure, rare attributes, query patterns, and exports. **Conclusion:** privacy-preserving mechanisms reduce rather than erase risk.

### Example 10

API traffic has migrated from an old resolver, but annual compliance jobs, mobile snapshots, model features, backup restores, and unresolved review cases still depend on its IDs. **Conclusion:** retirement requires dependency and evidence closure.

## Cross-Program Connections

- **Data engineering:** source contracts, normalization, candidate indexes, incremental processing, temporal clusters, events, snapshots, reconciliation, replay, and deletion implement resolution flows.
- **Platform engineering:** identity stores, graph and search services, workflow, model serving, APIs, policy, observability, recovery, isolation, and paved migrations support the product.
- **API and service engineering:** qualified identifiers, typed outcomes, evidence levels, versions, idempotency, consistency, corrections, aliases, and deprecation shape consumer contracts.
- **Security engineering:** proofing, authentication, authorization, key protection, input integrity, enumeration resistance, fraud signals, abuse monitoring, and incident containment intersect identity decisions.
- **Privacy engineering:** linkability, purpose, minimization, pairwise identifiers, derived sensitivity, retention, deletion, access, and transparency constrain legitimate resolution.
- **Machine learning:** retrieval, comparison, classification, calibration, drift, labels, slice evaluation, abstention, human review, and adversarial robustness require governed evidence.
- **Organizational design:** entity authority, source ownership, stewardship, appeals, consumer responsibility, escalation, and funding determine actual control.
- **Reliability engineering:** index lag, queues, hot blocks, source outages, backpressure, stale writes, degraded modes, recovery, replay, and correction time define service behavior.
- **Economics and decision science:** asymmetric error loss, review cost, delayed decisions, value of information, option value of abstention, and exit cost guide policy.
- **Systems engineering:** boundaries, stakeholders, hazards, configuration control, assurance cases, lifecycle, and verification keep resolution accountable.

## References

1. U.S. Census Bureau, *Overview of Record Linkage and Current Research Directions*. <https://www.census.gov/library/working-papers/2006/adrm/rrs2006-02.html>
2. U.S. Census Bureau, *Statistical Quality Standard C4: Linking Data Records*. <https://www.census.gov/about/policies/quality/standards/standardc4.html>
3. U.S. Census Bureau, *Methods for Record Linkage and Bayesian Networks*. <https://www.census.gov/content/dam/Census/library/working-papers/2002/adrm/rrs2002-05.pdf>
4. NIST, *SP 800-63A: Enrollment and Identity Proofing*. <https://pages.nist.gov/800-63-4/sp800-63a.html>
5. W3C, *Decentralized Identifiers (DIDs) v1.0*. <https://www.w3.org/TR/did-core/>
6. W3C, *Verifiable Credentials Data Model v2.0*. <https://www.w3.org/TR/vc-data-model/>
7. W3C, *PROV-O: The PROV Ontology*. <https://www.w3.org/TR/2013/REC-prov-o-20130430/>
8. NIST, *Privacy Framework*. <https://www.nist.gov/privacy-framework/privacy-framework>
9. NIST, *Artificial Intelligence Risk Management Framework*. <https://www.nist.gov/itl/ai-risk-management-framework>
10. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design identity-resolution architecture for a party, supplier, product, device, or organization domain. Define entity scope, population, purpose, sources, evidence, candidates, policy, decision states, clusters, publication, protection, service, ownership, and lifecycle.

### Exercise 2

A resolver has 99.5% pairwise accuracy but false links in a vulnerable population cause account denial and data exposure. Explain why the aggregate measure is insufficient and redesign evaluation and policy.

### Exercise 3

Three records have pairwise scores A–B 0.94, B–C 0.91, and A–C 0.18 because A and C contain mutually exclusive verified identifiers. Design the cluster decision and evidence record.

### Exercise 4

A new normalization rule and model would change 250,000 cluster memberships while live source changes and reviews continue. Design safe comparison, cutover, correction, and rollback.

### Exercise 5

An organization will retire a central identity resolver after moving products to domain services. Define evidence that identity functions, consumers, protection, history, and correction duties have moved or ended.

## Answers to the Exercises

### Answer 1

Define the entity precisely—for example legal organization rather than supplier account or establishment—and declare geography, source coverage, time, purpose, prohibited reuse, consumers, deadlines, and false-link and missed-link harms. Inventory source records and qualified identifiers with authority, collection, effective and observation time, quality, missingness, correction, deletion, and protection. Preserve original assertions and version every normalization. Design multiple candidate passes and measure coverage, skew, truncation, and slice behavior.

Define deterministic or statistical signals, negative evidence, thresholds, margins, linked, not-linked, unresolved and prohibited states, review workflow, policy version, and evaluation evidence. Issue stable nonrecycled enterprise IDs only within that scope; keep temporal membership, source cross-references, aliases, and reversible merge and split lineage. Publish minimized APIs, events, and snapshots with generations, freshness, correction, replay, and reconciliation. Protect features, graph, decisions, histories, and exports. Assign domain, source, resolution, model or rule, stewardship, platform, consumer, privacy, security, incident, and retirement owners. Measure outcome loss and value, then close every dependency and retained obligation explicitly.

### Answer 2

Accuracy combines true links and true nonlinks across a usually imbalanced pair population, so abundant easy nonlinks can dominate it. It does not express which false links occurred, their cost, who was harmed, whether blocking excluded true candidates, how often the system abstained, or how long correction took. Data exposure and denial show the system is unsafe for the affected use even if the aggregate number is high.

Measure candidate recall, false-link and missed-link rates, precision and recall, calibration where scores are interpreted probabilistically, abstention, review decisions, appeals, correction time, and downstream losses. Report by relevant population, language, script, source, evidence pattern, sparsity, geography, time, and consequence tier while protecting sensitive attributes. Increase evidence minima, threshold, or required margin for the vulnerable high-consequence path; use typed unresolved and accessible human review instead of forced links. Independently sample decisions and noncomplaints, review label provenance and selection bias, test adversarial cases, and require accountable approval based on expected harm rather than aggregate accuracy.

### Answer 3

Do not take transitive closure. Preserve all three pairwise comparisons, inputs, transformations, model or rule version, score semantics, thresholds, timestamps, and source provenance. Record the verified identifiers as cluster-level negative evidence and confirm their namespaces, issuers, status, entity types, temporal overlap, and authority. If they truly identify mutually exclusive subjects, A and C cannot occupy one cluster under the policy.

The system can link A–B only if B's evidence is compatible with A and does not imply that B also links C. Otherwise it returns unresolved for the component and opens a review case. The reviewer sees scoped evidence and decides which edge, if any, is supported; the rationale, policy, reviewer, effective interval, and supersession are versioned. Preserve rejected edges and prior states. Publish a new cluster generation only after constraints pass, and route downstream consumers through stable IDs and correction contracts rather than silently rewriting membership.

### Answer 4

Pin source snapshots and change positions, original assertions, transformation and reference versions, candidate policy, model, thresholds, overrides, code, and prior cluster generation. Run the candidate rule and model in an isolated namespace. Compare memberships, stable IDs, aliases, false-link and missed-link evaluation, unresolved volume, queue demand, slice outcomes, high-consequence decisions, performance, and protection exposure. Sample changes for blind adjudication and obtain domain, model, privacy, security, operational, and consumer approval appropriate to risk.

Capture live changes and reviews after the snapshot and apply them deterministically to both old and candidate generations or reconcile at a declared boundary. Cut over by cohort or atomic generation with expected-version writes, idempotent events, old-to-new aliases, monitoring, rate limits, and a preserved prior read path. A rollback must handle facts already written using new IDs; it may require forward correction rather than pointer reversal. Track consumer acknowledgement, replay affected derivatives, and close only after keyed membership reconciliation and correction. Never allow an old batch or delayed review to overwrite a newer live generation.

### Answer 5

Inventory every entity domain, namespace, source feed, transformation, candidate index, rule, model, threshold, cluster generation, negative decision, override, cross-reference, alias, API, event, snapshot, cache, package, analytical join, model feature, report, review and appeal case, credential, export, backup, retention rule, deletion path, and incident duty. For each capability, name the receiving domain service and verify its authority, contract, protection, reliability, recovery, funding, and escalation—or prove the capability is no longer required.

Run old and new resolvers in bounded comparison, migrate consumers by cohort, preserve stable resolution or governed aliases, and reconcile source coverage, memberships, histories, corrections, and downstream decisions. Include seasonal, offline, disaster-recovery, investigative, and manual consumers that live traffic misses. Stop new resolution and feeds only after authority transfers; close queues and appeals; revoke access; delete prohibited features, graphs, and copies; preserve required provenance with a custodian; and test correction and recovery without the old service. Verify that backups, jobs, old binaries, or replay cannot resurrect unsupported identity state before accountable retirement.
