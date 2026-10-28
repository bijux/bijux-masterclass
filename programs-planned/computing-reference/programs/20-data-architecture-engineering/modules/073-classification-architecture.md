---
module_id: DARCH-073
program: Data Architecture Engineering
level: 2
module_number: 73
title: Classification Architecture
status: complete
last_verified: 2026-09-03
---

# Classification Architecture

## One-Page Review

### Governing question

How should an organization identify and maintain decision-relevant classes of data across fields, records, datasets, products, systems, copies, transformations, and lifecycle states so controls respond to actual meaning and consequence rather than to one ambiguous label or unreliable automated guess?

### Essential definitions

- **Classification** is an attributable decision that an information object belongs to one or more defined classes for a stated purpose, scope, time, and authority.
- A **classification scheme** is a governed set of stable class identities, definitions, relations, decision rules, authorities, versions, and lifecycle states.
- An **information type** characterizes what information denotes or supports, independently of its current storage format and protection level.
- A **classification axis** is one dimension of concern, such as confidentiality impact, integrity impact, availability impact, privacy category, legal authority, business criticality, dissemination, retention, or quality.
- A **class assertion** links a governed object to a class with axis, scope, basis, evidence, issuer, confidence or review state, effective interval, and limitations.
- A **label** is a human- or machine-readable lexical representation of a class; it is not the class identity.
- A **marking** is a visible or encoded indicator intended to communicate classification or handling at a boundary; an absent, stale, or forged marking does not determine the underlying class.
- A **handling rule** states controls for collection, access, storage, processing, display, copying, transmission, sharing, logging, retention, deletion, incident response, and recovery under specified conditions.
- **Security categorization** evaluates potential impact to confidentiality, integrity, and availability; those axes need not have the same value.
- **Privacy classification** identifies personal-data relationships, identifiability, sensitivity, context, purpose, affected population, and possible adverse effects; it is not exhausted by a `PII` Boolean.
- **Dissemination classification** constrains which communities may receive information and under what redistribution conditions; it is distinct from content sensitivity and system impact.
- **Derived classification** is the result of an explicit transformation rule applied to inputs, operation semantics, output, purpose, and evidence—not blind propagation of the maximum input label.
- **Declassification or decontrol** is an authorized decision that a class or control no longer applies under stated conditions; deleting a tag is not proof of that decision.
- **Inference** proposes a classification from content, structure, lineage, context, or models; **verification** is an accountable acceptance for a stated control scope.
- **Closure** ends active class assertions, markings, policy, access, copies, automation, exceptions, and recovery dependencies while retaining required historical evidence.

### Central model, mechanism, or theorem

Represent a classification architecture as:

`C = (S, O, A, B, E, P, H, V, R, L)`

where `S` is schemes and stable class identity, `O` governed objects and granularity, `A` independent classification axes, `B` authoritative basis, `E` evidence and assertion state, `P` propagation and transformation, `H` handling and enforcement, `V` versions and effective time, `R` review, correction, and reclassification, and `L` lifecycle and closure. No scalar label can preserve every relevant distinction. Effective controls must evaluate a scoped vector of current assertions plus purpose, operation, environment, jurisdiction, consumer, and uncertainty.

### Critical invariants

- Scheme, class, label, marking, assertion, information object, handling rule, control, and observed outcome have separate identities.
- Every class assertion names object and version, axis, class, basis, evidence, issuer, review state, scope, effective time, and limitations.
- Confidentiality, integrity, availability, privacy, legal, dissemination, retention, criticality, and quality concerns do not silently collapse into one ordered scale.
- Unknown, mixed, disputed, inferred, stale, not applicable, decontrolled, and verified states remain distinguishable.
- Classification follows the smallest governable object and explicitly aggregates to fields, records, datasets, products, systems, and physical media.
- Derived outputs receive classifications through reviewed transformation rules and output evidence; encryption, hashing, aggregation, masking, or tokenization do not automatically remove class.
- Markings communicate current decisions but do not create authority, replace metadata, or prove correct handling.
- Automated findings cannot silently become high-consequence enforcement facts without calibrated evidence and authorized review.
- Access, masking, sharing, retention, deletion, monitoring, incident, and recovery controls resolve from applicable assertions and context, not from label text alone.
- Reclassification preserves prior assertions and identifies affected copies, decisions, consumers, models, and evidence.
- Declassification and decontrol require authorized conditions, proof of execution, and control over later restoration or replay.
- Metrics publish denominators and distinguish inventory, assertion coverage, review state, control activation, effectiveness, incidents, and outcomes.

### Common failures

Common failures include calling all sensitive data confidential; treating `PII` as a universal yes-or-no property; using one public/internal/confidential scale for every concern; letting a file suffix define class; assuming the highest source label always describes a derived output; assuming encryption reduces classification; treating a hash as anonymous; propagating privacy classes through every lineage edge; dropping labels after aggregation without testing reidentification; trusting column-name regexes; accepting classifier confidence as authority; storing only current labels; making markings optional metadata with no downstream enforcement; granting access from classification alone; mapping different schemes by color or ordinal position; classifying systems but not fields or exports; ignoring free text, logs, backups, caches, prompts, and model features; and restoring decontrolled data and obsolete policies during recovery.

### Compact example

Six invented source fields are described across five axes and five derived assets receive declared outcomes. One derived asset is public, two internal, and two restricted. One source is a direct identifier; two derived assets are pseudonymous. Three retention classes, two high-integrity sources, and one high-availability source appear. Two derived assets require manual review and one remains unresolved. Executable evidence confirms only those declarations and counts. It proves no real class, authority, sensitivity, reidentification risk, handling control, compliance, or outcome.

### Connections

[DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md), [DARCH-061](061-metadata-architecture.md), [DARCH-064](064-lineage-architecture.md), [DARCH-070](070-connecting-technical-metadata-to-business-meaning.md), [DARCH-071](071-federated-data-governance.md), and [DARCH-072](072-policy-as-code-for-data.md) establish vocabulary, metadata, provenance, semantics, authority, and executable policy foundations. [DARCH-074](../ROADMAP.md) next develops consent and purpose limitation.

## Governing Question

The same data can be low confidentiality, high integrity, high availability, personally identifying, subject to a specific statute, restricted to a partner community, retained for seven years, and unsuitable for an automated decision. A single `confidential` label cannot express those facts or their different authorities.

The governing question is how to preserve those distinctions as data moves and changes. A durable architecture classifies governed objects through versioned schemes and attributable assertions, treats uncertainty explicitly, derives handling from context, observes enforcement, and supports correction and decontrol. Classification is a decision system embedded in the data lifecycle, not a one-time scanning campaign.

## Why This Matters

