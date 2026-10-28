---
module_id: DE-028
program: Data Engineering
level: 1
module_number: 28
title: Deduplication and Record Identity
status: complete
last_verified: 2026-09-02
---

# Deduplication and Record Identity

## One-Page Review

### Governing question

How can a data system distinguish repeated delivery of one occurrence, repeated representations of one source record, and uncertain evidence that different records describe the same entity—without deleting legitimate history, merging distinct subjects, or making identifiers unstable?

### Essential definitions

- **Record grain** states what one row/event represents and at which time or version; duplicate meaning is undefined until grain is fixed.
- An **occurrence identity** names one source event, file row, transaction change, or logical fact across delivery retries.
- A **source record identity** names a record in one authoritative source and epoch, usually as a namespaced key rather than a bare value.
- A **canonical entity identity** is a durable analytical identity assigned through an explicit linkage process; it is not merely the surviving source key.
- **delivery deduplication** suppresses repeated transport of the same occurrence identity and payload.
- **exact duplicate detection** compares records under a declared canonicalization and equality projection.
- **entity resolution** estimates whether distinct records refer to the same underlying entity using deterministic or probabilistic evidence.
- **blocking** generates plausible candidate pairs without comparing every record to every other record.
- A **linkage decision** is `match`, `non-match`, or `unresolved`, with evidence, model/rule version, threshold, and decision provenance.
- **survivorship** selects or derives canonical attribute values after linkage while preserving source-level records and field provenance.
- A **merge** combines entity clusters; a **split** repairs an incorrect cluster. Both require stable identity and downstream correction semantics.
- A **duplicate horizon** is the domain over which identity evidence remains available, such as a source epoch, retained event history, or bounded streaming window.

### Central model, mechanism, or theorem

For record $r$, keep distinct functions:

$$
O(r)=\text{occurrence identity},\quad S(r)=\text{source record identity},\quad E(r)=\text{canonical entity identity},\quad H(r)=hash(C(r)).
$$

$C$ is a versioned canonicalization for a declared equality projection. Equal $O$ with equal payload is delivery replay; equal $O$ with unequal payload is an identity conflict. Equal $H$ is evidence of equality only under $C$ and the selected fields. Different $S$ values may still map to one $E$ through linkage; one $S$ may change over time without becoming a new entity.

A safe pipeline stores immutable source occurrences, resolves delivery identity first, normalizes comparisons without erasing raw values, generates candidates, scores or applies rules, permits abstention, persists source-to-canonical mappings and decision provenance, derives survivors separately, and publishes merge/split corrections explicitly.

### Critical invariants

- Dataset grain, source namespace/epoch, occurrence and source identities, version/order, and duplicate class are explicit.
- One occurrence identity binds to one payload digest; conflicting reuse fails closed.
- Raw occurrences are retained or recoverable; deduplication creates decisions/views rather than destructive evidence loss.
- Canonicalization is field-, locale-, type-, and version-specific; normalized equality is not promoted automatically to entity equality.
- Candidate generation has measured recall; pairs excluded by blocking are not silently treated as proven non-matches.
- Match decisions include features, missingness, rule/model version, thresholds, constraints, and provenance; uncertain cases can remain unresolved.
- Canonical entity IDs remain stable across reruns and incremental arrival; cluster membership is not used as a volatile identifier derivation.
- Entity linkage and attribute survivorship are separate decisions, with field-level source/time/quality provenance.
- Merge and split are reversible governed events that propagate to downstream aggregates, permissions, privacy, and deletion state.
- Quality is evaluated on representative labeled data with false-merge and missed-match costs, subgroup behavior, and drift.
- Deduplication state and tombstones outlive every permitted replay/window, or late records enter an explicit reprocessing path.

### Common failures

Running `SELECT DISTINCT *` and calling it entity resolution; dropping duplicates before defining grain; using an email, phone, name, timestamp, or row number as universal identity; generating a new canonical ID on every rebuild; choosing the first row without a total order; using `ROW_NUMBER` with unresolved peers; treating hash equality as semantic truth; lowercasing or punctuation removal without locale/domain policy; comparing every pair at quadratic scale; assuming blocking misses are non-matches; merging on transitive closure of weak pairwise links; forcing every score to yes/no; overwriting source evidence with a golden row; ignoring null-versus-unknown semantics; letting late data escape a streaming window; forgetting deletion/tombstone identity; or evaluating only the percentage of rows removed.

### Compact example

Six deliveries contain four legitimate occurrence IDs: one exact replay and one attempt to reuse an occurrence ID with changed content. The replay becomes a no-op and the conflict is rejected. Three source records from CRM and support carry verified account `acct-101`; the identity registry maps them to durable `ent-001`. Survivorship chooses a newer CRM name by declared source/version precedence while retaining all member records and provenance. Reversing delivery order produces the same mapping and survivor. A similar email alone would create a candidate, not an automatic merge.

### Connections

[DE-011](011-grain-and-the-meaning-of-a-row.md) defines record meaning, [DE-016](016-event-and-activity-models.md) separates events from entities, [DE-023](023-file-arrival-and-manifest-processing.md) supplies immutable file evidence, [DE-026](026-database-change-data-capture.md) supplies occurrence/version semantics, and [DE-027](027-idempotent-loads.md) uses stable identities for replay-safe effects. The following modules develop quarantine and replayable raw ingestion.

## Governing Question

What evidence justifies saying that two delivered records are the same occurrence, two stored rows are duplicate representations, or two source records refer to the same real-world entity—and what must happen when that evidence later changes?

“Remove duplicates” sounds like one operation but hides different claims. A broker redelivery of event `e17` is a transport duplicate even if its payload has many common fields with other legitimate events. Two identical rows in one snapshot may be separate people who share attributes, a repeated source record, or legitimate repeated facts at an omitted grain. Two customer records with different names and addresses may describe one person, but that conclusion is uncertain and policy-sensitive.

These claims demand different identities and remedies. Delivery replay is usually suppressed by stable occurrence ID plus payload binding. Exact duplicate representations can be grouped under a canonicalization contract. Entity resolution links distinct source identities using rules or statistical evidence and must support uncertainty, provenance, merge, and split. Survivorship then decides which field values to expose; it does not prove the linkage.

Record identity is also temporal. An email can be reassigned, a household can divide, a company can merge, a device can change owner, and a source system can recycle an integer after migration. Identity domains require namespace, epoch, validity interval, and entity type. A globally formatted UUID can reduce accidental identifier collision without proving what the identifier denotes.

The governing question is therefore evidentiary: which equality is being claimed, at what grain and time, from which sources, under what rules/model, with which error costs, and through which reversible decision history?

