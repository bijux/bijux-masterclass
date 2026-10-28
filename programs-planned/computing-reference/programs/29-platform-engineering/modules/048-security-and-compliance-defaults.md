---
module_id: PLAT-048
program: Platform Engineering
level: 1
module_number: 48
title: Security and Compliance Defaults
status: complete
last_verified: 2026-09-02
---

# Security and Compliance Defaults

## One-Page Review

### Governing question

How should a platform turn security and compliance obligations into safe, usable, versioned workload defaults that reduce common risk without claiming universal protection, shifting product accountability to the platform, freezing one framework in code, or making exceptions easier than the supported path?

### Essential definitions

- A **security default** is an automatically selected control configuration with a named threat, scope, owner, compatibility envelope, verification method, exception rule, and lifecycle.
- A **secure-by-default path** starts workloads in a defensible state without requiring every team to rediscover controls; it is not secure for every asset or adversary.
- A **guardrail** constrains or checks a dangerous action while preserving bounded choice; preventive, detective, and corrective guardrails have different failure semantics.
- A **control objective** states the outcome to achieve, while a **control implementation** is one technical or procedural mechanism intended to contribute to it.
- A **compliance mapping** relates evidence and implementations to framework requirements; it is traceability, not proof that the requirement or whole system is satisfied.
- **workload identity** is an authenticated identity bound to a running workload and its execution context rather than a reusable human or shared static credential.
- An **exception** is a time-bounded, owned deviation with threat analysis, compensating controls, evidence, expiry, and a removal trigger.
- **break-glass access** is exceptional emergency authority that is strongly authenticated, narrowly scoped, short-lived, logged, alerted, reviewed, and revoked.
- **control evidence** is attributable, time-bounded information about design, operation, or results; configuration presence alone is weaker than operating-effectiveness evidence.
- **residual risk** is risk remaining after the selected controls and assumptions, accepted by an accountable risk owner rather than silently inherited by a platform team.

### Central model, mechanism, or theorem

For asset class $a$, execution context $x$, threat $t$, and policy revision $v$, define a default decision $D_v(a,x,t)=(m,e,r)$: mechanism $m$, required evidence $e$, and residual-risk disposition $r$. A release is admissible only when applicable decisions are satisfied or a valid exception covers each deviation. A weighted evidence score $C=\frac{\sum_i w_i q_i}{\sum_i w_i}$, where $0\leq q_i\leq1$, can prioritize remediation, but aggregation can hide one catastrophic missing control; every mandatory control must therefore retain an independent pass/fail gate.

### Critical invariants

- Defaults derive from assets, data classes, trust boundaries, workload archetypes, threats, and obligations—not from a fashionable tool or undifferentiated checklist.
- Product teams retain responsibility for domain authorization, data use, application logic, and risk disclosure; platform controls provide bounded capabilities and evidence.
- Human, workload, build, deployment, and emergency identities are separate, least-privileged, short-lived where feasible, and attributable.
- New workloads receive non-root execution, blocked privilege escalation, reduced capabilities, a tested security profile, declared writable paths, and explicit exceptions.
- Network location alone conveys no identity or authorization; ingress and egress are intentionally bounded and enforcement is tested at the data plane.
- Secrets are never source defaults, ordinary configuration, image layers, logs, or long-lived shared values; delivery, access, rotation, revocation, and deletion are tested.
- Artifacts are immutable by digest and admitted through verified source/build identity, provenance, inventory, policy, and risk evidence—not signature presence alone.
- Admission policy is versioned, tested, observable, fail-mode-specific, and protected from bypass; mutation never silently changes application semantics.
- Compliance controls map to versioned obligations and named evidence, owners, populations, collection methods, freshness, retention, exceptions, and reviewer decisions.
- Preventive controls have staged rollout and recovery paths; detective controls have action owners and response objectives; neither may silently fail open.
- Exceptions and break-glass events are scarce, expiring records that create alerts and follow-up, never permanent labels or invisible administrator habits.
- A control is retired only after enforcement, credentials, bindings, policy objects, stored evidence, exceptions, and consumers have been migrated or deliberately disposed.

### Common failures

Calling a hardened image a security program; equating benchmark percentage with safety; installing policy but not testing enforcement; enforcing one namespace while privileged paths bypass it; granting wildcard RBAC; sharing service accounts; automounting unused tokens; assuming an internal network is trusted; creating NetworkPolicy resources under a non-enforcing plugin; default-denying egress without DNS or recovery design; storing base64 as if encrypted; logging secrets; accepting any signed image; generating but never verifying provenance; scanning tags instead of deployed digests; allowing mutation to hide rejected requirements; making admission depend on an unavailable webhook without a deliberate fail mode; treating audit logs as prevention; mapping one artifact to many compliance controls without examining substance; retaining stale screenshots; granting permanent exceptions; using break-glass for routine work; and claiming compliance when the system boundary, population, period, or residual risks are unknown.

### Compact example

A platform profile for an internet-facing payment API classifies restricted customer data, public ingress, database egress, and high integrity/availability needs. It creates a dedicated workload identity with no default token mount, namespace-scoped deployment rights, restricted Pod security, read-only root filesystem, explicit temporary storage, default-deny ingress/egress plus DNS and named service flows, externally brokered short-lived credentials, encrypted storage, immutable artifacts with verified provenance and inventory, and admission gates for ownership and approved policy revision. Domain authorization and payment rules remain application-owned and are tested against an adopted application-security standard. Evidence records the exact workload/digest/policy, enforcement result, data-plane tests, credential rotation, control owner, collection time, and expiry. A native profiler exception grants one capability on isolated nodes for seven days, with approval, telemetry, compensating egress restriction, and automatic expiry. No score substitutes for the mandatory identity, privilege, data, and recovery gates.

### Connections

This module turns the platform guardrails of [PLAT-005](005-self-service-and-guardrails.md), runtime isolation of [PLAT-022](022-runtime-isolation-and-resource-controls.md), secret delivery of [PLAT-036](036-secret-delivery.md), workload contracts of [PLAT-041](041-workload-archetypes.md) through [PLAT-047](047-health-and-telemetry-contracts.md), and build/deployment capabilities into one assurance contract. PLAT-049 governs policy change; PLAT-050 addresses adoption without coercive friction.

## Governing Question

What must a platform standardize so an ordinary workload begins with defensible security and reviewable compliance evidence, while specialized risk decisions remain explicit and owned?

