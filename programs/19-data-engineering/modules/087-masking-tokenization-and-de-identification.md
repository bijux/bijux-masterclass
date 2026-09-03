---
module_id: DE-087
program: Data Engineering
level: 2
module_number: 87
title: Masking, Tokenization, and De-Identification
status: complete
last_verified: 2026-09-03
---

# Masking, Tokenization, and De-Identification

## One-Page Review

### Governing question

How can a data organization choose, implement, validate, and govern masking, tokenization, pseudonymization, generalization, suppression, aggregation, perturbation, synthetic generation, and formal privacy mechanisms for a precise data use and threat model, while preserving necessary utility and avoiding the false claim that removing names, hashing identifiers, or meeting one sample statistic makes data anonymous in every context?

### Essential definitions

- **Masking** replaces or obscures values to reduce exposure in a particular interface; it may be static or computed dynamically by access context.
- **Redaction/suppression** removes a value, field, row, cell, group, or output that would disclose too much.
- **Tokenization** replaces a value with a surrogate token, commonly through a vault mapping, randomized token service, or cryptographic construction.
- **Pseudonymization** replaces or separates identifying associations so records require additional separately protected information to attribute to a person; it commonly remains reversible or linkable and is not anonymity.
- **Encryption** protects confidentiality with a key; ciphertext is not de-identified merely because unauthorized parties cannot read it.
- **Generalization** maps a value to a broader category, interval, hierarchy, or reduced precision.
- **Perturbation** changes values or statistics, often by adding randomness, swapping, microaggregation, or another distortion.
- **De-identification** is a governed process intended to reduce identity, attribute, or inferential disclosure risk for stated data, recipients, purposes, environments, auxiliary information, and time.
- **Re-identification** associates a record or data with a subject; **linkability** connects records about the same subject even without recovering a civil identity.
- A **direct identifier** names a subject in context; a **quasi-identifier** can distinguish or link a subject when combined with other data; a **sensitive attribute** is information whose association may cause harm.
- **$k$-anonymity** requires each released quasi-identifier pattern to occur in at least $k$ records; it does not by itself protect sensitive-attribute homogeneity, composition, or arbitrary auxiliary knowledge.
- **Differential privacy** bounds how much a randomized mechanism's output distribution can change when one subject's contribution changes, under a declared adjacency relation and privacy parameters.
- **Disclosure risk** is contextual likelihood and consequence of identity, attribute, inferential, membership, or reconstruction disclosure.
- **Utility** is fitness of transformed data for declared analyses, including bias, error, relationships, tails, reproducibility, and subgroup behavior—not merely row count.
- A **release** is the complete disclosure surface across datasets, queries, documentation, schemas, codebooks, models, repeated versions, and recipients.

### Central model, mechanism, or theorem

Choose a transformation $M_\theta$ only relative to input generation $X_g$, intended use $u$, recipient/environment $e$, adversary/auxiliary knowledge $A$, release history $H$, and risk/utility thresholds:

$$
Y=M_\theta(X_g), \qquad Risk(Y,A,H,e)\le \tau_R, \qquad Utility(Y,u)\ge \tau_U.
$$

For $k$-anonymity with quasi-identifier projection $Q$, every released record $r$ must satisfy

$$
|\{r'\in Y:Q(r')=Q(r)\}|\ge k.
$$

That is a specific indistinguishability property, not universal anonymity. For randomized mechanism $M$, $(\varepsilon,\delta)$-differential privacy instead requires adjacent datasets $x\sim x'$ and all measurable outputs $S$ to satisfy