## Why This Matters

Duplicate delivery can inflate facts, balances, counts, and downstream notifications. Source duplication can make cohorts and operational queues inconsistent. Missed entity links fragment histories and undercount lifetime behavior. False entity merges are often worse: they can combine medical, financial, identity, or access data belonging to different subjects.

A false merge propagates. Aggregates blend, feature vectors leak information, communications reach the wrong person, deletion requests affect another subject, and authorization decisions cross boundaries. Keeping only one “best” row destroys the evidence needed to discover and repair the error.

At scale, naive comparison is infeasible. $n$ records have $n(n-1)/2$ unordered pairs. One million records imply nearly $5\times10^{11}$ possible pairs. Blocking reduces work, but every blocking rule creates a recall boundary: a true pair sharing no generated block cannot be scored.

Incremental systems add stability constraints. Rebuilding clusters and assigning `MIN(source_id)` as canonical ID can rename entities when an earlier key arrives or when a cluster splits. Downstream foreign keys, aggregates, consent, and audit trails then drift even if linkage quality improves. Durable identity requires a registry and explicit mapping history.

Normalization can itself cause harm. Removing accents, punctuation, apartment numbers, honorifics, or leading zeros can increase comparison recall while collapsing meaningful distinctions. Unicode-equivalent text may use different code-point sequences; Unicode normalization helps compare them but does not define name, address, or person equivalence.

Finally, quality cannot be summarized as “10% duplicates removed.” The relevant measures include false merges, missed links, coverage, unresolved cases, cluster errors, survivor correctness, subgroup disparities, decision stability, and downstream correction time. The metric must reflect the cost of being wrong.

## Prerequisites and Retrieval

Retrieve the dataset owner and purpose; entity types; row/event grain; source systems, namespaces, epochs, and key-reuse policies; occurrence/event IDs; source primary/business keys; file/object/partition/offset lineage; source versions and valid/event/ingestion times; operation and deletion semantics; immutable raw retention; schemas; field types; null/empty/unknown/redacted meaning; Unicode, locale, collation, casing, punctuation, transliteration, address/phone/email standards; personally identifying fields; authentication strength of identifiers; canonicalization versions; payload digests; duplicate classes; deterministic business rules; candidate blocking rules; labeled match/non-match data; match features; missingness; correlated evidence; model/rule version; thresholds; false-positive/false-negative costs; constraints such as one-per-source or household membership; canonical identity registry; cluster version; merge/split history; survivor rules; field provenance; human review; appeals/corrections; downstream consumers; foreign-key propagation; metrics; privacy/legal basis; consent; deletion/retention; access control; encryption; bias/fairness evaluation; streaming windows/state TTL; backfill/rebuild procedures; and disaster recovery.

Distinguish occurrence identity from payload hash; source record key from real-world entity; entity from account, household, device, address, or organization; duplicate delivery from duplicate source creation; exact equality from normalized equality; representation equivalence from referential identity; null from empty, unknown, redacted, or not applicable; similarity from probability; probability from calibrated decision cost; pairwise match from valid cluster; candidate omission from non-match; canonical ID from selected survivor key; linkage from survivorship; current member set from mapping history; merge from alias; split from deletion; source trust from source recency; deterministic output from correct output; unlabeled volume reduction from measured quality; and irreversible erase from reversible deduplicated view.

Create an identity contract:

| Concern | Required evidence |
|---|---|
| Grain | Entity/fact/event represented, time/version, legitimate multiplicity |
| Namespaces | Source, tenant, environment, epoch, entity type, key reuse |
| Occurrence | Stable ID derivation, payload binding, retry and retention horizon |
| Equality | Fields, canonicalization version, null/locale/type semantics |
| Candidates | Blocking keys, expected reduction, measured pair recall, fallbacks |
| Decision | Rules/features, missingness, model version, thresholds, constraints, abstention |
| Canonical ID | Registry allocation, stability, aliases, merge/split versioning |
| Survivor | Field-level precedence, valid time, quality, provenance, conflict behavior |
| Evaluation | Labeled population, pair/cluster metrics, costs, subgroups, drift |
| Operations | Incremental state, correction propagation, privacy, retention, recovery |

Before processing, write examples of legitimate identical-looking records. Two cash purchases can share all captured values. Twins can share surname, address, and birth date. A sensor can emit the same reading twice at distinct event positions. A customer can intentionally own multiple accounts. These counterexamples prevent convenient field equality from silently redefining grain.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish delivery replay, exact duplicate representation, and entity resolution;
2. specify record grain and layered occurrence, source-record, canonical-entity, and effect identities;
3. design versioned canonicalization and payload fingerprinting without confusing representation with truth;
4. enforce occurrence identity conflicts and exact-dedup determinism under concurrency;
5. generate scalable linkage candidates and measure blocking recall;
6. construct deterministic and probabilistic match evidence with explicit missingness and thresholds;
7. explain why pairwise links do not automatically form a valid equivalence relation or cluster;
8. maintain stable canonical IDs, reversible merge/split history, and field-level survivor provenance;
9. evaluate false merges, missed links, calibration, cluster quality, subgroup behavior, and drift; and
10. operate deduplication across streaming windows, backfills, privacy workflows, and downstream correction.

## Core Exposition

### Name the duplicate class before removing anything

At least four cases recur:

1. **delivery replay:** one logical occurrence is transported more than once;
2. **representation duplicate:** two stored representations are equal under declared fields and canonicalization;
3. **source duplicate:** a producer created multiple source records for what its own contract treats as one record/entity;
4. **cross-source entity link:** distinct source identities are judged to refer to one underlying entity.

The first is usually an exact identity problem. The second is an equality-projection problem. The third may require source-domain repair. The fourth is entity resolution and can be uncertain. Calling all four “duplicate rows” invites destructive logic.

The action differs too. Suppress a verified redelivery from materialized effect but retain receipt. Group exact representations while retaining lineage. Correct a source duplicate through a governed merge or upstream fix. Link cross-source records in a mapping layer that supports disagreement and later split.

### Fix grain and legitimate multiplicity

Define what one record represents: one event occurrence, order line, account state version, customer-source profile, person, household, device session, or daily snapshot. Include valid time, transaction time, source version, and operation where relevant.

Two records cannot be called duplicates merely because their projected business fields match. If event identity or time belongs to grain, identical payloads at different positions may be legitimate repetitions. Conversely, two differently formatted records can be duplicate representations of one source occurrence.

