---
module_id: DARCH-077
program: Data Architecture Engineering
level: 2
module_number: 77
title: Deletion and the Right to Erasure
status: complete
last_verified: 2026-09-03
---

# Deletion and the Right to Erasure

## One-Page Review

### Governing question

How should a data architecture recognize and decide erasure requests, locate every governed representation, preserve data that remains authorized, stop prohibited use, execute suitable deletion or de-identification, propagate obligations, and prove outcomes across active systems, recipients, backups, models, and recovery without promising impossible or legally incorrect “total deletion”?

### Essential definitions

- **Deletion** is a governed change that makes a defined data representation unavailable for specified future processing through an identified mechanism and assurance level.
- **Erasure** is the legally or policy-governed outcome required for personal data in an applicable context; it is not synonymous with an HTTP method, database command, or media wipe.
- A **right-to-erasure request** is an expression by a person or authorized representative seeking an applicable erasure outcome for defined personal data.
- An **erasure determination** decides scope, applicability, grounds, exceptions, identity confidence, response duties, deadline, and remedy under an authorized rule set.
- A **deletion target** is a specific row, object version, event, document, index entry, cache item, feature, model artifact, export, replica, backup cohort, or downstream copy addressed by a plan.
- A **deletion plan** binds a determination to targets, actions, dependencies, order, controls, deadlines, exceptions, evidence, and owners.
- **Logical deletion** removes ordinary addressability or marks information unavailable to normal processing while physical remnants may persist temporarily.
- **Physical sanitization** renders access to target data on media infeasible for a stated effort and threat model using an approved method.
- **Cryptographic erase** makes encrypted target data infeasible to recover by sanitizing the necessary cryptographic keys under verified assumptions.
- **De-identification** transforms data so an approved identifiability criterion is met in context; replacing a direct identifier is not sufficient proof.
- A **tombstone** is a durable deletion marker used to prevent stale replicas, retries, imports, or restores from resurrecting a deleted identity or object.
- **Suppression** retains a minimal restricted signal needed to prevent a prohibited future action, such as contacting a person again; it is not ordinary product retention.
- A **deletion receipt** records target, action, actor, policy, time, result, verification, limitations, and residual state without retaining the deleted content unnecessarily.
- **Propagation** communicates and enforces deletion or restriction across copies, processors, recipients, indexes, derived assets, and future recovery paths.
- **Commercially or operationally unrecoverable** describes a bounded provider or system state; it is not proof that no physical remnant, compelled copy, recipient copy, or independent derivative exists.
- **Closure** resolves all targets, exceptions, recipients, failures, backup cohorts, model decisions, tombstones, notices, and recovery paths while retaining the minimum authorized request and outcome evidence.

### Central model, mechanism, or theorem

Represent erasure governance as:

`E = (U, A, R, D, G, T, P, V, O, L)`

where `U` is requester and subject authority, `A` applicability and grounds, `R` retained purposes, bases, holds, and exceptions, `D` discovered data and representations, `G` lineage and downstream relationships, `T` deletion targets and methods, `P` propagation and prevention of resurrection, `V` verification and evidence, `O` operations and remedy, and `L` lifecycle and closure. Completion requires a defensible determination plus verified outcomes for every in-scope target; neither a successful request nor a hidden record alone proves erasure.

### Critical invariants

- Request, requester, subject, representative, identity proof, determination, target, retained exception, action, event, receipt, and outcome have separate stable identities.
- Erasure rights are evaluated under applicable rules and facts; they are not absolute and are not inferred from account deletion alone.
- Purpose, legal or policy basis, retention schedule, hold, claim, public interest, archival rule, and technical dependency remain distinct constraints.
- Data retained under a separate authorized reason is isolated from prohibited product use and explained at an appropriate level.
- Primary content, history, indexes, caches, queues, logs, telemetry, derived data, exports, recipients, models, replicas, backups, and recovery artifacts are inventoried separately.
- API acceptance, logical deletion, background execution, physical reclamation, media sanitization, cryptographic erase, backup expiry, and recipient confirmation remain distinct evidence.
- Tombstones and suppression records are minimized, protected, purpose-bound, and cannot become a hidden customer profile.
- Holds and immutable-retention controls block destructive action visibly rather than causing false success.
- Unknown, unreachable, conflicting, partially complete, unverifiable, or resurrected state is reported and remediated.
- Deletion is idempotent for the same target version and cannot silently delete a replacement object, shared subject data, or another person's record.
- Metrics distinguish requests, determinations, targets, completed actions, retained exceptions, failures, deadlines, resurrection, complaints, and outcomes.
- Recovery and migration replay deletion state before enabling ordinary processing and cannot recreate previously erased data from stale sources.

### Common failures

Common failures include treating the right to erasure as absolute; equating account closure with data deletion; treating HTTP `DELETE 204` as proof of erasure; deleting one primary row; overlooking aliases, representatives, shared records, devices, logs, indexes, vector stores, exports, processors, and backups; retaining everything under vague fraud or legal claims; destroying records under active hold; masking a value while keeping the mapping; deleting a key without checking plaintext and copies; calling pseudonymization anonymous; removing training rows while ignoring checkpoints and deployed models; issuing events without consumer receipts; dropping tombstones too early; using deleted payloads in evidence logs; restoring stale backups into production; and reporting request completion while targets remain unknown.

### Compact example

Ten invented deletion targets for one request are classified. Three are declared verified deleted, two are retained under separate bases, one is blocked by a hold, one system is unavailable, one downstream recipient is pending, one backup cohort has aged out, and one model requires review. Ten systems, nine asset planes, three subjects, and ten decision events are counted. Executable evidence confirms only those declarations. It proves no identity, applicable right, valid exception, actual deletion, sanitization, recipient behavior, backup expiry, model influence removal, non-resurrection, or beneficial outcome.

### Connections

[DARCH-064](064-lineage-architecture.md), [DARCH-069](069-metadata-apis-and-eventing.md), [DARCH-072](072-policy-as-code-for-data.md), [DARCH-074](074-consent-and-purpose-limitation.md), [DARCH-075](075-data-residency-and-sovereignty.md), and [DARCH-076](076-retention-and-legal-hold.md) establish provenance, interfaces, policy, purpose, location, schedules, and preservation. [DARCH-078](../ROADMAP.md) next develops masking, tokenization, and clean rooms.

## Governing Question

A person can request erasure of a profile while invoices must remain under a separate duty, a legal hold preserves selected messages, a suppression record prevents further marketing, an external processor retains a copy, a backup expires later, and a model cannot be honestly described as unlearned merely because training rows disappeared. One `deleted = true` field cannot represent these outcomes.

The governing question is how to translate an authorized rights or lifecycle decision into a complete, safe, observable plan across real dependencies. A durable architecture prevents continued use quickly, distinguishes retained evidence from denied requests, chooses deletion techniques by representation and threat model, verifies distributed effects, communicates limitations, and ensures restoration or delayed events cannot resurrect prohibited processing.

## Why This Matters

The European Union's [General Data Protection Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679) establishes a right to erasure in defined circumstances, exceptions, communication duties concerning recipients, time requirements for rights responses, and broader controller accountability. The legal scope is specific and requires professional interpretation. Architecturally, the right is a governed determination with possible partial outcomes, not an unconditional delete endpoint.