$$
\Pr[M(x)\in S]\le e^\varepsilon \Pr[M(x')\in S]+\delta.
$$

The guarantees answer different questions and depend on their assumptions, parameters, composition, and implementation.

### Critical invariants

- Name the goal: presentation safety, least-privilege display, stable linkage, reversible recovery, testing, internal research, controlled sharing, public release, or aggregate statistics.
- Bind every transform to exact input/output generations, field/cohort scope, code/config/parameter version, purpose, recipient, environment, threat model, release history, owner, reviewer, and validity interval.
- Preserve a distinction among masking, tokenization, pseudonymization, encryption, de-identification, anonymization, and legal/regulatory determinations.
- Removing direct identifiers does not address quasi-identifier linkage, unique combinations, free text, rare events, locations, timestamps, images, or learned representations.
- Deterministic tokens preserve equality and linkability; format and frequency can leak information; reversibility and token vault/key access remain sensitive powers.
- Unsalted hashes of low-entropy identifiers are vulnerable to enumeration; a salt does not stop per-record linkage if exposed, and keyed transforms require domain separation and key governance.
- Token/key/vault compromise, chosen-input oracles, cross-domain reuse, collisions, retries, rotation, backup, recovery, and deletion are designed explicitly.
- Generalization and suppression are evaluated on the released population and declared quasi-identifiers, not only a convenient sample.
- $k$-anonymity does not establish sensitive-attribute diversity, distributional similarity, resistance to background knowledge, or protection across repeated releases.
- Aggregates can expose small groups, outliers, membership, differences, and reconstruction; minimum group size is one control, not a complete guarantee.
- Differential-privacy parameters, adjacency, contribution bounds, unit of privacy, mechanism, accountant, composition, clipping, randomness, and implementation are explicit.
- Synthetic data is tested for memorization, nearest-neighbor leakage, rare-record reproduction, membership/attribute inference, and utility; “synthetic” is not a guarantee.
- Risk assessment includes other available datasets, recipients, incentives, capabilities, contracts, access controls, query interfaces, and future/repeated releases.
- Utility evaluation covers intended estimands, joins, ordering, temporal intervals, correlations, tails, small groups, missingness, bias, and uncertainty.
- Transformation happens in a least-privilege trusted boundary; raw data, mappings, keys, samples, logs, failures, intermediate files, and backups remain protected.
- Output classification and handling are derived from residual risk and context; a transform does not automatically erase source obligations.
- De-identification decisions are documented, independently reviewed where risk warrants, time-bounded, re-evaluated after change, and revocable where technically possible.
- Tests include known linkage attacks, mutation/canary fixtures, full coverage, reproducibility, failure behavior, output scanning, release composition, and incident response.

### Common failures

Common failures include deleting names and declaring anonymity; replacing identifiers with sequential numbers; hashing email addresses without a secret; reusing deterministic tokens across customers and purposes; storing a token vault beside the output; truncating cryptographic output until collisions corrupt joins; preserving exact dates and locations; applying $k$-anonymity to an incomplete quasi-identifier set; ignoring homogeneous sensitive values; assessing one file but releasing monthly differencing versions; using a group threshold as a formal privacy guarantee; publishing synthetic rows without memorization testing; logging raw failed transformations; letting tokenization-oracle access expand; losing key/version provenance; rotating tokens without reconciliation; treating encryption as de-identification; and claiming a legal result from a tool's “de-identify” button.

### Compact example

Four records share generalized quasi-identifiers `age=20–39` and `postal_prefix=021`, so the fixture has $k=4$. Every record, however, has the same rare diagnosis. Anyone who knows a person appears in that group learns the diagnosis even without learning which row is theirs. The release satisfies its stated $k$-anonymity check but does not prove attribute confidentiality, resistance to linkage, or legal anonymity. A correct review expands the risk model and may suppress the group, broaden/generalize it, use a controlled query interface, or apply a suitable formal mechanism.

### Connections

[DE-028](028-deduplication-and-record-identity.md) explains identity and linkage, [DE-066](066-time-travel-and-reproducible-reads.md) binds exact releases, [DE-076](076-data-contracts.md) states allowed use, [DE-078](078-data-incident-detection-and-triage.md) responds to disclosure, [DE-082](082-dataset-and-column-lineage.md) traces copies, [DE-084](084-ownership-and-stewardship.md) assigns review authority, [DE-085](085-classification-and-sensitive-data.md) supplies contextual risk evidence, and [DE-086](086-access-control-for-analytical-data.md) constrains recipients and interfaces. [DE-088](../ROADMAP.md) next governs retention and deletion.

## Governing Question

Transformation names are dangerously reassuring. “Masked” can mean four visible trailing digits in a user interface, irreversible removal in a test fixture, or a reversible warehouse expression. “Tokenized” can mean a random vault reference, deterministic encryption, or an unkeyed hash. “Anonymous” may be a legal conclusion under one regime, a colloquial description, or an unsupported marketing label.

The engineering question begins with use and threat. Does a support agent need recognition, a pipeline need stable joins, a scientist need population statistics, a vendor need row-level microdata, or the public need an aggregate release? Who receives it, what auxiliary data can they access, can they submit chosen inputs, can releases be combined, and what harms matter? A transform is not good or bad independently of these answers.

Privacy and utility interact. Suppression can erase rare populations; generalization can bias geographic analysis; date shifting can break event order across subjects; deterministic tokens enable joins but reveal equality; random noise can protect individuals while altering small estimates. The goal is not maximum distortion. It is documented residual risk below an authorized threshold with sufficient measured utility for a bounded purpose.

Therefore, build a release system rather than a string-replacement script: classify and scope, model adversaries and recipients, choose layered controls, transform inside a protected boundary, validate risk and utility, govern mappings and keys, register outputs and releases, enforce access and retention, monitor composition, and revisit the determination as data and context change.

## Why This Matters

Identifiers are not confined to obvious fields. Exact dates, fine locations, occupations, households, device traces, rare events, free text, images, and behavior can distinguish people. Public and commercial auxiliary datasets make linkage easier over time. Removing names while preserving useful detail may leave a nearly unique fingerprint.

Reversible transformations reduce exposure but concentrate power. A token vault or decryption key becomes a high-value service. Deterministic tokens can join records across products, sometimes creating a richer profile than the raw data was allowed to support. Operational mistakes—wrong key, missing domain context, partial failure, stale replicas—can silently mix identities or leak raw values.

Statistical releases face composition. One table can appear safe; two overlapping tables reveal a hidden value. A sequence of query answers can reconstruct records. A synthetic model can memorize uncommon training rows. Controls must reason about release history rather than bless each artifact in isolation.

False confidence also harms data subjects and organizations. Underprotection creates disclosure; excessive distortion produces invalid research and inequitable decisions. A serious process reports both residual risk and lost utility, preserves assumptions, and refuses claims broader than the evidence.

## Prerequisites and Retrieval

Retrieve the data: stable product/dataset/field/generation IDs, subjects/entities, grain, population, schemas, types, nulls, direct/quasi identifiers, sensitive attributes, free text/media, rare values, spatial/temporal resolution, correlations, lineage, prior transformations, quality, and classification.

Retrieve the use: questions/estimands, joins, grouping, ordering, matching, longitudinal behavior, precision, tails, subgroups, acceptable error/bias, reproducibility, recipient, purpose, environment, outputs, onward sharing, retention, and deletion.

Retrieve the threat model: identity/attribute/membership/inference/reconstruction harms; attacker/recipient knowledge, auxiliary sources, access, compute, incentives, query ability, chosen inputs, collusion, vault/key access, compromised insiders, and future data availability.

Retrieve release history: earlier/later versions, overlapping cohorts, samples, aggregates, dashboards, APIs, papers, codebooks, schemas, public facts, models, logs, exports, and recipient-specific releases. Treat documentation and data dictionaries as part of disclosure.

Retrieve transformations: selection/detection rules, redaction, substitution, masking, tokenization architecture, crypto algorithm/mode, key/vault version, domain/tweak/context, generalization hierarchies, suppression, sampling, swapping, microaggregation, noise, synthesis, code/container/config, randomness, seed policy, and error handling.

Retrieve governance: applicable law/contract interpreted by qualified authorities, release model, risk/utility thresholds, review board/expert, approvals, independence, access controls, mapping/key custody, monitoring, incident route, validity/expiry, re-evaluation triggers, revocation, and destruction evidence.

Distinguish presentation mask from stored transform; static from dynamic mask; random token from deterministic token; vault token from cryptographic token; keyed transform from plain hash; pseudonymized from anonymous; reversible from irreversible; singling out from identification; identity from attribute/membership disclosure; sample from population; risk metric from legal test; $k$-anonymity from differential privacy; synthetic from safe; aggregate from non-sensitive; utility from fidelity; and one release from composed history.

Create a transformation/release record:

| Concern | Required evidence and decision |
|---|---|
| Input | Exact generation, fields/cohorts, classification and quality |
| Goal | Use, recipient, environment, needed operations and utility thresholds |
| Threat | Harms, attacker, auxiliary data, access, capability and release history |
| Transform | Method, code/config/parameters, key/vault/domain and randomness |
| Coverage | Eligible/transformed/failed/excluded/unknown records and fields |
| Risk | Metrics, attacks, assumptions, worst cases, residual risk and threshold |
| Utility | Estimands, error/bias, joins, time, tails, subgroups and acceptance |
| Output | Stable ID/generation, lineage, owner, classification, access and retention |
| Decision | Reviewer/authority, scope, rationale, validity, conditions and dissent |
| Lifecycle | Monitoring, composition, re-evaluation, incident, revocation and deletion |

Write a falsifiable claim: “Release R7 derives from generation G42 using transform bundle B9; direct identifiers are suppressed, quasi-identifiers Q1–Q4 use hierarchies H2/H3 and suppression S4, subject-scoped dates shift under protected key K8, project-specific deterministic tokens use domain D5, eligible/transformed/failed counts reconcile, population equivalence and linkage tests L6 pass threshold T3, intended estimands E1–E8 remain within registered bias/error bounds, prior releases P1–P4 are included, independent reviewer V2 approves recipient/environment U9 through 2027-01-31, and access, output classification, key/vault custody, monitoring and deletion controls remain active without claiming universal anonymity.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish masking, redaction, tokenization, hashing, encryption, pseudonymization, de-identification, anonymization, aggregation, synthesis, and formal privacy;
2. define a contextual threat/release model covering identity, attribute, membership, inference, reconstruction, auxiliary data, and composition;
3. design reversible and irreversible token systems with domain separation, key/vault custody, rotation, collision, oracle, recovery, and deletion controls;
4. apply suppression, generalization, sampling, swapping, microaggregation, perturbation, and query controls deliberately;
5. calculate and interpret $k$-anonymity while explaining homogeneity, background-knowledge, dimensionality, and composition limitations;
6. state differential-privacy adjacency, unit, contribution bounds, parameters, mechanism, accounting, and utility implications without overclaiming;
7. evaluate synthetic and transformed data for leakage, memorization, rare records, bias, error, joins, tails, and subgroup utility;
8. build a reproducible least-privilege transformation pipeline with full coverage, protected intermediates, lineage, failure handling, and output controls;
9. govern release review, documentation, recipient conditions, re-evaluation, revocation, retention/deletion, and incidents; and
10. test known attacks and mutations across single and composed releases while preserving exact evidence and claim boundaries.

## Core Exposition

### Start with the release model

Choose among public release, recipient-specific transfer, protected enclave, governed query interface, synthetic product, or internal pseudonymized use. These models expose different surfaces. Public microdata cannot rely on an access agreement alone; an enclave can combine technical restrictions, monitoring, trained users, and output review; a query interface can limit composition but becomes a stateful privacy boundary.

State the protected unit: person, household, device, organization, establishment, event, or another entity. State adjacency or participation semantics where formal mechanisms require it. Inventory the complete release—including metadata, codebook, schema, counts, models, repeated snapshots, and earlier disclosures.

Model realistic auxiliary information. Exact identity recovery is not the only harm. Singling out, linking the same pseudonym across contexts, learning membership in a study, inferring a diagnosis, reconstructing events, or targeting a rare organization may matter. Separate likelihood from consequence and document uncertainty.

### Choose masking by observation need

Dynamic masking computes a representation at query time according to access policy: a support agent may see `***-**-1234`, while an authorized investigator may unmask. It reduces routine display exposure but leaves raw storage and privileged paths sensitive. Test filters, joins, ordering, aggregates, exports, errors, caches, logs, and alternate engines.

Static masking transforms a copy. Redaction removes all or part of a value; substitution uses plausible or fixed surrogates; shuffling swaps values; date shifting preserves some intervals; bucketing generalizes numbers; nulling suppresses. Each preserves and destroys different relationships. Plausible fake data can still accidentally name real people and should come from governed generators, not casual lists.

Masking is not a declassification rule. Last-four display preserves recognition and partial value; stable substitution preserves equality; bucketing preserves ranges. Record residual properties so consumers do not use a masked dataset for an unsupported join or inference.

### Engineer tokenization as a security system

Random vault tokenization generates an unrelated token and stores a protected mapping. It hides frequency when repeated inputs can receive different tokens, but stable joins require reuse or a separate linkage service. The vault must authenticate callers, authorize tokenize/detokenize operations separately, rate-limit, log safely, back up, recover, rotate, and delete mappings.

Deterministic cryptographic tokenization produces the same token for the same input under the same key and context. It enables joins and reveals equality/frequency. Domain separation—by tenant, product, purpose, recipient, or field—prevents unintended cross-domain linkage. The context must be canonical and versioned. Reusing one token domain everywhere creates an organization-wide correlation identifier.

Plain hashing is usually unsuitable for identifiers drawn from enumerable spaces such as phone numbers or known email lists. Attackers can hash guesses. Per-record random salts impede equality but also prevent ordinary joins and, when stored, do not solve all offline attacks. A secret-key MAC resists unaided guessing better, yet anyone with key or oracle access can test candidates. Password hashing is a different problem with specialized slow, salted algorithms.

Design token length and alphabet for collision probability and downstream validation. Truncation or format constraints reduce the space. Format-preserving encryption keeps shape and can ease legacy integration but also exposes format and length and remains reversible encryption. Follow current cryptographic standards and key-management review rather than inventing a cipher.

Separate keys/vaults from outputs and ordinary analysts. Define generation, storage, envelope protection, access, dual control, rotation, re-tokenization, disaster recovery, compromise response, audit, retention, and cryptographic deletion assumptions. Key destruction can make reversal infeasible but does not erase copies, auxiliary data, or already linked derivatives.

### Remove identifiers and transform quasi-identifiers

Detect direct identifiers in structured fields, nested data, free text, images, filenames, paths, metadata, logs, and errors. Detection has false negatives; combine schema declarations, scanners, dictionaries, business context, review, and coverage evidence. Suppress unnecessary records and fields before using subtler transforms.

Quasi-identifiers require contextual selection. Age, postal area, occupation, sex, dates, locations, and event sequences may distinguish subjects together. Generalize with domain hierarchies, reduce temporal/spatial precision, top/bottom-code outliers, suppress rare cells or records, sample, swap, or microaggregate as appropriate. Optimize against both risk and declared utility rather than maximizing one metric.

$k$-anonymity measures equivalence-class size under a specified quasi-identifier projection. Compute it over the relevant released population, including null semantics and suppression. It can fail in high-dimensional sparse data where useful combinations are naturally unique. More importantly, a class of size $k$ can share one sensitive value, have a skewed distribution, or become distinguishable with background knowledge. Extensions such as diversity or distribution constraints address some cases but inherit assumptions and composition limits.

### Protect aggregates and repeated queries

Aggregation removes row-level detail but small groups, extremes, differencing, complementary suppression, repeated filters, and overlapping releases can disclose facts. Thresholds, suppression, controlled rounding, top/bottom coding, query-set restrictions, contribution limits, output review, and release-history checks are conventional controls. Attack them as a system.

Differential privacy provides a formal distributional stability definition for adjacent datasets. It does not mean “add some noise.” Specify subject or event adjacency, contribution bounding, clipping, mechanism, sensitivity, $\varepsilon$, $\delta$, randomness, accounting, composition, post-processing, and public versus private parameters. Poor unit choice or unbounded contributions invalidates the intended statement.

Smaller privacy loss typically requires more distortion; composition consumes budget across releases. Formal privacy protects participation influence under its model, not data accuracy, fairness, secure implementation, or every secret about a person learned from population facts. Validate mechanism code and accountant and report uncertainty with outputs.

### Evaluate synthetic data, models, and unstructured content

Synthetic generation learns a distribution and samples artificial records. It may support development or aggregate analysis, but models can memorize rare training examples, reproduce outliers, leak membership, or encode biases. Evaluate nearest-neighbor similarity, exact/near duplicate rates, membership and attribute inference, rare-subgroup behavior, model extraction, and recipient access. Formal private training offers a particular guarantee only when correctly parameterized and implemented.

Free text can contain identifiers, relationships, events, and distinctive narratives that rules miss. Images, audio, genomic data, trajectories, and high-dimensional behavior often retain biometric or near-unique structure after superficial masking. Use modality-specific threat expertise, minimize detail, prefer controlled environments, and avoid promising safe public microdata merely because obvious metadata was stripped.

Utility testing mirrors intended work: marginal and joint distributions, correlations, joins, longitudinal order/duration, spatial patterns, causal or predictive estimands, tails, missingness, calibration, subgroup error, and uncertainty. A dataset can look statistically similar overall while becoming useless or biased for the rare population it was meant to study.

### Build a reproducible protected pipeline

Execute transformations near raw data with least privilege and isolated temporary storage. Pin input snapshot, schema, code/container, rules, hierarchies, configuration, key/vault/token domain, randomness policy, and output destination. Count eligible, transformed, suppressed, failed, excluded, and unknown records/fields; fail closed on incomplete high-risk scope.

Avoid raw values in logs, exception traces, dead-letter queues, samples, metrics labels, or review tickets. Make retries idempotent without reusing randomness incorrectly. Validate schemas and referential behavior before publication. Register output ID/generation, lineage, owner, classification, controls, recipient, purpose, retention, and expiry.

Run risk attacks and utility checks against release candidates in a protected assessment environment. Review worst cases, not only averages. Bind approval to exact output digest and release history. Publication copies the approved immutable artifact; it does not rerun an unpinned transformation.

### Govern determinations through time

Different laws and policies define personal, pseudonymous, de-identified, and anonymous data differently. HHS describes HIPAA-specific Expert Determination and Safe Harbor routes; the GDPR defines pseudonymization and treats identifiability contextually. Engineers provide technical evidence, while qualified authorities make scoped legal and policy determinations.

Record reviewer competence/independence, methods, results, assumptions, recipient/environment, residual risk, utility, conditions, dissent, validity interval, and re-evaluation triggers. Changes in sources, auxiliary data, population, transform, threat capability, recipient, purpose, environment, regulation, or release history can invalidate a prior decision.

Monitor access, unexpected joins, token/vault/key use, oracle patterns, exports, new releases, public auxiliary datasets, risk signals, and incidents. If risk crosses bounds, stop further release, revoke controlled access, rotate/disable tokens or keys where useful, notify owners/recipients, contain derivatives, preserve evidence, and reassess. Public data may not be retractable, which raises the standard before release.

## Definitions and Notation

Let $X_g$ be an identified input generation; $M_\theta$ a transform with versioned parameters $\theta$; $Y=M_\theta(X_g)$ the candidate release; $Q$ a declared quasi-identifier projection; $S$ sensitive attributes; $A$ adversary and auxiliary information; $H$ prior/concurrent release history; $e$ recipient/environment; and $u$ intended utility.

The equivalence class of record $r$ under $Q$ is $E_Q(r)=\{r'\in Y:Q(r')=Q(r)\}$. Then

$$
k(Y,Q)=\min_{r\in Y}|E_Q(r)|.
$$

This minimum is undefined for an empty release unless policy defines a convention; report emptiness separately rather than claiming infinite privacy. Let $Risk_i$, $Risk_a$, $Risk_m$, and $Risk_r$ denote identity, attribute, membership, and reconstruction risk estimates under stated assumptions. A release decision considers their vector and consequences, not an unlabeled scalar alone.

For differential privacy, $x\sim x'$ declares neighboring datasets, usually differing in one protected unit's contribution according to the mechanism's contract. $\varepsilon$ is a multiplicative privacy-loss bound and $\delta$ an additive failure probability term. Composition combines losses across mechanisms; it is not reset by changing filenames or recipients.

A deterministic token can be modeled as $Tok_{K,d}(v)$ for secret key $K$, token domain $d$, and canonical value $v$. Equality within one domain follows:

$$
v_1=v_2 \Rightarrow Tok_{K,d}(v_1)=Tok_{K,d}(v_2),
$$

while well-designed domain separation aims to prevent useful equality comparison across $d_1\ne d_2$. This is a linkage property, not proof of anonymity or collision-free identity.

## Mechanisms, Invariants, or Proof Structure

### Release decision sequence

1. Identify exact input generation, subjects, fields, cohorts, modalities, classification, quality, owners, lineage, and prior transformations.
2. Define use, recipient, environment, protected unit, output, retention, utility requirements, and whether public release, enclave, transfer, query interface, or synthesis is appropriate.
3. Define adversaries, auxiliary information, identity/attribute/membership/inference/reconstruction harms, capabilities, incentives, chosen-input access, and release history.
4. Minimize records and fields; detect direct identifiers and enumerate quasi-identifiers/sensitive attributes with coverage and uncertainty.
5. Select layered suppression, masking, tokenization, generalization, perturbation, query, access, contractual, and monitoring controls with explicit parameters.
6. Execute in a protected reproducible boundary; reconcile eligible/transformed/failed/excluded/unknown scope and protect raw/intermediate/key/vault evidence.
7. Measure identity/linkage/inference risk with known attacks and worst cases; account for composition and document model limitations.
8. Measure intended utility, error, bias, relationships, tails, subgroups, reproducibility, and downstream compatibility against acceptance thresholds.
9. Obtain authorized, independent-where-needed review bound to the output digest, conditions, recipient, history, residual risk, and validity interval.
10. Publish/register the exact artifact, enforce access/export/retention, monitor new risk and releases, re-evaluate on triggers, and execute incident/revocation/deletion plans.

### Counterexample to a broad $k$ claim

**Claim.** $k$-anonymity of quasi-identifiers alone does not imply confidentiality of a sensitive attribute.

**Proof.** Construct an equivalence class of $k\ge2$ records with identical released quasi-identifiers and the same sensitive value $s$. The release satisfies the $k$-anonymity condition because every member is indistinguishable from at least $k-1$ others under $Q$. Yet anyone who knows a target belongs to that class learns $S=s$ with certainty from the class, without selecting the target's row. Therefore $k$-anonymity alone does not imply sensitive-attribute confidentiality.

This counterexample does not show that every $k$-anonymous release is unsafe or that a diversity rule guarantees universal safety. It isolates one guarantee boundary and motivates contextual attribute, background-knowledge, and composition analysis.

### Executable equivalence-class illustration

The fixture generalizes four different ages and postal codes into one quasi-identifier class. Its homogeneous sensitive attribute demonstrates the proof without representing real people or performing a de-identification certification.

<!-- bijux-verify: {"id":"equivalence-class-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=4\ngeneralized_equivalence_classes=1\nminimum_class_size=4\nk_anonymity=4\nminimum_sensitive_diversity=1\nidentity_ambiguity_in_fixture=true\nattribute_confidentiality_not_proved=true\n","stderr":""}} -->
```python
from collections import defaultdict


records = [
    {"age": 29, "postal": "02139", "condition": "rare"},
    {"age": 31, "postal": "02138", "condition": "rare"},
    {"age": 34, "postal": "02140", "condition": "rare"},
    {"age": 36, "postal": "02141", "condition": "rare"},
]


def generalized_key(record: dict[str, object]) -> tuple[str, str]:
    age = int(record["age"])
    return ("20-39" if 20 <= age <= 39 else "other", str(record["postal"])[:3])


classes: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
for record in records:
    classes[generalized_key(record)].append(record)

minimum_class_size = min(len(group) for group in classes.values())
minimum_sensitive_diversity = min(
    len({str(record["condition"]) for record in group}) for group in classes.values()
)
print(f"records={len(records)}")
print(f"generalized_equivalence_classes={len(classes)}")
print(f"minimum_class_size={minimum_class_size}")
print(f"k_anonymity={minimum_class_size}")
print(f"minimum_sensitive_diversity={minimum_sensitive_diversity}")
print("identity_ambiguity_in_fixture=true")
print("attribute_confidentiality_not_proved=true")
```