The answer is not “turn on every control.” Controls interact with workloads, recovery, cost, accessibility, privacy, and one another. A default-deny egress policy can stop exfiltration paths and also stop DNS, certificate renewal, time synchronization, package mirrors, or emergency diagnostics. A fail-closed admission webhook can prevent unsafe deployment and also prevent restoring the webhook itself. Security defaults are control-loop decisions with failure modes.

Nor can a platform inherit the product team’s whole security obligation. The platform can authenticate a workload, constrain a container, verify an artifact, broker a secret, and retain audit evidence. It cannot infer whether a refund actor may approve their own refund, whether a medical attribute may be used for analytics, or whether a domain event discloses forbidden information. Those rules live closer to product meaning.

A useful default therefore states what it protects, under which assumptions, against which threats, for which workload and data classes, using what mechanism, with what evidence and failure behavior, and how teams request a stricter profile or a temporary deviation.

## Why This Matters

Platform defaults have multiplicative reach. A safe identity template can remove thousands of copied static credentials; an overbroad deployment role can grant thousands of unintended privilege-escalation paths. Small defaults become fleet policy.

Most teams face the same recurring mechanics: runtime privilege, service identity, secret retrieval, artifact verification, encryption, network segmentation, audit collection, patching, and evidence export. Requiring every team to assemble them separately produces inconsistent semantics, slow review, and controls that exist only in documentation.

Compliance adds a second scaling problem. Framework language is intentionally broad and outcome-oriented. Auditors and risk owners need system boundaries, populations, control ownership, design evidence, operating evidence, exceptions, sampling, and review decisions. A dashboard showing “97% compliant” may obscure the one production workload with cluster-administrator credentials or the one data store outside the assessed boundary.

Threats and infrastructure evolve. A safe Kubernetes field, cipher suite, base image, identity lifetime, scanner policy, or framework mapping may change. Defaults must be versioned products with rollout, compatibility, rollback, and retirement—not timeless YAML fragments.

Usability is a security property. If the supported route cannot perform a legitimate high-risk workload, teams will accumulate hidden bypasses. The platform must make the common safe path easy, the specialized safe path possible, and unsafe ambiguity visible.

## Prerequisites and Retrieval

Retrieve assets, adversaries, attack surfaces, trust boundaries, confidentiality/integrity/availability, privacy, safety, threat modeling, risk, control objectives, preventive/detective/corrective controls, defense in depth, least privilege, separation of duties, authentication, authorization, federation, public-key infrastructure, certificates, encryption, key management, secret management, audit, vulnerability management, secure development, dependency and artifact supply chains, SBOMs, provenance, signatures, containers, Linux users/capabilities/seccomp/MAC, Kubernetes service accounts/RBAC/admission/Pod security/NetworkPolicy, data classification, retention/deletion, evidence, control testing, incident response, exceptions, SLOs, deployment strategies, and decommissioning.

You should distinguish identity from permission; authentication from authorization; encryption from access control; hash from signature; signature from trusted provenance; vulnerability from exploitable risk; control implementation from control objective; configuration evidence from operating effectiveness; framework mapping from certification; audit from prevention; namespace from trust boundary; internal network from trusted actor; workload identity from human identity; secure default from universal guarantee; exception from silent bypass; and break-glass authority from permanent administration.

## Learning Objectives

After completing this module, you should be able to:

1. derive security defaults from system boundary, asset/data class, workload archetype, threats, and obligations;
2. allocate platform, product, security, compliance, infrastructure, and risk ownership without gaps or double claims;
3. design least-privilege human, workload, build, deployment, and emergency identity contracts;
4. specify runtime, network, secret, data, supply-chain, admission, and telemetry controls with tested failure behavior;
5. translate control objectives into versioned implementations and attributable evidence without confusing mappings with assurance;
6. stage preventive and detective controls across brownfield fleets using observe, warn, enforce, quarantine, and retire states;
7. evaluate exceptions, compensating controls, break-glass access, residual risk, and expiry;
8. test control presence, effectiveness, bypass resistance, recovery, compatibility, and evidence freshness; and
9. measure security-default outcomes without allowing aggregate scores to hide mandatory failures.

## Core Exposition

### Start with boundary, assets, and decisions

Define the system boundary before selecting controls. Include source repositories, CI workers, artifact stores, control planes, nodes, workload namespaces/accounts, data services, identity providers, secret/key systems, telemetry pipelines, administrator endpoints, vendors, and recovery systems. Record external dependencies and shared-responsibility assumptions.

Inventory assets by business role and security need: customer data, credentials, signing keys, source, artifacts, build authority, deployment authority, production effects, logs, backups, and evidence. Classify data by sensitivity, jurisdiction, purpose, retention, and deletion obligation. “Production” and “non-production” are not sufficient classifications; a test environment can contain production credentials or copied personal data.

Model actors and threats. Include external attackers, compromised workloads, malicious or mistaken insiders, dependency maintainers, CI compromise, stolen tokens, confused deputies, tenant escape, misconfiguration, denial of service, data loss, evidence tampering, and failed recovery. State capabilities and trust assumptions. Do not design only for a perfect control plane.

Express decisions as policy: who may perform which action on which resource, under which context, for what duration, with what evidence and response. Link each default to threats and control objectives. A non-root container primarily limits consequences of process compromise; it does not authenticate requests or prevent vulnerable application logic.

Publish scope and non-guarantees. The platform profile may assure deployment mechanics for admitted workloads, but not product authorization correctness, lawful data purpose, vendor behavior outside the boundary, or zero vulnerabilities.

### Classify profiles instead of promising one universal baseline

Create a small profile taxonomy based on risk-relevant differences: public versus private exposure, ordinary versus restricted data, stateless versus stateful effect, standard versus elevated privilege, single versus multi-tenant execution, and normal versus critical availability.

A baseline profile should cover ordinary internal workloads. A restricted-data profile may add stronger identity, dedicated stores, narrower egress, enhanced audit, encryption/key boundaries, regional placement, and evidence retention. A privileged infrastructure profile needs isolated nodes, stronger admission ownership, reduced tenancy, and explicit host access; it should not weaken every namespace.

Define inheritance. Higher profiles accumulate requirements unless a control becomes inapplicable and the reason is recorded. Avoid copying independent policy bundles that drift. Version the profile and every referenced implementation.

Risk tiers should drive rigor, not prestige. A small cron job rotating production keys may deserve stronger controls than a large public documentation site. Classify effects and authority as well as data.

### Allocate ownership across the assurance chain