Write a candidate uniqueness constraint in domain language. For example, “Within source epoch and tenant, one CDC occurrence identity denotes one committed row mutation and binds to one canonical payload.” That is narrower and safer than “email must be unique.”

### Layer identities rather than overload one key

Use separate columns and registries for:

- transport/delivery attempt ID;
- logical occurrence/event ID;
- immutable raw-record ID or file-position identity;
- namespaced source record/entity ID;
- canonical entity ID;
- entity-cluster version;
- target effect/receipt ID; and
- payload/canonical-comparison digest.

A source identity should include source system, tenant/domain, entity type, and epoch when keys can be recreated. `(crm-prod, customer, epoch-4, 123)` is not interchangeable with bare `123` from support or a restored CRM database.

RFC 9562 defines UUID formats and discusses uniqueness, collision resistance, locality, sorting, and opacity considerations. A UUID can be a sound allocated identifier. It does not show that two records describe the same person, that a producer never reused an ID, or that two independently generated IDs describe different entities.

### Bind occurrence identity to content

Maintain a unique registry keyed by occurrence namespace and ID. On arrival:

- absent key plus valid payload creates the occurrence record;
- existing key plus equal canonical source payload is delivery replay;
- existing key plus unequal payload is identity conflict;
- malformed or untrusted key is rejected or quarantined.

Do not silently select the first or latest conflicting payload. Reuse can signal source bugs, epoch confusion, hash/canonicalization change, corruption, or adversarial substitution. Preserve both deliveries and their provenance outside trusted effects for investigation.

Commit the occurrence receipt with its accepted raw record/effect as [DE-027](027-idempotent-loads.md) describes. A process-local set or a state store with insufficient retention protects only a subset of retries.

### Canonicalize representations explicitly

Canonicalization $C_v(r)$ maps selected fields to a reproducible representation under contract version $v$. Possible operations include type parsing, Unicode normalization, case folding, whitespace policy, punctuation treatment, phone country-code parsing, email-domain handling, timestamp/time-zone normalization, and deterministic field order.

RFC 8785 specifies a JSON canonicalization scheme intended to make hashing/signing reproducible for supported JSON data. It is one representation contract, not a business-record equality standard. Similarly, Unicode Standard Annex #15 defines normalization forms and canonical equivalence for code-point sequences; it does not say two spellings, transliterations, names, or addresses denote one entity.

Preserve raw values and record normalized derivatives plus canonicalization version. Changing $C_v$ can change exact groups, fingerprints, blocking keys, and model features. Recompute as a new governed decision generation rather than rewrite history invisibly.

### Define exact duplicate equality

For declared projection $F$ and canonicalization $C_v$, define

$$
r_i\equiv_{F,v}r_j \iff C_v(F(r_i))=C_v(F(r_j)).
$$

This relation means equal selected representations, not necessarily equal source occurrence or entity. Record excluded fields. If `ingested_at` and file path are excluded, two physical rows can be equal under the business projection while remaining separately traceable.

A digest

$$
H_{F,v}(r)=hash(encode(C_v(F(r))))
$$

accelerates comparison when canonical encoding and hash version are stable. Compare canonical content on collision-sensitive paths or use a cryptographic digest with an explicit threat/error model. Hash equality never repairs an incorrect projection.

### Select deterministic representatives

If an exact-equivalence group needs one representative, define a total precedence over all possible ties: source authority, valid version, deletion state, completeness/quality, event time, ingestion time, immutable occurrence identity. Every direction and null rule must be explicit.

`ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC)` is not deterministic when `updated_at` ties. BigQuery documents that row-number order inside a peer group is nondeterministic. Add a stable final tiebreaker and test that it is unique; a random or physical row address is not durable.

Representative selection is a view decision. Retain group membership, rule version, winning reason, and losing records. Do not let “keep first” depend on input file or distributed partition order.

### Enforce exact uniqueness physically where appropriate

Use unique constraints or atomic conditional writes for identities whose equality is authoritative. Application-side `SELECT` then `INSERT` races. Database null and collation semantics must match the identity contract.

PostgreSQL documents that unique constraints normally treat null values as distinct and supports `NULLS NOT DISTINCT` to change that behavior; it also notes SQL implementations can differ. A composite identity containing null therefore needs explicit semantics. Often a missing identifier means “cannot establish identity,” not “all missing identifiers are equal.”

Constraints protect the declared stored key, not real-world identity. A unique normalized email can reject family/shared mailboxes, aliases, or reassigned addresses. Use physical uniqueness only when the domain owner establishes it.

### Separate deterministic linkage from exact equality

Deterministic linkage uses domain-approved rules such as verified government identifier plus country, authenticated account federation key, or source crosswalk issued by an authoritative system. A rule can link non-equal records, so it is not exact deduplication.

Rules need priority, prerequisites, validity intervals, conflict behavior, and versioning. “Exact email and date of birth” can be high-signal in one population and unsafe in another. Missing and contradictory strong identifiers should block or escalate rather than be outweighed casually by many weak similarities.

Track which rule fired. If several rules disagree, do not use rule evaluation order as hidden truth. Produce an unresolved/conflict decision with evidence.

### Generate candidates with measured blocking

All-pairs comparison grows quadratically:

$$
N_{pairs}=\frac{n(n-1)}{2}.
$$

Blocking maps records into one or more candidate neighborhoods: phonetic surname plus birth year, normalized email, phone suffix plus postal area, address tokens, locality-sensitive signatures, or learned retrieval embeddings. Multiple blocking passes can recover pairs missed by any one key.

Blocking is a recall mechanism, not a match decision. Measure **pairs completeness** (blocking recall): the share of labeled true-match pairs that appear in the candidate set. Also measure reduction ratio and candidate skew. A rare huge block can dominate cost; an over-specific key can erase recall.

Records excluded from every shared block are “not compared,” not proven non-matches. Maintain a fallback/manual path for high-risk records and audit blocking behavior across scripts, languages, name distributions, and missingness patterns.

### Build comparison features deliberately

Features can include exact agreement, edit distance, token similarity, phonetic agreement, numeric/date difference, geographic distance, domain validity, source trust, frequency/rarity, and temporal compatibility. Each feature must define normalization, missingness, invalid values, and whether disagreement is contradictory or merely uninformative.

Do not turn missing values into agreements. Two null phone numbers provide no shared-phone evidence. A common surname agreement is weaker than a rare surname agreement. Correlated fields—city, postal code, address—do not necessarily contribute independent evidence.

Preserve feature values and comparison version for audit. Sensitive raw fields can be access-controlled, tokenized, or computed in a protected environment, but privacy-preserving linkage transformations have their own collision, frequency, attack, and utility trade-offs.