## Alternatives and Trade-Offs

1. **Dynamic versus static masking.** Dynamic policy preserves one source and context-specific views but retains privileged raw paths. Static copies reduce routine raw exposure but multiply lifecycle and drift.
2. **Redaction versus substitution.** Redaction minimizes disclosure but can break formats and workflows. Substitution preserves shape but may preserve relationships, create misleading values, or collide with real entities.
3. **Random versus deterministic tokens.** Random tokens hide repeated-value equality unless mappings are reused; deterministic tokens support joins but leak frequency and enable cross-record linkage.
4. **Vault versus cryptographic tokenization.** Vaults permit random mapping and revocation but add a stateful critical service. Cryptographic tokens can scale without per-value storage but intensify key, domain, oracle, and rotation concerns.
5. **Generalization versus suppression.** Generalization retains more records with less precision; suppression retains precision elsewhere but can remove rare groups and bias analyses.
6. **Microdata versus query interface.** Microdata supports flexible research but transfers broad attack capability. A query interface constrains computation and composes policy, at cost of flexibility, latency, and stateful accounting.
7. **Traditional disclosure controls versus differential privacy.** Traditional methods can preserve familiar data and fit controlled settings; differential privacy offers a formal participation guarantee but requires contribution bounds, budget, noise, and specialized utility communication.
8. **Real transformed versus synthetic data.** Transformed rows retain actual relationships but may remain linkable. Synthetic data can support some tasks without one-to-one rows, yet can memorize, distort tails, and fail unfamiliar analyses.
9. **One global versus domain-separated tokens.** Global tokens simplify joins and create organization-wide correlation risk. Domain separation limits linkage but requires approved cross-domain reconciliation services.
10. **Reversible versus irreversible transformation.** Reversibility supports correction, operations, and approved recontact but leaves a recovery power. Irreversibility narrows that path but may still permit inference and complicates subject correction/deletion.
11. **Public release versus enclave.** Public release maximizes reuse and is hard to retract. Enclaves restrict users, computation, and output but require durable operations, monitoring, and trust.
12. **More protection versus more utility.** Aggressive transformation can reduce risk while introducing bias or destroying purpose. Report a Pareto frontier and reject candidates that miss either authorized threshold.