The platform team owns default mechanisms, interfaces, policy revisions, conformance tests, rollout, evidence production, support, and retirement. Security specialists own threat methods, control guidance, security review, monitoring strategy, and incident coordination. Compliance owners interpret obligations, define evidence expectations, and coordinate independent assessment. Infrastructure operators secure shared control planes/nodes/networks. Product teams own assets, data purpose, domain authorization, secure application behavior, dependency use, and disclosed exceptions. Risk owners accept residual risk.

Use a responsibility matrix for each control objective, but do not let a matrix replace the interface. Specify what the platform emits, what product teams declare, what the assessor examines, and who acts on failure.

Separate duties where compromise would be severe. Code authors should not unilaterally change protected release policy and approve the same production release. Build steps should not hold provenance-signing authority. Platform administrators should not use emergency credentials for daily work. Separation must include recovery; otherwise one unavailable approver can make unsafe bypass the only incident route.

### Design identity before permissions

Inventory human, workload, node, CI/build, deployment, controller, database, vendor, and emergency identities. Assign stable subjects to stable roles, while credentials remain short-lived and rotatable. Shared user accounts and reused service accounts destroy attribution and enlarge blast radius.

For humans, federate through the organizational identity provider, require phishing-resistant authentication where risk warrants it, use group/role assignment, time-bound elevation, session recording or command audit for sensitive access, and rapid deprovisioning. Authorization must respond to role change, not wait for a static certificate to expire months later.

For workloads, bind identity to attested execution context: namespace/account, deployment, environment, cluster, image or policy attributes as appropriate. SPIFFE illustrates a model of workload identifiers, trust domains, short-lived verifiable identity documents, a workload API, and rotating trust bundles. The platform must still securely perform workload attestation and authorization; a certificate is not permission.

For CI and deployment, prefer federated workload identity to stored cloud keys. Bind issuer, repository/project, protected revision/environment, workflow, audience, and lifetime. Separate build read authority from artifact publication and deployment effects.

### Make authorization least-privileged and analyzable

Start denied and add named actions on named resources. In Kubernetes, prefer namespace-scoped Roles/RoleBindings where possible, avoid wildcards, constrain powerful service accounts, and review privilege-escalation paths. Rights to create Pods can imply access to mounted Secrets or node capabilities even when direct Secret reads are denied.

Give each workload a dedicated service account and disable token automount when it does not call the API. Scope tokens by intended audience and lifetime where the integration supports it. Never use a namespace’s default service account as an ambient application identity.

Analyze effective permissions, not only authored manifests. Role aggregation, group membership, impersonation, controller behavior, custom resources, admission mutation, and cloud IAM bindings can change authority. Continuously inventory subject-to-action edges and alert on new high-impact paths.

Treat authorization decisions as domain-specific at the application boundary too. Platform RBAC cannot decide which customer may view which invoice. Provide authentication/context libraries and policy hooks, but keep resource/action semantics with the owning service.

### Harden runtime execution by default

For ordinary Linux workloads, default to non-root, no privilege escalation, dropped capabilities, a default seccomp profile, no host namespaces/devices, explicit user/group strategy, read-only root filesystem where compatible, and declared bounded writable mounts. Test signal handling, crash collection, temporary files, certificate updates, and language-runtime behavior under these restrictions.

Kubernetes Pod Security Standards provide privileged, baseline, and restricted profiles, and Pod Security Admission can apply enforce, audit, and warn modes at namespace scope. Pin versions during controlled rollout so a cluster upgrade does not silently change enforcement. The built-in profile is a broad Pod hardening baseline, not a complete workload security policy.

Use stronger isolation for untrusted tenants, privileged code, kernels exposed to hostile inputs, or regulated boundaries: dedicated nodes/clusters/accounts, sandboxed runtimes, mandatory access control, or virtualization as justified. “Namespace” is an API grouping and partial policy boundary, not automatically a hard tenant boundary.

Resource requests/limits, process limits, storage quotas, and concurrency bounds contribute to availability containment. They do not alone stop distributed denial of service or noisy shared infrastructure. Couple them to admission, quotas, rate controls, and capacity policy.

### Bound network flows and authenticate peers

Document ingress and egress as allowed flows: source identity/class, destination, protocol/port, name resolution, encryption, authentication, authorization, purpose, and owner. Default-deny can be valuable only when required control-plane, DNS, identity, secret, telemetry, update, health, and recovery flows are intentionally restored.

Kubernetes NetworkPolicy controls selected layer 3/4 flows only when the network plugin enforces it. Policies combine additively; source egress and destination ingress must both allow a connection. Test the actual data plane because merely creating the API object proves nothing, and implementation behavior for some protocols/NAT paths varies.

Do not make IP address or “inside the cluster” the principal identity. Authenticate service peers and authorize resources/actions. NIST zero-trust guidance rejects implicit trust from network location or ownership; this is an architectural principle, not a product toggle.

Control egress destinations, proxies, metadata endpoints, and DNS semantics according to threat and operability. A domain allow-list may resolve to changing/shared addresses; an IP rule may not express service identity. Record the limitation and test exfiltration/resolution paths.

### Deliver secrets and keys without creating new copies

Classify passwords, API tokens, private keys, database credentials, encryption keys, signing authority, recovery materials, and vendor credentials. For each, define issuer/source, authorized subjects, delivery, lifetime, rotation, revocation, audit, memory/file exposure, backup, and deletion.

Kubernetes Secret values are base64-encoded rather than encrypted by that representation, and etcd encryption at rest must be configured separately. Limit `get`, `list`, and `watch`; list access reveals data, and permission to create a Pod that mounts a Secret can be an indirect read path.

Prefer short-lived brokered credentials through workload identity. Mount only into containers that need them; avoid environment variables when child processes, crash dumps, debug endpoints, or process listings can expose them. Never place secrets in source, generated manifests, image layers, build arguments, caches, logs, metrics, traces, or attestations.

Rotation is a protocol: issue new, distribute, reload, verify use, revoke old, and prove recovery. Test overlap and outage behavior. A platform that rotates storage but workloads never reload has not completed rotation.

Keep encryption keys separated from encrypted data and from ordinary administration where feasible. Define envelope boundaries, algorithm/key versions, backup/recovery, cryptographic erasure assumptions, and re-encryption. Encryption does not correct overbroad authorized access or unlawful processing.

### Verify the software supply chain at admission

Protect source branches, review/merge rules, dependency resolution, CI definitions, build workers, registries, release metadata, and deployment references. Threat-model every authority that can change produced bytes or accepted policy.