### Interpret probabilistic linkage carefully

The Fellegi–Sunter family compares feature agreement patterns under match and non-match hypotheses. In a simplified independent-feature presentation, feature $i$ contributes a log likelihood ratio

$$
w_i=\log\frac{m_i(\gamma_i)}{u_i(\gamma_i)},
$$

where $m_i$ is the probability of observed comparison outcome $\gamma_i$ among true matches and $u_i$ among non-matches. With prior match probability $\pi$, a total log-odds score can be written

$$
W=\log\frac{\pi}{1-\pi}+\sum_i w_i.
$$

Splink's theory documentation explains match prior, $m$ probabilities, $u$ probabilities, weights, and match probability. Real deployments must examine conditional-dependence violations, training/estimation data, calibration, population shift, and blocking-conditioned priors rather than treat a score as universal truth.

A model score ranks evidence under a model. It is not an identity oracle. Preserve the model version, features, candidate-generation context, and calibration population.

### Use two thresholds and an unresolved region

Let $T_M$ be a high threshold for automatic match and $T_U$ a lower threshold below which automatic non-match is acceptable:

$$
decision(W)=
\begin{cases}
match, & W\ge T_M,\\
unresolved, & T_U<W<T_M,\\
nonmatch, & W\le T_U.
\end{cases}
$$

Choose thresholds from labeled validation data and asymmetric costs. In safety-, rights-, finance-, health-, or access-sensitive contexts, false merges can have far greater cost than missed links, justifying conservative automatic matches and broader abstention.

Human review needs calibrated evidence, privacy safeguards, consistent policy, reviewer quality checks, and appeal. It is not a magical ground truth source. Persist reviewer, reason, decision time, policy/model context, and later corrections.

### Validate constraints beyond pair scores

Domain constraints can invalidate locally strong pairs: one canonical person cannot have two mutually exclusive verified identifiers valid at the same time; one source may allow at most one active record per entity; a device can belong to different people at different intervals; organizations can have parent/subsidiary relationships rather than equality.

Apply constraints during cluster construction and review, not only after building a transitive closure. Contradictory strong evidence should prevent or split a cluster even when weak similarities connect it.

Temporal compatibility matters. Two addresses five years apart can belong to one person; two simultaneous verified identities may contradict. Model validity intervals instead of flattening every historical attribute into one bag.

### Do not assume pairwise matches form valid clusters

Entity equality should behave as an equivalence relation—reflexive, symmetric, and transitive—within a fixed entity definition. Pairwise classifier outputs need not. The model can score $A$–$B$ and $B$–$C$ above threshold while $A$–$C$ strongly contradicts.

Connected components over thresholded edges enforce transitivity mechanically but can create chain merges. One ambiguous bridge can combine two large clusters. Alternatives include constrained clustering, correlation clustering, center/representative policies, source cardinality constraints, conservative edge pruning, and human adjudication.

Store edges and cluster-decision provenance. A cluster is a governed inference version, not raw truth. Evaluate cluster-level errors and sensitivity to bridge removal.

### Allocate stable canonical entity IDs

Do not derive canonical ID from current minimum source key, cluster member hash, or row order. Adding/removing members or fixing a split would rename the entity. Allocate an opaque durable ID in a registry and map namespaced source records to it with validity and decision versions.

On merge, choose one surviving canonical ID by stable policy, retain the other as an alias, and emit a merge event with lineage. On split, allocate or reactivate IDs for separated clusters, version mappings, and emit correction events. Never reuse an retired canonical ID for a different entity.

Downstream tables may need effective-dated mapping rather than destructive foreign-key rewrite, especially when reproducing historical decisions. State whether analytics use “identity as known now” or “identity as decided then.”

### Separate linkage from survivorship

Linkage answers which records belong together. Survivorship answers which attribute values a canonical view exposes. A match decision does not imply that one whole row is best.

Define field-level rules using source authority, verification status, validity interval, recency in a comparable source domain, quality, and explicit conflict behavior. Legal name might prefer a verified registry; contact preference might prefer a newer consented channel; birth date disagreement might remain unresolved rather than choose latest.

For every survivor value record source record, occurrence/version, original value, normalization, rule version, selection reason, and validity time. Preserve alternatives as permitted. A “golden record” without field provenance is an opaque overwrite.

### Model time, deletion, and reappearance

Source profiles evolve. Distinguish new version of an existing source record from a new source record; distinguish corrected attribute from entity split; distinguish inactive/closed from deleted; distinguish source deletion from privacy erasure.

Keep mapping validity intervals and cluster versions. A deleted source record may remain part of historical linkage evidence under retention law, or may require erasure from features and survivors. Tombstone identity can prevent replay from recreating a deleted mapping while minimizing retained personal data.

Reassigned identifiers need time. A phone number or email used by person A until June and person B from August must not connect both across all history. Candidate and cluster rules should reason over compatible intervals and authenticated ownership strength.

### Engineer streaming deduplication horizons

A streaming state store cannot remember every occurrence forever without bound. Define state key, event-time/processing-time basis, watermark, allowed lateness, state TTL, source redelivery maximum, backfill behavior, and late-record route.

Apache Beam's `RemoveDuplicates` documentation describes deduplication by value or key within a time domain and duration. Such bounded state supports a bounded claim. A duplicate arriving after expiry can pass unless a durable downstream uniqueness/receipt registry still recognizes it.

Window-scoped row equality can also be wrong for entities whose versions cross windows. Use stable source versions and persistent identity mappings for entity state; use windows only when the duplicate definition itself is window-bounded.

### Preserve provenance as part of correctness

W3C PROV-O provides classes and properties for representing and exchanging provenance about entities, activities, and agents. A production identity system need not adopt that ontology, but it should answer comparable questions: which source records and transformations generated this mapping and survivor, under which agent/rule/model, and what superseded it?

Store raw lineage, canonicalization version, candidate blocks, pair features/scores, decisions, reviewer actions, cluster versions, survivor selections, merges/splits, and publication identity. Apply access control and retention; linkage evidence is often more sensitive than any one source because it connects contexts.

Provenance makes correction possible. Without it, operators cannot tell whether a canonical attribute came from source authority, recency, arbitrary row order, or a stale model.

### Evaluate the decision system

For pair decisions on labeled data:

$$
precision=\frac{TP}{TP+FP},\qquad recall=\frac{TP}{TP+FN}.
$$

False positive pairs often correspond to harmful false merges; false negatives to missed links. Report denominators, confidence intervals where appropriate, threshold, candidate-generation coverage, and labeling method. Evaluate calibration if probabilities are used.