## Failure Modes and Misconceptions

1. **“No names means anonymous.”** Quasi-identifiers, narratives, behavior, location, and auxiliary data can identify or link.
2. **“Pseudonymized means no longer personal.”** Pseudonymization commonly retains attribution through additional information and needs controls.
3. **“Encrypted data is de-identified.”** A key-bearing system can recover plaintext; encryption protects access, not contextual identifiability by itself.
4. **“Hashing is irreversible, therefore safe.”** Low-entropy domains can be enumerated; equality and frequency remain visible.
5. **“A salt solves identifier hashing.”** Stored salts do not prevent all guessing, and random per-record salts destroy stable joins.
6. **“One token domain maximizes utility.”** It also maximizes unintended cross-product linkage.
7. **“Format preservation leaks nothing.”** Length, alphabet, validity, equality, frequency, and format remain visible.
8. **“The vault is merely metadata.”** It is a re-identification system requiring stronger custody, authorization, resilience, and audit.
9. **“Masking the output protects predicates.”** Filters, joins, ordering, groups, errors, and timing may reveal raw-derived facts.
10. **“Static masking covers every row.”** Failed, skipped, malformed, nested, new-schema, and dead-letter records require reconciliation.
11. **“$k=5$ means five possible identities everywhere.”** The claim applies only to declared $Q$, released population, and current release assumptions.
12. **“Higher $k$ always means safer.”** Poor quasi-identifier choice, homogeneous attributes, composition, or external data can dominate.
13. **“Diversity alone stops disclosure.”** Semantic similarity, skew, background knowledge, and repeated releases remain.
14. **“Aggregates cannot identify.”** Small cells, extremes, differencing, membership, and reconstruction attacks contradict this.
15. **“Minimum group size is differential privacy.”** Differential privacy is a randomized distributional guarantee with adjacency and parameters.
16. **“Noise makes a mechanism private.”** Sensitivity, clipping, randomness, accounting, composition, and implementation determine the guarantee.
17. **“Changing the release resets privacy budget.”** Composition follows protected contributions, not filenames.
18. **“Synthetic means invented and safe.”** Learned generators can memorize or closely reproduce training data.
19. **“Overall fidelity proves utility.”** Rare groups, tails, temporal order, joins, and target estimands can be badly distorted.
20. **“A sample risk test covers the population.”** Rare and unique records are often exactly what sampling misses.
21. **“One recipient's determination transfers.”** Auxiliary data, incentives, controls, purpose, and release history differ by recipient/environment.
22. **“Contracts replace technical controls.”** Agreements affect environment and remedies but cannot prevent every misuse or compromise.
23. **“Technical controls replace contracts and governance.”** Recipient duties, purpose, onward sharing, review, and authority remain necessary.
24. **“The transformation log may show failed values.”** Logs become an alternate raw dataset unless minimized and protected.
25. **“Key deletion deletes data.”** Plaintext copies, caches, vault exports, tokens, derivatives, and auxiliary mappings may remain.
26. **“Rotation always reduces risk.”** Unplanned rotation can break joins, duplicate identities, strand deletes, and preserve old tokens indefinitely.
27. **“Public releases can be patched later.”** Copies and combined knowledge may be irreversible.
28. **“One successful attack proves every record identifiable.”** Report attack scope and assumptions precisely; do not overgeneralize either direction.
29. **“No successful attack proves safety.”** Tests cover known methods and available evidence, not all future attacks.
30. **“A tool can certify legal anonymity.”** Tools produce scoped transformations and metrics; authorized experts interpret applicable law and context.