The UK Information Commissioner's Office's current [right-to-erasure guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/) emphasizes that the right is not absolute, describes grounds and exceptions, addresses recipient notification and backup systems, and distinguishes request recognition from compliance. The page is under review following UK legal changes, which reinforces source versioning and jurisdiction-specific decision profiles.

The European Data Protection Board's final [Guidelines 5/2019](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-52019-criteria-right-be-forgotten-search-engines_en) address criteria for delisting search-engine results under the GDPR. Delisting a result and erasing source content are different outcomes. Architecture must model the target relation and effect rather than call both “delete.”

The California Privacy Protection Agency's current [CCPA statute and regulations effective January 1, 2026](https://cppa.ca.gov/regulations/pdf/ccpa_statute_eff_20260101.pdf) define California-specific deletion requests, verification, timelines, methods, service-provider and contractor directions, and exceptions. These rules differ from EU and UK regimes. A global deletion workflow therefore selects an authorized profile rather than applying one jurisdiction's checklist everywhere.

NIST [SP 800-88 Revision 2](https://csrc.nist.gov/pubs/sp/800/88/r2/final), published in September 2025 and superseding Revision 1, defines media sanitization around rendering target data access infeasible for a given level of effort. It emphasizes an organizational sanitization program, approved standards, assurance, and trust in implementations. Media sanitization is one lifecycle mechanism; record-level erasure in active distributed systems needs additional controls.

NIST [SP 800-53 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) includes media sanitization, information disposal, retention, minimization, privacy, system disposal, audit, contingency, and external-service controls. The catalog supports control design and assessment but does not decide whether an individual's request applies or identify all copies.

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) specifies that HTTP `DELETE` requests removal of the association between a target resource and its current functionality; it does not require destruction of every representation or reclamation of storage. A 202, 204, or 200 response communicates protocol status, not enterprise-wide erasure proof.

Google Cloud's current [data deletion documentation](https://docs.cloud.google.com/docs/security/deletion) describes a provider-specific pipeline involving request, marking, recovery periods, logical deletion, garbage collection, backup expiry, and possible cryptographic erasure. It explicitly scopes its commitments and timing. This illustrates why architecture must model stages and provider evidence rather than promise instantaneous physical destruction.

Microsoft's current [data retention, deletion, and destruction guidance](https://learn.microsoft.com/en-us/compliance/assurance/assurance-data-retention-deletion-and-destruction-overview) distinguishes active and passive deletion and different data categories and provider timelines. Provider commitments are service- and contract-specific and do not replace a controller's inventory or downstream verification.

AWS [S3 Object Lock documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) explains that fixed retention and legal holds protect individual object versions and that a simple delete can create a delete marker while protected versions remain. This demonstrates why a successful API response and absence from the default view may not mean a specific version was destroyed.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, derivations, attributions, associations, delegations, and qualified relations. Erasure planning needs provenance connecting source data, copies, transformations, recipients, models, deletion actions, and receipts. Provenance helps find effects but does not prove that every derivative remains personal or that every deletion occurred.

Together these sources support architecture that separates applicable rights, data discovery, retained authority, deletion mechanics, provider lifecycle, distributed propagation, provenance, evidence, limitations, and recovery-safe closure.

## Prerequisites and Retrieval

You should understand privacy and data-protection rights, identity and representation, purpose limitation, lawful bases, records schedules, legal hold, data classification, lineage, distributed systems, databases, object storage, search indexes, caches, event streams, backups, media sanitization, encryption and keys, machine learning, APIs, observability, incident response, and recovery.

Retrieve erasure, deletion, right to be forgotten, delisting, de-identification, anonymization, aggregation, suppression, logical delete, soft delete, hard delete, tombstone, garbage collection, sanitization, clear, purge, destroy, cryptographic erase, key destruction, replica, recipient, processor, downstream, exception, legal hold, immutable retention, backup expiry, unlearning, verification, receipt, resurrection, and closure.

As a retrieval test, inspect `DELETE /users/42 → 204`. Ask who requested it and for which subject; which jurisdiction, grounds, verification, deadline, and exceptions apply; whether the target is an account, URI mapping, row, or full data relationship; which invoices, messages, logs, indexes, caches, exports, processors, models, versions, backups, keys, and tombstones exist; which actions each requires; and what evidence proves completion. The response code alone answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish erasure rights, lifecycle deletion, account closure, delisting, restriction, de-identification, sanitization, cryptographic erase, and media destruction;
2. design request intake, identity and representative verification, applicable-rule selection, grounds, exceptions, deadlines, explanation, and remedy;
3. discover target data across identifiers, subjects, purposes, systems, copies, versions, recipients, derived assets, models, and backups;
4. preserve separately authorized records while preventing their use for erased purposes;
5. select representation-specific deletion methods and state their threat, recovery, integrity, and verification assumptions;
6. implement idempotent plans, dependency ordering, tombstones, events, acknowledgements, retries, reconciliation, and non-resurrection controls;
7. address shared and multi-subject data, legal holds, immutable storage, downstream processors, unavailable systems, and provider timelines;
8. make bounded decisions about models, aggregates, logs, and backups without unsupported anonymity or unlearning claims;
9. operate evidence, metrics, incidents, corrections, migration, recovery, communication, and closure; and
10. identify where automation must defer to legal, privacy, records, security, domain, and affected-person judgment.

## Core Exposition

**Begin with the processing relationship.** Identify requester, data subject, representative authority, controller or decision owner, products, purposes, bases, data categories, recipients, and applicable jurisdictions before searching by email address.

An account is not always a person, one person can have several identities, and one account can contain information about several people.

**Separate rights requests from ordinary lifecycle deletion.** Retention schedules, contract closure, test-data cleanup, incident containment, and user-initiated erasure can all cause deletion. Preserve their authorities, deadlines, notices, exceptions, and evidence separately.

One deletion engine may execute actions for several workflows, but the workflow identity determines scope and explanation.

**Recognize requests across channels.** A valid request may arrive through an interface, email, support call, letter, representative, regulator, or another authorized path depending on the rule set. Train people and classifiers to route possible requests without making final legal decisions.

Record receipt time, channel, original expression, subject candidates, requested scope, jurisdiction candidates, language, accessibility need, acknowledgement, and owner.

**Verify proportionately.** Match identity assurance to the data and harm of disclosure or deletion. Use existing authenticated sessions where sufficient; request additional evidence only when necessary.

Separate requester, subject, account holder, guardian, executor, agent, employee, household member, and representative. Minimize verification artifacts and prevent the process from becoming identity-data collection.

**Select an authorized decision profile.** Applicable rules can differ by subject, controller, establishment, location, age, sector, service, contract, and time. A profile defines grounds, exceptions, deadlines, extension, fee or refusal rules, recipient duties, backup treatment, evidence, and appeal.

Version every determination. Do not merge EU, UK, California, sector, and internal commitments into an unexplained “strictest” Boolean.

**Determine grounds and exceptions.** Ask why the data was collected and is still processed, which basis applies, whether consent was withdrawn or an objection succeeded, whether processing was unlawful, and whether another obligation or protected interest requires retention.

Record each purpose and representation separately. An invoice may remain under a legal duty while personalization features, marketing history, and profile attributes are erased.