Pair metrics can conceal cluster damage: one false bridge can merge two large clusters while adding few false edges. Add cluster/entity metrics such as exact-cluster accuracy, B-cubed precision/recall, pairwise closure metrics, cluster-size distribution, constraint violations, merge/split stability, and downstream effect tests as appropriate.

Slice by source pair, geography, script/language, data completeness, time, entity type, and protected or operationally relevant groups under lawful governance. Monitor feature/missingness/candidate/score/decision drift. A global average can hide concentrated harm.

### Reconcile identity coverage and exclusivity

Reconcile each immutable input occurrence to exactly one state: accepted unique occurrence, exact replay, identity conflict, invalid/quarantined, or intentionally excluded. Ensure every materialized effect traces to one accepted occurrence.

For source-to-canonical mappings, check each eligible source record has the permitted number of active canonical memberships; each canonical ID exists in the registry; aliases do not cycle; merge/split lineage is valid; constraints hold; survivor values trace to active eligible members; and deletion/consent rules propagate.

Compare reruns with the same input/rules: occurrence classifications, candidates, scores, pair decisions, clusters, mappings, and survivors should be byte- or set-stable under the declared determinism contract. Changed model/rules create a new decision generation with an explainable delta.

### Test adversarial and boundary cases

Test exact replay and same-ID/different-payload conflict; null, empty, redacted, malformed, and extreme-length fields; Unicode composed/decomposed text; casing, punctuation, leading zero, locale, collation, and invalid encoding; hash/canonicalizer version migration; UUID/key namespace collision; and concurrent insert.

Test legitimate identical facts; shared/family email and phone; twins; aliases; transliteration; reordered names; address move; reassigned identifiers; source key reuse after restore; late delete; entity type mismatch; one source record linked to competing clusters; and strong identifier contradiction.

Test no shared block, oversized block, skew, missing features, correlated comparisons, score ties, exact thresholds, probability drift, label leakage, class imbalance, bridge-chain clusters, clique contradiction, merge then split, split then remerge, and downstream correction replay.

Test streaming duplicate just before/after watermark and TTL, checkpoint loss, backfill overlap, state restore, and receipt expiry. Test privacy erasure, subject correction, access boundaries, poisoning attempts, and audit immutability.

## Definitions and Notation

Let:

- $r$ be an immutable observed record occurrence;
- $G$ be the declared record grain;
- $O(r)$ be namespaced logical occurrence identity;
- $S(r)$ be namespaced source record/entity identity;
- $E(r)$ be durable canonical entity identity;
- $C_v$ be canonicalization under version $v$;
- $F$ be the field/equality projection;
- $H_{F,v}(r)$ be digest of canonical projected representation;
- $B(r)$ be the set of blocking keys/candidate neighborhoods;
- $\gamma_i(r,s)$ be comparison outcome for feature $i$;
- $m_i$ and $u_i$ be comparison-outcome probabilities under match/non-match hypotheses;
- $W(r,s)$ be linkage score or log odds;
- $T_M,T_U$ be automatic match and non-match thresholds;
- $M_t$ be source-to-canonical mapping generation at decision time $t$;
- $P(f,E)$ be provenance for surviving field $f$ of entity $E$; and
- $D_h$ be the stated duplicate horizon.

Exact representation equality under a declared contract is

$$
r\equiv_{F,v}s\iff C_v(F(r))=C_v(F(s)).
$$

Occurrence identity binding requires

$$
O(r)=O(s)\implies
\begin{cases}
replay, & payload(r)=payload(s),\\
conflict, & payload(r)\ne payload(s).
\end{cases}
$$

It must never infer that unequal occurrence IDs imply different entities. Candidate comparison is limited to generated pairs

$$
Q=\{(r,s):B(r)\cap B(s)\ne\varnothing\},
$$

so a true match outside $Q$ is unreachable to the scorer. Measure that boundary.

For simplified Fellegi–Sunter-style evidence,

$$
W(r,s)=\log\frac{\pi}{1-\pi}+\sum_i\log\frac{m_i(\gamma_i(r,s))}{u_i(\gamma_i(r,s))}.
$$

The formula requires estimated meanings and assumptions; it does not transform an uncalibrated score into truth.

An entity cluster relation should satisfy, for the declared entity/time definition,

$$
r\sim r,\qquad r\sim s\Rightarrow s\sim r,\qquad (r\sim s\land s\sim t)\Rightarrow r\sim t.
$$

Thresholded pair predictions do not automatically satisfy the last condition without a clustering policy, and enforcing it by connected components may introduce unsupported links.

## Mechanisms, Invariants, or Proof Structure

**Conditional exact-replay theorem.** Suppose each logical occurrence identity $O$ is unique in a durable registry, binds atomically to one canonical source payload digest and accepted raw/effect record, and persists for every permitted replay. Then any number of equal-payload deliveries for the same $O$ produce one accepted occurrence/effect; any unequal-payload reuse is detected as conflict.

**Proof sketch.** The first successful transaction creates the unique binding and effect. Concurrent first claims serialize or conflict at the registry. Later equal deliveries read the binding and do not reapply; unequal deliveries fail digest comparison. Atomicity excludes effect without binding and binding without effect. The result does not establish entity equality, source completeness, or safety after binding expiry.

**Grain invariant.** Duplicate classification is relative to declared $G$, time/version, scope, and equality fields. Records at distinct legitimate grains cannot be removed solely for shared payload.

**Namespace invariant.** Occurrence, source, and canonical IDs include or resolve through source/tenant/entity-type/epoch domains. Bare key equality across domains conveys no identity.

**Canonicalization invariant.** $C_v$ is deterministic and versioned; raw values remain available. Equality under $C_v\circ F$ is not automatically referential entity equality.

**Deterministic representative invariant.** Exact groups use a total stable precedence with a unique final tiebreaker; delivery/partition order never chooses the winner.

**Blocking boundary invariant.** Only pairs in $Q$ can be classified by the scorer. Candidate recall is measured separately from scorer accuracy.

**Decision provenance invariant.** Every match/non-match/unresolved outcome carries candidate reason, features, score/rule, version, threshold, constraints, agent/reviewer, and decision time.

**Cluster consistency invariant.** Active membership satisfies declared source-cardinality, strong-identifier, entity-type, and temporal constraints. Weak transitive bridges cannot silently override contradiction.

**Stable canonical-ID invariant.** $E$ is allocated by a registry, never recomputed from current members. Merge/split changes mappings through versioned events and preserves aliases/history.

**Survivorship invariant.** Each exposed field value carries field-level source/version/rule provenance; linkage membership alone never chooses all attributes.