## Worked Examples

### Example 1

**Situation.** A support UI shows account numbers as `******1234`, while support staff can filter by exact account number.

**Reasoning.** The presentation mask hides most characters, but the equality-filter endpoint acts as an oracle and logs exact inputs. Raw data remains in storage. Policy must separately restrict filter use, rate-limit and audit it, protect logs, and decide whether last-four display is appropriate for recognition.

**Conclusion.** A dynamic display mask reduces shoulder-surfing exposure but does not de-identify the account or secure every observation path.

### Example 2

**Situation.** Two business units HMAC email addresses with the same secret so analysts can join customers.

**Reasoning.** The keyed transform resists unaided dictionary calculation better than plain hashing, but equal emails produce equal tokens across both units. Anyone with both outputs gains the cross-unit linkage, and anyone with tokenization-oracle access can test candidate emails. Separate domains prevent default linkage; an approved linkage service can mediate exceptional joins.

**Conclusion.** Deterministic token utility is exactly the linkage risk that domain design must govern.

### Example 3

**Situation.** A team truncates random tokens to six decimal digits to satisfy a legacy schema for two million identities.

**Reasoning.** The token space contains only one million values, fewer than the identities, so collisions are guaranteed by the pigeonhole principle. Even below that count, birthday collisions become likely. The schema cannot represent a collision-resistant unique surrogate at this scale.