**Do not use vague exceptions.** “Fraud,” “security,” “legal,” “research,” “public interest,” and “claims” require applicable authority, specific purpose, data scope, necessity, safeguards, retention, owner, review, and expiry.

An exception permits only the bounded continued processing it supports. It does not preserve product access or unrelated analytics.

**Coordinate with retention and holds.** Resolve record schedules, minimum and maximum retention, archival transfer, investigations, litigation holds, regulatory freezes, and security containment before destructive action.

If a hold applies, record the target as preserved and restrict ordinary use. Do not report it as deleted, and do not expose sensitive matter details unnecessarily in the response.

**Build a subject identity graph.** Link verified person and representative identities to accounts, aliases, devices, customer numbers, employee IDs, cookies, advertising IDs, pseudonyms, tokens, payment references, households, and domain identifiers with source, confidence, and valid time.

Avoid uncontrolled fuzzy matching. False positives delete another person's data; false negatives leave the subject's data active.

**Build a data reliance graph.** Register source records, copies, topics, queues, tables, object versions, indexes, caches, reports, files, exports, processors, recipients, backups, features, models, and outputs with purpose, basis, subject relation, owner, location, retention, and deletion capability.

Lineage proposes targets. It does not decide whether a transformed node remains personal, belongs to multiple people, or is independently retained.

**Inventory every representation.** Include active rows, temporal history, change logs, audit records, unstructured content, attachments, metadata, search indexes, vectors, caches, queues, dead letters, telemetry, support bundles, local devices, reports, data lakes, sandboxes, notebooks, exports, recipient copies, replicas, snapshots, archives, and backups.

Declare exclusions with authority and evidence. “Logs” and “backups” are not valid blanket exclusions.

**Handle multi-subject and shared data.** A message, household record, transaction, photograph, genetic relation, meeting, or case may concern several people. Deleting the whole object can impair others' rights or evidence; retaining it can continue the requester's exposure.

Consider field removal, redaction, access restriction, unlinking, delisting, account detachment, replacement representation, or segregated retention under authorized review.

**Define target granularity.** Use stable row keys, object version IDs, event IDs, partitions, subject edges, index documents, cache keys, export manifests, recipient references, model versions, backup cohorts, and media identities.

A path or object name can be reused. Idempotency must bind to immutable target identity or generation so retries cannot delete replacement data.

**Choose the required effect.** Possible outcomes include immediate restriction, logical deletion, unlinking, redaction, delisting, de-identification, aggregation, key revocation, background purge, backup aging, media clear, purge, destruction, or documented retention.

Name the effect honestly. Hiding an object from an interface is not physical sanitization; delisting a search result is not source erasure.

**Stop prohibited use early.** Rights deadlines and distributed physical deletion may differ. Once a determination is approved, block ordinary reads, writes, recommendations, marketing, exports, profiling, training, and recipient sync as required while deeper deletion proceeds.

Use a protected intermediate state with clear failure handling. A recoverable grace period must be authorized and must not allow ordinary processing.

**Use logical deletion deliberately.** Soft-delete flags and tombstones can enable recovery, propagation, and non-resurrection. They also retain identifiers and may leave payloads queryable to administrators or forgotten code paths.

Separate the minimal tombstone from content, enforce access and expiry, and test every query path. A global `WHERE deleted = false` convention is not sufficient assurance.

**Use physical sanitization for media lifecycle.** Define media type, confidentiality, ownership, reuse or disposal scenario, adversary effort, approved standard, method, tool or provider, validation, documentation, custody, and failure response.

Record-level deletion in a shared SSD, database, or managed service may not map to immediate block overwrite. Provider architecture and contract determine feasible assurance.

**Use cryptographic erase under explicit assumptions.** Identify which target data is encrypted by which unique keys, copies of keys, wrapping hierarchy, escrow, caches, plaintext replicas, snapshots, application memory, recipient exports, and recovery material.

Destroying one key proves little if shared keys protect unrelated data or another key copy remains. Crypto erase requires verified key sanitization and a defensible mapping from keys to target ciphertext.

**Evaluate de-identification in context.** Removing name and email can leave unique behavior, location, free text, linkage keys, rare combinations, or model membership. Define attacker knowledge, recipients, auxiliary data, release context, governance, and testing.

If the approved criterion is not met, treat the output as still governed. Do not use “anonymized” as a deletion status without evidence.

**Delete from databases with integrity.** Plan referential actions, shared rows, history tables, materialized views, search indexes, CDC logs, replicas, caches, constraints, aggregates, audit evidence, and transactional boundaries.

Avoid cascade deletion chosen solely by schema relationships. Preserve necessary aggregate integrity without retaining linkable subject data where not authorized.

**Delete from streams and logs with bounded methods.** Event logs may be immutable or compacted. Options include subject-partition deletion, encryption-key separation, redacted replacement, bounded topic retention, protected tombstones, and derived-store cleanup.

Document what cannot be selectively removed and prevent replay into active state. Future architectures should avoid placing unnecessary personal payloads in hard-to-delete logs.

**Invalidate indexes and caches.** Search, CDN, browser, application, database, feature, query, and recommendation caches can keep data visible after the source disappears.

Publish versioned invalidation, revoke URLs and tokens, remove index documents, verify representative queries, bound offline caches, and reconcile expiry. Cache invalidation evidence is separate from source deletion.

**Control downstream recipients.** Record controllers, processors, contractors, affiliates, data buyers, researchers, public releases, and accidental recipients. Determine which must be informed or instructed under the applicable profile.

Use stable request and subject references that do not expose unnecessary content. Require acknowledgement, target-level status, exceptions, deadlines, failure escalation, and closure; an outbound email is not proof.

**Address public publication and search.** Source removal, web-cache invalidation, search delisting, mirror removal, archive policy, and third-party republication are distinct actions with different authorities and practical control.

Do not promise deletion from parties outside control. Document reasonable steps, recipients, requests, known residuals, and remedy accurately.

**Address backups by design.** Know backup contents, cohorts, keys, retention, immutability, searchability, selective-delete capability, provider commitments, and restore paths. Stop copying deleted data into new backups.

Where approved profiles permit aging rather than immediate mutation, make backup data unavailable for ordinary use, record the maximum residual interval, and replay tombstones before restored data becomes accessible.

**Address archives and legal preservation.** An archive is not a backup. Permanent or public-interest records can have separate authority, access controls, subject rights, and descriptive obligations.

Segregate retained material from product systems and prevent it from being used to reconstruct an erased profile beyond authorized archival purposes.

**Address machine-learning systems honestly.** Delete source and feature rows, queued examples, training manifests, evaluation samples, prompts, outputs, embeddings, vector indexes, checkpoints, and model copies where applicable and feasible.

Decide whether retraining, unlearning, output filtering, access restriction, model retirement, or documented residual risk is required. Do not claim individual influence removal without a validated method and target-specific evidence.

**Protect deletion from abuse.** Attackers can use account takeover, forged requests, enumeration, race conditions, replay, or excessive scope to destroy evidence and availability. Use proportionate authentication, authorization, rate limits, anomaly detection, dual control for high-consequence actions, and recovery boundaries.

Do not expose whether a sensitive subject or record exists through response differences.