**Retention invariant.** Occurrence bindings, tombstones, and mapping history outlive $D_h$ and every recovery path, or a governed reprocessing/rebootstrap boundary handles late input.

**Evaluation invariant.** Report candidate coverage, pair/cluster errors, abstention, decision stability, and relevant subgroup/cost slices; volume removed is not quality evidence.

<!-- bijux-verify: {"id":"layered-record-identity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deliveries=6\nunique_occurrences=4\ndelivery_replays=1\nidentity_conflicts=1\ncanonical_entities=2\nentity_101_members=3\nsurvivor_101=Ada Lovelace\norder_stable=True\n","stderr":""}} -->
```python
from hashlib import sha256

records = (
    ("crm", "o-1", "c-7", "acct-101", 1, "Ada N", "ADA@example.com"),
    ("crm", "o-2", "c-7", "acct-101", 2, "Ada Lovelace", "ada@example.com"),
    ("support", "o-3", "s-9", "acct-101", 1, "Ada L", " ada@example.com "),
    ("crm", "o-4", "c-8", "acct-202", 1, "Grace Hopper", "grace@example.com"),
)
deliveries = (records[0], records[1], records[2], records[3], records[0])
conflicting_delivery = (
    "crm", "o-2", "c-7", "acct-101", 2, "Wrong Replacement", "ada@example.com"
)
canonical_ids = {"acct-101": "ent-001", "acct-202": "ent-002"}
source_priority = {"crm": 2, "support": 1}

def payload_digest(record):
    return sha256(repr(record[2:]).encode()).hexdigest()

def accept(delivered):
    accepted = {}
    replays = 0
    for record in delivered:
        occurrence = (record[0], record[1])
        digest = payload_digest(record)
        if occurrence in accepted:
            assert accepted[occurrence][0] == digest
            replays += 1
        else:
            accepted[occurrence] = (digest, record)
    return accepted, replays

def resolve(delivered):
    accepted, _ = accept(delivered)
    members = {}
    for _, record in accepted.values():
        entity = canonical_ids[record[3]]
        members.setdefault(entity, []).append(record)
    survivors = {}
    for entity, group in members.items():
        winner = max(group, key=lambda r: (source_priority[r[0]], r[4], r[1]))
        survivors[entity] = winner[5]
    return members, survivors

accepted, replays = accept(deliveries)
identity_conflict = payload_digest(conflicting_delivery) != accepted[("crm", "o-2")][0]
members, survivors = resolve(deliveries)
reverse_members, reverse_survivors = resolve(tuple(reversed(deliveries)))
print(f"deliveries={len(deliveries) + 1}")
print(f"unique_occurrences={len(accepted)}")
print(f"delivery_replays={replays}")
print(f"identity_conflicts={int(identity_conflict)}")
print(f"canonical_entities={len(members)}")
print(f"entity_101_members={len(members['ent-001'])}")
print(f"survivor_101={survivors['ent-001']}")
print(f"order_stable={survivors == reverse_survivors and set(members) == set(reverse_members)}")
```

The executable fixture models a trusted external account crosswalk, occurrence-level payload binding, a duplicate delivery, a conflicting identity reuse, a stable canonical-ID registry, and deterministic source/version survivorship. Its email trimming/casing is illustrative only and is not used for linkage. It does not implement probabilistic matching, concurrent durable constraints, Unicode/domain normalization, cluster merge/split, or privacy controls.

## Alternatives and Trade-Offs

**Drop duplicates versus retain-and-map.** Dropping reduces storage and downstream volume. Retaining immutable occurrences plus decisions preserves audit, correction, and model evaluation. Trusted views can expose one effect without erasing evidence.

**Exact identity registry versus payload-only distinct.** Stable occurrence IDs distinguish legitimate identical events and detect changed-payload reuse. Payload-only distinct works for explicitly set-like datasets but can collapse repeated facts and cannot identify source conflict.

**Natural key versus allocated canonical ID.** Natural keys are interpretable but mutable, reused, sensitive, or only locally unique. Opaque registry IDs stay stable while mappings evolve, at the cost of registry operations and joins.

**Deterministic rules versus probabilistic linkage.** Strong domain rules are explainable and precise within coverage. Probabilistic methods combine noisy evidence and improve recall but require labels/estimation, calibration, thresholds, monitoring, and review. Hybrid systems often reserve automatic linkage for high-confidence evidence.

**Exact blocking versus approximate retrieval.** Exact blocks are transparent and efficient but brittle to errors. Approximate/learned retrieval can improve recall across variants while increasing compute, drift, explainability, and privacy risk. Measure candidate recall either way.

**Connected components versus constrained clustering.** Components are simple and deterministic once edges exist, but weak bridges can cause large false merges. Constrained methods protect invariants and may leave unresolved fragments, with greater implementation complexity.

**Whole-row survivor versus field-level survivor.** Whole-row choice is easy to reproduce but discards authoritative values from other sources. Field-level survivorship improves quality and provenance but must handle internal consistency between related fields.

**Current identity view versus as-decided history.** A current remapping incorporates corrections for present analytics. Historical decision versions reproduce past reports/audits. Supporting both costs metadata and clear query semantics.

**Global state versus bounded streaming window.** Global durable identity catches arbitrarily late replay within retention but consumes storage. Windowed state bounds cost/latency but makes the guarantee explicitly time-bounded and needs a late/backfill path.

**Automatic decision versus abstention.** Forced classification maximizes coverage but converts uncertainty into false merges or misses. Abstention protects quality and rights while creating review queues and latency. Budget the queue and prioritize by expected harm.

**Plaintext comparison versus privacy-preserving linkage.** Protected cleartext can offer better explainability/accuracy under strict access controls. Encoded/tokenized linkage reduces some exposure but can leak frequency, collide, impede correction, and complicate evaluation. Use threat modeling, not a “hashed means anonymous” assumption.

## Failure Modes and Misconceptions

**“Duplicate means identical row.”** Equality depends on grain and projection. Identical payloads can be legitimate different events; nonidentical records can refer to one entity.

**“`DISTINCT` creates clean data.”** It removes exact projected repetitions without preserving why they occurred, which row won, or whether entity identity is shared.

**“A UUID proves real-world uniqueness.”** It supplies an identifier format/generation scheme. Producer bugs, namespace misuse, duplicate entity creation, and multiple IDs per entity remain possible.

**“Hash equality proves the same entity.”** It proves equal hashed canonical representation under assumptions. Projection and canonicalization can be semantically wrong, and identity can differ despite equality.

