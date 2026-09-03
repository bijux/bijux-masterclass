---
module_id: DARCH-078
program: Data Architecture Engineering
level: 2
module_number: 78
title: Masking, Tokenization, and Clean Rooms
status: complete
last_verified: 2026-09-03
---

# Masking, Tokenization, and Clean Rooms

## One-Page Review

### Governing question

How should a data architecture reduce what people and systems can learn from sensitive data while preserving approved utility, linkage, and collaboration, with explicit threat models and evidence, instead of assuming that a masked display, tokenized identifier, or product called a clean room makes data anonymous or safe?

### Essential definitions

- **Masking** transforms or suppresses values for a defined audience and operation; it can be static in a derived copy or dynamic at query or presentation time.
- **Redaction** removes or obscures selected content in a released representation while the source may remain unchanged.
- **Pseudonymization** replaces or separates identifying information so attribution requires additional information that is protected separately; pseudonymous data can remain personal data.
- **Tokenization** substitutes a value with a token under a defined token domain and mapping or generation method.
- A **token domain** defines eligible inputs, uniqueness, format, stability, scope, collision behavior, and who may compare or reverse tokens.
- A **token vault** protects reversible mappings between source values and tokens; a vault is a concentrated trust boundary, not merely a lookup table.
- **Detokenization** is an authorized, attributable operation that resolves a reversible token to its protected source value.
- **Format-preserving encryption** is reversible encryption whose ciphertext remains in a selected alphabet and length domain; it is not synonymous with tokenization.
- **De-identification** applies technical and governance measures to reduce identification risk for a defined release and environment.
- **Anonymization** is a contextual claim that people are not identifiable under the applicable test and realistic means, not a name for one transformation.
- A **clean room** is a governed collaboration environment that restricts data, code, queries, identities, outputs, and operations among parties that need not reveal raw inputs to one another.
- An **analysis rule** constrains allowed joins, columns, predicates, functions, groups, outputs, recipients, or approved templates.
- An **output gate** evaluates proposed results against aggregation, disclosure, purpose, budget, and human-review rules before release.
- A **privacy budget** accounts for cumulative permitted disclosure under a specified mechanism; it is not a generic spending limit or guarantee against every attack.
- **Remote attestation** supplies evidence about an executing workload and environment to a relying party; it does not prove the workload's purpose, correctness, or harmless output.
- A **release receipt** records inputs by protected identity, policy and code versions, execution, budget use, output decision, recipients, time, evidence, and limitations without recreating sensitive content.

### Central model, mechanism, or theorem

Represent protected-data use as:

`M = (D, U, T, K, C, Q, O, A, R, L)`

where `D` is the data and identification environment, `U` approved utility, `T` transformations and token domains, `K` keys, vaults, and trust boundaries, `C` collaboration parties and computing boundary, `Q` permitted queries and workloads, `O` output and composition controls, `A` assurance and attack testing, `R` risk, remedy, and review, and `L` lifecycle and closure. A release is defensible only when transformations and execution controls jointly satisfy a stated purpose and threat model. No technique name alone proves anonymity, confidentiality, minimization, or compliance.

### Critical invariants

- Source value, masked value, token, ciphertext, pseudonym, anonymous release, query, result, and claim have separate identities and evidence.
- Every transformation binds input and output schema, purpose, audience, environment, method and version, keys or mappings, time, reversibility, and limitations.
- Pseudonymous and tokenized data remains governed according to realistic linkability and available additional information.
- Stable cross-context tokens are issued only when authorized linkage is an explicit purpose; domain separation prevents accidental universal identifiers.
- Low-entropy identifiers are not protected by plain unsalted hashing against enumeration.
- Vault, key, configuration, logs, caches, exports, and recovery copies receive controls at least as strong as the relationships they expose.
- Dynamic masking cannot substitute for row, purpose, export, query, and administrative authorization.
- Clean-room input confidentiality, workload integrity, output privacy, purpose limitation, and operational governance are assessed independently.
- Query approval, aggregation thresholds, differential privacy, attestation, and audit logs are complementary and do not imply one another.
- Repeated queries, overlapping cohorts, auxiliary data, collusion, timing, errors, and releases outside the room enter the attack model.
- Unknown identifiability, policy conflict, exhausted budget, unapproved code, unverifiable execution, or unsafe output fails closed and remains observable.
- Revocation, correction, deletion, key rotation, vault recovery, collaborator departure, and later reidentification findings propagate through every dependent asset.

### Common failures

Common failures include calling masking encryption; calling tokenization anonymization; publishing deterministic hashes of emails; using one token across customers and purposes; keeping a vault beside its data; granting broad detokenization; leaking source values in logs; masking displays but permitting exports; applying fixed substitution to tiny domains; ignoring free text and images; treating k-anonymity as a universal guarantee; selecting thresholds without population or auxiliary-data analysis; assuming aggregation prevents differencing; resetting privacy budgets through aliases; approving SQL text while dependencies change; allowing arbitrary user-defined functions; trusting a clean-room product name; confusing attestation with code review; sending raw results to an unrestricted recipient; and retaining joined datasets after the collaboration ends.

### Compact example

Ten invented release attempts are evaluated against declared purpose, token domain, approved template, minimum group size, remaining budget, output columns, and recipient. Three are declared allowed, two fail purpose, one uses a cross-domain token, one uses an unapproved query, one has a small group, one exceeds budget, and one exposes a forbidden column. Executable evidence confirms only those declarations and counts. It proves no real identity protection, cryptographic strength, vault security, differential-privacy guarantee, workload integrity, absence of side channels, legal compliance, or beneficial outcome.

### Connections

[DARCH-064](064-lineage-architecture.md), [DARCH-069](069-metadata-apis-and-eventing.md), [DARCH-072](072-policy-as-code-for-data.md), [DARCH-073](073-classification-architecture.md), [DARCH-074](074-consent-and-purpose-limitation.md), and [DARCH-077](077-deletion-and-the-right-to-erasure.md) establish provenance, interfaces, policy, classification, purpose, and lifecycle control. [DARCH-079](../ROADMAP.md) next develops audit and provenance architecture.

## Governing Question

An analyst may need stable customer linkage without names, a support agent may need only the last four digits of an account number, and two firms may need an aggregate overlap count without seeing one another's rows. Those are different uses, adversaries, outputs, and failure consequences. One `masked = true` field cannot represent them.

