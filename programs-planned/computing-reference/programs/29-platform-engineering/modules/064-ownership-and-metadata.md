---
module_id: PLAT-064
program: Platform Engineering
level: 2
module_number: 64
title: Ownership and Metadata
status: complete
last_verified: 2026-09-02
---

# Ownership and Metadata

## One-Page Review

### Governing question

How should a platform represent ownership and metadata so people can find accountable teams, route work, evaluate quality, and automate safely while organizational change, conflicting authorities, staleness, and authorization boundaries remain explicit?

### Essential definitions

- **Accountable owner** is the one active organizational identity answerable for an entity's continued fitness and able to coordinate decisions; it need not perform every task.
- **Responsibility role** is a typed relationship such as operator, responder, data steward, cost owner, security partner, or change approver.
- **Contact** is a discoverable communication endpoint; **escalation** is an ordered, tested routing policy. Neither alone proves accountability.
- **Metadata assertion** is a claim that a source makes about one field or relation, accompanied by provenance and validity evidence.
- **Source of authority** is the system or governed process entitled to decide a particular fact; a catalog, repository, or collector may merely transport it.
- **Steward** is accountable for a metadata field's definition, allowed values, quality objective, evolution, and retirement.
- **Freshness** is age since authoritative observation, not age since catalog processing.
- **Ownership coverage** is the fraction of independently known in-scope entities having a resolvable, active, suitably typed accountable owner.
- **Transfer** is an auditable, coordinated change of accountability and dependent duties from one identity to another.
- **Authorization** is a policy decision about an actor, action, resource, and context; an owner label is only one possible input and never an implicit grant.

### Central model, mechanism, or theorem

Represent a metadata assertion as

$$
a=(e,k,v,s,r,t_o,t_e,q,c),
$$

where $e$ is entity, $k$ field or relation key, $v$ value, $s$ authoritative source, $r$ source revision, $t_o$ observation time, $t_e$ optional expiry, $q$ quality evidence, and $c$ classification. A resolver $R_k$ applies the field contract—authority, validation, precedence, merge, freshness, and conflict rules—to assertions for $(e,k)$. It must not use arrival order as governance. Ownership is a typed relation $Own(e,g,h,[t_s,t_e))$, where active group $g$ holds role $h$ during a defined interval. Consequential action evaluates a separate authorization policy $Permit(p,a,e,x)$ against current authoritative facts. Catalog ownership can aid discovery or policy evaluation, but $Own(e,g,h)$ does not imply $Permit(p,a,e,x)$.

### Critical invariants

- Every in-scope entity has exactly one active accountable owner or an explicit, time-bounded exception; auxiliary roles may be many.
- Owners are stable organizational identities, normally groups, resolved through the current identity authority; personal contacts do not replace team accountability.
- Accountable owner, operator, responder, steward, cost owner, security partner, and approver remain distinct even when one group fills several roles.
- Each governed field has defined semantics, type, authority, writer, validation, sensitivity, freshness, conflict, default, evolution, and retirement rules.
- Source observation time and revision survive ingestion; reprocessing stale input cannot make it fresh.
- Missing, unresolved, inactive, stale, conflicted, unauthorized-to-view, and intentionally unowned are distinct states.
- Owner metadata does not itself grant repository, platform, cloud, data, or production access.
- Ownership transfer coordinates catalog, directory, repository review, support, on-call, cost, security, credentials, and pending work without an unowned interval.
- Sensitive contacts, membership, classifications, and business context are filtered before search, export, notification, and analytics disclosure.
- Quality metrics use independent denominators and measure correctness and routability, not merely non-null fields.

### Common failures

One overloaded `owner` string; person-as-owner; mailing list as accountability; CODEOWNERS as service ownership; stale group aliases; repository writers self-granting production access; catalog owner as runtime role binding; last-writer-wins metadata; timestamps refreshed by reprocessing; free-form tags as policy; inferred ownership without provenance; mandatory fields with meaningless defaults; permanent exceptions; silent fallback to a platform team; untested escalation; transfers that update only the portal; search leaking hidden teams; metadata copied into every system; quality measured from catalog rows alone; and organizational deletion before owned assets are disposed.

### Compact example

`Component:payments/ledger-api` declares `accountableOwner=group:payments-ledger` in reviewed source. The directory confirms that group is active and maps its stable ID to a renamed display label. The incident system owns `responder`, finance owns `costCenter`, security owns `dataClassification`, and telemetry supplies observed runtime identity. The repository's CODEOWNERS file routes review for `/ledger/**` but does not overwrite the accountable owner. A resolver shows the accountable owner as valid, the runbook contact as stale, and a conflicting cost center as unresolved. A transfer record names old and new owners, approvals, effective time, obligation checklist, and rollback. Runtime access remains governed by an authorization service that rereads directory membership and policy; editing catalog YAML grants nothing.

### Connections

This module specializes the catalog model from [PLAT-063](063-software-catalogs.md) and the portal/API authority boundaries from [PLAT-061](061-platform-api-layers.md) and [PLAT-062](062-developer-portal-architecture.md). It prepares workflow and policy composition in PLAT-065 and PLAT-066. Identity federation, audit, and capability retirement are developed in PLAT-074, PLAT-079, and PLAT-097.

## Governing Question

How can a platform make organizational accountability and descriptive metadata trustworthy enough for discovery, routing, governance, and carefully bounded automation without pretending that a mutable catalog field is identity, authority, or permission?

The hard problem is not adding an `owner` key. It is defining what the key means, who may assert it, how it resolves to a living organization, what happens when it is stale or disputed, and which consumers may rely on it. The same questions apply to lifecycle, tier, classification, cost center, support channel, repository, runbook, and other metadata.

Ownership is relational and temporal. A team owns something for a purpose during an interval, within an organizational and policy context. Organizations rename, split, merge, outsource, and dissolve. Systems move between teams. Incident response, maintenance, approval, and funding can belong to different groups. A timeless string cannot represent this adequately.