Use isolated builds with controlled inputs and least-privileged identity. Bind artifacts, SBOMs, vulnerability results, licenses, tests, signatures, and provenance to immutable digests. SLSA defines increasing build/source assurance tracks and emphasizes verifying provenance against expectations; provenance that nobody checks is inert metadata.

Admission should verify subject digest, trusted issuer/builder identity, source/revision, build type and parameters, approved base/dependencies, required attestations, policy revision, risk decisions, and exception. “Signed” is insufficient if any developer key, unknown workflow, or compromised post-build uploader is trusted.

Scanner output needs exploitability, reachability, exposure, affected version confidence, fix availability, compensating controls, and deadlines. False positives and incomplete inventories exist. A critical reachable flaw can block while a lower-priority issue enters an owned remediation window; policy must explain the difference.

Re-evaluate deployed artifacts when vulnerability intelligence, trust roots, builders, dependencies, or policy changes. Build-time pass does not remain current forever.

### Treat admission policy as production software

Admission sits after authentication/authorization for mutating API requests; Kubernetes admission does not intercept ordinary reads. Define which resources, operations, namespaces, users/controllers, subresources, and versions each rule covers. Protect alternative deployment paths and direct infrastructure APIs.

Prefer validation for required declarations and safety bounds. Use mutation only for deterministic, visible, ownership-preserving defaults. Record the effective object and explain mutations; otherwise teams reason about source while production runs something else.

Version policy source, tests, bundles, dependencies, rollout state, and decision schema. Test valid/invalid inputs, missing fields, type/version changes, generated resources, exemptions, controller identities, timeout, unavailable dependencies, overload, rollback, and bootstrap/recovery.

Choose fail behavior per threat and operation. Failing closed for high-risk privilege escalation may be justified; a fragile external webhook that blocks all cluster recovery may create unacceptable availability risk. Reduce dependencies, replicate/protect policy engines, cache verified bundles carefully, and maintain a tested recovery authority.

Stage observe, warn, enforce for brownfield adoption. Metrics must separate evaluation, violation, error, exemption, timeout, and bypass. An enforcement service returning errors is not evidence that resources are safe.

### Keep application security in the contract

Platform controls do not replace secure design and coding. Require product threat modeling for meaningful changes, secure review, dependency policy, input/output handling, domain authorization tests, session/token design, safe cryptography, error behavior, abuse/rate controls, and security testing appropriate to exposure.

NIST SSDF organizes outcome-based secure-development practices that can be integrated into existing lifecycles. OWASP ASVS provides versioned application-security verification requirements. Adopted requirements must be selected and versioned for the product profile; blindly claiming an entire standard without evidence is worse than a narrower honest contract.

Provide paved libraries and test fixtures for authentication context, authorization hooks, TLS, secret refresh, logging redaction, headers, serialization, and common abuse defenses. Keep them upgradeable and disclose which risks remain application-owned.

Security tests include misuse and adversarial cases, not only scanners: cross-tenant access, confused deputy, replay, stale authorization, injection, unsafe deserialization, request smuggling across proxies, sensitive error/log output, resource exhaustion, and recovery after key/policy rotation.

### Protect data across its lifecycle

Bind collection and use to declared purpose, classification, subject/category, location, retention, sharing, and deletion. Enforce storage and transport protection, but also minimize fields and copies. Backups, caches, analytics, debug captures, queues, dead letters, logs, and test datasets are part of the data inventory.

Define authorization and audit at the data service, not only the network. Separate administrative, application, analytics, migration, backup, and emergency identities. Use row/tenant/domain controls where required and test isolation with adversarial identities.

Retention must result in deletion or irreversible transformation across replicas and derived stores under documented limits. Legal holds and immutable backup windows need explicit reconciliation. “Deleted from the primary table” is not system deletion.

Telemetry has its own sensitivity. Redact at the producer where feasible, restrict query/export authority, encrypt, bound retention/cardinality, and audit high-risk access. A security dashboard must not become the easiest source of credentials or personal data.

### Translate obligations into evidence contracts

Build a control catalog with stable IDs. For each objective, record applicability, rationale, implementation(s), owner/operator, system boundary, population, evidence type/source, collection method, frequency/freshness, retention, reviewer, test procedure, exceptions, and residual risk.

Map control IDs to chosen framework/version requirements such as NIST SP 800-53. Many-to-many mappings are normal. A single access-review process may support several requirements; one requirement may need identity, authorization, logging, review, and remediation evidence. Never clone evidence solely to inflate coverage.

Distinguish design evidence (the control is specified), implementation evidence (configuration exists), operating evidence (it executed over the period), and result evidence (tests/incidents/remediation show outcomes). A screenshot is a weak point-in-time artifact unless its source, object, time, query, and integrity are attributable.

Evidence must identify exact population and exclusions. “All clusters” requires an inventory and reconciliation of clusters, not a sample chosen by the tool. Record missing/unreachable systems as unknown or failed, not silently absent.

Preserve collection code, query/policy revision, raw result or integrity-protected reference, timestamps, actor/workload identity, and transformation. Restrict evidence because it may reveal topology, vulnerabilities, identities, or personal data. Define retention and defensible deletion.

### Measure without turning scores into truth

Let controls $i=1,\ldots,n$ have review weight $w_i>0$ and evidence quality $q_i\in[0,1]$. A portfolio score

$C=\frac{\sum_{i=1}^{n} w_iq_i}{\sum_{i=1}^{n}w_i}$

can prioritize effort. It is not a probability that the system is secure, because controls and threats are dependent, weights are judgments, evidence can be incomplete, and one failed mandatory control may dominate loss.

Track mandatory gates separately: unknown assets, privileged identities, public exposure, restricted data, unverified artifacts, control errors, expired evidence, overdue critical findings, exceptions past expiry, and unreviewed break-glass events.

Measure outcomes and operations: time to revoke, rotate, patch, remediate, detect drift, close exceptions, restore enforcement, and produce reconciled evidence; denied/bypassed attempts; control-error rate; affected population; and recurrence. Avoid rewarding teams for finding fewer vulnerabilities or requesting fewer exceptions.

For expected-loss prioritization, a rough model $R=\sum_j p_jL_j$ can expose assumptions about scenario likelihood $p_j$ and loss $L_j$. Do not sum mutually exclusive/dependent scenarios without qualification or present speculative values as measured risk. Use ranges and sensitivity analysis.

### Engineer exceptions as expiring products