**Conclusion.** Reject or redesign the legacy interface; truncation can corrupt identity before privacy is even assessed.

### Example 4

**Situation.** A release has $k=4$ for age band and postal prefix, but every member of one class has the same rare diagnosis.

**Reasoning.** Each record shares its quasi-identifier pattern with three peers, so the stated $k$ condition holds. A person known to belong to that group has an uncertain row but a certain diagnosis. Broader classes, suppression, controlled access, distribution constraints, or a different release model may be needed.

**Conclusion.** Identity ambiguity under selected fields does not imply attribute confidentiality.

### Example 5

**Situation.** Monthly releases each suppress cells below ten; membership changes by one person between March and April.

**Reasoning.** Comparing overlapping totals can reveal the entering/leaving person's contribution even though each table meets its threshold. Release history is part of the attack surface. Coordinate suppression, restrict differencing, bound contributions, use formal accounting where suitable, or release less frequently.

**Conclusion.** Single-release checks cannot establish safety under composition.

### Example 6

**Situation.** Dates are shifted independently per event by random offsets.

**Reasoning.** Independent shifting hides absolute dates but can reverse event order and destroy intervals, making longitudinal analysis invalid. Subject-scoped consistent shifts preserve within-subject intervals/order but also preserve a recognizable temporal signature and require a protected key/context.