Metadata is also a control surface. Fields that begin as display hints often become search filters, scorecards, deployment gates, cost allocation keys, access-policy inputs, or deletion criteria. Platform engineers must govern the transition from descriptive convenience to consequential dependency.

## Why This Matters

When an incident occurs, finding a plausible name is not enough. Responders need an active team, a tested escalation route, current operational context, and confidence that the record applies to the failing production identity. Incorrect routing increases recovery time even if the catalog field is nonempty.

Ownership gaps compound other risks. Vulnerabilities wait without accountable remediation. Deprecated APIs persist because no one can accept migration obligations. Cloud resources accumulate without cost accountability. Data sets remain unclassified. Shared platform teams become the default dumping ground and silently inherit more work than they can execute.

Overloaded ownership creates political and technical confusion. A developer team may maintain code, an operations group may respond after hours, a data office may steward meaning, security may approve exceptional exposure, and finance may own budget. Flattening these into one label either hides real duties or invites every consumer to interpret the label differently.

Metadata errors propagate. A wrong tier can alter paging or resilience expectations. A stale lifecycle can expose unsupported templates. A classification copied from an untrusted repository can weaken controls. The greater the consequence, the stronger the need for authoritative rereads, provenance, validation, and safe failure behavior.

Good ownership metadata reduces cognitive load. It makes responsibility visible at the point of need, supports platform product feedback, and exposes gaps as managed work. Its value comes from correct routing and decisions, not from maximizing the number of populated fields.

## Prerequisites and Retrieval

Retrieve organizational identity and group directories, stable identifiers and mutable display names, role-based and attribute-based authorization, responsibility assignment, source-of-truth boundaries, schemas and controlled vocabularies, provenance, eventual consistency, freshness and expiry, incident escalation, service catalogs, repository review policy, labels and annotations, temporal intervals, entity resolution, conflict handling, data quality, privacy and information disclosure, lifecycle management, audit, migrations, and decommissioning.

You should distinguish accountable owner from contributor; group identity from display name; contact from escalation; on-call responder from service owner; data steward from infrastructure operator; repository reviewer from runtime operator; assertion from resolved value; source authority from transport; source time from processing time; required field from correct field; unknown from intentionally unowned; ownership relation from authorization grant; organizational membership from catalog ownership; and transfer of accountability from renaming a label.

## Learning Objectives

After completing this module, you should be able to:

1. define a typed ownership model with accountable and supporting roles;
2. bind owners to durable organizational identities and current directory evidence;
3. design field-level metadata contracts, vocabularies, provenance, and quality objectives;
4. resolve conflicting, missing, stale, expired, and unauthorized metadata without semantic collapse;
5. separate discovery ownership, code review, support routing, policy inputs, and authorization;
6. design atomic ownership transfer across catalog, operational, financial, security, and access obligations;
7. protect sensitive metadata in ingestion, search, APIs, notifications, exports, and analytics;
8. measure coverage, validity, freshness, routing success, conflict, exception debt, and repair time; and
9. test organizational rename, split, merge, acquisition, outsourcing, abandonment, restore, and retirement.

## Core Exposition

### Begin with decisions and user journeys

List the questions users need answered: Who is accountable for this service? Who responds now? Who approves an exception? Which team maintains this library? Who pays for this resource? Who defines a data element? Where should a vulnerability be routed? Each question implies a role, authority, freshness need, and disclosure policy.

Do not begin with a universal metadata form. Begin with decisions and failure costs. A documentation link can tolerate delayed reconciliation; an emergency escalation route needs tighter freshness and testing; a production access decision may require a direct authoritative query and fail closed.

Record intended consumers. Human display, search, reporting, notification, scorecards, workflow routing, admission policy, and runtime authorization impose progressively stronger contracts. A field that becomes consequential needs an explicit promotion review rather than accidental reuse.

Define non-goals. The ownership registry is not necessarily the human-resources master, identity provider, paging system, repository permission store, financial ledger, or authorization service. It integrates references to those systems while preserving their authority.

### Define ownership as a typed relation

An owner is not an arbitrary string property of an object. Model ownership as a relation among an entity, organizational identity, role, scope, and validity interval. The role answers “responsible for what?” The interval makes transfer and historical questions meaningful.

Require one accountable owner for ordinary active entities. Singularity gives users a final coordination point. It does not mean that one team performs every duty or can act without consultation. Multiple co-equal accountable owners commonly create a coordination gap: each can assume the other will decide.

Allow many supporting roles with distinct semantics. Useful examples include maintainer, operator, incident responder, data steward, security partner, privacy contact, cost owner, product owner, and change approver. Avoid a globally fixed list when domains differ, but govern a registry of role definitions and permitted entity kinds.

Separate responsibility from capability. A group may be accountable but temporarily lack staffing or access. Surface that as a breached readiness invariant rather than silently selecting a capable platform administrator as owner.

### Prefer durable groups over people

Teams normally outlive individuals and make continuity explicit. Bind an ownership relation to a stable directory group ID or canonical entity reference, not a display label, email address, chat channel, or employee name. Display names and contacts remain mutable attributes.

Person ownership can be appropriate for a personal sandbox or explicitly time-bounded experiment. Require expiry and a succession rule. Production and regulated assets should have group accountability even if a named technical lead is also shown.

Resolve the group through the organizational authority. Confirm active state, canonical ID, aliases, parent organization where relevant, and usable contact/escalation. A syntactically valid but deleted group is unresolved ownership.

Avoid copying complete membership lists into broadly visible catalog records. Membership may be sensitive, high-churn, and authorization-relevant. Resolve only what the journey needs, under current access policy.

### Distinguish contacts and escalation