**“Hashing personal data anonymizes it.”** Low-entropy identifiers can be guessed or frequency-attacked; linkage itself increases sensitivity. Apply privacy/security controls and threat modeling.

**“Normalize everything aggressively.”** Accent, punctuation, apartment, suffix, leading-zero, and locale changes can destroy distinctions. Version field-specific normalization and retain raw values.

**“Null equals null for deduplication.”** Two unknown values provide no identity evidence, and database unique-null behavior varies. Define missingness separately.

**“Email is a person ID.”** Addresses can be shared, mistyped, aliased, compromised, and reassigned. Verification and time improve evidence but do not make universal identity.

**“Take the latest row.”** Latest by which trustworthy version domain? Ingestion time favors delays/retries; timestamps tie; older corrections may be authoritative. Define precedence and total ties.

**“`ROW_NUMBER` always picks the same winner.”** Without a unique total ordering, peer order may be nondeterministic. Add stable tiebreakers and validate them.

**“Unique constraints resolve entities.”** They enforce stored key equality. They cannot infer referential identity and can encode harmful assumptions if placed on weak attributes.

**“Blocking non-candidates are non-matches.”** They were not scored. Blocking recall is a separate gate.

**“More matching fields always means more confidence.”** Common or correlated fields can add little independent evidence; strong contradictions can dominate many weak agreements.

**“A match score is a probability.”** Only a defined calibrated model under a relevant population supports probability interpretation. Arbitrary similarities and thresholds do not.

**“One threshold is enough.”** A forced binary decision hides uncertainty. Match/non-match thresholds with unresolved review can reflect asymmetric costs.

**“Pairwise links can be transitively closed safely.”** Classifier edges are not guaranteed transitive. One weak bridge can create a catastrophic cluster merge.

**“Canonical ID should be the smallest member key.”** Membership changes rename the entity. Allocate IDs independently and preserve merge/split aliases.

**“The golden row can replace source rows.”** It destroys provenance and makes splits/corrections unverifiable. Survivors are derived views.

**“Deduplication never changes after publication.”** New evidence, corrected data, model changes, identifier reassignment, and appeals require versioned merge/split propagation.

**“Ten percent removed means ten percent better.”** Removal rate measures activity, not false merges, missed links, coverage, or survivor truth.

**“A streaming dedup operator is global.”** State is bounded by key, watermark, TTL, checkpoint, and retained history. State the horizon and late-data behavior.

## Worked Examples

### Example 1

A broker delivers occurrence `(orders, epoch-3, partition-4, offset-91)` twice with the same canonical source envelope digest. The durable registry accepts it once and reports replay once. A third delivery reuses the same coordinate with a different digest after a source restore. The pipeline blocks it as epoch/identity conflict rather than choose latest. Entity resolution is not involved.

### Example 2

Two point-of-sale cash purchases have identical store, product, amount, and second-level timestamp but different receipt/event IDs. The grain is one sale occurrence, so payload equality does not make them duplicates. A `DISTINCT` projection without receipt ID would undercount legitimate revenue. Exact delivery dedup uses occurrence identity.

### Example 3

JSON objects differ only in member order and number/string representation. The team first defines a supported canonical JSON/value contract, then hashes it with version. Equal digests support exact representation grouping for those fields. They do not show that the two customer-source IDs refer to one person; that requires linkage evidence.

### Example 4

A snapshot has three rows for source account 42 with the same source version and payload but different ingestion metadata. The equality projection excludes pipeline metadata, groups all three, and uses immutable occurrence ID as final survivor tiebreaker. The view exposes one source-state record while a membership table preserves all three paths and explains a producer retry defect.

### Example 5

Customer candidates share exact verified email and similar names, but one record is active in 2017 and the email was demonstrably reassigned in 2024. A timeless exact-email rule would merge two people. The linkage feature includes ownership validity intervals and turns the pair into a non-match or unresolved conflict despite textual equality.

### Example 6

Ten million records would yield about $5\times10^{13}$ unordered pairs. Blocking on three independent passes—verified phone, normalized postal/name tokens, and email/domain token—reduces candidates dramatically. Evaluation finds that transliterated names with missing phones are absent from all passes, so the team adds a protected approximate-name/locality pass and measures candidate recall again before scoring.

### Example 7

Pairs A–B and B–C score above automatic match, while A and C carry simultaneous contradictory verified tax identifiers. Connected components would merge all three. A constrained cluster builder rejects the bridge, records an unresolved decision around B, and preserves two clusters until adjudication. It reports the constraint violation rather than hide it behind transitivity.

### Example 8

Canonical `ent-77` and `ent-92` are later proven to be one organization. A merge event keeps `ent-77`, maps `ent-92` as an alias, versions all source mappings, and triggers affected downstream rebuilds. Months later, one subsidiary is shown to be distinct; a split event assigns a durable ID to that member set and restates only lineage-dependent outputs. Raw sources and prior decisions remain reproducible.

### Example 9

A canonical profile links a government registry, CRM, and support record. Legal name comes from the verified registry; contact preference comes from the newest consented CRM version; support language comes from the support record; birth-date disagreement remains flagged. Every field exposes source/version/rule provenance. No whole row is declared universally best.

### Example 10

A stream retains dedup state for seven days, but mobile clients can replay queued events after 30 days. The seven-day operator cannot claim global deduplication. The design either extends a durable event registry beyond 30 days, changes client/event identity and retention contracts, or routes expired-window events into a reconciliation path that checks the authoritative ledger before effect.

## Cross-Program Connections

**Database Engineering.** Unique constraints, collation, null semantics, isolation, temporal tables, indexes, and transaction recovery determine exact identity enforcement and mapping updates.

**Algorithms and Data Structures.** Hashing, sorting, union-find, graphs, nearest-neighbor retrieval, edit distance, sketches, and external-memory processing support candidates and clusters while exposing complexity trade-offs.

**Statistics and Probability.** Likelihood ratios, priors, calibration, sampling, labeling error, class imbalance, threshold costs, confidence intervals, and drift are essential to probabilistic linkage evaluation.

**Machine Learning Engineering.** Feature pipelines, train/validation leakage, model/version registries, monitoring, human feedback, and reproducible inference govern learned entity-resolution systems.

**Security Engineering.** Identity poisoning, cross-tenant collisions, sensitive linkage graphs, hashed-identifier attacks, access control, audit, deletion, and consent make linkage a security/privacy boundary.

**API and Service Engineering.** Idempotency keys, resource identifiers, aliases, merge/split endpoints, optimistic concurrency, and correction events connect operational identity to analytical mappings.