**Design a request API.** Accept channel, authenticated requester, subject and representative evidence, requested scope, authority candidates, accessibility and communication preferences, and idempotency key. Return request identity, receipt time, next action, deadline basis, status, and safe explanation.

An API should recognize a request even if later verification fails. Request content in HTTP `DELETE` has no general semantics; use explicit resources and schemas for enterprise workflows.

**Design a determination API.** Return applicable profile, grounds, target purposes and data, retained exceptions, required actions, recipients, deadlines, obligations, reviewer, decision version, expiry, explanation, and appeal path.

Keep privileged, security-sensitive, and third-party details in protected evidence rather than broad response payloads.

**Design a deletion orchestration service.** Compile determination into immutable target manifests and a dependency graph. Stop use, apply tombstones, dispatch repository actions, wait for acknowledgements, retry safely, verify state, handle exceptions, notify recipients, and close.

Each adapter declares supported operations, target granularity, latency, reversibility, verification, provider residuals, hold behavior, and failure modes.

**Use explicit target states.** Useful states include discovered, excluded, retained-authorized, hold-blocked, queued, restricted, logically-deleted, purge-pending, recipient-pending, backup-aging, model-review, verified-complete, failed, unavailable, disputed, and unverifiable.

Do not collapse intermediate or partial states into `deleted`. State transitions retain actor, reason, time, version, evidence, and limitations.

**Publish immutable events.** Emit request, verification, determination, target discovery, restriction, action, acknowledgement, failure, retention exception, backup cohort, model review, verification, response, appeal, correction, and closure with effective and record time.

Consumers deduplicate and reject stale versions. A deletion event is an instruction and history fact, not proof of consumer enforcement.

**Prevent resurrection.** Tombstones or equivalent negative knowledge must outlive every plausible delayed event, replica, offline client, import, snapshot, backup, and retry that could recreate the data.

On ingest and restore, compare subject, object generation, deletion version, and event time before applying old state. Preserve enough minimal identity to block resurrection without retaining the deleted profile.

**Verify outcomes independently.** Combine repository receipts with queries that confirm absence or restriction, object-version inventory, index and cache probes, recipient acknowledgements, key evidence, backup cohort status, model action, and restore exercises.

Verification must avoid recreating or broadly exposing deleted data. Sampling and negative queries have coverage limits that must be reported.

**Communicate precisely.** Tell the person what was erased, retained under another authority, sent to recipients, delayed by backup lifecycle, unavailable, refused, or still under review at a level permitted by the profile. State deadlines, extensions, rights, and complaint or appeal routes.

Do not reveal legal strategy, another person's data, security architecture, or the existence of protected investigations unnecessarily.

**Protect deletion evidence.** Receipts can reveal identity, account history, sensitive categories, systems, recipients, disputes, and security controls. Store target identifiers or keyed references rather than deleted content where possible.

Give request evidence its own purpose, basis, retention schedule, access, residency, and deletion lifecycle.

**Measure complete denominators.** Track received and recognized requests, verification outcomes, determinations, deadlines, targets, discovered systems, retained exceptions, hold blocks, restricted use, completed actions, failures, recipient status, backup cohorts, model reviews, complaints, resurrection incidents, and closure.

Coverage is verified targets divided by expected in-scope targets, not successful jobs divided by attempted jobs. Unknown systems remain visible.

**Handle incidents and correction.** Premature deletion, deletion of the wrong subject, continued processing, resurrection, missed recipient, false completion, or overretention is an incident. Contain, preserve facts, identify affected people and decisions, restore only when authorized, notify, remedy, fix controls, and verify closure.

Never backdate a deletion receipt or rewrite failed history.

**Migrate legacy deletion safely.** Preserve old request, account, mapping, job, tombstone, recipient, exception, and audit semantics. Resolve legacy `deleted` states into explicit target and outcome records with unknown where evidence is missing.

Dual-evaluate new requests, replay historical tombstones before imports, canary adapters, and prove that old jobs cannot bypass current holds or identity boundaries.

**Recover policy before data.** Restore current determinations, tombstones, holds, target versions, completed receipts, recipient state, and backup-cohort rules before enabling product reads or lifecycle replay.

Quarantine restored data, reapply deletion and restriction, reconcile expected targets, and destroy transient recovery copies.

**Close deliberately.** Closure requires all targets to be verified complete, retained under an explicit current authority, transferred to a tracked external obligation, or recorded as unresolved with active escalation. Send the authorized response and keep appeal and remedy paths open.

Retire temporary access, preservation and recovery copies, credentials, jobs, exceptions, and debug artifacts while retaining only minimum lifecycle evidence under a separate schedule.

## Definitions and Notation

Let `q` denote an erasure request, `u` a subject or representative, `a` an applicability determination, `d` a data representation, `g` a lineage or reliance edge, `t` a deletion target, `m` a method, `r` a retained exception, and `v` verification evidence.

Define a determination as:

`A = (requester, subject, profile, grounds, purposes, data, exceptions, recipients, deadline, decision, explanation, version)`

The decision can be granted, partially granted, refused, pending verification, or disputed.

Define a target as:

`T = (system, object, generation, subject_relation, purpose, representation, action, dependency, owner, deadline, state)`

The generation prevents a retry from applying to a replacement object that reused an identifier.

Define a deletion receipt as:

`V = (target, requested_action, observed_effect, actor, mechanism, policy, effective_time, evidence, residuals, limitations)`

The receipt should not contain the deleted payload unless separately authorized and necessary.

Let `I(q)` be the expected in-scope targets, `C(q)` the targets verified complete, `R(q)` targets retained under authorized exceptions, and `F(q)` failed or unresolved targets. Then:

`closure(q) ⇒ I(q) = C(q) ∪ R(q) ∪ F(q)`

with pairwise explicit states and active escalation for `F(q)`. Closure does not mean every target is physically overwritten.

Define deletion coverage as:

`coverage(q) = |C(q)| / |I(q)|`

Report retained and unresolved targets separately. Unknown inventory cannot be removed from the denominator merely to improve the metric.

Define resurrection safety for an incoming version `x` as:

`accept(x) = no_applicable_tombstone(x.subject, x.object, x.generation, x.event_time)`

The production predicate must reflect authorized identity and version semantics; this shorthand is not a universal algorithm.

## Mechanisms, Invariants, or Proof Structure

An erasure architecture should implement the following assurance gates.

**Intake gate.** Recognize requests across approved channels, preserve receipt and requested scope, acknowledge, assign deadline, and support language and accessibility.

**Identity gate.** Resolve requester, subject, representative, accounts, aliases, devices, and shared relationships with proportionate evidence and protected uncertainty.

**Applicability gate.** Select the governing profile, evaluate grounds, purposes, bases, objections, withdrawal, exceptions, fees, extensions, response, and appeal through authorized review.

**Retention and hold gate.** Resolve schedules, legal duties, claims, archives, investigations, holds, freezes, and security constraints before destructive action.

**Discovery gate.** Enumerate systems, identifiers, content, history, indexes, caches, streams, logs, devices, exports, recipients, derived assets, models, replicas, archives, backups, and recovery paths.

**Target gate.** Bind each action to stable object and generation identity, subject relation, purpose, owner, deadline, dependency, and method.