A contact endpoint says where a message can be sent. It does not say anyone will respond, within what time, or how to escalate. Record contact type, audience, authority, observation time, expected use, and sensitivity.

An escalation policy is ordered and operational: primary response route, delay or trigger, fallback route, terminal accountable group, and test evidence. The paging system should own current on-call schedules; the catalog should link or display a permission-filtered summary.

Do not infer 24-hour support from the presence of an on-call URL. Define support hours, severity applicability, service objective, and fallback. Test routing through exercises or synthetic notifications where safe.

Separate feature requests, routine support, security reports, privacy inquiries, and incidents. Sending every concern to one chat room produces hidden queues and weak auditability.

### Build a field-level authority matrix

Metadata authority is granular. Repository owners may define source links and intended API associations. The directory owns group existence and membership. Incident tooling owns escalation. Finance owns cost allocation. Security or data governance owns classification. Runtime registries own observed deployments.

For each field define: semantic meaning, data type, cardinality, allowed values, entity kinds, authoritative source, allowed writers, validation, precedence or merge rule, observation/freshness/expiry, sensitivity, consumers, failure behavior, schema version, and retirement path.

“The repository owns the entity” is too broad. A repository can transport a team-selected owner reference while a directory determines whether that reference resolves. It cannot authoritatively assert current membership merely because YAML is reviewed.

Publish the matrix as a machine-readable registry when fields drive multiple consumers. Schema validation catches shape errors; authority validation catches forbidden writers; semantic validation checks cross-field meaning; referential validation checks targets; temporal validation checks age and expiry.

### Treat metadata as assertions with provenance

Keep the submitted assertion distinct from the resolved view. Store source identity, source object, revision or ETag, observation time, processing time, transformation version, validation outcome, expiry, and classification. This lets users answer “why does the portal say this?”

Observation time is when the authority knew or emitted the fact. Processing time is when the platform handled it. Replaying a week-old snapshot today updates processing time but not freshness.

If sources disagree, apply the field contract. A higher-authority assertion may win; a set-valued field may merge; incompatible equal-authority assertions should become a visible conflict. Network arrival order is not a defensible precedence rule.

Record derivation. “Responder group” may be obtained from an incident-policy reference, while “accountable owner” came from repository intent resolved through the directory. Derived assertions should name inputs and transformation revision.

### Govern vocabulary and extension points

Metadata keys are public interfaces once consumers depend on them. Give each governed key an owner, description, examples, schema, allowed values, and compatibility policy. Use stable domain-qualified prefixes for extensions to avoid collisions.

Use controlled vocabulary when consumers interpret semantics. Lifecycle, criticality, data classification, support model, and ownership role are not good free-form tags. A new value must define behavior and migration impact.

Keep free-form tags for low-consequence discovery and grouping. Do not let an informal tag silently become a security or deployment policy input. Promote it to a governed field first.

Kubernetes illustrates a useful boundary: labels support selection and grouping, while annotations carry non-identifying data. Even so, platform-specific keys need an owner and documented consumer. OpenTelemetry service attributes illustrate interoperable identity metadata; translate deliberately rather than inventing unrelated service names in each tool.

### Model metadata state explicitly

Do not collapse all failures into empty. Useful states include valid, stale-but-displayable, expired, missing, unresolved reference, invalid shape, unauthorized source, conflict, unauthorized-to-view, deprecated field, and intentionally not applicable.

Defaults require care. A display default such as “unknown” must not be stored as evidence of an actual owner or classification. Fail closed for consequential security facts; route remediation for required accountability; degrade gracefully for optional presentation fields.

Last-known-good values may remain visible if labeled with source age and current failure. For emergency routes, stale fallback might be better than no route; for revocation or classification, stale fallback can be unsafe. Decide per field.

Expose resolution evidence without overwhelming ordinary users. A compact badge can show valid/stale/conflict, with an authorized diagnostic view for assertions and provenance.

### Separate ownership from authorization

Catalog ownership answers who is accountable or who should be contacted. Authorization answers whether a principal may perform an action on a resource in context. Backstage explicitly describes catalog ownership as primarily for display and warns against using it directly to assign runtime authorization.

CODEOWNERS is narrower still. It routes review requests for matching repository paths and can participate in merge protection. It does not prove service accountability, operational support, budget ownership, or production access. Its source branch, matching precedence, team visibility, and repository permissions have their own semantics.

An authorization policy may use governed ownership as one input, but it must bind a current principal to current group membership, action, resource, environment, conditions, approvals, and deny behavior. It should define which ownership role qualifies and how stale or conflicted data is handled.

Never let a developer gain production privileges merely by editing an owner field in a repository. Require the authorization authority to validate source, approval, membership, and policy. Keep policy decision and enforcement independent and auditable.

### Design ownership transfer as a transaction-like workflow

A transfer changes obligations, not just a label. Record entity, old owner, new owner, initiator, approvals, reason, effective time, conditions, dependent roles, open risks, and rollback or exception plan.

Inventory affected surfaces: catalog relations, repository review routing, support queues, paging policies, dashboards, SLOs, cost centers, security findings, secrets and privileged roles, data stewardship, supplier contracts, documentation, roadmaps, and pending incidents or changes.

Use a handover interval when knowledge transfer is necessary, but preserve one accountable owner at every instant. Supporting roles may overlap. The effective change should update authoritative records coherently or expose partial completion as a failed transfer, not claim success after one portal edit.

Require acceptance from the new accountable group and authorization from appropriate governance. The old group cannot unilaterally abandon a production service; the new group cannot silently claim a system to acquire privileges.

Verify completion with current reads from each authority, notification tests, access review, unresolved-obligation count, and audit. Time-bound any exception and assign an escalation owner.

### Handle organizational change deliberately

A team rename should preserve stable group identity while changing display attributes and aliases. Ownership relations need not churn if they reference the durable ID. Deep links and search should redirect from old names for a bounded period.