**Data Architecture and Governance.** Entity ownership, master/reference data, stewardship, lawful purpose, lineage, quality policy, retention, and dispute resolution define acceptable canonical identity.

**Systems Engineering.** False merge, missed link, unstable ID, incomplete correction, and privacy propagation are emergent hazards requiring end-to-end controls across producers and consumers.

## References

1. IETF, [RFC 9562: Universally Unique IDentifiers](https://www.rfc-editor.org/rfc/rfc9562.html). Defines current UUID formats and discusses collision resistance, uniqueness, monotonicity, opacity, sorting, and database considerations.
2. IETF, [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html). Specifies an invariant JSON representation for repeatable cryptographic hashing/signing within its supported data model.
3. Unicode Consortium, [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/). Defines Unicode normalization forms, canonical/compatibility equivalence, stability, and implementation considerations.
4. PostgreSQL Global Development Group, [PostgreSQL: Unique Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS). Documents unique-constraint indexes, default null distinctness, `NULLS NOT DISTINCT`, and implementation differences.
5. Google Cloud, [BigQuery GoogleSQL Numbering Functions: ROW_NUMBER](https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#row_number). Documents row numbering and nondeterministic order inside peer groups or without ordering.
6. Apache Beam, [RemoveDuplicates](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.deduplicate.html). Documents value/key deduplication within configurable processing- or event-time durations.
7. Splink, [The Fellegi–Sunter Model](https://moj-analytical-services.github.io/splink/topic_guides/theory/fellegi_sunter.html). Explains prior match probability, match/non-match comparison probabilities, weights, and match probability in probabilistic linkage.
8. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/). Defines an ontology for representing and interchanging provenance information about entities, activities, and agents.

## Exercises

### Exercise 1

A dataset contains two identical sensor readings at different authoritative event offsets, one repeated delivery of the first offset, and a changed payload reusing the second offset. Classify the four observations, design occurrence identities and payload binding, and explain why payload `DISTINCT` is wrong for the stated event grain.

### Exercise 2

A team chooses one exact-duplicate representative with `ROW_NUMBER() OVER (PARTITION BY normalized_email ORDER BY updated_at DESC)`. Shared emails are valid, two records tie on `updated_at`, null emails exist, and input partition order changes. Identify each identity/determinism error and propose a safer exact-grouping and representative contract without turning email equality into person identity.

### Exercise 3

There are 2,000 records. Compute all unordered comparison pairs. A blocking scheme emits 18,000 unique candidate pairs and includes 930 of 1,000 labeled true-match pairs. Compute reduction ratio relative to all pairs and pairs completeness. Explain what the missing 70 pairs mean for end-to-end recall, even if the scorer has 99% recall on candidates.

### Exercise 4

Pair scores make A–B and B–C automatic matches, while A–C has simultaneous contradictory verified identifiers. Design a cluster decision, canonical-ID allocation, unresolved evidence, and later merge/split propagation. Explain why connected components alone and `MIN(source_id)` canonical identity are unsafe.

### Exercise 5

A linkage system reports pairwise $TP=920$, $FP=20$, and $FN=80$. Compute precision and recall. One false positive edge joins clusters of 800 and 600 records. Explain why the pair metrics understate possible harm and propose a fuller evaluation and release gate, including subgroup and correction evidence.

## Answers to the Exercises

### Answer 1

Let occurrence identity be `(source, source_epoch, sensor, partition, offset)` and bind it atomically to canonical source-envelope digest plus raw record/effect. The two distinct authoritative offsets are two legitimate event occurrences even though readings are identical. The second delivery of the first offset with equal digest is delivery replay and produces no second effect. Reusing the second offset with unequal digest is an identity conflict and blocks/quarantines rather than overwrite. Payload `DISTINCT` would collapse the two legitimate readings because payload does not include the full event grain; it would also conceal the changed-payload identity violation instead of diagnosing it.

### Answer 2

The query assumes normalized email defines a grouping worth collapsing, even though shared mailboxes mean it cannot define people. Null handling is unclear and database/window semantics can group all nulls despite “unknown” not being identity. `updated_at` ties leave peers unordered, so `ROW_NUMBER` can choose different representatives when execution order changes. Define the goal as an exact representation group only over an approved projection and versioned email canonicalization, preserving every raw/source identity. Exclude missing emails from equality groups or assign each unknown record its own occurrence-based group unless the domain says otherwise. Choose a total representative order such as verified source authority, comparable source version, timestamp, completeness, then unique immutable occurrence ID. Label the output “representative of equal email representation,” not canonical person, and send cross-record entity linkage through separate evidence/rules.

### Answer 3

All unordered pairs are $2000\times1999/2=1,999,000$. The reduction ratio is $1-18,000/1,999,000\approx0.9909955$, or about 99.10%. Pairs completeness is $930/1000=93\%$. Seventy labeled true pairs are outside the candidate set and cannot be recovered by the scorer. If scorer recall on candidates is 99%, optimistic end-to-end pair recall is $0.93\times0.99=0.9207$, or 92.07%, before other pipeline losses. Blocking recall and scorer recall must be reported separately; “not candidate” is not non-match truth.

### Answer 4

Do not close the A–B–C component automatically. The simultaneous contradictory verified identifiers violate a hard cluster constraint. Preserve both high pair scores and the A–C contradiction, mark at least the bridge/member assignment unresolved, and keep conservative separate clusters pending adjudication; which edge remains depends on stronger authenticated evidence, time, and policy. Allocate canonical IDs from a durable registry independent of members. If later evidence justifies a merge, keep one stable ID, alias the other, version mappings, emit a merge event, and restate dependent outputs. If later split is required, allocate/reactivate stable IDs, version the split, and propagate corrections. `MIN(source_id)` changes when an earlier key arrives or membership changes, so it destabilizes every downstream reference.

### Answer 5

Pairwise precision is $920/(920+20)=920/940\approx97.87\%$. Recall is $920/(920+80)=92\%$. Those averages do not express cluster blast radius: one false bridge between clusters of 800 and 600 can cause a 1,400-record false merged component and many implied incorrect co-memberships, permissions, aggregates, or survivor fields. Add candidate recall, calibration/threshold curves, abstention, exact-cluster and B-cubed or suitable cluster metrics, cluster-size/bridge sensitivity, hard-constraint violations, survivor-field accuracy/provenance, and downstream impact tests. Slice results by source pair, missingness, geography, language/script, time, and governed groups. A release gate should cap high-cost false merges and giant unexplained cluster changes, require representative labeled validation and drift checks, verify merge/split replay and downstream correction, and retain rollback/audit evidence rather than rely on the global pair percentage.