**Conclusion.** Choose date transformation from required temporal utility and explicitly assess the linkage it preserves.

### Example 7

**Situation.** A public count mechanism adds Laplace noise but allows unlimited repeated identical queries.

**Reasoning.** Averaging many independent noisy answers estimates the true count increasingly well. A valid differential-privacy design accounts for each release, bounds total budget, may memoize answers under a declared scheme, and specifies adjacency and sensitivity. “Noise added” is not the guarantee.

**Conclusion.** Query composition and accounting are part of the mechanism, not operational extras.

### Example 8

**Situation.** A synthetic patient table has excellent marginal distributions but contains exact copies of three rare training records.

**Reasoning.** Aggregate fidelity did not test memorization. Exact/near-duplicate, nearest-neighbor, membership/attribute inference, and rare-record analysis reveal unacceptable leakage. The team changes training/privacy controls or chooses a protected environment and retests utility.

**Conclusion.** Synthetic data needs explicit leakage evaluation as well as fidelity evaluation.

### Example 9

**Situation.** A batch tokenization job processes 99.7% of rows and writes failures with raw values to a dead-letter queue.

**Reasoning.** The output mixes protected tokens with missing identities, and the queue becomes a concentrated raw dataset. Completion must reconcile eligible/transformed/failed counts, quarantine the release, protect or eliminate raw failure payloads, correct parsing, rerun idempotently, and verify no partial consumer use.

**Conclusion.** Coverage and failure handling are privacy controls.

### Example 10

**Situation.** A de-identified partner release was approved last year; a new public registry now contains the same rare occupations and fine locations.

**Reasoning.** Auxiliary-data availability changed a core assumption. The owner pauses new transfers, reevaluates linkage and consequences, tightens generalization or moves the work to an enclave, notifies the partner of conditions, inventories derivatives, and records a new time-bounded decision. Existing public copies may be irrecoverable.

**Conclusion.** De-identification is a lifecycle determination, not a permanent property stamped onto bytes.

## Cross-Program Connections

- [DE-028](028-deduplication-and-record-identity.md) supplies entity resolution and linkage concepts that become adversarial inputs here.
- [DE-066](066-time-travel-and-reproducible-reads.md) binds transformation and approval to immutable input/output generations.
- [DE-082](082-dataset-and-column-lineage.md) finds raw, intermediate, tokenized, masked, released, and downstream copies.
- [DE-085](085-classification-and-sensitive-data.md) models direct/quasi identifiers, context, aggregation and evidence-backed downgrading.
- [DE-086](086-access-control-for-analytical-data.md) supplies recipient, query, unmask, export, vault, key, and enclave controls that reduce but do not erase residual risk.
- Security Engineering's privacy-threat-model and differential-privacy modules own deeper adversary and formal-mechanism treatment; this chapter focuses on production data transformations and releases.
- [DE-088](../ROADMAP.md) applies retention and deletion obligations to raw inputs, keys, vault mappings, intermediates, releases and derivatives.

## References

- National Institute of Standards and Technology, *De-Identifying Government Datasets: Techniques and Governance*, SP 800-188, 2023. <https://csrc.nist.gov/pubs/sp/800/188/final>
- National Institute of Standards and Technology, *De-Identification of Personal Information*, NISTIR 8053, 2015. <https://csrc.nist.gov/pubs/ir/8053/final>
- U.S. Department of Health and Human Services, “Guidance Regarding Methods for De-identification of Protected Health Information,” current official guidance. <https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html>
- European Union, *Regulation (EU) 2016/679*, especially Article 4 and Recital 26, official text. <https://eur-lex.europa.eu/eli/reg/2016/679/oj>
- UK Information Commissioner's Office, “Pseudonymisation,” current guidance. <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/>
- UK Information Commissioner's Office, “Anonymisation,” current guidance hub. <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/>
- National Institute of Standards and Technology, *Methods for Format-Preserving Encryption*, SP 800-38G, 2016. <https://csrc.nist.gov/pubs/sp/800/38/g/upd1/final>
- Google Cloud, “Transformation Reference,” Sensitive Data Protection, current documentation. <https://cloud.google.com/sensitive-data-protection/docs/transformations-reference>
- Google Cloud, “Pseudonymization,” Sensitive Data Protection, current documentation. <https://cloud.google.com/sensitive-data-protection/docs/pseudonymization>
- Latanya Sweeney, “k-Anonymity: A Model for Protecting Privacy,” *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems* 10(5), 2002. <https://doi.org/10.1142/S0218488502001648>
- Cynthia Dwork, “Differential Privacy,” ICALP, 2006. <https://doi.org/10.1007/11787006_1>
- Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith, “Calibrating Noise to Sensitivity in Private Data Analysis,” TCC, 2006. <https://doi.org/10.1007/11681878_14>

## Exercises

### Exercise 1

Distinguish a dynamic display mask, random vault token, deterministic cryptographic token, unkeyed hash, encryption, pseudonymization, and contextual de-identification. For each, name one property it preserves and one risk it does not eliminate.

### Exercise 2

A release contains quasi-identifiers `(age_band, postal_prefix)` with class sizes 8, 5, 5, and 2. The two-record class shares one sensitive diagnosis. Compute $k$, explain the attribute-disclosure counterexample, and propose alternatives while preserving as much geographic utility as possible.

### Exercise 3

Design a tokenization service for customer IDs used by three tenants and two purposes: fraud investigation and product analytics. Address token domains, reversibility, vault/key custody, chosen-input oracle risk, collisions, retries, rotation, cross-domain joins, audit, incident response, and deletion.

### Exercise 4

Compare releasing generalized microdata, synthetic microdata, a protected enclave, and a differentially private query interface for longitudinal research on a rare condition. State threat, utility, composition, operational, and governance trade-offs and choose a justified design.

### Exercise 5