A split needs disposition for every owned entity and responsibility role. Do not bulk-copy all assets to both successor groups. A merge maps former identities to one successor and checks conflicts in role, policy, and contact data.

An acquisition may bring colliding names, separate directories, and different role vocabularies. Namespace identities, preserve source authority, map terms through reviewed policy, and delay high-consequence automation until resolution quality is proven.

Before deleting an organizational group, require an ownership-zero check across independently inventoried asset classes, not just one catalog. Preserve historical identity for audit while removing active membership and permissions according to authority policy.

### Set metadata quality objectives

Quality has several dimensions: coverage, validity, resolvability, accuracy, freshness, consistency, uniqueness, routing success, and repairability. A non-null field can be wrong, inactive, or unusable.

Use an independent denominator. If the catalog itself supplies both the set of entities and the count with owners, missing entities disappear from the metric. Reconcile against runtime, repository, cloud, data, or business inventories appropriate to the scope.

Measure ownership coverage by criticality and environment. A 98% global result can hide every tier-zero gap. Track stale and conflicted separately from missing. Sample accuracy against owners and operational evidence.

Measure outcomes: time to find accountable owner, successful delivery or acknowledgement, correct incident routing, transfer completion time, exception age, and repair time. Avoid scorecards that incentivize placeholder values.

### Automate metadata without erasing accountability

Derive low-ambiguity facts such as repository URL, language, runtime namespace, or observed service version when the source contract supports them. Mark them observed or derived and preserve source time.

Suggested ownership can aid adoption, but require confirmation before it becomes accountable ownership. Inference from commit frequency, deployment actor, or cloud tag is probabilistic and can reflect contractors, automation, or historical work.

Automated remediation should be proportional. Notify and offer a repair action for stale docs; block a new production registration missing owner; quarantine an unauthorized classification change; do not delete a service because a metadata relationship vanished.

Keep generated and human-governed fields separate. Prevent controllers from fighting with repository edits. Expose the writable authority and repair path next to each rejected change.

### Protect metadata as sensitive information

Metadata can reveal unreleased projects, security posture, internal topology, employee membership, incident contacts, customer association, data classification, cost, or privileged systems. “It is only metadata” is not a security model.

Classify fields and relations. Enforce access before search indexing, autocomplete, counts, graph traversal, exports, notification templates, and analytics. Redacting the detail page after an entity name appeared in suggestions is too late.

Validate links and rendered content. Constrain URL schemes and destinations, escape untrusted markup, prevent formula injection in exports, and avoid embedding secrets or tokens in annotations. Audit reads of highly sensitive metadata where required.

Minimize replication. Prefer stable references and scoped resolution over copying identity membership, phone numbers, or classifications into many stale caches. Define deletion and retention for historical provenance.

### Operate ownership and metadata as a platform capability

Assign a product owner for the capability and stewards for schemas and vocabularies. Provide self-service repair paths, clear validation errors, bulk transfer tools, and APIs that return state and provenance rather than only strings.

Observe ingestion lag, resolution latency, directory failures, conflict count, invalid assertions, notification outcomes, transfer backlog, exception age, and policy-consumer errors. Alert on critical coverage regression and mass ownership churn.

Test fault modes: directory outage, deleted group, delayed incident provider, conflicting finance feed, repository replay, schema rollback, clock skew, malicious labels, unauthorized search, bulk reorganization, and restore from backup.

Back up non-derivable decisions, transfer records, exceptions, vocabulary registry, source authority configuration, aliases, and audit. Rebuild derived views from authoritative assertions and verify quality before enabling consequential consumers.

### Retire metadata and ownership integrations safely

A field cannot be removed when consumers still interpret it. Inventory writers, readers, search filters, dashboards, exports, policy rules, templates, stored events, and retained backups. Publish replacement semantics and a compatibility window.

Stop new writes, dual-read or translate where necessary, migrate stored assertions with provenance, measure zero use, remove policy dependence, then remove the field and old decoder. Keep historical interpretation available for retained audit records.

Retiring a source requires reassignment or explicit disposition of each field it owned. A new transport does not automatically inherit authority. Compare revisions and values, expose conflicts, and revoke old credentials only after reconciliation.

Retiring an entity requires closure or transfer of every active responsibility role. Catalog deletion is not proof that runtime resources, data obligations, costs, findings, or access grants are gone.

## Definitions and Notation

Let $E$ be entities, $G$ organizational groups, $P$ principals, $K$ metadata keys or relation types, $V$ values, $S$ sources, $R$ source revisions, and $T$ time. Let $\rho \in \mathcal{R}$ be a responsibility role and $x$ be authorization context.

An assertion is $a=(e,k,v,s,r,t_o,t_e,q,c)$ as defined in the review. Its applicability at time $t$ requires a valid interval, valid source authority, accepted schema, and field-specific freshness. Let $A_{e,k}$ be assertions about key $k$ on entity $e$. The resolver is

$$
R_k(A_{e,k},t) \rightarrow (v,z,p),
$$

where $z$ is state such as valid, stale, missing, unresolved, invalid, or conflict, and $p$ is provenance. Returning state and provenance prevents a bare value from hiding uncertainty.

Ownership is $Own(e,g,\rho,[t_s,t_e))$. For accountable role $\rho_a$, the ordinary active-entity invariant is

$$
\left|\{g \in G: Own(e,g,\rho_a,[t_s,t_e)) \land t_s \le t < t_e \land Active(g,t)\}\right|=1.
$$

An approved exception can replace equality with an explicitly governed exception state for a bounded interval; it must not masquerade as ordinary ownership.

Let independent inventory $I$ contain $N=|I|>0$ in-scope entities. If $M$ map uniquely to entities having valid active accountable ownership, coverage is $C_o=M/N$. Let $F_k$ be the number of resolved key-$k$ assertions within freshness objective among $D_k>0$ applicable entities; freshness compliance is $C_f=F_k/D_k$. Neither ratio proves semantic accuracy, so sample and operational confirmation remain necessary.