An exception record names requester, owner, approver/risk owner, asset/profile, exact control/deviation, threat/rationale, affected scope, start/expiry, compensating controls, evidence, monitoring, incident action, migration/removal plan, and renewal rules.

Enforce the narrowest machine-readable scope: specific workload, namespace, digest, permission, destination, or policy version. A label like `security-exempt=true` with no signed record is a bypass primitive.

Compensating controls must address the same objective with evidence. “Team will be careful” is not a control. A profiler needing one capability might run only on isolated nodes, use a dedicated identity, deny external egress, restrict images, enable enhanced audit, and expire automatically.

Alert before expiry and at use. Expiry should remove admission or authority safely; rehearse rollback if removal can interrupt critical service. Renewal is a new risk decision with current evidence, not automatic date extension.

### Design break-glass for emergencies, not convenience

Define emergencies, eligible responders, approval or accountable unilateral conditions, authentication, credential issuance, maximum duration, resource/action scope, logging, notification, revocation, and post-event review. Store recovery factors independently from the system they recover.

Use just-in-time credentials rather than shared permanent administrator tokens. Alert immediately on issuance and use. Capture commands/API events and protect logs from the emergency actor where possible. Ensure the mechanism works during identity-provider, network, policy-engine, and control-plane partial failures.

Reconcile every session: what changed, what data was accessed, what temporary resources/credentials remain, whether ordinary policy must be updated, and what incident/follow-up owns remediation. A dormant untested emergency account is not a recovery capability.

### Migrate brownfield fleets without normalizing drift

Inventory all workloads and policy paths before enforcement. Classify current state as conforming, nonconforming, unknown, exempt, or unreachable. Unknown is not conforming.

Provide machine-generated remediation proposals, compatible template/library upgrades, test environments, owners, deadlines, and support. Start new-workload enforcement earlier while existing workloads progress through warning and bounded exceptions. Do not let “legacy” become an identity with permanent privilege.

Canary policy by cluster, tenant, workload class, operation, and control. Compare decision logs and application outcomes. Pause on policy errors or unexpected business harm, distinguish them from intended violations, and maintain an audited rollback.

Quarantine may be safer than deletion: block new deploys or network exposure while preserving controlled diagnosis and recovery. Define terminal retirement of obsolete policy versions, exceptions, webhook credentials, scanner accounts, cached bundles, and evidence pipelines.

### Test control effectiveness and recovery

For every default, test syntax/schema, policy selection, positive admission, negative denial, indirect bypass, data-plane effect, drift detection, telemetry, failure behavior, recovery, upgrade, rollback, and removal. A unit test of policy expression cannot prove the network plugin enforced a packet denial.

Use controlled adversarial probes: attempt wildcard escalation, token use from the wrong audience, Pod creation to read a Secret, privileged container admission, metadata-service access, unapproved egress, unsigned or wrong-provenance artifact, stale exception, secret leakage into logs, and emergency credential use.

Reconcile desired policy, admitted resource, runtime state, external cloud/data policy, and observed behavior. Controllers and manual APIs can create drift after admission.

Exercise control-plane failure: identity provider unavailable, trust bundle stale, policy webhook timeout, log sink down, scanner feed delayed, key-management throttled, or registry unreachable. Verify bounded degradation and incident signals rather than assuming fail-open or fail-closed is always right.

### Govern lifecycle and policy change

Assign every default a semantic policy revision, component versions, owner, support status, compatibility statement, rollout cohort, evidence schema, deprecation date, and retirement condition. Distinguish tightening, relaxation, clarification, and implementation-only changes.

Threat intelligence, incidents, vulnerabilities, framework revisions, platform upgrades, new jurisdictions, and false-positive evidence can trigger change. Assess affected workloads and controls, then test enforcement and evidence migration.

Publish change previews and explanations. Provide queryable violations and remediation, not opaque rejection. Emergency tightening can accelerate cadence but still needs scope, incident authority, rollback criteria, and retrospective.

Retire a control implementation only after replacement coverage is proven and bypasses are closed. Remove code, admission objects, roles, service accounts, signing/trust roots, webhook certificates, network rules, secret paths, dashboards, alerts, evidence jobs, retained data, exceptions, and documentation according to policy. A deleted repository file is not retirement.

### Use an executable contract inventory

The following synthetic inventory checks whether ten control profiles carry minimum design fields. It does not inspect a cluster, validate threats, prove control effectiveness, establish compliance, or replace independent assessment.