An organization learns that an approved pseudonymized dataset was copied to notebooks, object storage, a partner, two dashboards, and a trained model; its token key may be compromised. Design containment, investigation, re-tokenization or revocation, release-risk reassessment, deletion, consumer communication, and evidence needed to close the incident.

## Answers to the Exercises

### Answer 1

A **dynamic display mask** preserves a recognizable partial representation and current source value; it does not protect raw storage, privileged queries, filters, logs, or inference. A **random vault token** preserves recoverability through a mapping and can avoid deterministic equality; it does not eliminate vault compromise, access misuse, or downstream linkage once mapped. A **deterministic cryptographic token** preserves equality and joins inside its domain; it does not hide frequency, prevent oracle guesses, or eliminate key compromise. An **unkeyed hash** preserves deterministic equality; it does not resist enumeration of low-entropy identifiers.

**Encryption** preserves exact recoverability with a key and protects against parties lacking it; it does not make data anonymous to authorized key holders or remove metadata/linkage. **Pseudonymization** preserves a controlled way to associate records or subjects while separating additional information; it does not generally eliminate personal-data status or re-identification/linkability risk. **Contextual de-identification** combines technical and governance controls to reduce stated disclosure risks for a particular release model; it does not establish safety for every future recipient, auxiliary dataset, purpose, law, attack, or composed release.

### Answer 2

The minimum equivalence-class size is $k=2$. The two-record class meets that identity-ambiguity property under the declared pair of quasi-identifiers, but both records share one diagnosis. If an attacker knows a target belongs to that class, the attacker learns the diagnosis without determining the exact row. Thus $k=2$ does not protect attribute confidentiality.

Inspect whether age can be broadened while retaining three-digit geography; if not, broaden the postal prefix only for the risky class, merge defensible categories, or suppress that class. Evaluate bias introduced for the rare group. Alternatives include releasing coarser aggregates with composition controls, providing detailed data only in a protected enclave, or using an approved query interface. Recompute classes over the full population, test background knowledge and previous releases, and measure the intended geographic estimands. Do not raise $k$ mechanically if doing so destroys the research purpose or masks the rare population entirely.

### Answer 3

Create separate token domains at least by tenant and purpose so product analytics cannot correlate fraud identities or cross tenants by default. Use stable canonical input encoding and versioned context. If detokenization is required for investigations, expose it as a separate strongly authenticated and authorized operation with case ID, dual control where warranted, rate limits, independent alerting, and minimized audit. Product analytics receives no detokenization power. A mediated linkage service can produce a scoped, expiring reconciliation result after approval rather than sharing a global token.

Choose a reviewed cryptographic or random-vault design with adequate token space; quantify collisions and reject silent collision resolution. Protect keys in managed custody and vault mappings in a separately administered service, including backup/recovery. Prevent bulk or chosen-input tokenization from becoming a dictionary oracle through caller/action limits, quotas, anomaly detection, and purpose checks. Make retries idempotent within the intended domain. Version tokens and plan rotation with dual-read/controlled migration, relationship reconciliation, downstream inventory, old-token expiry, and rollback. A compromise triggers key/vault containment, token-domain exposure analysis, credential revocation, re-tokenization where it reduces risk, derivative/partner review, and incident handling. Deletion maps subject-to-token under protected authority and removes required mappings, source and derivatives according to retention policy, with evidence and explicit limits.

### Answer 4

Generalized microdata preserves flexible row-level longitudinal analysis but remains vulnerable to trajectories, rare-condition homogeneity, auxiliary linkage, and release composition; public retraction is weak. Synthetic microdata can support exploration and reduce one-to-one semantics, but rare trajectories may be memorized or distorted, so leakage and subgroup utility tests are essential. A protected enclave keeps detailed real data behind identity, purpose, query, export, monitoring, and output review controls; it costs more to operate and places trust in the enclave and reviewers. A differentially private interface can bound participation influence under defined person-level longitudinal adjacency and contribution limits, but repeated analysis consumes budget and noise can overwhelm rare-condition estimates.

A defensible design uses an enclave for approved qualified researchers needing longitudinal detail, with strict output review and complete release history. Publish only preplanned aggregates through a person-level differentially private mechanism whose contribution bounds, $\varepsilon$, $\delta$, accountant, composition, uncertainty, and utility for the rare condition are reviewed. Synthetic data may support workflow development only after memorization and rare-record tests, with a claim scoped to that use. Avoid public generalized microdata if realistic linkage and trajectory attacks exceed threshold. Governance names recipients, contracts, access, retention, review board, validity, incident and re-evaluation triggers.

### Answer 5

Stop new releases and detokenization/tokenization-oracle access, restrict the suspected key, preserve independently protected logs and configuration, and rotate credentials without destroying forensic evidence. Inventory exact input/output generations, token domain/key versions, vaults, notebooks, storage objects, dashboard caches, partner transfers, model artifacts, scheduled refreshes, backups, users, queries, exports, and lineage. Determine whether the key was accessed or exfiltrated, which tokens and raw values could be tested or reversed, whether domains were reused, and what auxiliary/release data enables identity, attribute, membership, or reconstruction attacks.

Re-tokenization helps only if old tokens and mappings can be contained and downstream joins migrated safely. Create a new domain/key, transform from an authorized source, reconcile counts and identities, update consumers in controlled order, invalidate old access, and prevent mixed-token silent joins. Revoke sessions, services, shares, caches and jobs; quarantine notebooks/objects; ask the partner to suspend use and preserve evidence under agreement. Delete or retain each copy according to legal hold, contract, retention and incident policy; verify actions, including model disposition or retraining where memorization/linkage risk exists.

Reassess disclosure using compromise capability, token equality/frequency, chosen-input access, auxiliary sources, all releases, recipients and harms. Owners, security/privacy/risk authorities and qualified legal reviewers decide notification, continued use and remediation. Closure evidence includes scope/coverage, timeline, key/vault audit, access/export history, artifact and recipient attestations, containment tests, re-tokenization reconciliation, old-domain denial tests, deletion receipts, model decision, residual-risk approval, consumer communication, control corrections and recurrence monitoring. Absence of confirmed re-identification is not by itself proof of closure.