Authorization is $Permit(p,a,e,x) \in \{allow,deny\}$. The critical non-implication is

$$
Own(e,g,\rho,t) \land Member(p,g,t) \not\Rightarrow Permit(p,a,e,x).
$$

An explicit policy may use those facts, but action, environment, conditions, approvals, authoritative freshness, and enforcement still matter.

## Mechanisms, Invariants, or Proof Structure

### Ownership and metadata protocol

1. Define entity scope, user journeys, decisions, consequence levels, and non-goals.
2. Register responsibility roles and select the singular accountable role per entity kind.
3. Bind group references to stable identity authority and define active/alias/deletion semantics.
4. Register each metadata key with schema, authority, writer, sensitivity, freshness, conflict, compatibility, and consumers.
5. Ingest source assertions with revision, observation time, expiry, classification, and transformation provenance.
6. Validate shape, authority, references, cross-field meaning, temporal bounds, and sensitive-content rules.
7. Resolve deterministically, preserving missing, stale, invalid, unresolved, conflict, and hidden states.
8. Serve permission-filtered values, state, provenance, contacts, and repair actions appropriate to each journey.
9. Reread authoritative identity and policy for consequential workflows; never promote display ownership implicitly.
10. Transfer obligations through acceptance, approval, coordinated updates, verification, audit, and rollback.
11. Measure against independent inventories and test routing, organizational changes, faults, recovery, and disclosure.
12. Retire sources, fields, roles, groups, and entities only after consumer and obligation disposition.

### Core invariants

- **Typed accountability:** every responsibility relation states a governed role and scope.
- **Singular coordination:** every ordinary active entity has one current accountable group.
- **Identity continuity:** relations target durable identities; renames do not invent new owners.
- **Authority locality:** every field is decided only by its declared authority or approved resolution rule.
- **Temporal honesty:** source time and validity survive processing; stale facts remain stale.
- **State preservation:** unknown, invalid, unresolved, conflict, hidden, and not applicable remain distinguishable.
- **No implicit privilege:** ownership and membership alone never grant an action.
- **Transfer continuity:** an ownership change has no ungoverned accountability interval.
- **Least disclosure:** all discovery surfaces enforce field/entity policy before revealing metadata.
- **Independent evidence:** coverage and quality denominators do not come only from the catalog being evaluated.

### Proof sketch: ownership is insufficient for authorization

Assume ownership plus membership implied permission for every action. Let group $g$ own service $e$, and principal $p$ be a new member of $g$. Consider action $a$ that decrypts regulated production data. The ownership relation contains no environment, action, clearance, separation-of-duty, approval, incident condition, or revocation information. Two contexts with identical ownership and membership can legitimately require opposite decisions: development log read may be allowed while production decryption is denied. Therefore ownership and membership do not determine permission. An authorization policy must evaluate additional authoritative facts. This is a proof sketch of insufficiency, not a claim that ownership can never be a policy input.

### Executable ownership-state audit

The following synthetic audit applies explicit state categories to ten records. It demonstrates classification mechanics, not integration with a directory, paging system, catalog, or authorization engine.

<!-- bijux-verify: {"id":"ownership-state-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=4\nstale=2\nconflict=1\nunresolved=1\nexpired=1\nunauthorized=1\n"}} -->
```python
from collections import Counter

records = [
    {"entity": "ledger", "state": "valid"},
    {"entity": "pricing", "state": "valid"},
    {"entity": "search", "state": "valid"},
    {"entity": "profile", "state": "valid"},
    {"entity": "settlement", "state": "stale"},
    {"entity": "notifications", "state": "stale"},
    {"entity": "tax", "state": "conflict"},
    {"entity": "legacy-export", "state": "unresolved"},
    {"entity": "experiment", "state": "expired"},
    {"entity": "vault", "state": "unauthorized"},
]

counts = Counter(record["state"] for record in records)
for state in ("valid", "stale", "conflict", "unresolved", "expired", "unauthorized"):
    print(f"{state}={counts[state]}")
```

Expected output is four valid records, two stale records, and one each conflict, unresolved, expired, and unauthorized. A production audit must also verify source authority, source time, identity activity, role semantics, independent scope, and disclosure policy.

### Verification strategy

Schema tests cover required keys, types, bounds, vocabulary, prefixes, and compatibility. Authority tests attempt protected-field writes from every source. Identity tests cover stable IDs, aliases, inactive groups, missing targets, membership privacy, and rename/split/merge.

Resolver tests permute arrival order and replay identical revisions; results must remain semantically stable. Temporal tests cover exact expiry, clock skew, delayed snapshots, replay, and last-known-good policy. Conflict tests verify that equal authority does not disappear behind a chosen string.

Authorization tests prove that owner edits cannot grant privileges, stale membership cannot satisfy policy, and denial reaches every enforcement point. Disclosure tests cover search, autocomplete, counts, graphs, notifications, exports, caches, and analytics.

Transfer tests inject failures after each external update and require visible partial state, safe retry, compensation or completion, and no false success. Organizational simulations cover person departure, group rename/deletion, mass reassignment, acquisition collisions, and abandonment.

Quality validation reconciles independent inventories, samples accuracy, exercises contact routes, and measures repair. Recovery tests rebuild resolved views from backed-up decisions and fresh authorities before consequential consumers resume.

## Alternatives and Trade-Offs