**Restriction gate.** Stop prohibited read, write, profiling, marketing, training, export, sharing, and replay while deeper actions and reviews continue.

**Method gate.** Choose logical deletion, unlinking, redaction, delisting, de-identification, purge, crypto erase, backup aging, sanitization, destruction, or justified retention with explicit assumptions.

**Propagation gate.** Notify processors and recipients, enforce on copies and derivatives, collect acknowledgements, retry, reconcile, and escalate gaps.

**Non-resurrection gate.** Persist minimal protected tombstones through replica delay, offline clients, import, backup, and recovery horizons and compare incoming versions.

**Verification gate.** Corroborate receipts using target queries, version inventory, cache and index probes, key evidence, backup cohorts, recipient state, model action, and restore exercises.

**Evidence gate.** Minimize and protect request, determination, target, exception, action, receipt, response, incident, and appeal records under their own lifecycle.

**Communication gate.** Explain granted, retained, refused, delayed, unavailable, downstream, backup, and model outcomes accurately without exposing protected information.

**Correction gate.** Detect wrong-subject deletion, continued use, missed targets, resurrection, false closure, and overretention; contain, notify, remedy, and verify repair.

**Recovery and closure gate.** Restore deletion state before product data, replay tombstones, quarantine stale copies, resolve every target, remove temporary access and artifacts, and preserve minimum evidence.

### Executable evidence: deletion-target outcome evaluation

This Python example classifies ten invented targets for one deletion request according to declared retained authority, hold, reachability, downstream acknowledgement, backup state, model review, and completion.