<!-- bijux-verify: {"id":"security-compliance-profile-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"profiles 10\nthreat_scoped 10\nidentity_bounded 9\nruntime_bounded 8\nnetwork_tested 8\nsecret_lifecycle 9\nsupply_chain_verified 9\nevidence_fresh 10\nexceptions_expire 9\nrecovery_tested 8\n","stderr":""}} -->
```python
profiles = [
    ("web-public", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("api-private", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("consumer", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("batch", 1, 1, 1, 0, 1, 1, 1, 1, 1),
    ("scheduled", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("stateful", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("restricted-data", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("privileged-infra", 1, 1, 0, 1, 1, 1, 1, 1, 1),
    ("legacy-migrate", 1, 0, 0, 0, 0, 0, 1, 0, 0),
    ("emergency-recovery", 1, 1, 1, 1, 1, 1, 1, 1, 0),
]
labels = [
    "threat_scoped", "identity_bounded", "runtime_bounded", "network_tested",
    "secret_lifecycle", "supply_chain_verified", "evidence_fresh",
    "exceptions_expire", "recovery_tested",
]
print("profiles", len(profiles))
for index, label in enumerate(labels, start=1):
    print(label, sum(profile[index] for profile in profiles))
```

The zeros identify deliberate review questions, not permission to omit controls. For example, a batch profile may have no inbound application flow, while the legacy profile records incomplete current conformance and therefore needs an owned migration state.

## Definitions and Notation

- $a$: asset or data classification relevant to a default decision.
- $x$: execution context, including environment, tenant, workload archetype, exposure, and authority.
- $t$: modeled threat or misuse scenario.
- $v$: version of a policy/default profile.
- $D_v(a,x,t)=(m,e,r)$: selected mechanism, evidence contract, and residual-risk disposition.
- $m$: technical or procedural control implementation.
- $e$: attributable evidence required for design, operation, result, or review.
- $r$: residual-risk state such as accepted, remediating, excepted until a date, or rejected.
- $w_i>0$: prioritization weight for control $i$.
- $q_i\in[0,1]$: assessed quality/currentness value for control evidence $i$.
- $C$: weighted evidence score, used for prioritization rather than assurance probability.
- $p_j$: estimated likelihood or frequency for scenario $j$, with uncertainty stated.
- $L_j$: estimated loss for scenario $j$ under a declared unit and horizon.
- $R$: rough expected-loss aggregation over suitably modeled scenarios.
- **applicability**: whether a control objective applies to an asset/context and why.
- **compensating control**: alternate mechanism addressing the same objective during a deviation.
- **unknown**: a first-class state where inventory, enforcement, or evidence cannot establish a result.

## Mechanisms, Invariants, or Proof Structure

1. **Scope:** enumerate systems, actors, assets, data, authority, environments, dependencies, and recovery paths.
2. **Model:** connect threats and obligations to explicit control objectives and non-guarantees.
3. **Profile:** select inherited defaults by asset, exposure, archetype, tenancy, privilege, and availability.
4. **Allocate:** name platform, product, security, compliance, infrastructure, assessor, and risk owners.
5. **Implement:** compose identity/RBAC, runtime, network, secrets/keys, data, supply chain, admission, application, and telemetry controls.
6. **Evidence:** bind policy, object, population, source, method, identity, time, freshness, retention, exception, and result.
7. **Enforce:** progress from inventory/observe through warn, canary, enforce, quarantine, and retirement with explicit fail behavior.
8. **Test:** verify intended allow/deny, indirect bypass, runtime/data-plane effect, telemetry, partial failure, recovery, upgrade, rollback, and deletion.
9. **Except:** narrow, approve, monitor, expire, reconcile, and remove deviations and emergency authority.
10. **Reconcile:** compare inventory, desired policy, admission decisions, runtime/cloud/data state, observations, and review records.
11. **Evolve:** version mappings and mechanisms, migrate consumers/evidence, revoke obsolete authority, and retire all residual resources.

The weighted-score limitation follows from construction. If nine low-impact controls each have $w_i=1,q_i=1$ and one catastrophic mandatory control has $w=1,q=0$, then $C=0.9$. The high score coexists with failure of the mandatory control. Therefore $C$ can rank work only when independent gates preserve non-compensable requirements.

The admission assurance chain is conjunctive: authenticated request, authorized subject, correct policy selection, successful policy evaluation, protected enforcement path, reconciled runtime state, observed effect, and current evidence. If any link is unknown, the whole control claim must be narrowed rather than promoted to “secure.”

## Alternatives and Trade-Offs

- **One fleet baseline versus risk profiles:** one baseline is legible but either too weak for high-risk workloads or too restrictive for ordinary ones; a small inherited profile set adds complexity while preserving meaning.
- **Prevent versus detect:** prevention reduces unsafe state but can block recovery; detection preserves availability but accepts exposure until response. Choose per threat, latency, and recovery.
- **Fail closed versus fail open:** fail closed protects the gated objective during evaluator failure; fail open protects availability. Use operation-specific degraded modes, not slogans.
- **Validation versus mutation:** validation keeps intent visible but asks teams to declare more; mutation improves ergonomics but can surprise owners and obscure effective state.
- **Built-in standards versus custom policy:** built-ins are maintained and interoperable but broad; custom rules express organization/application needs but require versioning, tests, and operations.
- **Namespace versus dedicated isolation:** namespaces are efficient policy domains but share control plane/kernel layers; separate nodes, clusters, or accounts increase isolation and expense.
- **Static secrets versus brokered credentials:** static values are widely compatible but copyable and hard to revoke; short-lived identity-derived credentials reduce exposure but depend on identity/control-plane availability.
- **Network identity versus cryptographic workload identity:** network rules are useful containment but weak actor identity; cryptographic identity enables peer authorization but adds attestation, PKI, and rotation failure modes.
- **Central policy versus delegated policy:** central control improves consistency; delegation captures domain semantics. Bound delegation with schemas, ownership, tests, and higher-level invariants.
- **Continuous collection versus audit snapshots:** continuous evidence detects drift and covers populations but costs more and can expose sensitive metadata; samples need justified population and sampling rules.
- **Quarantine versus deletion:** quarantine preserves diagnosis/recovery while constraining harm; deletion removes exposure faster but can destroy evidence or state.
- **Automatic remediation versus human review:** automation shortens exposure for reversible known changes; high-impact or ambiguous changes require approval, canarying, and rollback.
- **Aggregate score versus mandatory gates:** scores communicate portfolios but hide distribution/tail failures; gates preserve critical invariants but need careful applicability and exception handling.
- **Broad emergency authority versus narrow just-in-time access:** broad access is flexible during unknown incidents but has enormous blast radius; narrow access needs prepared workflows and multiple recovery scenarios.

## Failure Modes and Misconceptions

- **“Restricted Pod security means the application is secure.”** It bounds selected runtime privileges, not domain authorization, dependencies, data use, or denial of service.
- **“A namespace is a tenant boundary.”** isolation depends on control plane, node/kernel, network, RBAC, admission, storage, secrets, and operator authority.
- **“Default deny proves isolation.”** the enforcement plugin, selected endpoints, additive rules, protocols, NAT, DNS, host paths, and tests determine actual behavior.
- **“Internal traffic is trusted.”** network location neither authenticates a principal nor authorizes a domain action.
- **“Read-only Secret access is harmless.”** reading is the sensitive action; list/watch can expose values, and Pod creation can create indirect reads.
- **“Base64 protects a Secret.”** encoding provides no confidentiality.
- **“Encryption solves access control.”** authorized misuse and compromised endpoints can still read plaintext.
- **“The image is signed, so it is trusted.”** verifier expectations, signer identity, provenance, digest, build path, and policy decide trust.
- **“An SBOM proves no vulnerable code exists.”** inventory may be incomplete, and component presence differs from reachability/exploitability.
- **“The scanner passed at build time.”** intelligence, policy, deployed digest, exposure, and runtime state can change.
- **“Admission sees every dangerous action.”** reads bypass admission, and alternative APIs, existing objects, controllers, nodes, or clouds may bypass the gate.
- **“Mutation is invisible convenience.”** it changes effective configuration and can violate application assumptions unless surfaced and tested.
- **“Fail closed is always secure.”** unavailable enforcement can block repair, credential rotation, or incident recovery and amplify harm.
- **“Audit equals prevention.”** a log may support detection/accountability only if complete, protected, monitored, and acted on.
- **“Compliance percentage is assurance.”** mappings, weights, missing populations, stale evidence, and catastrophic gaps invalidate that inference.
- **“One screenshot proves a control operated all quarter.”** point-in-time presence lacks population and period evidence.
- **“No findings means no vulnerabilities.”** coverage, tool errors, exclusions, suppressed results, and unknown assets matter.
- **“Compensating means any extra control.”** it must address the same objective and have comparable evidence.
- **“An exception is permanent support.”** it expires and creates a migration/removal obligation.
- **“Break glass is an administrator account.”** emergency authority must be issued, bounded, alerted, reconciled, and revoked.
- **“Legacy cannot comply.”** brownfield state may require staged remediation, isolation, or retirement, not timeless exemption.
- **“Deleting a policy file retires the control.”** roles, webhooks, credentials, trust roots, rules, caches, evidence, exceptions, and dependencies remain.

## Worked Examples

### Example 1

A team applies `restricted` Pod Security Admission and declares its payment service secure. Review finds public ingress, an application-level horizontal authorization flaw, and a static database password. The claim is narrowed: Pod privilege controls pass, while domain authorization and credential lifecycle fail mandatory gates. Conclusion: one implementation proves only its named objective and scope.

### Example 2

A namespace has default-deny ingress and egress YAML, but its development cluster uses a network plugin without NetworkPolicy enforcement. A data-plane test still reaches arbitrary destinations. Inventory records implementation present/effect failed, blocks the claim, and prevents promotion. Conclusion: API-object presence is not operating effectiveness.

### Example 3

Nine controls pass and one production service account retains wildcard Secret access. With equal weights, $C=9/10=0.9$. The portfolio score looks strong, yet the wildcard permission fails a mandatory gate and triggers containment. Conclusion: aggregates prioritize but cannot compensate catastrophic failures.

### Example 4

A deployer cannot `get` Secrets but can create arbitrary Pods using any service account in the namespace. It creates a Pod that mounts a database Secret and prints it. RBAC analysis models indirect capabilities and restricts Pod/service-account use. Conclusion: least privilege must include privilege-escalation paths, not only direct verbs.

### Example 5

A signed image is admitted because the verifier trusts every key in a developer group. An attacker signs a locally built image with valid credentials. Policy changes to verify digest-bound provenance from the protected builder, expected source/revision/build type, and approved workflow. Conclusion: authentic signature is weaker than verified production expectations.

### Example 6

A new egress default blocks all traffic, including DNS and the workload-identity endpoint. Credential renewal fails and services expire simultaneously. The profile restores explicit DNS/identity flows, canaries expiry, tests failure, and limits cached credential lifetime. Conclusion: containment controls require dependency and recovery modeling.

### Example 7

A profiler needs `SYS_PTRACE` for seven days during a performance incident. The exception binds one workload digest and namespace, isolated nodes, no public ingress, narrow egress, enhanced audit, named approver, automatic expiry, and cleanup verification. Conclusion: narrow compensating control preserves the objective better than a fleet-wide privilege relaxation.

### Example 8

An auditor requests proof that all production images used approved builders during a quarter. The platform reconciles the production digest population, provenance subjects/builders/source revisions, admission decisions, policy version, exceptions, and daily drift results. Two unreachable clusters remain “unknown,” not omitted. Conclusion: evidence needs population, period, provenance, and exceptions.

### Example 9

A policy webhook times out during a control-plane incident and blocks the Deployment that would restore it. A predesigned recovery path uses independently stored, short-lived, dual-approved authority limited to the policy namespace; use pages responders and produces a reconciliation record. Conclusion: fail-closed controls need protected bootstrap and recovery.

### Example 10

A service is deleted, but its service account, cloud role, trust mapping, external secret, egress policy, admission exception, evidence exporter, and retained audit data remain. Retirement revokes authority, verifies no callers, removes control artifacts, applies retention/deletion, and records a tombstone. Conclusion: security and compliance resources have independent lifecycles.

## Cross-Program Connections

- **Security engineering:** assets, adversaries, trust, attack surfaces, control objectives, assurance, incident response, and residual risk provide the primary reasoning model.
- **Systems engineering:** boundaries, requirements allocation, interface contracts, verification evidence, hazards, common-cause failure, lifecycle, and disposal prevent isolated controls from overclaiming.
- **API engineering:** authentication context, authorization, rate/abuse limits, schemas, errors, compatibility, and deprecation carry security semantics across service boundaries.
- **Software engineering:** secure development, review, dependency management, testing, maintainability, and architecture determine risks the platform cannot infer.
- **Operating systems:** users, capabilities, namespaces, seccomp, mandatory access control, filesystems, processes, and kernels ground runtime isolation.
- **Distributed systems:** partial failure, stale identity/policy, revocation, clocks, caches, retries, consensus, and recovery shape enforcement behavior.
- **Networking:** routing, names, addresses, TLS, segmentation, proxies, NAT, DNS, and traffic policy distinguish reachability from identity.
- **Cryptography:** keys, signatures, certificates, hashes, encryption, trust roots, and rotation support mechanisms but do not decide authorization or governance.
- **Data engineering:** classification, lineage, copies, transformations, quality, retention, deletion, and evidence pipelines determine data/compliance truth.
- **Reliability engineering:** SLOs, blast radius, overload, degradation, observability, incidents, rollback, and disaster recovery constrain preventive controls.
- **Governance and law:** obligations, accountability, assessment scope, segregation, evidence retention, privacy purpose, and risk acceptance remain organizational decisions.
- **Economics and human factors:** friction, incentives, alert fatigue, security debt, review capacity, cognitive load, and usability determine whether defaults are adopted or bypassed.

## References

1. Kubernetes Authors, “Pod Security Standards,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/pod-security-standards/
2. Kubernetes Authors, “Pod Security Admission,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/pod-security-admission/
3. Kubernetes Authors, “Role Based Access Control Good Practices,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/rbac-good-practices/
4. Kubernetes Authors, “Network Policies,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/services-networking/network-policies/
5. Kubernetes Authors, “Good Practices for Kubernetes Secrets,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/secrets-good-practices/
6. Kubernetes Authors, “Admission Control in Kubernetes,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/
7. Kubernetes Authors, “Linux Kernel Security Constraints for Pods and Containers,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/
8. National Institute of Standards and Technology, “Secure Software Development Framework (SSDF) Version 1.1,” SP 800-218, February 2022. https://doi.org/10.6028/NIST.SP.800-218
9. National Institute of Standards and Technology, “Security and Privacy Controls for Information Systems and Organizations,” SP 800-53 Revision 5, September 2020, including published updates. https://doi.org/10.6028/NIST.SP.800-53r5
10. National Institute of Standards and Technology, “Zero Trust Architecture,” SP 800-207, August 2020. https://doi.org/10.6028/NIST.SP.800-207
11. SLSA Authors, “SLSA Specification,” version 1.2, retrieved 2026-09-02. https://slsa.dev/spec/v1.2/
12. SLSA Authors, “Verifying Artifacts,” version 1.2, retrieved 2026-09-02. https://slsa.dev/spec/v1.2/verifying-artifacts
13. SPIFFE Authors, “SPIFFE Concepts,” current documentation, retrieved 2026-09-02. https://spiffe.io/docs/latest/spiffe/concepts/
14. OWASP Foundation, “Application Security Verification Standard,” version 5.0.0, May 2025. https://owasp.org/www-project-application-security-verification-standard/
15. Cloud Native Computing Foundation, “Cloud Native Security Whitepaper,” version 2, November 2022. https://github.com/cncf/tag-security/blob/main/security-whitepaper/v2/cloud-native-security-whitepaper.md

## Exercises

### Exercise 1

Design security-default profiles for an internal reporting API, a public payment API processing restricted data, and a privileged node agent. State boundaries, threats, inherited controls, specialized controls, non-guarantees, ownership, and mandatory gates.

### Exercise 2

Given eight controls with equal weights and evidence qualities $[1,1,1,1,1,0.5,0,0]$, compute $C$. Then explain why the result cannot establish security or compliance and design a separate mandatory-gate report.

### Exercise 3

Create an admission rollout for blocking privileged containers and unverified artifacts across 400 brownfield workloads. Include inventory states, observe/warn/enforce cohorts, policy errors, exceptions, recovery, evidence, and retirement.

### Exercise 4

Specify a seven-day exception for a stateful migration tool that needs a normally forbidden host mount and external egress. Include threat, exact scope, compensating controls, approval, telemetry, expiry, incident action, and cleanup evidence.

### Exercise 5

Construct a quarterly evidence contract for “only approved workloads access production customer data.” Include population, identity/authorization, data/service controls, collection, freshness, integrity, exclusions/unknowns, exceptions, review, retention, and residual risk.

## Answers to the Exercises

### Answer 1

Use a shared baseline: owned workload identity, minimum RBAC, non-root/no-escalation runtime, declared storage/network, secret broker, immutable verified artifact, admission, telemetry redaction, patching, and expiring exceptions. The internal API adds private ingress and named analytics/data flows but receives no implicit network trust. The public payment API adds internet threat/abuse controls, restricted-data region/key/retention rules, stronger workload and operator authentication, narrow egress, dedicated data identities, enhanced audit, and mandatory domain-authorization/application tests. The node agent uses a privileged-infrastructure profile: dedicated isolated nodes, digest/source/build restrictions, exact host mounts/capabilities, no ordinary tenancy, minimal egress, stronger review, and recovery tests. Platform owns mechanisms/evidence; product owns data purpose/domain rules; security/compliance interpret objectives; infrastructure owns nodes/control planes; an accountable business/security owner accepts residual risk. Mandatory gates include unknown inventory, wildcard authority, unverified artifacts, restricted-data mismatch, public exposure without abuse controls, policy errors, and expired exceptions. No profile guarantees bug-free application code or lawful business use.

### Answer 2

$C=(1+1+1+1+1+0.5+0+0)/8=5.5/8=0.6875$, or 68.75%. This is a prioritization summary, not a probability or certification: weights are judgments, evidence qualities may be stale or incomplete, controls are dependent, applicability matters, and either zero may represent catastrophic exposure. Report mandatory gates independently with control ID, applicable population, state (`pass`, `fail`, `unknown`, `excepted`), affected assets, owner, evidence time/source, remediation/expiry, and risk decision. The score may accompany but never override a failed identity, privilege, public-exposure, restricted-data, artifact, or recovery gate.

### Answer 3

First reconcile all 400 workloads as conforming, nonconforming, unknown, exempt, or unreachable, including controllers and alternative deployment paths. Run versioned rules in observe mode and test both denials and policy-engine errors. Publish effective decisions, remediations, verified-artifact tooling, support, owners, and deadlines. Enforce immediately for new ordinary workloads, then canary low-risk existing cohorts by cluster/team while comparing application outcomes. Separate intended violation from timeout/error; page on evaluator failure and preserve a narrow independently protected recovery route. Exceptions bind workload/digest/control, compensating isolation, owner, evidence, and expiry. Evidence records population, request, decision, policy revision, runtime reconciliation, errors/bypasses, and exception. Progress high-risk public/privileged workloads under security review, quarantine unresolved exposure where appropriate, and finally remove warning rules, obsolete bundles, bypass roles, webhook credentials, and expired exceptions after full enforcement is reconciled.

### Answer 4

Bind the exception to the migration tool’s immutable digest, namespace, service account, named node pool, exact read-only host path where feasible, destination/protocol, and seven-day window. Threats include host data disclosure/write, container escape, credential theft, exfiltration, and persistence. Compensate with dedicated drained nodes, no unrelated tenants, dropped capabilities except those strictly needed, read-only root, restricted source/builder/provenance, short-lived workload credential, deny-all other egress, destination authentication, bounded data/time, enhanced file/network/process audit, and an on-call kill path. Name requester, platform/security approvers, risk owner, incident conditions, automatic expiry, alerts at issue/use/pre-expiry, and no automatic renewal. Cleanup proves Job completion, mount and node restoration, credential revocation, network/policy/role removal, exception closure, output integrity, and retention/deletion of logs/data.

### Answer 5

Define the production customer-data services/stores, all application/batch/analytics/admin/emergency subjects, environments, replicas/backups, and quarterly period. Reconcile that population from authoritative service, identity, deployment, and data inventories; mark missing/unreachable elements unknown. Evidence binds short-lived workload/human identity, effective authorization and changes, approved source/build/digest, service/data policy, network reachability tests, encryption/key controls, query/access audit, periodic access review, revoked leavers, denied attempts, break-glass events, and domain-authorization tests. Preserve collection query/code and revision, raw integrity-protected results, actor, timestamp, transformations, freshness and retention limits. List service accounts/controllers with indirect access, sampled items and sampling rationale, exclusions, policy errors, exceptions/expiry/compensation, incidents and remediation. Named control owners attest operation; an independent reviewer records scope and findings; the risk owner accepts stated residual risk. The claim remains bounded: approved technical access does not prove lawful purpose, correct business authorization, or absence of endpoint compromise.