1. **One owner versus co-ownership.** One accountable group gives a final coordination point; co-ownership represents collaboration but often diffuses decisions. Use supporting roles rather than ambiguous co-accountability.
2. **Group versus person owner.** Groups preserve continuity; people can clarify leadership but create departure risk. Restrict personal ownership to bounded low-risk contexts.
3. **Central registry versus repository declarations.** A registry offers consistent governance; repository metadata supports local review. Combine repository intent with field authority and directory resolution.
4. **Single record versus assertions plus resolved view.** A flat record is simple; assertion storage preserves provenance, disagreement, and rebuildability at higher complexity.
5. **Strict required fields versus progressive adoption.** Strictness prevents new debt; immediate enforcement can block migration. Enforce high-risk new entities and time-bound legacy exceptions.
6. **Controlled vocabulary versus free-form tags.** Controlled terms support automation; tags support exploration. Match governance to consequence.
7. **Push events versus periodic reconciliation.** Events reduce latency; reconciliation repairs loss and authority drift. Important fields usually need both.
8. **Last-known-good versus fail closed.** Stale display can aid routing; stale security facts can be dangerous. Define behavior per field and consumer.
9. **Derived ownership versus explicit declaration.** Inference accelerates discovery; it can mistake activity for accountability. Use it as a suggestion with confidence and confirmation.
10. **Catalog caching versus live authority reads.** Caching improves latency and resilience; live reads improve currency. Consequential consumers should reread or use freshness-bounded signed evidence.
11. **Unified roles versus domain-specific roles.** A small common core aids comprehension; domains need specialized duties. Govern extensions under owned namespaces.
12. **Atomic cutover versus overlap transfer.** Atomic effective time clarifies accountability; overlap helps knowledge transfer. Keep one accountable owner while supporting roles overlap.
13. **Broad visibility versus least disclosure.** Visibility improves discovery; metadata can expose sensitive systems and people. Filter every derived surface, not only detail pages.
14. **Blocking quality gates versus repair workflows.** Gates prevent bad new state; overblocking encourages bypasses. Couple proportionate gates with fast, explicit repair paths.

## Failure Modes and Misconceptions

1. **“Owner” has obvious semantics.** Consumers may mean maintainer, responder, approver, budget holder, or accountable group; define the role.
2. **A nonempty owner field means coverage.** The target can be inactive, wrong, stale, or unreachable.
3. **A person is the most accountable owner.** Person-based ownership loses continuity and encourages hero dependency.
4. **A chat channel is an owner.** It is a contact endpoint with uncertain membership and response behavior.
5. **An on-call schedule is ownership.** It identifies current response routing, not ultimate lifecycle accountability.
6. **CODEOWNERS defines service ownership.** It defines review routing for matched repository paths under GitHub's rules.
7. **Repository approval makes every field authoritative.** Reviewers cannot authoritatively assert HR membership, finance allocation, or runtime observation by convention alone.
8. **Last write wins is neutral.** It delegates governance to timing, retry order, and outages.
9. **A new processing timestamp makes data fresh.** Freshness begins at authoritative observation.
10. **One source owns the whole entity.** Different facts commonly belong to different authorities.
11. **Missing and hidden are equivalent.** Treating authorization filtering as absence can leak information or trigger unsafe remediation.
12. **Unknown is a useful default value.** It masks missing evidence and corrupts metrics.
13. **Free-form tags are harmless.** Once gates or policies consume them, undefined semantics become operational risk.
14. **Owner membership implies access.** Authorization requires an explicit policy and current context.
15. **Catalog edits can grant production privileges.** This creates a privilege-escalation path through a lower-trust writer.
16. **Transfer means changing one relation.** Operational, financial, security, access, and knowledge obligations must move.
17. **Two owners increase resilience.** Without decision rules they can reduce accountability; supporting roles and succession are clearer.
18. **Platform teams should own every orphan.** Silent fallback hides debt and overloads the shared team.
19. **Directory deletion proves no obligations remain.** The deletion may strand assets and destroy audit references.
20. **Quality equals percentage populated.** Correctness, freshness, resolvability, routing, and independent scope matter.
21. **Metadata is public because it is not payload data.** It can expose topology, people, classifications, and business plans.
22. **Redacting the detail page is sufficient.** Search indexes, counts, graphs, caches, and notifications can still leak.
23. **Automation should fill every gap.** Probabilistic suggestions are not accountable acceptance.
24. **Retiring a field only requires removing its form input.** Readers, policies, templates, events, exports, and backups retain semantics.

## Worked Examples

### Example 1

**Situation.** A production service lists `alice@example.com` as owner, but Alice leaves the company.

**Reasoning.** Resolve the service to a durable group, make Alice a removable contact or lead, verify the group is active, and test its escalation route. Treat the current record as an ownership breach until corrected; do not silently assign the platform team.

**Conclusion.** Group accountability survives individual turnover.

### Example 2

**Situation.** `payments-ledger` is renamed `money-movement`, retaining the same directory ID.

**Reasoning.** Keep the ownership target ID unchanged, update display name and contact attributes from the directory, retain a bounded search alias, and avoid rewriting every historical audit record as if ownership changed.

**Conclusion.** Rename is identity continuity, not transfer.

### Example 3

**Situation.** Repository YAML says Team A owns a service while an approved transfer registry says Team B became owner at noon.

**Reasoning.** The ownership field contract gives the transfer registry authority after its effective time. Preserve the stale repository assertion, show Team B as resolved owner, open a repair for source consistency, and do not use arrival time.

**Conclusion.** Temporal authority resolves the conflict without deleting evidence.

### Example 4

**Situation.** A developer changes `owner` to a group they belong to and expects production administrator access.

**Reasoning.** The catalog accepts or reviews the discovery assertion according to its contract, but the authorization service independently evaluates principal, current membership, action, production resource, required approval, and policy. No grant follows from the edit.

**Conclusion.** Ownership metadata is not a privilege assignment API.

### Example 5

**Situation.** A catalog shows 980 of its 1,000 services with owners and reports 98% coverage.