NIST [FIPS 199](https://csrc.nist.gov/pubs/fips/199/final) categorizes federal information and systems by potential impact to confidentiality, integrity, and availability using low, moderate, and high impact values. It demonstrates that security categorization is multidimensional and consequence-based. Its federal scope and high-water-mark rules should not be copied into unrelated contexts without authority and analysis.

NIST [SP 800-60 Volume I Revision 1](https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final) provides a methodology for mapping information types and systems to security categories and provisional impact levels. The method begins with information type and adjusts provisional values using organizational context. This separates semantic identification from consequence assessment and control selection.

NIST [SP 800-122](https://csrc.nist.gov/pubs/sp/800/122/final) gives context-based guidance for identifying personally identifiable information and choosing protection levels. It emphasizes inappropriate access, use, and disclosure and connects PII confidentiality to broader privacy principles. Identifiability and harm depend on combinations, context, and environment rather than names alone.

NIST's [Protecting Controlled Unclassified Information FAQ](https://csrc.nist.gov/Projects/protecting-controlled-unclassified-information/faqs) describes the U.S. CUI program, points to registry categories, and identifies designation, safeguarding, dissemination, marking, decontrol, disposal, oversight, and responsible authority. The CUI program is jurisdiction-specific. Architecturally, it shows why protected classes need authoritative definitions, legal or policy bases, approved notations, dissemination controls, and decontrol procedures.

The Forum of Incident Response and Security Teams publishes [Traffic Light Protocol 2.0](https://www.first.org/tlp/) for indicating how recipients may share potentially sensitive information. TLP is a dissemination protocol, not a general measure of confidentiality impact, legal category, or storage requirement. `TLP:AMBER` and a corporate amber color must never be assumed equivalent.

The UK Cabinet Office [Government Security Classifications Policy](https://www.gov.uk/government/publications/government-security-classifications/government-security-classifications-policy-html) defines OFFICIAL, SECRET, and TOP SECRET tiers plus baseline behaviors and additional markings for UK government information. Its scope is specific. It illustrates the link among assessed threat and damage, accountable handling, markings, suppliers, reclassification, and legacy information.

W3C [SKOS](https://www.w3.org/TR/skos-reference/) represents concept schemes, stable concepts, lexical labels, notations, definitions, scope and history notes, semantic relations, collections, and mappings. It can exchange a classification vocabulary while distinguishing class concepts from labels. SKOS does not establish legal authority or automatically infer handling controls.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) models entities, activities, agents, derivation, attribution, association, delegation, and qualified relations. A classification assertion needs provenance: which scanner or steward acted, from which evidence, under which activity and authority. Provenance explains origin and change; it does not prove the assertion correct.

W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) distinguishes dimensions, metrics, measurements, policies, annotations, standards, and provenance. Classification quality can be measured by sampled precision, review agreement, staleness, coverage, and control activation. These measurements must name denominator, resource, method, producer, and limitations.

W3C [ODRL 2.2](https://www.w3.org/TR/odrl-model/) expresses permissions, prohibitions, duties, constraints, parties, assets, actions, profiles, and conflict strategies. Classification assertions can inform usage policies, but a class does not itself grant or deny. Purpose, party, action, jurisdiction, obligations, and applicable authority still determine the decision.

W3C [SHACL](https://www.w3.org/TR/shacl/) validates RDF graphs against shapes and returns validation results with severities. A profile can require class identity, scheme version, issuer, evidence, time, and review state. Shape conformance establishes declared graph structure under that evaluation, not the truth of the classification or adequacy of handling.

Together these sources support consequence-based security categories, contextual privacy identification, authority-backed protected categories, bounded dissemination markings, interoperable schemes, provenance, quality evidence, policy links, and structural validation. The organization must still design its own authorized axes, transformations, controls, and assurance.

## Prerequisites and Retrieval

You should understand data governance, metadata, concept schemes, security risk, privacy, legal and contractual obligations, identity, access control, data lineage, quality, schemas, transformations, storage, distributed systems, machine learning, audit, incident response, records management, recovery, and lifecycle management.

Retrieve classification, categorization, information type, scheme, class, concept, label, notation, marking, banner, caveat, axis, confidentiality, integrity, availability, privacy, personal data, identifier, pseudonymity, anonymity, criticality, dissemination, retention, legal authority, assertion, basis, evidence, provenance, confidence, verification, scope, aggregation, high-water mark, propagation, derivation, transformation, downgrading, reclassification, declassification, decontrol, handling, enforcement, exception, and closure.

As a retrieval test, inspect a column called `customer_hash` marked `internal`. Ask which hash algorithm, salt or key, input namespace, linkability, population, attacker data, and purpose apply; whether the source is personal or specially protected; which confidentiality, integrity, availability, retention, legal, and dissemination axes apply; who asserted `internal`; whether the label is current; which transformations and joins can reidentify subjects; which controls follow; and how deletion and recovery work. The name, hash, and label answer none of those questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish information types, classification schemes, class identities, assertions, labels, markings, handling rules, controls, and outcomes;
2. design multidimensional classification across security impact, privacy, legal, dissemination, retention, criticality, and quality concerns;
3. select classification granularity for fields, records, datasets, products, systems, media, copies, and derived outputs;
4. define authoritative assertions with basis, evidence, provenance, confidence or review state, versions, time, and limitations;
5. specify aggregation and transformation rules for joins, filters, masking, encryption, tokenization, hashing, aggregation, and release;
6. evaluate automated discovery and machine-learning classification with representative evidence, thresholds, abstention, review, and drift;
7. connect classification to access, masking, storage, transfer, sharing, retention, deletion, monitoring, incident, and recovery policy;
8. operate APIs, events, synchronization, observability, exceptions, correction, reclassification, and decontrol;
9. compare high-water-mark, risk-based, rule-based, inherited, and output-tested approaches; and
10. migrate and retire classification schemes while preserving historical interpretation and blocking obsolete reactivation.

## Core Exposition

**Begin with decisions and harms.** Inventory collection, access, modification, publication, export, retention, deletion, model training, automated decision, incident, and recovery decisions. Identify affected people, mission, assets, obligations, and credible adverse effects.

Classification exists to make those decisions more accurate and consistent. A label inventory without a decision and control map measures annotation activity, not governance value.

**Separate classification from categorization.** Organizations use the terms inconsistently. Define them locally. One useful distinction is classification as membership in information or handling classes and categorization as consequence or risk levels across defined objectives.

Do not rely on the English word to carry semantics. Use stable scheme and class identifiers in interfaces and evidence.

**Design independent axes.** Common axes include information type, confidentiality impact, integrity impact, availability impact, privacy category, identifiability, legal or regulatory basis, contractual restriction, intellectual property, export control, dissemination, records class, retention, business criticality, safety, quality, and decision consequence.

Not every asset needs every axis, but an omitted axis must be not applicable or unknown rather than silently mapped to `low`.

**Avoid the universal sensitivity ladder.** Public, internal, confidential, and restricted can be useful for one confidentiality scheme. They do not express integrity, availability, retention, privacy purpose, legal authority, or dissemination community.

Use composite views for users while preserving source assertions. A user-friendly badge can summarize controls but must link to complete current context.

**Give schemes stable identity.** Record issuing authority, namespace, purpose, scope, class definitions, notations, relations, mappings, rules, versions, effective intervals, change history, deprecation, and retirement.

Never reuse a class identifier for materially different meaning. Preserve old versions so historical decisions and markings can be interpreted.

**Define classes precisely.** A class definition includes inclusion and exclusion criteria, examples, counterexamples, scope, basis, expected evidence, controlling authority, related classes, default handling profile, and exceptions.

Avoid circular definitions such as “restricted data is data requiring restricted handling.” The class and its default controls are related but distinct.

**Treat labels as lexical aids.** Preferred, alternative, abbreviated, translated, legacy, and hidden labels support presentation and search. A color, word, acronym, or ordinal is meaningful only inside its scheme and version.

Never map `red`, `secret`, level 3, or `restricted` across schemes by display equality. Use reviewed mappings with scope and loss.

**Treat markings as communication.** Markings can appear in headers, files, documents, messages, schemas, APIs, user interfaces, exports, and physical media. They help recipients recognize and handle data.

Marking must derive from current authoritative assertions and survive supported transformations. An unmarked object can still be protected; a forged or stale marking cannot authorize release.

**Model class assertions.** Store object identity and version, axis, class identity and version, basis, evidence, issuer, method, confidence, review state, reviewer, scope, effective interval, creation time, supersession, and limitations.

Multiple assertions can coexist from different authorities. Preserve conflict and route adjudication rather than overwriting with last writer wins.

**Define assertion states.** Useful states include proposed, inferred, verified, disputed, stale, superseded, decontrolled, rejected, and retired. Confidence and authority are separate.

A high-confidence scanner result can remain inferred. A verified assertion can later become stale when source content or scheme changes.

**Classify at governable granularity.** Objects can be field definitions, field values, records, partitions, files, tables, streams, topics, messages, datasets, data products, reports, features, models, prompts, logs, backups, and physical media.

Choose the smallest object for which identity, policy, lineage, and enforcement are reliable. Finer granularity without operational support creates false precision.

**Separate schema and instance classes.** A schema can declare that a field is expected to contain direct identifiers. A particular record can be null, synthetic, corrupted, or unexpectedly contain a different sensitive value.

Use schema assertions for design and baseline controls and instance discovery for validation and exceptional content. Do not let sampling prove every record safe.

**Aggregate explicitly.** A table classification can be the maximum, union, rule-based composition, distribution, or risk assessment of field and record assertions depending on the axis and decision.

Publish the aggregation function, input scope, unknown behavior, overrides, and rationale. FIPS-style high-water marks suit some system security categorization but can be wrong for retention, dissemination, or output release.

**Model mixed content.** A file can contain public instructions and protected attachments; a table can contain identifiers and public codes; a stream can interleave tenants and classes.

Use component assertions where enforcement supports them. Otherwise classify and handle the enclosing object for the most constraining credible content while recording the mixture.

**Identify information type before impact.** Determine what the data represents, whose activities it supports, source authority, population, purpose, and use. Then assess potential effects of disclosure, modification, loss, or misuse.

Starting with a preferred protection level encourages labels chosen to justify existing controls rather than consequences.

**Keep confidentiality, integrity, and availability separate.** Public safety schedules can be public yet high integrity and availability. A confidential archive can require high confidentiality but low immediate availability.

System-level decisions aggregate resident information and mission dependencies. Document why values were raised or lowered and who accepted the assessment.

**Model privacy context.** Record relationship to individuals, identifiability, linkability, inference, sensitivity, population, purpose, power, scale, retention, sharing, decision consequence, and likely adverse effects.

Do not assume non-PII is privacy-neutral. Group, household, device, behavioral, aggregate, and inferred data can create risks even when direct identifiers are absent.

**Distinguish direct, indirect, and pseudonymous identifiers.** Direct identifiers name or uniquely contact a person. Indirect attributes can identify in combination. Pseudonymous identifiers remain linkable under keys, tables, context, or outside knowledge.

Anonymity is a claim about realistic identification risk under a stated data environment and time, not a string transformation name.

**Link protected categories to authority.** Legal, regulatory, contractual, export, records, and sector classifications name exact basis, jurisdiction, covered objects, applicable conditions, authority, effective time, and required controls.

A generic `regulated` tag cannot tell a consumer which duties conflict, which rights apply, or when decontrol is possible.

**Separate dissemination from sensitivity.** Traffic-light or community labels state who may share information and with whom. They need not rank inherent harm or define storage, encryption, retention, or deletion.

Preserve originator authority, recipients, redistribution rules, expiry, and released versions. Do not infer public release merely because a message was widely distributed inside one community.

**Model criticality and business value independently.** Critical reference data may be public. Highly confidential research may be noncritical to immediate operations. Controls for availability, resilience, integrity, recovery, and investment depend on this difference.

Avoid calling high-value data more confidential by default. Value can arise from accuracy, uniqueness, timing, or collective use.

**Connect classification to handling profiles.** Map scoped assertions plus purpose, actor, action, environment, jurisdiction, and lifecycle state to access, masking, encryption, network, location, copying, sharing, logging, retention, deletion, incident, and recovery controls.

Keep default profiles versioned and attributable. Permit justified product-specific strengthening and controlled exceptions without changing class definitions.

**Do not grant from class alone.** Classification supplies attributes for policy. Authorization also requires principal, action, resource, purpose, relationships, context, obligations, and current authority.

`public` can mean disclosure is generally allowed, not that anyone may modify, delete, impersonate a source, or bypass rate and integrity controls.

**Design derivation functions.** For each transformation type and axis, specify inputs, operation semantics, output tests, attacker or consumer context, loss, unknown behavior, authority, and review.

Different axes propagate differently. A join can increase identifiability; aggregation can reduce disclosure while increasing decision criticality; filtering can preserve confidentiality; redaction can fail on free text.

**Treat encryption as a control, not reclassification.** Ciphertext can reduce exposure under a threat model while keys, metadata, access paths, endpoints, and plaintext recovery remain.

Keep underlying content classification and record encryption state, algorithm, key authority, scope, and evidence separately. Decrypted output restores full handling requirements.

**Treat tokenization and hashing contextually.** Deterministic tokens can support linkage. Unsalted hashes over small domains can be reversed. Keyed tokens remain reidentifiable by an authority.

Classify outputs using linkability, key separation, attack data, population, purpose, access, and combination risk rather than method names.

**Validate masking and redaction.** Test every format, encoding, nested structure, free-text pattern, image, attachment, export, error, and alternative path. Record what information remains.

Masking a display does not protect query predicates, counts, timing, cache keys, logs, or raw exports.

**Assess aggregation and release.** Define minimum groups, dominance, outliers, differencing, repeated queries, external auxiliary data, longitudinal linkage, and update behavior.

A safe-looking aggregate can reveal individuals through small cells or subtraction. Release classification is relative to the publication environment and attack model.

**Use lineage as candidate propagation.** Lineage identifies transformations and downstream objects that may require classification. It does not prove semantics or correct propagation.

Apply transformation-specific rules and validate outputs. Preserve source and rule versions so a change can trigger bounded impact analysis.

**Govern copies and exports.** New location, custodian, format, jurisdiction, recipient, purpose, retention, and access path can change applicable assertions and controls even when bytes are identical.

Register copy identity and relationship, transfer decision, markings, policy, receipt, expiry, onward-sharing rules, and deletion evidence.

**Classify operational metadata.** Catalog descriptions, lineage, schemas, query histories, quality results, policy decisions, access logs, incident evidence, and classification metadata can reveal sensitive structure and activity.

Apply their own assertions and access rules. Hiding all metadata can impede safe discovery, so separate public summaries from protected details.

**Cover unstructured and multimodal data.** Free text, documents, source code, images, audio, video, prompts, responses, embeddings, and attachments can contain unexpected or inferred classes.

Use format-aware extraction, bounded models, sampling, human review, and containment. Preserve original evidence securely and record unsupported formats.

**Design automated discovery as candidate generation.** Rules can inspect names, types, formats, dictionaries, checksums, values, entropy, context, and lineage. Models can classify documents and infer entities.

Store method, feature or rule version, evidence summary, evaluation population, score semantics, threshold, state, and limitations. Separate detection confidence from class probability and policy authority.

**Evaluate classifiers by consequence.** Build representative labeled sets across domains, languages, formats, rarity, ambiguity, protected groups, and adversarial cases. Measure precision, recall, abstention, calibration where applicable, reviewer disagreement, and control impact.

High false negatives can expose data; high false positives can block legitimate use and overload review. Choose thresholds by class and action, not one global score.

**Preserve abstention and unknown.** Unsupported format, encrypted content, insufficient context, low confidence, or model disagreement should create a visible review or containment state.

Forcing every object into a known class produces false certainty. Set safe interim handling proportional to consequence.

**Design human review.** Route candidates to authorized reviewers with object context, source evidence, values only when permitted, definitions, examples, lineage, model rationale, current controls, and consumer impact.

Record acceptance, correction, rejection, conditions, disagreement, reviewer authority, and expiry. Use outcomes for evaluation under leakage and bias controls.

**Detect classification drift.** Trigger review on schema, content distribution, source, transformation, purpose, consumer, jurisdiction, scheme, authority, threat, or external-data change.

Stable field names and model scores do not prove stable class. Monitor assertion age, unknown rate, sampled error, policy mismatch, incidents, and unexpected egress.

**Version APIs and events.** Expose object and class identities, scheme versions, assertion states, provenance, effective time, handling profile, and safe explanations. Provide immutable historical retrieval.

Events distinguish proposed, inferred, verified, disputed, superseded, decontrolled, and retired assertions. Consumers deduplicate, order per subject where promised, and reconcile from authoritative state.

**Protect classification services.** Attackers can remove, downgrade, flood, infer, or probe labels. Threat-model scanners, review queues, registries, models, catalogs, policies, APIs, events, logs, and administrative paths.

Use least privilege, separation of duties, integrity protection, signed or authenticated changes, anomaly detection, rate limits, and independent audit for consequential reclassification.

**Measure the right layers.** Inventory coverage, assertion coverage, verification rate, age, conflict, unknowns, scanner precision and recall, review latency, propagation lag, policy activation, enforcement, incidents, correction, and outcome are different measures.

Publish denominators by class, format, domain, product, and consequence. Do not hide unscanned or inaccessible objects from coverage.

**Design reclassification.** A new assertion supersedes rather than overwrites. Record trigger, old and new class, basis, evidence, authority, effective time, affected copies, controls, consumers, decisions, exceptions, and remediation.

Urgent upgrades can restrict access immediately. Downgrades usually require stronger review because they relax controls and may enable irreversible disclosure.

**Design declassification and decontrol.** Define who may act, which condition or date applies, required review, redaction or transformation, residual classes, marking changes, recipient notification, and proof of control updates.

Removing one legal category can leave privacy, contract, integrity, retention, or dissemination requirements. Decontrol is axis-specific.

**Correct historical effects.** When a classification was wrong, identify decisions, disclosures, denials, deletions, retained copies, derived products, models, reports, and affected parties through versioned evidence.

Contain current risk, issue corrected assertions, update controls, notify as required, support appeal, remediate actual effects, and preserve the original record.

**Recover classifications before broad use.** Back up schemes, classes, mappings, assertions, basis, evidence, models, reviewer decisions, policies, events, copies, exceptions, decontrol records, and tombstones.

Restore identities, time, authority, and current status; reconcile object inventory and downstream copies; validate high-consequence handling; invalidate stale caches; then authorize resumption.

**Migrate schemes semantically.** Inventory identities, definitions, axes, notations, mappings, assertions, handling profiles, policies, APIs, events, integrations, histories, and decontrol rules.

Map with exact, close, broader, narrower, related, split, merge, and unmapped relations as appropriate. Dual-classify and compare controls; preserve loss and old resolution.

**Retire end to end.** Stop new assertions, publish successors, migrate policies and consumers, replace markings, expire caches, close exceptions, revoke administration, stop events, and update recovery.

Retain required scheme versions, assertion history, authority, evidence, mappings, decisions, and correction records. Prove retired labels and policy cannot regain current authority through restore or replay.

## Definitions and Notation

Let scheme `s = (authority, identifier, purpose, scope, axes, classes, relations, mappings, version, effective)`. A class label or color is an attribute, not identity.

Let object `o = (authority, identifier, kind, version, environment, location)`. Location can influence policy but does not replace stable object identity.

Let assertion `a = (o, axis, class, basis, evidence, issuer, method, confidence, review_state, scope, effective, limitations)`. Usability depends on current authority and the target decision profile.

Let classification vector `K(o,t) = {a : a.object = o and a is applicable at t}`. It can contain several assertions per axis from distinct authorities, including conflict and unknown.

Let handling decision `H(o,u,x,e,t) = Policy(K(o,t), use u, action x, environment e, time t)`. Classification informs policy but does not itself determine every action.

For transformation `f` over input objects `O`, derived assertions are `K(f(O)) = Derive(f, K(O), output_evidence, purpose, environment)`. `Derive` is axis- and transformation-specific.

Let aggregation `Agg_axis(K_1,...,K_n)` define how component assertions produce an enclosing object's axis value. Maximum, union, intersection, distribution, and contextual assessment are distinct choices.

Let inference record `m = (model_or_rule, version, inputs, feature_scope, population, score, threshold, abstention, proposed_class, evidence, time)`. It does not carry verification authority by default.

Let assertion coverage for inventory `I` and required axis `x` be `Cov(I,x,t) = |{o in I : current_usable_assertion(o,x,t)}| / |I|`. Publish excluded, inaccessible, unknown, and mixed objects.

Let observed accuracy on reviewed sample `Q` include per-class precision, recall, abstention, disagreement, and uncertainty. Sample results do not establish unsampled population truth without justified inference.

Let reclassification event `r = (object, prior_assertions, new_assertions, trigger, authority, evidence, effective, affected_dependencies, actions)`. Record time and valid time can differ.

Let decontrol predicate `D(a,t)` require authorized conditions, completed residual review, updated controls and markings, notified active recipients where required, and protected historical evidence.

Let closure predicate `Closed(s_v)` require no active assertion, marking generator, policy, scanner, model, cache, API default, consumer, exception, or recovery path treats retired scheme version `s_v` as current, while required history remains resolvable.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design and review classification architecture.

**Decision gate.** Name actions, purposes, affected parties, harms, obligations, reversibility, evidence, and controls classification must support.

**Scheme gate.** Verify authority, namespace, axes, class identity, definitions, notations, relations, mappings, versions, effective time, and retirement.

**Object gate.** Resolve stable field, record, dataset, product, system, media, copy, derivative, log, model, and backup identity at governable granularity.

**Assertion gate.** Require axis, class, basis, evidence, issuer, method, confidence, review state, scope, effective interval, and limitations.

**Information-type gate.** Identify meaning, source, population, purpose, mission, consumers, and context before assessing consequences.

**Impact gate.** Assess confidentiality, integrity, availability, privacy, safety, business, legal, and affected-party consequences independently.

**Protected-category gate.** Bind exact legal, regulatory, contractual, export, records, and sector basis, jurisdiction, authority, controls, and decontrol.

**Marking gate.** Connect display and encoded markings to current assertions, recipient context, format, placement, integrity, inheritance, and correction.

**Derivation gate.** Define axis-specific behavior for join, filter, copy, aggregate, encrypt, tokenize, hash, mask, redact, infer, train, publish, and restore.

**Automation gate.** Record rules or models, evaluation population, score semantics, thresholds, abstention, calibration, drift, review, and prohibited automation.

**Handling gate.** Resolve access, modification, masking, storage, location, transmission, sharing, logging, retention, deletion, incident, and recovery from assertions and context.

**Interoperability gate.** Exchange identities, schemes, mappings, assertions, provenance, versions, events, profiles, conflicts, and loss without label-based equivalence.

**Evidence gate.** Protect source samples, scanner outputs, model versions, reviewer decisions, measurements, policy activations, enforcement receipts, incidents, and corrections.

**Operations gate.** Observe inventory, coverage, verification, unknowns, conflict, age, accuracy, review, propagation, policy, enforcement, incident, and outcome denominators.

**Reclassification gate.** Preserve prior state, apply upgrade or downgrade authority, identify dependencies, update controls, notify, remediate, and verify effects.

**Recovery gate.** Restore schemes, assertions, authority, evidence, policies, events, copies, decontrol, and tombstones before broad data access.

**Closure gate.** End active assertions, markings, scanners, policies, exceptions, consumers, events, credentials, and recovery activation while preserving history.

### Executable evidence: multidimensional source and derived classifications

This Python example counts declared classification properties for six invented source fields and five invented derived assets.

<!-- bijux-verify: {"id":"multidimensional-source-and-derived-classifications","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source_fields=6\nclassification_axes=5\nderived_assets=5\npublic_assets=1\ninternal_assets=2\nrestricted_assets=2\ndirect_identifiers=1\npseudonymous_assets=2\nretention_classes=3\nhigh_integrity=2\nhigh_availability=1\nmanual_reviews=2\nunresolved=1\n","stderr":""}} -->
```python
source_fields = {
    "customer_email": {"confidentiality": "restricted", "integrity": "moderate", "availability": "low", "privacy": "direct", "retention": "one_year"},
    "order_total": {"confidentiality": "internal", "integrity": "high", "availability": "moderate", "privacy": "none", "retention": "seven_years"},
    "support_notes": {"confidentiality": "restricted", "integrity": "moderate", "availability": "low", "privacy": "sensitive_text", "retention": "ninety_days"},
    "country_code": {"confidentiality": "internal", "integrity": "moderate", "availability": "moderate", "privacy": "indirect", "retention": "one_year"},
    "order_id": {"confidentiality": "internal", "integrity": "high", "availability": "high", "privacy": "indirect", "retention": "seven_years"},
    "product_category": {"confidentiality": "public", "integrity": "low", "availability": "low", "privacy": "none", "retention": "one_year"},
}

derived_assets = {
    "email_token": {"confidentiality": "restricted", "privacy": "pseudonymous", "review": True, "resolved": True},
    "daily_revenue": {"confidentiality": "internal", "privacy": "none", "review": False, "resolved": True},
    "redacted_notes": {"confidentiality": "internal", "privacy": "sensitive_text", "review": True, "resolved": False},
    "published_categories": {"confidentiality": "public", "privacy": "none", "review": False, "resolved": True},
    "linked_profile": {"confidentiality": "restricted", "privacy": "pseudonymous", "review": False, "resolved": True},
}

axes = set(next(iter(source_fields.values())))
confidentiality_counts = {
    level: sum(asset["confidentiality"] == level for asset in derived_assets.values())
    for level in {"public", "internal", "restricted"}
}

print(f"source_fields={len(source_fields)}")
print(f"classification_axes={len(axes)}")
print(f"derived_assets={len(derived_assets)}")
print(f"public_assets={confidentiality_counts['public']}")
print(f"internal_assets={confidentiality_counts['internal']}")
print(f"restricted_assets={confidentiality_counts['restricted']}")
print(f"direct_identifiers={sum(v['privacy'] == 'direct' for v in source_fields.values())}")
print(f"pseudonymous_assets={sum(v['privacy'] == 'pseudonymous' for v in derived_assets.values())}")
print(f"retention_classes={len({v['retention'] for v in source_fields.values()})}")
print(f"high_integrity={sum(v['integrity'] == 'high' for v in source_fields.values())}")
print(f"high_availability={sum(v['availability'] == 'high' for v in source_fields.values())}")
print(f"manual_reviews={sum(v['review'] for v in derived_assets.values())}")
print(f"unresolved={sum(not v['resolved'] for v in derived_assets.values())}")
```

The expected output reports six source fields, five classification axes, five derived assets, one public, two internal, two restricted, one direct identifier, two pseudonymous assets, three retention classes, two high-integrity sources, one high-availability source, two manual reviews, and one unresolved result on separate lines.

The evidence is intentionally narrow. Dictionary keys and strings do not establish object identity, scheme authority, class meaning, legal basis, evidence, issuer, time, confidence, or handling. The derived results are declarations, not outputs of transformation-specific rules or content tests. `pseudonymous` does not establish privacy risk, and `public` does not authorize publication or modification. Counts ignore mixed content, conflicts, unknowns, copies, consumers, jurisdictions, purpose, attacker data, and enforcement. Production assurance requires governed schemes, attributable assertions, representative discovery evaluation, output and reidentification testing, lineage, authorized review, context-aware policy, control receipts, incident evidence, reclassification, and recovery exercises.

## Alternatives and Trade-Offs

**Single confidentiality ladder.** Users and controls receive a simple ordered label. Other axes and legitimate nonmonotonic rules are hidden.

**Multidimensional vector.** Independent concerns remain expressible and composable. Interfaces, policy, review, and user education become more complex.

**System-level categorization.** Control baselines and authorization boundaries are manageable. Fine-grained data sharing and mixed content are obscured.

**Field-level classification.** Masking and discovery can be precise. Identity, lineage, enforcement, and maintenance cost rise sharply.

**Record-level classification.** Exceptional subjects and cases can be protected accurately. Storage and query systems may not support consistent enforcement.

**High-water-mark aggregation.** Enclosing objects receive conservative protection. Sharing, cost, and availability can be unnecessarily restricted, and other axes may not order cleanly.

**Rule-based aggregation.** Transformation and axis semantics can be accurate. Rules need authority, tests, output evidence, and lifecycle maintenance.

**Manual classification.** Domain judgment and accountability handle nuance. Coverage, speed, consistency, reviewer capacity, and drift are challenges.

**Rules-based discovery.** Deterministic patterns are explainable and cheap. Names, formats, languages, combinations, and novel content create brittle errors.

**Machine-learning discovery.** Models can interpret diverse and unstructured content. Evaluation, bias, privacy, adversarial behavior, confidence, and drift require controls.

**Automatic enforcement from inference.** Response is rapid and scalable. False positives block work and false negatives expose data without accountable verification.

**Candidate plus human review.** Authority and context are preserved. Review queues can become a bottleneck and sampled content can expose reviewers.

**Schema-declared classes.** Protection starts before data arrives and contracts are clear. Unexpected instance content and semantic drift can remain undetected.

**Instance scanning.** Actual content anomalies become visible. Sampling, encrypted formats, scale, false results, and data exposure constrain assurance.

**Embedded labels.** Classification travels with files and messages. Markings can be stripped, forged, stale, or unsupported by destinations.

**Central classification registry.** Authority, history, search, and policy integration improve. Availability, synchronization, and central compromise create broad risk.

**Federated domain assertions.** Context and accountability remain close to data. Shared schemes, mappings, conflicts, and evidence interfaces require coordination.

**Static handling profiles.** Controls are predictable and auditable by class. Purpose, jurisdiction, environment, and exceptions can make them overbroad.

**Dynamic policy resolution.** Context-specific controls improve data use. Runtime dependencies, failure, explainability, and evidence become critical.

**Encryption-based downgrading.** Storage exposure can be reduced under a threat model. Keys, metadata, endpoints, and restored plaintext preserve underlying class.

**Aggregation-based release.** Useful statistics can be shared with reduced detail. small groups, differencing, auxiliary data, and repeated releases can reidentify.

**Long assertion history.** Audit, correction, replay, and legacy markings remain interpretable. Retention, privacy, security, and migration obligations increase.

**Current-state-only labels.** Implementation is simpler. Historical decisions and incidents cannot be reproduced after reclassification.

**Scheme replacement.** A cleaner taxonomy removes legacy complexity. Mapping loss, consumer migration, historical resolution, and reactivation risk require work.

**Incremental scheme evolution.** Consumers change gradually. Transitional mappings and overlapping versions can become permanent ambiguity.

## Failure Modes and Misconceptions

**“Classification means confidentiality.”** Integrity, availability, privacy, legal, dissemination, retention, criticality, and quality are separate concerns.

**“Sensitivity is one ordered scale.”** Different axes and contexts do not share a universal ordering.

**“Public data needs no controls.”** Integrity, authenticity, availability, privacy of use, and modification can still matter.

**“Internal means safe.”** Insider, partner, vendor, account compromise, and unintended reuse remain credible risks.

**“PII is a universal Boolean.”** Identifiability depends on combinations, environment, auxiliary data, time, and context.

**“No direct identifiers means anonymous.”** Indirect, behavioral, device, household, location, and linked attributes can identify.

**“Pseudonymous means nonpersonal.”** Linkage keys and contextual reidentification can remain.

**“Special categories are always more confidential.”** Legal, privacy, harm, and security axes overlap but are not identical.

**“High value means high confidentiality.”** Value can depend on integrity, availability, uniqueness, or public reuse.

**“A class name is its definition.”** Scope, basis, examples, exclusions, authority, version, and controls provide meaning.

**“Matching labels are equivalent.”** `restricted`, `secret`, colors, and numbers differ across schemes.

**“Ordinal mappings are exact.”** Level 3 in one scheme may not correspond to level 3 in another.

**“The marking creates the class.”** Authority and evidence create an assertion; marking communicates it.

**“Unmarked means public.”** Markings can be missing, stripped, stale, or unsupported.

**“Marked means correctly protected.”** Enforcement and recipient behavior remain separate.

**“A table has one natural class.”** Fields, records, purposes, and axes can differ.

**“Finer granularity is always better.”** Unsupported precision creates ungoverned gaps and policy inconsistency.

**“Schema classification proves every value.”** Instance anomalies, nulls, synthetic data, and drift can differ.

**“Scanning a sample proves the dataset.”** Rare sensitive cases can remain outside the sample.

**“High-water mark works for every axis.”** Retention, dissemination, privacy, and transformation can require other rules.

**“Maximum source class always propagates.”** Output meaning and risk depend on transformation and context.

**“Minimum source class is enough after filtering.”** Remaining fields and records can preserve or increase risk.

**“Encryption lowers the data class.”** It changes exposure under key and threat assumptions, not underlying meaning.

**“Hashing anonymizes identifiers.”** Domain size, salts, keys, linkability, and auxiliary data determine risk.

**“Tokenization removes privacy obligations.”** Token authorities and joins can reidentify.

**“Masking protects every path.”** Predicates, counts, errors, logs, caches, and exports can leak.

**“Aggregation guarantees safe release.”** Small cells, differencing, outliers, repeated queries, and external data can reveal.

**“Lineage proves classification propagation.”** It identifies derivation, not preserved meaning or risk.

**“Copies keep identical obligations.”** Location, recipient, purpose, jurisdiction, contract, and retention can change.

**“Operational metadata is harmless.”** Schemas, queries, lineage, policy, and incidents reveal structure and activity.

**“Free text is just one field.”** It can contain arbitrary identities, secrets, health, legal, or security content.

**“Embeddings contain no readable data.”** Membership, inversion, linkage, and model behavior can expose information.

**“A regex is a classifier.”** It detects selected patterns under assumptions and can miss semantics or match benign values.

**“Model confidence is class probability.”** Score semantics and calibration depend on model, population, and class.

**“High confidence grants authority.”** Verification and policy authority are independent of a score.

**“False positives are merely inconvenient.”** They can deny rights, block operations, and create costly workarounds.

**“False negatives are the only security risk.”** Overclassification can hide poor controls and impede legitimate sharing.

**“Every item must receive a class.”** Abstention and unknown can be safer than false certainty.

**“Human review eliminates error.”** Reviewers can lack authority, context, consistency, or independence.

**“Frequent use validates a class.”** Misclassified data can be widely consumed.

**“Classification directly grants access.”** Authorization also needs actor, action, purpose, context, and policy.

**“A lower label permits publication.”** Release requires authority, output testing, residual review, and obligations.

**“Current labels explain historical decisions.”** Scheme, assertion, policy, and context versions can differ.

**“Changing the tag corrects prior effects.”** Copies, disclosures, denials, models, and decisions require remediation.

**“Downgrading is just an edit.”** Relaxing controls needs stronger authority and proof than changing display metadata.

**“Declassification removes every obligation.”** Other axes, contracts, privacy, records, and integrity can remain.

**“Deleting a label decontrols data.”** Authorized conditions, control updates, markings, recipients, and evidence are required.

**“Catalog coverage equals control coverage.”** Assertions can be stale, inferred, ignored, or unenforced.

**“One accuracy score measures classification.”** Per-class precision, recall, abstention, drift, and consequence differ.

**“Retiring a scheme retires its effects.”** Policies, labels, caches, consumers, backups, and historical copies can reactivate it.

## Worked Examples

### Example 1

A public transit timetable is classified public for confidentiality, high for integrity, and high for availability. Publishing is allowed through an authenticated channel, but unauthorized modification and service outage receive strict controls. A universal sensitivity ladder would miss the important risks.

### Example 2

A table contains email, order identifier, product code, amount, and free-text notes. Field assertions identify direct, indirect, financial, public-reference, and unstructured-sensitive types. The table receives a mixed-content record and restrictive default handling, while approved views apply field and row policy.

### Example 3

A deterministic email token is proposed as anonymous. Review records the keyed transformation, token authority, linkage across datasets, population, potential external data, and supported purposes. It remains pseudonymous and restricted even though direct email text is absent.

### Example 4

A daily revenue aggregate removes customer and order identifiers. Release tests enforce minimum groups, dominance, differencing budget, outlier treatment, and delayed publication. Confidentiality can be reduced for the output, while integrity and business criticality increase because public reporting depends on it.

### Example 5

An incident report is shared under TLP 2.0. The dissemination assertion limits onward sharing to the intended community. Separate assertions cover personal data, vulnerability details, retention, legal privilege, and integrity. The TLP marking is not treated as a complete storage or access policy.

### Example 6

A scanner finds national-identifier patterns in a log field. The finding is high-confidence but inferred because synthetic tests and checksum collisions exist. The log is contained immediately, a steward reviews permitted samples and source code, and the final assertion records basis, scope, exception rows, and expiry.

### Example 7

A join of a coarse location table and pseudonymous activity table makes individuals distinguishable in rural areas. An axis-specific derivation rule raises privacy and confidentiality, opens manual review, and blocks external publication. Neither input label alone predicted the combined risk.

### Example 8

A field changes from billing country to current residence without a schema-type change. Semantic and distribution drift trigger reclassification of privacy, jurisdiction, retention, and sharing assertions. Lineage identifies dependent tax reports and marketing extracts for review rather than copying the new labels blindly.

### Example 9

A legal category reaches its decontrol date. The workflow validates authority and conditions, preserves a privacy class and records schedule, updates markings and access policy, notifies active recipients, expires caches, and records evidence. The data does not become public merely because one control basis ended.

### Example 10

After recovery, the registry contains both current and retired scheme versions. Services restore stable identities, replay assertion events, reconcile object inventories, invalidate old caches, and test high-consequence policies. A guard prevents legacy `restricted-3` from being interpreted as the current scheme's level 3.

## Cross-Program Connections

**Security Engineering.** Threats, confidentiality, integrity, availability, access, cryptography, monitoring, incident response, and recovery turn class assertions into protections.

**Privacy Engineering.** Identifiability, linkability, context, purpose, minimization, sensitive inference, affected-party harm, rights, and deletion make privacy classification more than pattern detection.

**Knowledge Representation.** Concept schemes, stable identifiers, definitions, hierarchies, relations, mappings, notations, and versions make classifications interoperable without false equivalence.

**Machine Learning Engineering.** Content classifiers require evaluation sets, calibration, abstention, drift, adversarial testing, human review, and controls over training evidence.

**Information Retrieval.** Extraction, entity recognition, pattern matching, indexing, ranking, sampling, and search support discovery while introducing sensitive metadata and recall limits.

**Data Engineering.** Schemas, profiling, lineage, transformations, copies, streams, storage, exports, retention, deletion, and replay determine where assertions must propagate and be tested.

**Platform Engineering.** Registries, scanners, workflows, policies, APIs, events, catalogs, dashboards, SDKs, and paved handling paths make classification operational at scale.

**API and Service Engineering.** Classification interfaces require stable resources, versioning, concurrency, authorization, caching, pagination, event semantics, idempotency, and reconciliation.

**Governance, Risk, and Compliance.** Authority, legal basis, impact, controls, exceptions, assurance, audit, reclassification, decontrol, and remedy give classifications legitimacy.

**Records and Information Management.** Record class, retention, legal hold, disposition, archival value, decontrol, and historical markings intersect but must not collapse into confidentiality.

**Systems Engineering.** Local labels, transformation rules, people, controls, and feedback compose into system behavior; classification errors can propagate and create emergent risk.

**Human-Computer Interaction.** Clear markings, explanations, warnings, review queues, correction, and accessible presentations determine whether users understand and follow handling rules.

## References

1. National Institute of Standards and Technology, [“FIPS 199: Standards for Security Categorization of Federal Information and Information Systems”](https://csrc.nist.gov/pubs/fips/199/final), 2004. Retrieved 2026-09-03.
2. National Institute of Standards and Technology, [“SP 800-60 Volume I Revision 1: Guide for Mapping Types of Information and Information Systems to Security Categories”](https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final), 2008. Retrieved 2026-09-03.
3. National Institute of Standards and Technology, [“SP 800-122: Guide to Protecting the Confidentiality of Personally Identifiable Information”](https://csrc.nist.gov/pubs/sp/800/122/final), 2010. Retrieved 2026-09-03.
4. National Institute of Standards and Technology, [“Protecting Controlled Unclassified Information: Frequently Asked Questions”](https://csrc.nist.gov/Projects/protecting-controlled-unclassified-information/faqs), retrieved 2026-09-03.
5. Forum of Incident Response and Security Teams, [“Traffic Light Protocol Version 2.0”](https://www.first.org/tlp/), 2022. Retrieved 2026-09-03.
6. UK Cabinet Office, [“Government Security Classifications Policy”](https://www.gov.uk/government/publications/government-security-classifications/government-security-classifications-policy-html), 2024. Retrieved 2026-09-03.
7. W3C, [“SKOS Simple Knowledge Organization System Reference”](https://www.w3.org/TR/skos-reference/), 2009. Retrieved 2026-09-03.
8. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/prov-o/), 2013. Retrieved 2026-09-03.
9. W3C, [“Data on the Web Best Practices: Data Quality Vocabulary”](https://www.w3.org/TR/vocab-dqv/), 2016. Retrieved 2026-09-03.
10. W3C, [“ODRL Information Model 2.2”](https://www.w3.org/TR/odrl-model/), 2018. Retrieved 2026-09-03.
11. W3C, [“Shapes Constraint Language”](https://www.w3.org/TR/shacl/), 2017. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design a multidimensional classification scheme for a healthcare commerce platform. Include information types, security impact, privacy and identifiability, legal and contractual basis, dissemination, retention, criticality, quality, class identity, markings, authority, and mappings.

### Exercise 2

Design derivation rules for a pipeline that joins customer, payment, support, location, and product data, then tokenizes identifiers, redacts text, aggregates metrics, trains a model, publishes a dashboard, exports a partner file, and archives inputs.

### Exercise 3

Design an automated discovery program for structured, free-text, document, image, audio, code, log, embedding, and encrypted data. Include evaluation, confidence, abstention, review, security, drift, metrics, and limits on enforcement.

### Exercise 4

A product was underclassified for twelve months and fed reports, features, exports, backups, and an external partner. Design containment, reclassification, impact analysis, notification, correction, evidence, appeal, and recovery changes.

### Exercise 5

Migrate three incompatible schemes into a federated classification architecture while preserving domain authority, legal categories, historical markings, policies, APIs, events, consumers, exceptions, decontrol, and disaster recovery.

## Answers to the Exercises

### Answer 1

Create stable schemes and versions for information type; confidentiality, integrity, and availability impact; personal-data relationship and identifiability; health, payment, consumer, child, employee, contract, export, and records bases; dissemination community; retention schedule; operational criticality; and quality or decision consequence. Define every class with scope, inclusions, exclusions, examples, counterexamples, authority, notation, evidence, defaults, and lifecycle. Do not put every concern on one public-to-restricted ladder.

Represent patients, customers, dependents, clinicians, merchants, devices, orders, claims, payments, prescriptions, support messages, and public products as distinct information types. Privacy assertions record population, purpose, linkability, inference, power, scale, and adverse effects. Security impact is assessed separately for disclosure, modification, and loss. Retention and dissemination classes link to exact authority and conditions. Critical public safety reference data can be public confidentiality yet high integrity and availability.

Markings expose a bounded summary with scheme version and resolve to full assertions. Use reviewed cross-scheme mappings rather than color or ordinal equality. Assign domain authorities for semantic and source assertions and shared authorities for mandatory legal and enterprise schemes. Connect assertions to policy profiles for access, masking, storage, transfer, sharing, monitoring, retention, deletion, incident, and recovery. Preserve unknown, mixed, inferred, disputed, stale, decontrolled, and superseded states.

### Answer 2

Give every input, transformation, output, and copy stable identity and version. For the join, union input assertions and assess increased linkability, population, inference, jurisdiction, and decision consequence. Tokenization keeps the source privacy relationship, records key and linkage authority, and produces a pseudonymous assertion rather than anonymity. Redaction rules are format-aware and require residual free-text tests, unsupported-format handling, and review.

Aggregation evaluates group size, dominance, outliers, differencing, repeated releases, auxiliary data, and update behavior. It can reduce output confidentiality while raising integrity and criticality. Model training creates a governed feature and model asset with training purpose, subjects, provenance, retention, memorization and inference risk, decision use, and deletion behavior. Dashboard policy covers displayed values, filters, drill-down, cache, export, and screenshot risks.

The partner export adds recipient, contract, destination, purpose, onward sharing, marking, expiry, and deletion receipt. The archive retains source classes, legal holds, access, integrity, key availability, restoration, and decontrol schedule. For each operation and axis, publish derivation rule, inputs, unknown behavior, authority, tests, evidence, loss, and review triggers. Lineage discovers dependencies but does not decide the output class.

### Answer 3

Inventory formats and decision consequences before selecting tools. Structured scanning uses schema, types, formats, checksums, dictionaries, values, entropy, and lineage. Text and code use parsers, entity recognition, secret patterns, language-aware rules, and bounded models. Documents, images, and audio require extraction quality and original-format checks. Logs need sampling and access controls. Embeddings require source provenance and attack analysis. Encrypted or unsupported objects produce unknown and containment rather than false safe results.

Build representative labeled evaluation sets by domain, language, format, rarity, class, ambiguity, protected population, and adversarial case. Measure per-class precision, recall, abstention, calibration where valid, reviewer agreement, queue latency, sampled population error, and downstream control effects. Thresholds vary by class and action. Store rule or model version, feature scope, population, evidence summary, score semantics, proposed class, time, and limitations.

Route consequential findings to authorized reviewers with minimized evidence and secure samples. Prevent scanners, models, logs, prompts, and outputs from becoming a new disclosure store. Monitor content, schema, source, language, model, and class drift. Use immediate containment for credible severe findings, but prohibit irreversible deletion, public release, or broad denial solely from unverified inference unless explicit authority exists. Reevaluate with sampled independent review and publish unscanned and inaccessible denominators.

### Answer 4

Freeze new high-risk sharing and derived production while preserving evidence. Issue a provisional restrictive assertion under emergency authority, identify affected objects and copies through catalogs, lineage, decisions, transfer receipts, consumer registries, and storage inventories, and protect classification logs. Determine when the wrong assertion began, which scheme and policy versions applied, and whether the cause was source meaning, scanner, review, mapping, propagation, or enforcement.

Assess actual reports, features, exports, partner uses, backups, caches, logs, models, and decisions rather than assuming every lineage descendant has the same exposure. Notify security, privacy, legal, records, domain owners, consumers, the partner, and affected people as required. Revoke access, rotate tokens or keys, recall or delete copies, retrain or withdraw models, correct reports and decisions, and support appeal and remedy.

Supersede the old assertion without rewriting it. Record basis, evidence, authority, valid and record times, affected dependencies, actions, residual risk, and closure. Update scheme definitions, training, scanner fixtures, derivation rules, policy, monitoring, and contracts. Test recovery in isolation and prove old labels, partner credentials, exceptions, model artifacts, and exports do not reactivate. Retain minimum required incident and correction evidence under its own protected classification.

### Answer 5

Inventory each scheme's authority, purpose, axes, stable identifiers, class definitions, labels, notations, hierarchy, mappings, assertions, handling profiles, policies, markings, APIs, events, integrations, metrics, exceptions, decontrol, history, and recovery. Preserve domain-specific classes where they carry legitimate distinctions. Establish shared minimum axes and exchange profiles without forcing all domains into one ladder.

Create explicit exact, close, broader, narrower, related, split, merge, and unmapped relations with direction, scope, evidence, version, and loss. Never map by color, label, or ordinal alone. Dual-publish old and new assertions and calculate handling under both for representative and adversarial objects. Explain every control difference and require stronger authority for downgrades. Provide immutable historical resolution for legacy markings and decisions.

Version APIs and events, use stable object identity, and migrate consumers by registered dependency. Update policy rules, scanners, models, dashboards, exports, documents, and physical markings. Carry exceptions into explicit new-scheme decisions rather than copying identifiers. Canary domains and high-consequence products, preserve rollback while compatible, reconcile inventories, and monitor unknowns and conflicts.

Deprecate old schemes, stop new assertions, expire caches, revoke authoring rights, close mappings and exceptions, stop old events, and update recovery. Closure proves no active assertion, marking generator, policy, scanner, model, consumer, or restore path treats a retired version as current while governed history, authority, mappings, decontrol, and correction evidence remain available.