The governing question is how to reduce exposure while retaining precisely approved utility. A durable architecture defines the data and attacker environment, separates transformations from access control, limits linkability and reversal, governs collaborative computation and cumulative outputs, tests residual identification risk, and keeps every claim proportional to evidence.

## Why This Matters

NIST [SP 800-188](https://www.nist.gov/publications/de-identifying-government-datasets-techniques-and-governance) describes de-identification as a lifecycle and governance discipline, covers direct and quasi-identifiers, masking, sampling, generalization, synthetic data, differential privacy, reidentification studies, disclosure review, and the Five Safes. It cautions that tools that merely mask personal information may not perform sufficient de-identification and recommends qualified review rather than a technique-name guarantee.

NIST [NISTIR 8053](https://csrc.nist.gov/pubs/ir/8053/final) analyzes de-identification of personally identifiable information, reidentification risk, data models, techniques, governance, and operational challenges. Identifiability changes with released attributes, population, outside data, recipients, agreements, and time. A transformation must therefore be evaluated in its data environment.

The UK Information Commissioner's Office's current [anonymisation guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/about-this-guidance/) distinguishes anonymisation and pseudonymisation, uses a risk-based identifiability analysis, and addresses accountability and governance. The guidance is under review following UK legal changes, so architecture should version both its source and its adopted decision profile.

The ICO's [pseudonymisation guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/) explains that pseudonymisation can reduce risk while retaining utility, that additional identifying information should be kept separately, and that hashing, encryption, and tokenisation have different properties. Pseudonymized data remains governed; weak or unkeyed hashes of guessable identifiers can be reversed through enumeration.

NIST [SP 800-38G](https://csrc.nist.gov/pubs/sp/800/38/g/upd1/final) specifies FF1 and FF3 format-preserving encryption methods over defined domains. Format preservation can ease integration with legacy fields, but encryption remains reversible and depends on approved algorithms, domains, tweaks, key management, and current guidance. A value that looks like a card number is not necessarily a token, and preserving format can preserve validation or inference surfaces.

The PCI Security Standards Council's [Tokenization Product Security Guidelines](https://www.pcisecuritystandards.org/documents/Tokenization_Product_Security_Guidelines.pdf) distinguishes irreversible, reversible cryptographic, and reversible non-cryptographic tokens and addresses generation, mapping, vaults, keys, administration, logging, and lifecycle. PCI SSC states that this material is supplemental guidance, not a validation program or replacement for a standard; its payment scope must not be generalized silently.

AWS [Clean Rooms analysis rules](https://docs.aws.amazon.com/clean-rooms/latest/userguide/analysis-rules.html) constrain configured tables through aggregation, list, or custom rule types and apply the more restrictive controls across referenced tables. Supported controls include allowed analyses, join and output columns, thresholds, comparison constraints, and differential privacy. These are product-specific primitives; correct policy and adversarial query analysis remain the customer's responsibility.

Google BigQuery's current [data clean rooms documentation](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms) describes governed sharing using views and analysis rules and explicitly cautions that analysis rules may not fully prevent sophisticated extraction, recommending approved query templates for tighter control. This is a useful reminder that a query grammar is not a complete disclosure-control proof.

Google Cloud's [Confidential Space overview](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview) describes an isolated trusted execution environment, encrypted collaborator resources, workload identity, attestation, and role separation among data collaborators, workload authors, and operators. Confidential computing can protect data during execution, while output logic, source correctness, endpoint security, and authorized purpose remain separate concerns.

Microsoft's [multi-party data analytics guidance](https://learn.microsoft.com/en-us/azure/confidential-computing/multi-party-data) presents confidential-computing building blocks for clean-room solutions. Provider examples show feasible trust boundaries, not universal privacy guarantees. Each deployment still needs explicit participant, code, key, attestation, output, logging, incident, and lifecycle design.

Snowflake's [clean-room differential privacy documentation](https://docs.snowflake.com/en/user-guide/cleanrooms/differential-privacy) distinguishes differential privacy from simple aggregation and masking, tracks query cost against a privacy budget, and states that customers must configure the controls for their requirements. A budget's adjacency definition, unit of privacy, contribution bounds, mechanism, allocation, and reset semantics determine what the numbers mean.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, derivations, attribution, association, and delegation. It can connect source versions, transformation jobs, token domains, approved workloads, queries, releases, and reviewers. Provenance explains how a protected release arose; it does not establish that the method or result is safe.

Together these sources support context-specific de-identification, distinct cryptographic and tokenization controls, governed collaboration, restrictive queries, cumulative release analysis, workload assurance, provenance, and lifecycle accountability. They do not justify a universal `anonymous` flag.

## Prerequisites and Retrieval

You should understand privacy and security risk, classification, purpose limitation, access control, data modeling, probability, cryptographic hashes and message authentication, symmetric encryption, key management, databases, query planning, distributed systems, confidential computing, differential privacy, audit, incident response, deletion, and recovery.

Retrieve masking, redaction, suppression, substitution, shuffling, generalization, perturbation, pseudonymization, de-identification, anonymization, token, token domain, vault, detokenization, deterministic encryption, format-preserving encryption, salt, pepper, HMAC, linkage, quasi-identifier, k-anonymity, l-diversity, t-closeness, differential privacy, adjacency, epsilon, delta, contribution bound, privacy budget, clean room, analysis rule, template, output gate, attestation, side channel, collusion, release, and closure.

As a retrieval test, inspect `sha256(lower(email))` shared with a partner. Ask whether the email population is guessable; whether normalization creates false matches; who can enumerate inputs; whether the same digest exists elsewhere; whether cross-purpose linkage is authorized; whether a secret key or domain separation exists; what unmatched and collision behavior means; which rows, outputs, and repeated queries are allowed; and whether deletion propagates. The digest length answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish display masking, redaction, pseudonymization, tokenization, hashing, encryption, format-preserving encryption, de-identification, and anonymization;
2. design static and dynamic masking at field, row, object, document, image, and output boundaries;
3. define token domains, generation, uniqueness, stability, reversibility, vault, detokenization, keys, and rotation;
4. evaluate linkability, enumeration, collision, frequency, auxiliary-data, insider, compromise, and recovery threats;
5. select release transformations according to purpose, utility, population, environment, recipients, and realistic identification risk;
6. architect clean rooms across participants, data, workloads, identities, queries, results, budgets, logs, and lifecycle;
7. combine templates, thresholds, contribution limits, differential privacy, attestation, output review, and contractual controls without conflating them;
8. implement policy, APIs, events, receipts, monitoring, incidents, correction, deletion, migration, and recovery;
9. test repeated queries, overlapping cohorts, collusion, side channels, malicious code, stale policy, and unsafe exports; and
10. state bounded assurance claims and defer legal, privacy, cryptographic, statistical, domain, and affected-person decisions to authorized reviewers.

## Core Exposition

**Begin with purpose and release.** State who needs which operation, on which population, for what decision, for how long, and with what output. Define forbidden learning and likely harm. “Protect the data” is not an actionable requirement.

**Model the data environment.** Inventory source values, quasi-identifiers, rare combinations, free text, images, metadata, joins, public records, brokered data, prior releases, recipient holdings, models, and future enrichment. Identification risk belongs to this environment, not to one column in isolation.

**Separate visibility from existence.** A masked user interface can hide values from one role while the API, export, query engine, logs, caches, browser, warehouse, or administrator still exposes them. Record the exact boundary and never label the source value itself masked merely because one renderer obscures it.

**Choose static or dynamic masking deliberately.** Static masking produces a governed derivative for development, testing, analytics, or release. It needs reproducible transformation, lineage, refresh, quality tests, storage, access, and deletion. Dynamic masking transforms results at access time and needs fail-closed policy, row context, query semantics, cache control, export rules, and administrator separation.

**Preserve utility intentionally.** Full suppression minimizes disclosure but can destroy analysis. Partial display preserves recognition. Generalization preserves coarse distributions. Shuffling may preserve marginal distributions but break relationships. Substitution can preserve realistic form. Perturbation changes values. Synthetic generation creates new records under a model. Each retains and leaks different structure.

**Treat free text and media as first-class.** Identifiers can occur in prose, code, images, audio, filenames, EXIF data, document history, embedded objects, and OCR. Detection has false positives and negatives. High-consequence releases require representative testing and review, not only regular expressions.

**Define pseudonymization context.** Record who holds the additional information, which systems can combine it, which users can request reidentification, whether external data links subjects, and how long the relation persists. Moving a mapping to another table without access separation is not meaningful separation.

**Define the token domain.** Specify input namespace and normalization, output alphabet and length, random or deterministic generation, uniqueness, collision handling, stability, tenant and purpose scope, reversibility, lifecycle, and allowed comparisons. A token without its domain contract is ambiguous data.

**Minimize linkability.** A universal deterministic token becomes a durable tracking identifier. Derive domain-specific tokens for approved joins, such as one collaboration and purpose, so compromise or sharing does not join unrelated contexts. Cross-domain translation should be a separately authorized service and event.

**Protect low-entropy identifiers.** Emails, telephone numbers, national identifiers, dates, postal codes, and product codes are often enumerable. Plain hashing, predictable salts, and globally shared peppers permit guessing or linkage. Use an appropriate keyed construction or token service with domain separation and rate limits when stable matching is required, and keep the key outside the released environment.

**Do not confuse HMAC with anonymity.** A keyed digest can resist outsiders who lack the key and support deterministic matching. Key holders can still compute candidates, the output remains linkable, compromise affects the domain, and auxiliary attributes can identify people. Describe it as a pseudonymization control under stated assumptions.

**Design reversible tokenization as privileged computation.** The vault maps tokens to source values, enforces caller, purpose, subject, field, action, case, and time, and emits minimized receipts. Detokenization should be narrow, rate-limited, monitored, dual-controlled where appropriate, and unavailable to ordinary analytics roles.

**Harden the vault.** Separate data, service, administration, keys, backups, and logs; encrypt transport and storage; protect integrity and availability; restrict bulk reads; detect enumeration; rotate credentials; test recovery; and apply retention and erasure. A perfectly random token does not compensate for an exported vault.

**Distinguish vaultless schemes.** Reversible cryptographic tokens or format-preserving ciphertext can avoid a mapping database but concentrate trust in keys, algorithms, tweaks, domains, and implementations. They require cryptographic review, current approved parameters, strong key isolation, versioning, misuse resistance, and migration plans.

**Treat format as leakage.** Preserving length, alphabet, prefixes, checksums, sorting, or frequency can simplify legacy integration while revealing class and relationships. Document retained structure. Do not let valid-looking protected values escape into real payment, identity, messaging, or operational networks.

**Manage collisions and normalization.** Random token generation needs collision detection appropriate to domain size. Deterministic inputs need canonicalization rules with locale, Unicode, punctuation, aliases, and valid time. A normalization change creates a new algorithm version and can split or merge identities.

**Version every transformation.** Store method identity, code and configuration digest, key or vault version, token domain, input and output schema, purpose, effective interval, owner, tests, and limitations. Never silently reinterpret old tokens under a new normalization or key.

**Rotate without breaking meaning.** Decide whether rotation preserves tokens, creates new tokens, or supports a bounded translation window. Re-tokenization must maintain lineage and authorized joins while preventing old and new domains from becoming a bridge. Retire keys and mappings only after dependent copies, restores, and deletion duties are resolved.

**Assess de-identification as a release process.** Define release unit, audience, agreement, access environment, allowed linking, output, attack resources, time horizon, and consequence. Direct-identifier removal is an input to assessment, not the conclusion.

**Analyze quasi-identifiers and rare values.** Combinations of age, location, dates, events, occupation, diagnoses, and behavior can isolate subjects. Generalization and suppression must be tested on relevant equivalence classes and important subpopulations. A global average can conceal severe risk for a rare group.

**Use k-anonymity carefully.** It can require each released quasi-identifier pattern to appear at least `k` times under a chosen attribute set. It does not prevent homogeneous sensitive values, background knowledge, semantic inference, linkage through omitted attributes, or composition with another release. `k` is not a probability or universal safety threshold.

**Treat differential privacy as a specified mechanism.** Name neighboring datasets, privacy unit, contribution bounds, clipping, sensitivity, mechanism, epsilon, delta where relevant, accounting method, allocation, release history, and implementation. The symbol `ε` without those semantics is decoration.

**Budget composition across identities and time.** Repeated and correlated queries can reveal what one result hides. Bind budget to the real analyst, organization, purpose, dataset version, privacy unit, and release family. Prevent account aliases, copied rooms, scheduled jobs, and exports from resetting the effective budget.

**Build clean rooms as systems, not rooms.** Identify data contributors, analysts, query authors, workload authors, operators, result recipients, reviewers, auditors, platform providers, and attackers. Separate duties and specify which parties may collude. A single administrator holding every role collapses the trust model.

**Keep source custody explicit.** Inputs may remain in contributor-controlled storage, be copied to a collaboration boundary, or be encrypted for an attested workload. Record exact location, ownership, keys, replicas, staging, logs, and deletion. “Data does not move” can still permit a remote workload to read it.

**Approve schemas and joins.** Specify allowed tables, versions, columns, identities, token domains, join graph, join direction, cardinality, null behavior, and temporal window. A blind match protects raw join values from some parties but can still reveal membership or overlap.

**Constrain query capability.** Prefer reviewed templates for high-risk uses. Parameter types, ranges, predicates, functions, subqueries, user-defined code, network access, files, errors, explain plans, intermediate results, and execution time are all capability surfaces. SQL parsing alone cannot establish semantic safety.

**Enforce contribution and group bounds.** Cap how much one privacy unit can affect a result. Apply minimum groups where appropriate. Guard against row duplication, many-to-many joins, null groups, sparse dimensions, filters, and correlated attributes that bypass intended limits.

**Design an independent output gate.** Evaluate schema, columns, groups, cells, statistical disclosure, policy, purpose, recipient, budget, prior releases, and reviewer requirements before results leave. The computation boundary and release boundary are distinct; an analyst who can write arbitrary output storage bypasses the gate.

**Account for differencing and composition.** Nearly identical cohort queries can reveal an excluded person's value. Overlapping rooms, dashboards, extracts, and public reports compose. Maintain a release ledger with canonical query meaning and data versions, not just SQL strings.

**Use confidential computing for a defined threat.** Attested isolated execution can restrict operator or collaborator access to plaintext. Validate endorsement, measurement, configuration, nonce, freshness, debug state, identity, key-release policy, and revocation. Review code and outputs separately; a faithfully attested malicious program remains malicious.

**Control side channels and egress.** Errors, counts, timing, memory, resource use, logs, network calls, package downloads, crash dumps, temporary storage, and model artifacts can disclose inputs. Disable unnecessary interfaces, bound responses, pin dependencies, isolate tenants, and test the actual platform threat model.

**Bind contracts to technical policy.** Agreements define purpose, parties, permitted data, analyses, outputs, onward use, retention, deletion, audit, incidents, rights, remedies, and departure. Encode enforceable portions as versioned policy, but keep signed authority and human interpretation distinct from configuration.

**Preserve provenance without preserving secrets.** A release receipt names protected source versions, transformation and policy digests, workload identity, query or template, budget decision, reviewer, output digest, recipient, and time. Do not copy raw query parameters, small groups, source values, or released payloads into broadly accessible logs.

**Measure controls and outcomes separately.** Track protected datasets, transformation coverage, token-domain exceptions, detokenization, vault failures, approved queries, denied queries, budget, group suppression, output review, incidents, reidentification tests, participant complaints, and useful decisions. Publish denominators and uncertainty.

**Plan incident response.** Prepare for key or vault compromise, cross-domain linkage, unsafe masking, query bypass, output leakage, malicious code, attestation failure, budget reset, collusion, wrong recipient, reidentification, and deletion failure. Contain access, freeze releases, preserve bounded evidence, assess affected domains, rotate, reissue, notify, correct, and verify.

**Support rights and deletion.** Tokenization does not eliminate subject relationships. Maintain protected lookup or subject-edge mechanisms needed to locate, restrict, correct, and erase source data, tokens, mappings, derivatives, room inputs, releases, and caches under authorized decisions.

**Recover policy before data access.** Restore identities, revoked collaborators, token-domain definitions, keys, vault controls, approved code, query rules, release ledger, budgets, tombstones, and incident blocks before enabling workloads. Quarantine restored outputs until current policy and deletion state are reconciled.

**Close collaborations completely.** Stop jobs, revoke identities and attestations, disable templates, remove keys and mappings according to authority, delete staged data and outputs, reconcile recipients, expire caches and backups, settle incidents and disputes, and retain minimum evidence. Later reuse requires a new authorized collaboration, not resurrection of an old room.

## Definitions and Notation

Let a protected-use specification be:

`M = (D, U, T, K, C, Q, O, A, R, L)`.

For a transformation `t`, define:

`t = (domain, input_schema, output_schema, purpose, audience, environment, method_version, key_or_mapping, reversibility, valid_time)`.

A token domain is:

`d = (namespace, normalization, alphabet, length, generation, uniqueness, stability, scope, collision_policy, reversal_policy)`.

For a release request `q`, let `allowed(q)` require current authority, approved data and purpose, an approved workload or template, authorized joins and outputs, a permitted recipient, a satisfied disclosure test, sufficient cumulative budget, and observable evidence.

For a simple threshold release with group sizes `n_g`, a necessary declared condition may be:

`min_g(n_g) ≥ k`.

This condition is not sufficient for anonymity: attribute homogeneity, auxiliary information, differencing, overlapping releases, and outliers can still disclose people.

For a differential-privacy mechanism, write:

`Pr[M(X) ∈ S] ≤ exp(ε) · Pr[M(X') ∈ S] + δ`

for defined neighboring datasets `X` and `X'`, outcomes `S`, and mechanism `M`. Assurance requires the adjacency relation, privacy unit, contribution bounds, sensitivity, accountant, implementation, and full release history—not only `ε` and `δ`.

Define declared query coverage as:

`C_q = governed_query_attempts / expected_query_attempts`.

Define declared output-gate coverage as:

`C_o = gated_external_releases / expected_external_releases`.

Define token-domain exception rate as:

`R_d = unauthorized_or_global_domain_findings / inspected_token_uses`.

Each denominator must include failed, shadow, scheduled, administrator, export, API, notebook, and recovery paths in scope. Unknown paths remain unknown.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Purpose gate.** Identify authority, parties, population, operation, utility, prohibited learning, outputs, time, and affected people.

**Environment gate.** Inventory source data, identifiers, quasi-identifiers, prior releases, auxiliary data, recipients, agreements, attackers, and likely future linkage.

**Transformation gate.** Select masking, suppression, generalization, substitution, pseudonymization, tokenization, encryption, synthetic generation, or statistical mechanisms with explicit semantics.

**Token-domain gate.** Approve normalization, scope, stability, uniqueness, collision behavior, reversibility, mapping, keys, translation, rotation, and retirement.

**Custody gate.** Isolate source data, mappings, keys, configuration, staging, logs, exports, backups, and administrative identities.

**Collaboration gate.** Define contributors, authors, analysts, operators, recipients, reviewers, providers, duty separation, and collusion assumptions.

**Workload gate.** Pin and review code, templates, dependencies, parameters, joins, functions, network, storage, errors, attestation, and revocation.

**Query gate.** Enforce approved tables, columns, joins, predicates, group and contribution bounds, budgets, rates, and current policy.

**Output gate.** Test result schema, small cells, rare values, differencing, cumulative release, purpose, recipient, and required review before egress.

**Evidence gate.** Record protected provenance, policy and code versions, decisions, executions, budget, reviewers, recipients, and limitations without leaking source or small-group data.

**Attack gate.** Test enumeration, frequency, linkage, auxiliary data, malicious query, composition, collusion, side channels, vault compromise, key compromise, and recovery.

**Operations gate.** Monitor detokenization, exceptions, queries, denied attempts, releases, drift, incidents, complaints, and useful outcomes with denominators.

**Correction gate.** Freeze unsafe releases, revoke access, rotate domains, reissue derivatives, notify recipients, investigate reidentification, delete unauthorized outputs, and verify repair.

**Recovery gate.** Restore policy, identities, keys, vault rules, ledgers, budgets, deletion state, and revocations before protected data and workloads.

**Closure gate.** End access and computation, delete or retain every asset under authority, reconcile recipients and backups, and preserve minimum interpretable evidence.

### Executable evidence: protected-release policy evaluation

The following program classifies ten invented release attempts using only declared fields.

<!-- bijux-verify: {"id":"protected-release-policy-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"attempts=10\nallowed=3\npurpose_denied=2\ncross_domain_token=1\nunapproved_query=1\nsmall_group=1\nbudget_exceeded=1\nforbidden_output=1\nparticipants=4\ndatasets=5\ntoken_domains=3\ndecision_events=10\n","stderr":""}} -->
```python
attempts = [
    {"participant": "analyst-a", "dataset": "orders", "purpose": True, "domain": "room-a", "expected_domain": "room-a", "template": True, "group": 40, "minimum": 20, "cost": 1, "budget": 5, "forbidden": False},
    {"participant": "analyst-b", "dataset": "visits", "purpose": True, "domain": "room-a", "expected_domain": "room-a", "template": True, "group": 31, "minimum": 20, "cost": 2, "budget": 5, "forbidden": False},
    {"participant": "analyst-a", "dataset": "campaigns", "purpose": True, "domain": "room-b", "expected_domain": "room-b", "template": True, "group": 25, "minimum": 20, "cost": 1, "budget": 2, "forbidden": False},
    {"participant": "analyst-c", "dataset": "orders", "purpose": False, "domain": "room-a", "expected_domain": "room-a", "template": True, "group": 50, "minimum": 20, "cost": 1, "budget": 5, "forbidden": False},
    {"participant": "analyst-d", "dataset": "claims", "purpose": False, "domain": "room-c", "expected_domain": "room-c", "template": True, "group": 60, "minimum": 20, "cost": 1, "budget": 5, "forbidden": False},
    {"participant": "analyst-a", "dataset": "visits", "purpose": True, "domain": "global", "expected_domain": "room-a", "template": True, "group": 35, "minimum": 20, "cost": 1, "budget": 5, "forbidden": False},
    {"participant": "analyst-b", "dataset": "orders", "purpose": True, "domain": "room-a", "expected_domain": "room-a", "template": False, "group": 45, "minimum": 20, "cost": 1, "budget": 5, "forbidden": False},
    {"participant": "analyst-c", "dataset": "research", "purpose": True, "domain": "room-c", "expected_domain": "room-c", "template": True, "group": 4, "minimum": 20, "cost": 1, "budget": 5, "forbidden": False},
    {"participant": "analyst-d", "dataset": "claims", "purpose": True, "domain": "room-c", "expected_domain": "room-c", "template": True, "group": 28, "minimum": 20, "cost": 6, "budget": 5, "forbidden": False},
    {"participant": "analyst-b", "dataset": "research", "purpose": True, "domain": "room-c", "expected_domain": "room-c", "template": True, "group": 27, "minimum": 20, "cost": 1, "budget": 5, "forbidden": True},
]

def evaluate(attempt):
    if not attempt["purpose"]:
        return "purpose_denied"
    if attempt["domain"] != attempt["expected_domain"]:
        return "cross_domain_token"
    if not attempt["template"]:
        return "unapproved_query"
    if attempt["group"] < attempt["minimum"]:
        return "small_group"
    if attempt["cost"] > attempt["budget"]:
        return "budget_exceeded"
    if attempt["forbidden"]:
        return "forbidden_output"
    return "allowed"

results = [evaluate(attempt) for attempt in attempts]
print(f"attempts={len(attempts)}")
for outcome in ["allowed", "purpose_denied", "cross_domain_token", "unapproved_query", "small_group", "budget_exceeded", "forbidden_output"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"participants={len({attempt['participant'] for attempt in attempts})}")
print(f"datasets={len({attempt['dataset'] for attempt in attempts})}")
print(f"token_domains={len({attempt['expected_domain'] for attempt in attempts})}")
print(f"decision_events={len(results)}")
```

The declared output contains ten attempts, three allowed outcomes, two purpose denials, and one result for each other denial. It also counts four participants, five datasets, three expected token domains, and ten decision events.

The evidence is deliberately narrow. Invented Booleans and integers do not establish identity, authority, purpose, domain isolation, query meaning, group independence, contribution bounds, budget accounting, recipient safety, cryptography, privacy, or real execution. The evaluator trusts declarations, ignores history and collusion, and performs no masking, tokenization, query, attestation, or release. Production assurance needs authorized profiles, representative data, protected keys and mappings, real engine controls, cumulative ledgers, independent output tests, incident correction, affected-party review, and recovery exercises.

## Alternatives and Trade-Offs

**Full suppression.** Disclosure falls sharply. Utility, debugging, support, and referential integrity may disappear.

**Partial display masking.** People can recognize values. Small domains and surrounding context can reveal them.

**Static masked copies.** Tools need fewer runtime controls. Copies drift, multiply, and require full lifecycle governance.

**Dynamic masking.** One source supports several audiences. Policy bypass, caching, exports, and privileged users become critical.

**Random tokens.** Frequency and source form can be hidden. Stable joins require a mapping service and collision control.

**Deterministic domain tokens.** Authorized matching is efficient. Frequency and within-domain linkability remain.

**Universal tokens.** Cross-system joins are easy. Compromise and secondary use create an enterprise tracking identifier.

**Vaulted tokenization.** Algorithms and mappings are separable and revocable. The vault is a high-value availability and confidentiality dependency.

**Vaultless cryptographic transformation.** Mapping storage disappears. Key, algorithm, domain, and implementation assurance become decisive.

**Format preservation.** Legacy integration is simpler. Structure, class, checksums, and accidental operational use remain risks.

**Generalization and suppression.** Interpretability can remain high. thresholds depend on selected quasi-identifiers and releases.

**Synthetic data.** Direct source rows need not be distributed. Memorization, outliers, fidelity, bias, and membership risk require testing.

**Minimum aggregation.** Rules are understandable. Differencing, homogeneity, correlated groups, and repeated queries can defeat them.

**Differential privacy.** Composition has a formal model. Correct contribution bounds, budgets, utility, and implementation are demanding.

**Reviewed templates.** Semantic control and repeatability improve. New questions require review and parameters can still leak.

**Restricted query grammar.** Exploration is more flexible. Equivalent attacks and engine features are hard to enumerate.

**Provider-managed clean room.** Integration and controls arrive quickly. Trust, feature, evidence, portability, and provider semantics are constrained.

**Confidential-computing room.** Operator access can be reduced. Hardware, firmware, attestation, code, side channels, and output remain in scope.

**Central output review.** Cross-release disclosure is visible. Latency, reviewer expertise, and concentrated authority increase.

**Automated output gates.** Scale and consistency improve. Misspecified rules can release unsafe results or block legitimate work.

**Short collaboration lifecycle.** Residual exposure shrinks. Reauthorization and repeat analyses cost more.

**Durable collaboration.** Longitudinal utility improves. Participant changes, policy drift, accumulated outputs, and deletion become harder.

## Failure Modes and Misconceptions

1. **“Masked means anonymous.”** Masking may only alter one representation for one audience.
2. **“Removing names removes identity.”** Quasi-identifiers and outside data can identify people.
3. **“Pseudonymous data is no longer personal.”** Linkability and additional information can remain.
4. **“A long hash cannot be reversed.”** Guessable inputs can be enumerated.
5. **“A public salt stops guessing.”** It changes precomputation, not the feasibility of targeted enumeration.
6. **“One secret pepper solves linkage.”** Compromise, broad scope, insiders, and auxiliary attributes remain.
7. **“HMAC output is anonymous.”** It is a keyed, often linkable pseudonym under stated assumptions.
8. **“Token means random.”** Tokens may be cryptographic, mapped, deterministic, or structured.
9. **“Tokenization is encryption.”** Mapping and cryptographic reversal have different mechanisms and evidence.
10. **“Encryption is tokenization.”** Ciphertext semantics do not create a token-domain contract.
11. **“Format preservation is harmless.”** Length, alphabet, prefixes, frequency, and validity can leak.
12. **“A vault is just another table.”** It is a concentrated identity, key, integrity, and availability boundary.
13. **“Detokenization needs only role access.”** Purpose, subject, field, case, rate, time, and evidence matter.
14. **“Stable tokens are always useful.”** Cross-context stability enables surveillance and unauthorized joins.
15. **“One enterprise token simplifies governance.”** It collapses purpose and tenant boundaries.
16. **“Normalization is an implementation detail.”** It changes matches, collisions, and identity meaning.
17. **“Random generation cannot collide.”** Finite domains require detection and policy.
18. **“Key rotation is transparent.”** It can break joins or create translation bridges.
19. **“Dynamic masking is access control.”** Source rows, predicates, exports, caches, and administrators remain.
20. **“Static masking is done once.”** Refresh, drift, deletion, and new fields require lifecycle control.
21. **“Regular expressions find every identifier.”** Context, free text, media, and unknown formats defeat them.
22. **“Substitution preserves only utility.”** Realistic surrogates can create confusion and new sensitive values.
23. **“Shuffling anonymizes a table.”** Marginals, rare values, and external relationships can remain.
24. **“Generalization always lowers risk.”** Poor bins can isolate groups or expose sensitive homogeneity.
25. **“k-anonymity is a probability guarantee.”** It is a property under selected attributes and data.
26. **“A high k proves safety.”** Homogeneity, background knowledge, and composition remain.
27. **“Synthetic means unrelated to people.”** Models can memorize or reproduce rare records.
28. **“Differential privacy is added noise.”** Adjacency, contribution bounds, mechanism, and accounting define the guarantee.
29. **“Epsilon is comparable without context.”** Units, adjacency, delta, population, and composition differ.
30. **“Budgets reset every day harmlessly.”** Repeated releases can compose across reset windows.
31. **“Aggregation prevents disclosure.”** Small cells, differencing, dominance, and auxiliary data remain.
32. **“A minimum group size is sufficient.”** One member can dominate a sum or every member share a trait.
33. **“A clean room is a physical location.”** The trust boundary includes identities, code, outputs, and operations.
34. **“A clean-room product guarantees privacy.”** Configuration and use determine its controls.
35. **“Data does not move.”** Remote computation, staging, logs, caches, and outputs still cross boundaries.
36. **“Hashed join keys reveal nothing.”** Membership, overlap, frequency, and enumerable identifiers leak.
37. **“Approved SQL text is permanently safe.”** Data, views, functions, engines, and policies change.
38. **“Restricted syntax prevents malicious analysis.”** Semantically equivalent differencing and side channels remain.
39. **“Attestation proves code is good.”** It proves scoped measurements and state, not purpose or correctness.
40. **“Confidential computing protects outputs.”** Authorized code can emit raw input.
41. **“The operator is the only attacker.”** Analysts, contributors, recipients, providers, and colluding parties matter.
42. **“Audit logs prove compliant use.”** Logs may omit paths, leak data, or describe only requests.
43. **“Query denials measure privacy.”** Attackers may succeed through allowed queries or exports.
44. **“Output review can inspect each result alone.”** Prior and parallel releases compose.
45. **“Contracts replace technical controls.”** Agreements cannot prevent every execution or leak.
46. **“Technical controls replace contracts.”** Purpose, remedies, duties, and parties require authority.
47. **“Tokenized data need not support deletion.”** Subject relationships and mappings remain governed.
48. **“Room closure means revoking users.”** Jobs, staged data, outputs, keys, backups, and recipients remain.
49. **“Recovery restores only data.”** Stale policy, budgets, keys, and identities can recreate exposure.
50. **“No known reidentification proves anonymity.”** Testing scope, attacker capability, time, and unknown attacks limit the claim.

## Worked Examples

### Example 1

A support screen reveals only the final four account digits. The API and export remain separately authorized, browser and observability capture are disabled, and administrators receive audited break-glass access. The claim is display masking for support, not source de-identification.

### Example 2

A test-data pipeline substitutes names, generalizes dates and locations, removes free text, preserves approved foreign-key relations, and scans the result. Each refresh is versioned and deleted with the source lifecycle; residual similarity is tested rather than called anonymous.

### Example 3

One company issues collaboration-specific HMAC tokens for normalized emails. The key remains in a controlled service, different rooms use different derivation contexts, match failures are measured, and neither partner receives the key. The tokens remain pseudonymous and membership-sensitive.

### Example 4

A payment service uses reversible random tokens. The vault separates application and detokenization roles, binds reversal to approved cases, rate-limits enumeration, records minimal receipts, rotates credentials, and tests recovery. Protected mappings remain in payment and deletion scope.

### Example 5

A legacy field uses reviewed format-preserving encryption because its schema cannot change. The architecture records retained length and validation leakage, prevents ciphertext from entering real transaction rails, versions algorithm and keys, and plans eventual schema replacement.

### Example 6

A health release generalizes age and geography and suppresses rare diagnoses. Review tests direct and quasi-identifiers, important minority groups, external registers, prior releases, and intended recipients. Its conclusion applies only to that release environment and time.

### Example 7

Two advertisers join domain-specific tokens in a clean room. Only approved aggregation templates run, contribution and group bounds apply, outputs pass a cumulative ledger, and neither raw keys nor row-level overlaps leave. Membership inference remains an explicit tested risk.

### Example 8

Three banks run fraud code in an attested confidential workload. Each releases keys only to an approved measurement and configuration. Network egress is closed, outputs are signed and gated, firmware revocation is monitored, and code review remains separate from attestation.

### Example 9

A statistical collaboration uses differential privacy with the person as privacy unit, bounded transaction contribution, named adjacency, versioned mechanism, and an accountant spanning scheduled and interactive queries. Analysts see utility and remaining-budget limits without claiming protection from every operational leak.

### Example 10

A collaborator leaves. The service revokes identities, disables templates, stops jobs, reconciles releases, deletes staging and domain mappings under authority, ages backups, propagates subject deletion, preserves minimal receipts, and tests that recovery cannot reopen the collaboration.

## Cross-Program Connections

**Security Engineering.** Key isolation, cryptographic review, trusted execution, side channels, least privilege, monitoring, and incident response determine technical assurance.

**Applied Cryptography.** HMAC, encryption, format-preserving modes, random generation, key derivation, rotation, and attestation must use current reviewed constructions.

**Privacy Engineering.** Purpose, identifiability, data minimization, differential privacy, affected people, rights, and remedy define acceptable residual risk.

**Database Engineering.** Views, policies, query planners, joins, user-defined functions, caches, exports, and transactions define enforcement surfaces.

**Data Engineering.** Static derivatives, schema evolution, lineage, orchestration, quality, refresh, streaming, and deletion determine lifecycle correctness.

**Machine Learning Engineering.** Synthetic data, embedding leakage, model memorization, clean-room training, evaluation, and output controls require model-specific testing.

**API and Service Engineering.** Tokenization, detokenization, policy, query, budget, attestation, receipt, revocation, and status interfaces need stable semantics and idempotency.

**Platform Engineering.** Identity, workload isolation, secrets, policy distribution, observability, provider integration, and recovery supply the execution substrate.

**Software Testing and Verification.** Property tests, adversarial queries, reidentification exercises, fault injection, attestation validation, and restore drills test bounded claims.

**Systems Engineering.** Trust boundaries, participant incentives, emergent composition, provider dependencies, migration, and closure must be reasoned about end to end.

## References

1. NIST, [SP 800-188: De-Identifying Government Datasets](https://www.nist.gov/publications/de-identifying-government-datasets-techniques-and-governance), techniques, governance, disclosure review, and the Five Safes.
2. NIST, [NISTIR 8053: De-Identification of Personal Information](https://csrc.nist.gov/pubs/ir/8053/final), data models, risk, techniques, and operational challenges.
3. Information Commissioner's Office, [Anonymisation guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/about-this-guidance/), contextual identifiability and governance.
4. Information Commissioner's Office, [Pseudonymisation guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/), hashing, encryption, tokenisation, separation, and risk.
5. NIST, [SP 800-38G](https://csrc.nist.gov/pubs/sp/800/38/g/upd1/final), FF1 and FF3 format-preserving encryption.
6. PCI Security Standards Council, [Tokenization Product Security Guidelines](https://www.pcisecuritystandards.org/documents/Tokenization_Product_Security_Guidelines.pdf), token classes, mappings, vaults, keys, and lifecycle.
7. AWS, [Analysis rules in AWS Clean Rooms](https://docs.aws.amazon.com/clean-rooms/latest/userguide/analysis-rules.html), aggregation, list, custom, and output controls.
8. Google Cloud, [Share sensitive data with data clean rooms](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms), BigQuery sharing, analysis rules, templates, and limitations.
9. Google Cloud, [Confidential Space overview](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview), participants, isolated workloads, key release, and attestation.
10. Microsoft, [Multi-party data analytics](https://learn.microsoft.com/en-us/azure/confidential-computing/multi-party-data), confidential-computing clean-room building blocks.
11. Snowflake, [Differential privacy in Data Clean Rooms](https://docs.snowflake.com/en/user-guide/cleanrooms/differential-privacy), privacy budgets, query costs, and customer configuration.
12. W3C, [PROV-O](https://www.w3.org/TR/prov-o/), provenance for entities, activities, agents, derivations, and delegation.

## Exercises

### Exercise 1

Design a protected customer-linkage service for three business units and two external collaborations. Specify normalization, token domains, generation, mappings or keys, reversal, collision behavior, translation, access, receipts, rotation, deletion, recovery, and bounded claims.

### Exercise 2

Design static test-data masking for a relational application containing names, addresses, payments, free text, images, tenant IDs, audit records, and temporal history. Preserve necessary test utility without silently copying production identity relationships.

### Exercise 3

Design a clean room for two health organizations measuring treatment outcomes. Specify participants, custody, joins, workloads, query rules, contribution and group bounds, outputs, repeated-release controls, evidence, incident response, subject rights, and closure.

### Exercise 4

Compare suppression, generalization, tokenization, encryption, format-preserving encryption, synthetic data, k-anonymity, differential privacy, and confidential computing for a rare-disease research use. State retained utility, adversaries, failure modes, and evidence.

### Exercise 5

Migrate universal email hashes, ad hoc masked copies, and unrestricted partner SQL into governed token domains and collaboration services. Include discovery, compatibility, dual operation, reissue, release reconciliation, rollback, and retirement.

## Answers to the Exercises

### Answer 1

Create separate internal-purpose and collaboration-purpose domains rather than one enterprise identifier. Define Unicode and address normalization with version and test vectors; reject ambiguous inputs; use sufficiently large random tokens with a protected mapping vault or a reviewed keyed derivation appropriate to the matching need. Bind every token to subject edge, tenant, purpose, domain, source version, creation time, and lifecycle. Detect collisions and normalization merges explicitly.

Expose tokenize and tightly scoped match operations broadly enough for approved workflows but detokenize only to named cases, fields, callers, and purposes with rate limits and dual control for bulk activity. Domain translation is a separate authorized event. Isolate service, keys, mappings, administrators, logs, exports, backups, and recovery. Rotation declares whether token stability changes and prevents old-new bridges from enabling unrelated linkage. Subject correction and erasure find every domain and derivative. Claims state resistance to defined outsiders and domains; they do not claim anonymity.

### Answer 2

Model required tests first: key and uniqueness constraints, tenant isolation, approximate geography, payment state, temporal sequences, search, image pipeline, and error handling. Build an isolated derivative that substitutes names and addresses, uses non-operational payment tokens, shifts or generalizes dates consistently, removes or generates free text, transforms or replaces images and metadata, and creates domain-scoped tenant identifiers. Maintain approved relationships only inside the test domain.

Version schema, detector, transform, key or mapping, seed policy, source snapshot, and test evidence. Scan direct and quasi-identifiers, rare combinations, files, history, logs, fixtures, and failure artifacts; sample with human review. Prevent messages or payments from reaching real systems. Refresh through the governed pipeline, propagate source deletion, restrict test access, and delete copies and backups on schedule. Utility and residual identification are measured separately.

### Answer 3

Name each contributor, analyst, workload author, operator, result recipient, reviewer, provider, and auditor and state collusion assumptions. Keep sources in controlled custody or encrypted staging; issue collaboration-specific patient tokens through an authorized linkage service. Approve exact datasets, versions, outcomes, covariates, time windows, join cardinality, missingness, and permitted recipients. Review and pin templates, libraries, parameters, network, storage, and error behavior.

Bound each person's contribution, suppress unsuitable groups, and use a formally specified differential-privacy mechanism where it fits the questions. Account across interactive, scheduled, and parallel releases. An independent output gate reviews rare diseases, outliers, small cells, differencing, prior results, purpose, and recipient. Receipts contain protected provenance and output digests, not source payloads. Incidents freeze release and address reidentification, wrong linkage, malicious code, or budget bypass. Rights propagate to staged data and mappings. Closure revokes identities and keys, stops jobs, reconciles recipients, deletes assets, and makes recovery preserve closure.

### Answer 4

Suppression best removes risky cells but loses rare-disease evidence. Generalization may retain coarse cohorts but can still isolate a patient. Tokenization supports authorized longitudinal linkage but remains pseudonymous. Encryption protects custody and transport; format preservation helps legacy schemas while retaining structure. Synthetic data can support development or exploration but needs memorization and subgroup fidelity tests. k-anonymity supplies one release property under selected quasi-identifiers but not protection from attribute disclosure or composition.

Differential privacy can bound one defined individual's effect on aggregate outputs when adjacency, contribution, mechanism, and composition are correct; utility for rare groups can be poor. Confidential computing can reduce exposure to an operator or collaborator during execution but not unsafe code or output. A defensible design layers purpose limitation, source minimization, domain tokens, controlled execution, reviewed aggregates, cumulative accounting, contractual duties, and output tests. Evidence and claims name the audience, attacker resources, time, releases, protected unit, residuals, and limitations.

### Answer 5

Inventory every hash construction, normalization, salt or pepper, table, copy, join, report, export, user, room, query, result, key, script, scheduled job, log, cache, backup, contract, purpose, and recipient. Treat existing hashes as linkable pseudonyms and preserve their mapping to dependent assets under restricted access. Define domain-specific tokens, canonical identities, approved matching, query templates, output rules, participant roles, release ledgers, incidents, deletion, and closure.

Issue new tokens alongside legacy hashes and compare authorized match coverage, false merges and splits, latency, key and vault failures, query results, and downstream compatibility. Do not expose both identifiers outside a protected translation boundary. Shadow and then enforce query and output decisions; reconcile historical releases into the composition model. Rollback disables new operations without reviving unsafe external sharing. Revoke legacy query access, remove old hashes and ad hoc copies from recipients, retire scripts and keys after dependency and recovery horizons, and verify no restore recreates universal linkage or unrestricted SQL.