**Reasoning.** An independent runtime/repository inventory contains 1,200 in-scope services; only 900 map uniquely to valid active owners. Thus $C_o=900/1200=0.75$, or 75%. The 980/1,000 ratio omitted uncataloged services and included 80 invalid mappings.

**Conclusion.** Coverage requires an independent denominator and validity criteria.

### Example 6

**Situation.** A tier-zero service has a runbook contact last observed 36 hours ago against a 4-hour objective.

**Reasoning.** Keep the last route visibly stale only if emergency fallback policy permits it, query the paging authority, escalate the failed sync, and block claims that the ownership record is healthy. Do not refresh age from catalog reprocessing.

**Conclusion.** Freshness is fact-specific and source-timed.

### Example 7

**Situation.** A group splits into Checkout and Ledger teams.

**Reasoning.** Inventory every entity and typed role owned by the original stable ID, assign one accountable successor per entity, allow temporary supporting-role overlap, collect acceptance, update incident/cost/security/access systems, and prevent deletion of the original group until the independent ownership-zero check passes.

**Conclusion.** A group split is obligation disposition, not bulk string replacement.

### Example 8

**Situation.** Search autocomplete reveals the name and security classification of a restricted acquisition service.

**Reasoning.** Apply entity and field authorization before indexing and query aggregation, isolate or encrypt restricted index partitions, filter counts and suggestions, test caches and exports, and audit access. Hiding only the entity page does not repair the leak.

**Conclusion.** Metadata authorization begins before discovery surfaces.

### Example 9

**Situation.** Commit activity suggests Team X maintains an abandoned library, but Team X refuses ownership.

**Reasoning.** Store Team X as a provenance-bearing suggestion with confidence and expiry, route a confirmation workflow to the current governance owner, and keep the entity explicitly unowned/exceptional until acceptance. Activity can reflect a one-time patch or automation.

**Conclusion.** Inference can propose ownership but cannot manufacture accountability.

### Example 10

**Situation.** A lifecycle field consumed by portal filters, deployment policy, and archived events must be replaced.

**Reasoning.** Register replacement semantics, inventory all writers/readers and policy dependencies, dual-read or translate, migrate assertions with provenance, update retained-event decoders, prove zero old-field use, then remove writes and eventually the field. Keep historical interpretation for audit retention.

**Conclusion.** Metadata retirement is an interface migration.

## Cross-Program Connections