<!-- bijux-verify: {"id":"deletion-target-outcome-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"targets=10\nrequests=1\nverified_deleted=3\nretained_separate_basis=2\nblocked_hold=1\nunavailable=1\ndownstream_pending=1\nbackup_aged_out=1\nreview_required=1\nsystems=10\nasset_planes=9\nsubjects=3\ndecision_events=10\n","stderr":""}} -->
```python
targets = [
    {"request": "erase-1", "subject": "u1", "system": "profile-db", "plane": "content", "separate_basis": False, "hold": False, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": False, "model": False, "complete": True},
    {"request": "erase-1", "subject": "u1", "system": "search-index", "plane": "index", "separate_basis": False, "hold": False, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": False, "model": False, "complete": True},
    {"request": "erase-1", "subject": "u1", "system": "recommendation-cache", "plane": "cache", "separate_basis": False, "hold": False, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": False, "model": False, "complete": True},
    {"request": "erase-1", "subject": "u1", "system": "invoice-ledger", "plane": "record", "separate_basis": True, "hold": False, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": False, "model": False, "complete": False},
    {"request": "erase-1", "subject": "u1", "system": "security-audit", "plane": "audit", "separate_basis": True, "hold": False, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": False, "model": False, "complete": False},
    {"request": "erase-1", "subject": "u2", "system": "shared-mailbox", "plane": "message", "separate_basis": False, "hold": True, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": False, "model": False, "complete": False},
    {"request": "erase-1", "subject": "u1", "system": "crm-saas", "plane": "content", "separate_basis": False, "hold": False, "reachable": False, "downstream": False, "acknowledged": False, "backup_expired": False, "model": False, "complete": False},
    {"request": "erase-1", "subject": "u1", "system": "mail-provider", "plane": "downstream", "separate_basis": False, "hold": False, "reachable": True, "downstream": True, "acknowledged": False, "backup_expired": False, "model": False, "complete": False},
    {"request": "erase-1", "subject": "u1", "system": "backup-vault", "plane": "backup", "separate_basis": False, "hold": False, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": True, "model": False, "complete": False},
    {"request": "erase-1", "subject": "u3", "system": "model-registry", "plane": "model", "separate_basis": False, "hold": False, "reachable": True, "downstream": False, "acknowledged": False, "backup_expired": False, "model": True, "complete": False},
]

def evaluate(target):
    if target["separate_basis"]:
        return "retained_separate_basis"
    if target["hold"]:
        return "blocked_hold"
    if not target["reachable"]:
        return "unavailable"
    if target["downstream"] and not target["acknowledged"]:
        return "downstream_pending"
    if target["plane"] == "backup" and target["backup_expired"]:
        return "backup_aged_out"
    if target["model"]:
        return "review_required"
    if target["complete"]:
        return "verified_deleted"
    return "unavailable"

results = [evaluate(target) for target in targets]

print(f"targets={len(targets)}")
print(f"requests={len({target['request'] for target in targets})}")
print(f"verified_deleted={results.count('verified_deleted')}")
print(f"retained_separate_basis={results.count('retained_separate_basis')}")
print(f"blocked_hold={results.count('blocked_hold')}")
print(f"unavailable={results.count('unavailable')}")
print(f"downstream_pending={results.count('downstream_pending')}")
print(f"backup_aged_out={results.count('backup_aged_out')}")
print(f"review_required={results.count('review_required')}")
print(f"systems={len({target['system'] for target in targets})}")
print(f"asset_planes={len({target['plane'] for target in targets})}")
print(f"subjects={len({target['subject'] for target in targets})}")
print(f"decision_events={len(results)}")
```

The expected output reports ten targets for one request, three declared verified deletions, two separately retained targets, one hold block, one unavailable system, one downstream target pending, one expired backup cohort, one model review, ten systems, nine planes, three subjects, and ten decision events on separate lines.

The evidence is deliberately narrow. Invented Booleans and strings do not establish identity, request validity, subject relation, applicable law, grounds, exception, hold, recipient duty, backup expiry, model influence, or real system state. The evaluator trusts `complete` as verified, treats backup expiry as deletion, and makes no target-specific queries. It performs no restriction, database mutation, index invalidation, key destruction, sanitization, recipient instruction, restore test, communication, or remedy. Production assurance requires authorized profiles and determinations, identity graphs, complete reliance inventory, immutable target versions, repository-specific methods, protected tombstones, independent verification, downstream evidence, incident correction, affected-person review, and recovery exercises.

## Alternatives and Trade-Offs

**Immediate hard deletion.** Exposure ends quickly. Mistaken identity, fraud, shared records, holds, referential integrity, and recovery can make irreversible harm more likely.

**Restricted grace state.** Errors can be corrected before purge. Residual data, hidden access paths, deadlines, and user expectations require tight bounds.

**Soft deletion.** Propagation and non-resurrection are easier. Payloads remain present and can leak through forgotten queries or administrators.

**Physical row removal.** Ordinary query exposure falls. logs, pages, snapshots, replicas, indexes, and media remnants can persist.

**Cryptographic erase.** Large encrypted cohorts can become inaccessible rapidly. Key sharing, copies, caches, plaintext, escrow, and algorithm assumptions limit scope.

**Media sanitization.** Reuse and disposal assurance improve. It is too coarse for shared live storage and does not find logical copies.

**Delete all subject-linked data.** Workflows appear simple. Shared data, independent records, legal duties, security evidence, and other people's rights can be harmed.

**Purpose-specific erasure.** Retention and use remain bounded. Identity, field, purpose, lineage, and access segmentation become complex.

**Redaction or unlinking.** Other subjects and record context can remain. Residual identifiers and re-linkage require testing.

**De-identification.** Analytical value may remain. Contextual identifiability, auxiliary data, group effects, and future linkage create uncertainty.

**Central deletion orchestrator.** State, deadlines, evidence, and retries are consistent. Integration gaps and authority concentration create systemic risk.

**Federated repository deletion.** Native semantics and ownership remain local. Status, identity, verification, and timing become heterogeneous.

**Synchronous deletion.** The requester sees an immediate outcome. Fan-out, provider delay, backups, large data, and partial failure make long transactions impractical.

**Asynchronous plan.** Distributed stages and retries are explicit. Status, deadlines, idempotency, evidence, and user communication become essential.

**One deletion event.** Integration is lightweight. Lost, stale, unauthorized, or misunderstood events can create false closure.

**Target receipts and reconciliation.** Assurance improves. Sensitive evidence, adapter complexity, cost, and latency increase.

**Short-lived tombstones.** Data minimization improves. Delayed replicas, imports, clients, and backups can resurrect data.

**Long-lived suppression records.** Resurrection and prohibited contact are prevented. Minimal identity becomes a sensitive permanent control asset.

**Selective backup mutation.** Residual intervals shrink. Integrity, immutability, deduplication, provider support, and restore confidence can suffer.

**Backup aging with replay protection.** Recovery design remains stable. Data persists longer in restricted form and needs honest disclosure and testing.

**Model retraining.** Influence from removed data can be reduced under a reproducible process. Cost, time, nondeterminism, dependent versions, and proof remain hard.

**Machine unlearning.** Targeted remediation may reduce retraining cost. Method validity, attack resistance, applicability, and verification are model-specific.

**Model retirement.** Continued inference ends clearly. Replacement capacity, downstream copies, historic decisions, and retained evidence remain.

**Full deletion evidence.** Audit and dispute response improve. Receipts can recreate sensitive inventories or retain deleted payloads.

**Minimal keyed receipts.** Privacy improves. Independent verification and later explanation can become more difficult.

**Provider-native deletion.** Service semantics and infrastructure lifecycle are supported. Cross-provider consistency and independent proof are limited.

**Application-owned deletion.** Domain context and subject relationships are known. Every team must implement complex controls correctly.

**Generic DELETE endpoints.** Interfaces are familiar. HTTP semantics do not express rights profiles, target graphs, exceptions, deadlines, or proof.

**Explicit erasure resources.** Workflow semantics are clear. API surface, state, protected explanations, and operational coordination grow.

## Failure Modes and Misconceptions

**“The right to erasure is absolute.”** Applicable grounds, exceptions, duties, claims, archives, and facts can produce partial or refused outcomes.

**“Account deletion and erasure are identical.”** Accounts, subjects, records, recipients, models, and purposes have different scopes.

**“A person has only one identifier.”** Aliases, devices, accounts, tokens, and domain keys create several subject links.

**“The account holder owns all account data.”** Shared messages, households, transactions, and representatives involve other people and rights.

**“Any support message saying delete is invalid.”** Requests may be recognized through several channels under applicable rules.

**“More identity evidence is always safer.”** Excess verification collects new sensitive data and creates exclusion or breach risk.

**“One global rule can implement every erasure right.”** Jurisdiction, sector, controller, contract, age, and time can change the decision.

**“Strictest means delete everything immediately.”** That can violate holds, duties, shared rights, integrity, and authorized archives.

**“Legal is a sufficient exception.”** Authority, purpose, scope, necessity, duration, safeguards, and reviewer must be explicit.

**“Fraud prevention permits indefinite retention.”** Risk purpose and data need bounded necessity and review.

**“A legal hold permits ordinary product use.”** Preservation does not authorize marketing, profiling, or unrelated access.

**“An invoice exception preserves the whole profile.”** Separate purposes and representations require separate decisions.

**“One email address finds all data.”** Identity graphs and domain relationships are needed for complete and safe discovery.

**“Fuzzy matching can delete likely identities automatically.”** False positives can destroy another person's records.

**“Lineage decides what must be deleted.”** It proposes relationships but not identity, applicability, shared rights, or transformed status.

**“Deleting the source deletes every derivative.”** Copies, indexes, exports, features, models, and reports can remain independent.

**“A successful HTTP DELETE proves erasure.”** It concerns a resource association, not every representation or storage remnant.

**“A 204 response means physical storage was reclaimed.”** Protocol success does not specify internal lifecycle or media state.

**“Soft delete hides data from every use.”** Administrators, bugs, joins, exports, and old code can still expose it.

**“A database cascade encodes policy.”** Referential relationships do not express purposes, people, duties, or holds.

**“Dropping a row removes database history.”** logs, MVCC versions, CDC, replicas, pages, and backups can persist.

**“Delete markers destroy object versions.”** They can only change the default visible version.

**“Removing a search result erases the source.”** Delisting, index deletion, cache invalidation, and source removal are distinct.

**“Cache expiry is immediate deletion.”** Offline and layered caches can retain data until verified invalidation or bounds expire.

**“Deleting from the lake deletes exports.”** Notebooks, files, recipients, sandboxes, and derived products may remain.

**“Logs are exempt because they are technical.”** Identifiers, payloads, decisions, and behavior can be personal and purpose-bound.

**“Immutable logs can never support erasure.”** Architecture can minimize payload, separate keys, bound retention, redact, or retain under authority.

**“Pseudonymization is anonymous deletion.”** Linkage, auxiliary information, and unique behavior can preserve identifiability.

**“Hashing an identifier erases it.”** Small domains, stable linkage, and retained mappings can permit recovery or association.

**“Aggregation always removes personal data.”** Small groups, outliers, repeated queries, and auxiliary data can reveal individuals.

**“Deleting one encryption key erases one subject.”** Keys may cover many subjects or have copies, wrapping keys, and plaintext replicas.

**“Cryptographic erase proves physical destruction.”** It proves bounded infeasibility only under key, algorithm, ciphertext, and threat assumptions.

**“Media sanitization finds every logical copy.”** Inventory and lineage remain separate requirements.

**“Processors delete when notified.”** Delivery, identity, interpretation, technical execution, and evidence can fail.

**“Recipient notification is completion.”** Acknowledgement and verified target outcomes remain.

**“Public data can always be removed everywhere.”** Independent republication and parties outside control limit practical reach.

**“Backups must always be rewritten immediately.”** Applicable profiles, provider architecture, immutability, risk, and replay controls determine treatment.

**“Backups never need deletion controls.”** Residual duration, ordinary access, new copies, restore, and final expiry must be governed.

**“Stopping new backups erases old snapshots.”** Existing cohorts persist until expiry, purge, or verified crypto erase.

**“Removing training rows unlearns a model.”** Checkpoints and weights can retain influence.

**“A model can always delete one person's influence.”** Technical methods and verification may be unavailable or unreliable.

**“A deletion event proves consumer enforcement.”** Delivery and acknowledgement do not prove target outcome.

**“Last event wins.”** Subject, object generation, scope, causation, and effective time determine whether a stale create may apply.

**“Tombstones can disappear after replication catches up.”** Offline clients, imports, archives, and backups may have longer resurrection horizons.

**“Deletion receipts should include the deleted record.”** That can recreate the very data and risk the process intended to remove.

**“Zero failed jobs proves full deletion.”** Unknown systems and missing targets can sit outside the attempted denominator.

**“A provider timeline is an enterprise guarantee.”** Service scope, contract, customer configuration, recipients, and local copies remain.

**“Deleting the wrong subject is reversible from backup.”** Restoration can violate other deletions, holds, and current authority.

**“Migration can discard old tombstones.”** Doing so lets legacy imports and delayed events resurrect erased data.

**“A clean restore can enable users immediately.”** Current deletion, restriction, hold, and recipient state must be replayed first.

## Worked Examples

### Example 1

A person closes a shopping account and requests erasure. The determination deletes profile, personalization, marketing, search, and cache targets while retaining minimized invoices under a separate duty. Invoice access is segregated from product use, and the response explains the partial outcome without exposing internal legal strategy.

### Example 2

A representative requests deletion for a child. The system verifies representative authority and the child's identities without treating the representative's account as the subject. It finds a family photograph involving two siblings and routes redaction and access review instead of deleting the shared object blindly.

### Example 3

An API returns `202 Accepted` for an erasure resource. The orchestrator first restricts reads and marketing, then deletes database rows, history, indexes, vectors, queues, and cache keys. Target receipts and negative queries eventually move the request from executing to verified closure.

### Example 4

A storage object has three versions, one under legal hold. A simple delete creates a marker but preserves every version. The plan reports the held version as separately retained, deletes eligible generations only, and recomputes the remaining action when the hold releases.

### Example 5

A recipient mailing provider acknowledges an instruction but its target count is zero because an alias mapping was missing. Reconciliation detects the mismatch against the export manifest, opens an incident, supplies the authorized alias reference, and verifies suppression and content deletion before closure.

### Example 6

A backup cohort cannot be selectively rewritten. Deleted subjects are removed from active systems and new backups; old encrypted backups remain restricted until a fixed expiry. Restore automation loads tombstones first, filters restored content before release, and destroys the transient recovery copy afterward.

### Example 7

A research dataset is transformed into aggregates. Review tests group sizes, rare combinations, auxiliary linkage, repeated releases, and recipient controls. Some outputs meet the approved de-identification criterion; an outlier table remains personal and is deleted rather than mislabeled anonymous.

### Example 8

A model used one person's support text. The plan deletes source, vectors, prompt logs, queued examples, and evaluation copies. Model experts find no validated target-specific unlearning method, so they restrict and retire the affected checkpoint at replacement rather than claiming the influence was erased.

### Example 9

A search-engine request results in delisting for a named query while the publisher retains source content under a separate decision. The architecture records query, result relation, search index, source, controller, decision, and effect independently, avoiding the false statement that the web page was deleted.

### Example 10

After disaster recovery, an old stream replays a `profile-created` event. The ingestion gate compares event time and object generation with a durable protected tombstone and rejects resurrection. Reconciliation verifies that no downstream consumer rebuilt the profile or recommendation vector.

## Cross-Program Connections

**Privacy Engineering.** Rights, identity, purpose, grounds, exceptions, minimization, de-identification, transparency, shared data, complaints, and remedy define the human outcome.

**Security Engineering.** Authentication, authorization, integrity, media sanitization, cryptographic erase, key custody, malicious deletion defense, audit, incident response, and recovery protect the process.

**Data Engineering.** Databases, CDC, streams, compaction, lakes, indexes, caches, exports, lineage, replicas, and orchestration determine where deletion must act.

**Machine Learning Engineering.** Training data, features, embeddings, prompts, outputs, checkpoints, memorization, unlearning, retraining, filtering, and retirement complicate erasure claims.

**API and Service Engineering.** Explicit request resources, idempotency, asynchronous state, versioned targets, protected errors, events, retries, acknowledgements, and receipts expose workflows safely.

**Platform Engineering.** Identity graphs, catalogs, policy, adapter SDKs, queues, tombstones, lifecycle controls, provider integrations, dashboards, and recovery make erasure operable at scale.

**Distributed Systems.** Event ordering, object generations, replication, caches, partitions, partial failure, delayed clients, retries, and restore create non-resurrection challenges.

**Records and Information Management.** Schedules, legal holds, archival transfer, official records, evidence, and defensible disposition constrain destructive action.

**Human-Computer Interaction.** Request discovery, language, accessibility, authentication burden, scope selection, status, explanation, appeals, and reassurance shape meaningful control.

**Governance, Risk, and Compliance.** Applicable profiles, authority, processors, recipient obligations, deadlines, refusals, exceptions, evidence, audit, and regulatory change govern decisions.

**Site Reliability Engineering.** Safe rollout, deletion SLOs, backpressure, provider outages, restore, backup cohorts, failure injection, incidents, and capacity determine reliable execution.

**Ethics and Responsible Innovation.** Group data, public memory, vulnerable people, power, historical value, scientific integrity, fairness, and community governance exceed individual database rows.

## References

1. European Union, [“Regulation (EU) 2016/679 (General Data Protection Regulation)”](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679), 2016. Retrieved 2026-09-03.
2. UK Information Commissioner's Office, [“Right to Erasure”](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/), retrieved 2026-09-03.
3. European Data Protection Board, [“Guidelines 5/2019 on the Criteria of the Right to Be Forgotten in Search Engine Cases”](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-52019-criteria-right-be-forgotten-search-engines_en), 2020. Retrieved 2026-09-03.
4. California Privacy Protection Agency, [“California Consumer Privacy Act Statute and Regulations Effective January 1, 2026”](https://cppa.ca.gov/regulations/pdf/ccpa_statute_eff_20260101.pdf), 2026. Retrieved 2026-09-03.
5. National Institute of Standards and Technology, [“SP 800-88 Revision 2: Guidelines for Media Sanitization”](https://csrc.nist.gov/pubs/sp/800/88/r2/final), 2025. Retrieved 2026-09-03.
6. National Institute of Standards and Technology, [“SP 800-53 Release 5.2.0: Security and Privacy Controls for Information Systems and Organizations”](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), 2025. Retrieved 2026-09-03.
7. Internet Engineering Task Force, [“RFC 9110: HTTP Semantics”](https://www.rfc-editor.org/rfc/rfc9110.html), 2022. Retrieved 2026-09-03.
8. Google Cloud, [“Data Deletion on Google Cloud”](https://docs.cloud.google.com/docs/security/deletion), updated 2024. Retrieved 2026-09-03.
9. Microsoft, [“Data Retention, Deletion, and Destruction in Microsoft 365”](https://learn.microsoft.com/en-us/compliance/assurance/assurance-data-retention-deletion-and-destruction-overview), 2025. Retrieved 2026-09-03.
10. Amazon Web Services, [“Locking Objects with Object Lock”](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html), retrieved 2026-09-03.
11. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/prov-o/), 2013. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design an erasure determination for a commerce platform covering account data, orders, invoices, support, marketing, fraud, security logs, shared reviews, recommendations, processors, and backups. Specify identity, grounds, exceptions, purposes, deadlines, responses, appeals, and evidence.

### Exercise 2

Design a deletion target and propagation graph for relational databases, event streams, object stores, indexes, caches, warehouses, notebooks, exports, recipient systems, models, replicas, and backup cohorts. Define action, dependency, version, verification, failure, and non-resurrection behavior.

### Exercise 3

Design an erasure API and orchestration control plane. Include intake, authentication, idempotency, asynchronous states, determination, target manifests, adapters, events, retries, receipts, metrics, protected explanations, incidents, and recovery.

### Exercise 4

Evaluate logical deletion, redaction, de-identification, physical purge, cryptographic erase, media sanitization, backup aging, retraining, unlearning, and model retirement for health research data. State threat models, assumptions, evidence, limitations, and communication.

### Exercise 5

Plan migration from account-deletion endpoints, Boolean flags, nightly scripts, ad hoc processor emails, and undocumented backup behavior to authoritative erasure governance. Include discovery, source preservation, mapping, unknowns, dual execution, canaries, remediation, tombstone replay, recovery, and retirement criteria.

## Answers to the Exercises

### Answer 1

Represent requester, subject, accounts, aliases, devices, household relations, guardians or agents, and verification evidence separately. Select an effective-dated jurisdiction and controller profile with grounds, exceptions, timing, communication, extension, refusal, and appeal. Evaluate account service, order fulfillment, invoice and tax records, customer support, marketing, personalization, fraud, security, reviews, processor relationships, and backup lifecycle as distinct purposes and representations.

Grant deletion for profile, optional personalization, marketing content, search and cache entries, and unsupported fraud attributes. Retain minimized invoices and security or claim evidence only under specific current authority, segregated access, bounded schedules, and no product reuse. Shared reviews require author unlinking, redaction, or retained attribution decisions that protect other participants and public context. Holds block only covered destructive actions. The response states granted, retained, recipient, backup, unavailable, and refused outcomes without exposing another person or privileged matter.

Build targets across rows, temporal history, CDC, objects, versions, indexes, caches, messages, reports, exports, processors, replicas, snapshots, and recovery. First restrict prohibited use, then execute dependency-aware actions. Verify repository state, recipient acknowledgements, backup cohort expiry, and non-resurrection. Evidence records identity confidence, decision version, target outcomes, limitations, response, and remedy under its own retention schedule.

### Answer 2

Create stable subject edges and immutable target identities for database rows and history, stream events and partitions, object generations, index documents, cache keys, warehouse tables and rows, notebook files, export manifests, recipient references, feature vectors, datasets, checkpoints, replicas, snapshots, and backup cohorts. Each edge records source, derivation semantics, purpose, basis, subjects, owner, location, retention, deletion capability, and evidence; lineage proposes scope but authorized review decides transformed and shared nodes.

Order operations to stop use and new propagation, write protected tombstones, remove queues and scheduled jobs, delete authoritative content, invalidate indexes and caches, update derived stores, instruct recipients, address model artifacts, stop new backup capture, and track existing cohorts. Bind every action to object generation and decision version. Adapters report discovered, retained, hold-blocked, restricted, queued, logical, purge-pending, recipient-pending, backup-aging, model-review, complete, failed, unavailable, and unverifiable states.

Events use effective and record time and stable idempotency keys. Consumers reject stale creation or update events against tombstones. Verification combines direct absence or restriction queries, version inventory, cache and index probes, export reconciliation, recipient target counts, key evidence, backup expiry, model actions, and restore exercises. Failed or unknown nodes remain in the denominator with escalation. Closure removes temporary artifacts and access but retains the minimum request and receipt graph needed to prevent resurrection and explain the outcome.

### Answer 3

The intake API accepts channel, authenticated requester, subject and representative evidence, requested scope, accessibility and communication preferences, and idempotency key. It returns request ID, received time, recognized scope, deadline basis, verification needs, and safe status without enumerating sensitive accounts. A determination resource records applicable profile, grounds, purposes, data, retained exceptions, recipients, actions, deadline, reviewer, explanation, appeal, version, and expiry.

The orchestrator compiles an immutable versioned target manifest and dependency graph. It restricts product access, writes minimal tombstones, dispatches repository-specific commands, receives idempotent receipts, retries bounded failures, verifies independent observations, coordinates processors, tracks backups and models, and closes only after every target is completed, retained-authorized, externally assigned, or unresolved with active escalation. Adapter capability records state granularity, supported methods, latency, reversibility, holds, verification, provider residuals, and recovery behavior.

Events cover request, verification, determination, discovery, restriction, action, acknowledgement, exception, failure, backup, model review, response, appeal, correction, and closure. Metrics use expected targets and systems as denominators. Evidence is minimized and access-separated. Incidents address wrong-subject deletion, continued use, resurrection, missed recipients, overretention, and false closure. Recovery restores current decisions, tombstones, holds, receipts, and backup rules before product data, quarantines stale content, replays actions, and verifies cleanup.

### Answer 4

For each data class—clinical observations, identifiers, free text, genomic relations, images, research measurements, derived features, aggregates, prompts, outputs, training sets, and model versions—identify subjects, other affected people, purpose, basis, consent, protocol, claims, archives, holds, recipients, and current retention. Define the required outcome and threat model before selecting mechanics.

Logical deletion quickly blocks normal use but leaves remnants. Redaction can protect one subject in shared records but may harm meaning. De-identification requires contextual reidentification testing and governance. Physical purge removes addressable objects while storage remnants can await sanitization. Crypto erase requires unique key-to-data mapping, complete key destruction, no plaintext copies, and trusted algorithms. Media sanitization applies to reuse or disposal under an approved standard. Backup aging needs isolation, bounded expiry, and tombstone-first restore.

For ML, remove source, features, vectors, queues, manifests, evaluation data, prompts, outputs, and copies. Evaluate retraining, validated unlearning, filtering, access restriction, checkpoint retirement, or documented residual. Preserve scientific and regulatory records only under separate authority and access. Evidence states method, target, tool and version, tests, actor, time, residuals, and limitations. Communication distinguishes immediate restriction, active deletion, backup timing, retained records, recipient state, and model uncertainty without claiming anonymity or unlearning beyond proof.

### Answer 5

Inventory every endpoint, flag meaning, subject identifier, table, object, job, script, queue, event, processor, email instruction, export, index, cache, model, replica, snapshot, backup policy, request record, exception, hold, receipt, and restore path. Preserve authoritative legacy sources and sample outcomes under restricted access. Define canonical request, identity, profile, determination, target, method, state, event, recipient, tombstone, backup cohort, model action, evidence, and closure objects.

A legacy `deleted = true` becomes a scoped assertion with system, object, generation if known, time, actor, and limitations—not verified enterprise erasure. Discover orphan systems through catalogs, code, network, identities, vendor contracts, lineage, provider inventory, restoration exercises, and stakeholder interviews. Unknown subject mapping, target version, exception, processor, backup behavior, or actual outcome remains unknown and enters remediation rather than being relabeled complete.

Dual-evaluate determinations and target plans, shadow events, compare target counts, canary low-risk repository adapters, and then execute approved cohorts with recovery boundaries. Replay historical tombstones before imports and restored data. Reconcile recipients, backups, models, and failed targets. Register consumers, retire ad hoc emails and scripts, block legacy endpoint writes, revoke unsafe permissions, and update incident and recovery runbooks. Closure proves no API, job, delayed event, import, replica, recipient, or restore path treats an ambiguous Boolean as complete erasure while required historical evidence remains interpretable.