1. **Identity and Access Management:** stable groups, membership, federation, lifecycle, and revocation establish who organizational actors are.
2. **Security Engineering:** least privilege, ABAC/RBAC, separation of duty, information disclosure, and audit keep metadata from becoming an escalation path.
3. **Reliability Engineering:** escalation, on-call freshness, routing tests, SLOs, and incident evidence make ownership operationally useful.
4. **Data Engineering:** provenance, schemas, data contracts, quality dimensions, lineage, and independent reconciliation govern metadata assertions.
5. **Database Systems:** temporal relations, constraints, transactions, materialized views, migrations, and retention shape implementation.
6. **Distributed Systems:** delayed and reordered events, partitions, replay, idempotency, clocks, and convergence shape resolution.
7. **Software Engineering:** repository structure, CODEOWNERS, maintainership, change review, and deprecation represent narrower responsibilities.
8. **API & Service Engineering:** identifiers, compatibility, schema evolution, typed errors, authorization, and pagination define metadata APIs.
9. **Organizational Design:** team boundaries, accountability, enabling teams, reorganizations, mergers, and succession shape the ownership model.
10. **FinOps and Governance:** cost allocation, policy evidence, risk acceptance, data stewardship, and regulatory retention require distinct roles.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
2. Backstage. [Software Catalog](https://backstage.io/docs/features/software-catalog/). Retrieved 2026-09-02.
3. Backstage. [Descriptor Format of Catalog Entities](https://backstage.io/docs/features/software-catalog/descriptor-format/). Retrieved 2026-09-02.
4. Backstage. [Well-known Relations between Catalog Entities](https://backstage.io/docs/features/software-catalog/well-known-relations/). Retrieved 2026-09-02.
5. Backstage. [Catalog FAQ](https://backstage.io/docs/features/software-catalog/faq/). Retrieved 2026-09-02.
6. Backstage. [Permission Framework Overview](https://backstage.io/docs/permissions/overview/). Retrieved 2026-09-02.
7. GitHub. [About Code Owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners). Retrieved 2026-09-02.
8. Kubernetes. [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/). Retrieved 2026-09-02.
9. Kubernetes. [Recommended Labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/). Retrieved 2026-09-02.
10. Kubernetes. [Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/). Retrieved 2026-09-02.
11. OpenTelemetry. [Resource Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/resource/). Retrieved 2026-09-02.
12. W3C. [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/). W3C Recommendation, 30 April 2013. Retrieved 2026-09-02.
13. W3C. [The Organization Ontology](https://www.w3.org/TR/vocab-org/). W3C Recommendation, 16 January 2014. Retrieved 2026-09-02.
14. IETF. [RFC 7643: System for Cross-domain Identity Management: Core Schema](https://datatracker.ietf.org/doc/html/rfc7643). September 2015. Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define accountable owner, maintainer, operator, responder, data steward, cost owner, security partner, approver, contact, escalation, assertion, authority, freshness, transfer, and authorization. Explain three non-equivalences.

### Exercise 2

Given ownership assertions from repository YAML, an identity directory, a transfer registry, an incident system, and a finance ledger, design field authority and resolution rules for owner, membership, responder, cost center, and lifecycle. Trace a stale conflict.

### Exercise 3

Design an ownership audit for 50,000 production entities across catalog, runtime, repository, cloud, and data inventories. Include identity resolution, independent denominators, freshness, accuracy, routing, disclosure, and repair metrics.

### Exercise 4

Design a safe transfer of a tier-zero payments service between teams during an organizational split. Cover every dependent obligation, failure recovery, effective time, access, and verification.

### Exercise 5

An acquired company uses personal owners, public metadata search, free-form criticality tags, and catalog owner fields to grant cloud access. Design a migration that preserves delivery while establishing safe ownership and metadata governance.

## Answers to the Exercises

### Answer 1

The accountable owner is the singular active group answerable for an entity's fitness and able to coordinate decisions. Maintainer changes its implementation; operator runs it; responder handles current incidents; data steward governs data meaning and quality; cost owner accepts allocation; security partner supplies security expertise; approver authorizes a defined change or exception. A contact is an endpoint; escalation is an ordered tested response policy.

An assertion is a provenance-bearing claim about a field. Authority is the system or process entitled to decide that fact. Freshness measures time since authoritative observation. Transfer coordinates accountability and obligations between identities. Authorization decides whether a principal may perform an action on a resource in context.

Key non-equivalences include responder $\ne$ accountable owner, because paging duty can rotate or be outsourced; CODEOWNERS maintainer/reviewer $\ne$ production operator, because repository review says nothing about runtime duty; and ownership $\ne$ authorization, because permission also depends on actor, action, environment, policy, current membership, approvals, and conditions. Contact $\ne$ escalation is a fourth: a reachable address offers no response contract.

### Answer 2

Repository YAML may author intended accountable-owner reference and declared lifecycle if the field contracts assign those facts there. The directory alone decides stable group existence, active state, aliases, and membership. An approved transfer registry supersedes repository owner intent at and after its effective time until repository metadata converges. The incident system owns responder and escalation; finance owns cost center.

Store each assertion's source key, revision, observation time, expiry, validation, and sensitivity. Resolve owner by temporal authority, then resolve its stable group in the directory. Resolve membership only on demand under policy. Do not merge responder into owner. Finance conflicts remain visible unless an explicit ledger hierarchy chooses one authoritative record.

Suppose repository revision 18 observed at 09:00 says Team A, a transfer effective 12:00 says Team B, and at 14:00 the old YAML is replayed. At 14:00 Team B resolves as accountable owner because effective governed transfer outranks the stale declaration; the Team A assertion remains as inconsistency evidence and opens a repair. If Team B is inactive in the directory, state becomes unresolved rather than falling back to Team A. Processing the replay at 14:00 does not change its 09:00 source time.

### Answer 3

Construct separate scoped inventories from runtime deployments, repositories, cloud resources, and data platforms; define entity-kind mappings and deduplicate canonical identities. Preserve unmatched and ambiguous subjects. Let the union after governed reconciliation be the denominator, segmented by environment, criticality, domain, and asset class rather than using catalog rows alone.

For each entity, verify exactly one active accountable group, stable directory resolution, required supporting roles, source authority, observation age, and usable contact/escalation. Compute valid ownership coverage, missing, inactive, unresolved, stale, conflict, duplicate, and exception rates. Sample mappings and ask owners to confirm accountability. Run safe routing exercises and measure acknowledgement, false routing, time to find owner, repair time, and exception age.

Test entity/field/search/graph/export permissions with principals from multiple tenants and sensitivity classes. Never expose hidden as missing to unauthorized users in a way that leaks counts. Produce remediation queues owned by domain governance, provide self-service repairs at the authoritative source, and protect against placeholder gaming. Alert separately for tier-zero regressions and mass changes. Record inventory timestamps and mapping uncertainty with every report.

### Answer 4

Create a transfer record naming the service, old and new stable group IDs, one accountable role, supporting roles, reason, approvals, effective time, open risks, and rollback authority. Inventory repository review, build/deploy permissions, cloud roles, secrets, paging, support queues, runbooks, dashboards, SLOs, security findings, data obligations, cost center, vendor contacts, roadmap, pending changes, and incidents.

Collect new-owner acceptance and required governance approval. Complete knowledge and operational readiness checks before the effective time. Supporting maintainers and responders may overlap, but the old team stays accountable until the instant the approved transfer becomes effective; the new team is accountable afterward. Update authorities through idempotent operations keyed by transfer ID. A coordinator records per-system completion without declaring overall success early.

If an update fails, surface partial transfer, preserve the current accountable owner according to effective-time policy, retry safely, and use predeclared compensation only where reversal is valid. Never revoke the old team's emergency access before new access and escalation are tested. Verify fresh reads from catalog, directory, repository, paging, finance, security, and authorization; exercise contact, review current privileges, close or transfer pending obligations, and retain audit evidence. Delete the old group only after independent ownership and access-zero checks.

### Answer 5

First classify consequences and stop new high-risk debt: require a group owner for new production assets, disallow public indexing of restricted metadata, freeze new policy dependence on free-form tags, and prevent catalog edits from directly creating cloud grants. Do not immediately remove existing access without understanding operational dependency.

Federate or import acquired identities with stable namespace-qualified group IDs. Convert personal owners into time-bounded provisional assertions, propose teams from organizational evidence, and require accountable acceptance. Maintain people as leads or contacts. Define common roles and map local roles explicitly. Create controlled criticality values with behavioral definitions; translate old tags while preserving provenance and conflict.

Introduce field contracts for authority, schema, freshness, sensitivity, and consumers. Partition or rebuild search so authorization filters before indexing, autocomplete, counts, and exports. Replace owner-derived cloud access with an authorization policy using current identity membership, action, resource, environment, approvals, and deny behavior. Compare old and new decisions in audit-only mode, resolve unexplained differences, then cut over with rollback and monitoring.

Reconcile against independent runtime, cloud, repository, and data inventories; measure valid group ownership, stale/unresolved records, mapping accuracy, routing success, policy parity, and repair time. Transfer critical services first with tested escalation and privilege review. Time-bound every exception, keep old decoders for retained records, and retire personal-owner fields, free-form criticality, public indexes, and owner-to-cloud bindings only after writers and consumers show zero dependence.
