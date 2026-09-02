---
module_id: PLAT-075
program: Platform Engineering
level: 2
module_number: 75
title: Workload Identity
status: complete
last_verified: 2026-09-02
---

# Workload Identity

## One-Page Review

### Governing question

How should a platform give each running workload a verifiable, short-lived identity across clusters and clouds without distributing static secrets, trusting network location, confusing authentication with authorization, or losing lifecycle control?

### Essential definitions

- A **workload** is software executing for a defined purpose: a process, pod, virtual machine, function, batch job, controller, or delivery job.
- A **workload principal** is the stable logical identity under which equivalent workload instances act; it is not an IP address, hostname, pod name, node, or credential file.
- **attestation** is evidence-based identification of a node or executing workload from trusted runtime properties.
- A **selector** is an attested property, such as cluster, namespace, service account, image digest, process UID, or node identity, used in an identity registration rule.
- A **credential** is a bounded proof of identity. Examples include an X.509 certificate/private key, JWT, or temporary cloud credential.
- A **trust domain** is an administrative root of identity authority. A SPIFFE ID has the form `spiffe://trust-domain/workload-path`.
- An **SVID** is a SPIFFE Verifiable Identity Document carrying one SPIFFE ID in X.509 or JWT form.
- A **projected service-account token** is a Kubernetes-issued, audience- and time-bounded JWT mounted into a pod and rotated by the kubelet.
- **workload identity federation** exchanges or presents an external workload proof to obtain access under a target trust system without a long-lived target-cloud key.
- A **sender-constrained credential** can be used only with proof of possession of a particular key; a bearer credential can be replayed by whoever obtains it.
- The **credential plane** attests and issues identity proofs; the **policy plane** decides permissions; the **data plane** authenticates and enforces on each request.
- **delegation** means a workload acts for another principal under a constrained, auditable chain rather than replacing the original actor.

### Central model, mechanism, or theorem

Let a workload principal be $w=(d,id)$ for trust domain $d$ and workload identifier $id$. A presented credential is

$$
C=(iss,sub,aud,t_i,t_e,k,a),
$$

where issuer and subject identify the asserted principal, audience bounds the recipient, $t_i,t_e$ bound time, $k$ identifies or proves possession of key material, and $a$ records attestation-derived attributes. The recipient accepts only if signature/trust, exact issuer, subject mapping, audience, validity, key binding where required, and current attestation/registration policy all hold. It then separately evaluates $Permit(w,actor,action,resource,context)$. Possessing a valid credential authenticates a principal; it does not grant every action.

### Critical invariants

- Workload identity is derived from stable, authoritative runtime properties; network address, DNS, pod name, or a copied secret cannot establish it alone.
- Every principal is scoped by a trust domain or issuer. Identical namespace/service-account names in different clusters cannot silently collide.
- Bootstrap evidence is verified before identity issuance; an unauthenticated request to the local agent is bound to the calling process by the agent.
- Credentials are short-lived, automatically rotated, audience-bound where applicable, and delivered only to the intended workload boundary.
- Bearer tokens are never logged, placed in URLs, persisted in images, or shared through broad environment/configuration surfaces.
- Identity issuance, credential validation, and resource authorization are separate decisions with separate policy and telemetry.
- Workload-to-cloud mappings use immutable, scoped attributes and least-privilege target roles; a whole identity pool or namespace is not granted by convenience.
- Human actor, calling workload, delegated workload, tenant, and target role remain distinguishable in on-behalf-of flows and audit.
- Deletion, rescheduling, image or service-account change, compromise, and registration removal converge to denial within a measured maximum exposure window.
- Issuer, CA, trust-bundle, signing-key, agent, broker, and cloud-role rotation preserve controlled overlap without indefinite old trust.
- Credential-plane outage has a bounded cached-credential policy; it cannot turn expired identity or stale authorization into permanent access.
- Node agents and admission/identity brokers are privileged security components with isolated sockets, least privilege, monitoring, and tested compromise response.

### Common failures

Static cloud keys in Secrets; one identity per node; IP allowlists treated as identity; default Kubernetes service account everywhere; non-expiring legacy tokens; audience not checked; trusting `namespace/service-account` without cluster/issuer scope; mutable names used where UIDs are needed; wildcard federation mappings; granting an entire pool; node metadata credentials reachable by pods; identity agent socket mounted broadly; selectors controlled by the workload; bearer tokens in logs; certificate issued but peer name not checked; service mesh authentication mistaken for authorization; sidecar acting as a confused deputy; human identity erased during delegation; CI token trusted for any repository/ref/environment; credential TTL extended to hide outages; old trust bundles retained forever; registration deleted without checking cached credentials; and restoring a retired issuer from backup.

### Compact example

Pod `payments/reconciler` in production cluster UID `c-9` runs under service-account UID `sa-41`. A node agent authenticates the node, binds the local socket caller to the pod, verifies selectors including cluster UID, namespace UID, service-account UID, and approved image digest, then supplies an automatically rotated X.509-SVID for `spiffe://prod.example/payments/reconciler`. The reconciler uses mTLS to authenticate to the ledger service, which validates the trust bundle and exact SPIFFE ID before independently authorizing `ledger:append` for tenant `tn-7`. For a cloud API, the pod presents a one-hour projected Kubernetes token whose issuer, subject, audience, object binding, and time are validated by a federation service; it receives a shorter temporary cloud credential for one role. No static cloud key enters the cluster.

### Connections

This module follows human [identity federation](074-identity-federation.md) and applies scoped trust to machines. It supplies principals to [policy decision and enforcement points](066-policy-decision-and-enforcement-points.md), tenant and isolation boundaries in [PLAT-071](071-tenant-models.md) and [PLAT-072](072-namespace-account-and-cluster-isolation.md), and the policy, admission, supply-chain, and audit systems in PLAT-076–079. API authentication, service-to-service authorization, secret delivery, zero trust, PKI, schedulers, and distributed revocation all depend on the same distinctions.

## Governing Question

How can a platform establish which software is calling, at the granularity required by policy, when instances are ephemeral, addresses are reused, and execution spans Kubernetes, virtual machines, serverless platforms, delivery systems, and several clouds?

The answer is not “put a client secret in every deployment.” A secret proves possession, not current workload placement, configuration, ownership, or lifecycle. Copies survive rescheduling and deletion. Rotation becomes a distribution problem, and compromise attribution is weak.

The platform needs an identity control loop: register stable principals and trustworthy selectors; attest nodes and running workloads; issue narrowly usable, short-lived credentials; authenticate peers and federation endpoints; authorize current actions separately; observe use; rotate trust; and reconcile deletion or compromise to denial.

## Why This Matters

Service-to-service calls often outnumber human interactions. A single overbroad machine credential can read secrets, publish artifacts, mutate infrastructure, or cross tenants continuously without an interactive warning.

Dynamic scheduling invalidates network-era assumptions. An IP is an ephemeral route, a node hosts many workloads, and a service name may select many revisions. Network policy remains valuable containment, but it cannot prove which process is on the other end.

Static credentials age badly. They are copied into manifests, CI variables, images, backup systems, developer machines, and logs. Operators lengthen their lifetime because rotation is disruptive. The platform then cannot determine whether an old credential belongs to a current instance.

Attested, short-lived identity changes the operational problem. The platform protects a smaller number of root and bootstrap authorities, automatically issues leaf credentials close to workloads, and bounds leaked-credential value by audience, proof of possession, authorization, and lifetime. This does not eliminate compromise: a hostile process inside the workload boundary may use current credentials. It makes the boundary explicit and recoverable.

## Prerequisites and Retrieval

Retrieve principals and credentials; authentication versus authorization; least privilege; public-key infrastructure; certificate chains, revocation, and mutual TLS; JWT/JWS/JWK and OIDC; OAuth audiences, scopes, and token exchange; Kubernetes pods, namespaces, service accounts, UIDs, projected volumes, TokenRequest, admission, nodes, and kubelet; cloud IAM roles and temporary credentials; schedulers and service meshes; secrets management; software supply-chain identity; network policy; clocks; caches; audit; incident response; and disaster recovery.

Distinguish human from workload identity; logical workload from instance; node from workload; name from immutable UID; issuer from trust domain; identity from credential; bearer from proof-of-possession credential; attestation from authorization; workload identity from device identity; authentication from service discovery; direct federation from service-account impersonation; calling service from human actor; rotation from revocation; expiration from deletion; certificate trust from policy permission; and credential availability from indefinite fail-open behavior.

## Learning Objectives

After completing this module, you should be able to:

1. define workload principals and trust domains at useful, collision-resistant granularity;
2. distinguish registration, node attestation, workload attestation, issuance, authentication, and authorization;
3. design SPIFFE/SPIRE and Kubernetes projected-token flows without a distributed static secret;
4. map Kubernetes, CI/CD, VM, batch, and serverless identities into least-privilege cloud roles;
5. choose X.509/mTLS, JWT, token exchange, managed identity, or brokered federation by protocol and threat model;
6. constrain credentials by audience, time, key possession, issuer, subject, and runtime context;
7. preserve caller, actor, tenant, and delegation chains through proxies and services;
8. operate issuer, CA, trust-bundle, agent, broker, credential, and authorization lifecycle safely;
9. measure credential exposure and revocation convergence under compromise and outage; and
10. migrate from static credentials and test adversarial identity cases across clusters and clouds.

## Core Exposition

### Define a workload principal before selecting a mechanism

Start with the authorization subject the organization needs, not with a vendor credential format. “Production payment reconciler” may be one principal across replicas, while canary and stable revisions may need distinct principals if policy or incident isolation differs.

Identity that is too coarse creates blast radius. A node identity makes every pod on the node equivalent. A namespace identity makes unrelated services peers. Identity that is too fine creates unmanageable policy: random pod UID or process ID should usually be attestation evidence, not the enduring principal.

Record owner, purpose, environment, tenant scope, executable/deployment source, allowed runtimes, selectors, credential profiles, audiences, permissions, dependencies, expiry/review, incident contacts, and retirement rule. A principal registry is security-critical configuration.

Separate the stable logical principal from instances. Replicas may share a principal only when they are intended to share permissions and trust. Every instance still has issuance and use telemetry so compromise can be localized.

### Scope identity by an explicit trust domain

A subject string is meaningful only under an issuer or trust domain. `system:serviceaccount:payments:reconciler` from cluster A must not automatically equal the same string from cluster B.

Use issuer URL, cluster UID, workload-pool/provider identity, or SPIFFE trust domain in the mapping. Include immutable UIDs where name deletion and recreation would otherwise inherit trust. Decide deliberately whether a rebuilt cluster is the same authority or a new one.

Trust domains are administrative and cryptographic boundaries. Separate production from weaker environments. Separate organizations or regions when control, incident, or regulatory practices require independent roots. Federation between domains is an explicit exchange of trust bundles and policy, not a reason to collapse names.

Avoid encoding every deployment fact into the principal path. Put stable ownership and function in identity; use attested attributes and policy for revision, node pool, image, or geography when those facts change at different rates.

### Understand registration and attestation

Registration maps a desired principal to a conjunction of selectors. In SPIRE, a registration entry maps a SPIFFE ID to properties the workload must possess. The node is attested first; an agent then identifies a local caller using operating-system and orchestrator evidence.

The workload should not simply self-report trusted selectors. A local agent can bind a Unix-domain-socket caller to a process, ask the kubelet/runtime for pod metadata, and compare resulting selectors to authorized entries. The security argument depends on kernel/runtime isolation, node attestation, agent integrity, registration authority, and the fidelity of each selector source.

Use several independent or complementary selectors for high-risk identities: cluster and namespace UID, service-account UID, workload controller, image digest/signature, node pool, process UID, or trusted deployment metadata. Labels controlled by the workload or a broad namespace editor are weak unless governance restricts who may mutate them.

Attestation proves current properties at issuance time under stated assumptions. It does not prove application code is benign, that a node remains uncompromised forever, or that every request is authorized.

### Bootstrap without distributing secret zero

Every identity system has roots: CA/signing keys, cloud control-plane trust, node enrollment, hardware identity, or operator-approved registration. “Secretless” normally means leaf workloads do not carry long-lived shared secrets, not that no root key exists.

SPIFFE Workload API can be reached locally without the workload presenting a bootstrap token because the agent identifies the calling process out of band. Cloud instance metadata can similarly deliver attached-role credentials, but only if network and runtime isolation prevent neighboring workloads from reaching them.

Kubernetes federation uses a control-plane-issued service-account token as bootstrap proof. The pod obtains it through a projected volume; the receiving service validates the cluster issuer and token contract or exchanges it for target credentials.

Protect bootstrap interfaces. Restrict agent sockets to intended pods/processes, block pod access to node metadata where not needed, secure kubelet/runtime APIs, isolate identity agents, authorize registration changes, and alert on unusual issuance.

### Use short-lived, automatically rotated credentials

Short lifetime reduces the period during which a stolen credential remains independently useful. Automation is essential: if applications require manual restart or redeployment, operators will choose unsafe durations.

The issuer should begin renewal before expiry with jitter and sufficient overlap for connection draining. Consumers must handle new credentials and trust bundles without restart. Validate both planned rotation and emergency cutover.

Lifetime is not revocation. A bearer JWT may remain valid until expiration even after the issuing pod is deleted if a verifier only checks OIDC signature and claims. Kubernetes TokenReview can consult object binding and invalidate a token when the bound object is deleted; offline OIDC validation trades that currency for availability.

Choose TTL from compromise risk, issuer capacity, renewal reliability, clock uncertainty, connection lifetime, and maximum acceptable exposure. Do not extend it merely to conceal an unreliable credential plane; fix availability and define bounded degraded operation.

### Use Kubernetes service accounts correctly

A Kubernetes ServiceAccount gives processes in a pod an identity within a cluster. Give each security-distinct workload a dedicated account and set `automountServiceAccountToken: false` when no Kubernetes or federated token is required.

Prefer TokenRequest/projected tokens. They carry audience and expiration, are bound to a pod or another object, and are refreshed by the kubelet. A relying service must require its own explicit audience and verify issuer, signature/key, time, subject, object binding where available, and scoped mapping.

Avoid manually created legacy service-account-token Secrets: they do not expire or rotate automatically. Avoid the `default` service account for a collection of applications. RBAC permissions to the Kubernetes API and cloud permissions mapped through federation are separate grants.

Treat the cluster OIDC issuer and signing keys as identity infrastructure. Rotate keys with overlap, restrict who can create service accounts/pods and bind identities, monitor TokenRequest and pod admission, and decide how cluster deletion/recreation affects trust.

### Establish SPIFFE identity for service-to-service authentication

SPIFFE IDs are URIs under a trust domain. An SVID is a cryptographically verifiable identity document containing one SPIFFE ID. X.509-SVIDs support mutual TLS and proof of private-key possession; JWT-SVIDs support token-shaped integrations and require an explicit audience.

The Workload API supplies SVIDs and trust bundles and streams rotation. It can return several authorized identities, so applications or proxies need deterministic selection. A workload should not choose an arbitrary more-privileged identity simply because several are available.

Prefer X.509-SVIDs for direct mutual authentication where the protocol supports mTLS. Bearer JWTs are easier to replay after theft. Certificate identity still needs peer verification: completing TLS without matching the peer SPIFFE ID and applying authorization is insufficient.

SPIFFE federation shares trust bundles between domains. Trusting a foreign root authenticates its subjects; local policy must still constrain which foreign SPIFFE IDs may call which resources. Bundle refresh, domain retirement, and collision-free paths are operational requirements.

### Federate workload identity into cloud IAM

Cloud federation replaces stored cloud keys with temporary credentials based on a trusted external proof. A Kubernetes token, SPIFFE credential, VM platform identity, or CI OIDC token is validated by a cloud security-token service or broker and mapped to a target principal/role.

AWS EKS supports IAM roles for service accounts and EKS Pod Identity. IRSA uses a cluster OIDC issuer and service-account trust relationship; Pod Identity uses EKS-managed associations and an agent. They are different operational mechanisms, so inventory which one grants each pod and keep node metadata credentials inaccessible.

Google Cloud Workload Identity Federation can authorize an external identity directly or let it impersonate a service account. Workload Identity Federation for GKE maps Kubernetes identities into Google IAM. Attribute mappings and conditions must use immutable, authoritative fields and distinguish shared multi-tenant issuers.

Microsoft Entra Workload ID establishes a federated credential between Kubernetes issuer/subject/audience and an application or managed identity. Admission/runtime components project a suitable token and client libraries exchange it. Across providers, the invariant is the same: exact issuer, exact subject pattern, target audience, short lifetime, narrow role, and auditable mapping.

### Prevent subject collisions and wildcard trust

A mapping like “any subject in this pool may impersonate production deployer” converts authentication into broad privilege. Grant specific subjects or tightly governed attributes, and add tenant/organization conditions when an issuer is shared by many organizations.

Use immutable repository/organization IDs for CI where available, not only reusable names. For Kubernetes, bind issuer plus namespace/service-account and incorporate cluster/namespace/service-account UID when the federation mechanism exposes them or maintain an equally strong cluster-specific provider boundary.

Treat mapping configuration as code with review, tests, ownership, drift detection, and unused-binding cleanup. A federation provider is an authorization ingress even when the final resource policy lives elsewhere.

Detect many-to-one mappings. Sharing a target role may be intentional, but it reduces attribution and couples permissions. Use application-specific target identities unless common responsibility justifies aggregation.

### Keep identity distinct from authorization

The credential validator answers “which principal presented acceptable proof for this recipient now?” The policy system answers “may that principal, possibly acting for another principal, perform this action on this resource in this tenant under current context?”

Do not encode all entitlements into identity names or certificates. Stable identity outlives frequently changing permissions. Resource servers retrieve or evaluate current policy, enforce audience and tenant boundaries, and record policy version/decision.

Service meshes can authenticate connections and convey peer identity, but authorization policy may reside in proxy, application, gateway, or a combination. Establish which component is authoritative and prevent bypass paths around it.

Network policy remains defense in depth. Identity-aware authorization does not permit arbitrary connectivity, and network reachability does not grant identity.

### Preserve delegation and actor chains

When portal service calls deployer for user Alice, choosing either Alice or portal as the only identity loses necessary context. The deployer should authenticate the calling workload, validate constrained delegation, and retain the human actor and tenant/action context.

OAuth token exchange defines subject and actor token relationships for some systems. Other systems use signed internal grants or capability tokens. In all cases constrain audience, action/scope, resource, tenant, lifetime, delegation depth, and replay; never let a downstream service freely mint broader authority.

A proxy or sidecar that holds credentials for many applications can become a confused deputy. Bind local callers to identities and policies, separate sockets/listeners, and prevent one container from asking the proxy to act as another.

Audit each hop with trace/request correlation, authenticated caller, original actor where relevant, target audience, decision, and resource—without recording bearer credentials.

### Handle multi-tenancy and cross-domain calls

Decide whether workload identity is tenant-specific. A shared control-plane service may have one platform principal but must carry and authorize an explicit tenant context. A tenant-dedicated data-plane workload may use distinct identity to reduce cross-tenant blast radius.

Do not infer tenant solely from namespace text or request hostname. Resolve tenant from trusted workload mapping and request/resource context, then verify consistency at the enforcement point.

Across clusters/clouds, use federation rather than copying roots or static keys. Establish directional trust: domain A may accept only a small subject set from B, while B need not trust A. Inventory bundle/provider dependencies and owners.

For mergers, partners, or customer workloads, specify identity namespace, assurance/attestation expectations, incident notification, key rotation, availability, audit, and exit. External authentication never delegates local resource policy implicitly.

### Cover CI/CD, batch, serverless, and ephemeral execution

Delivery jobs are workloads. Use the CI provider's OIDC token or runner attestation to request short-lived deployment credentials. Bind trust to immutable organization/repository, workflow/ref/environment, protected approval context, and expected audience. Pull requests from forks must not inherit release roles.

Self-hosted runners expand the boundary: a persistent compromised runner may obtain credentials for later jobs. Prefer isolated ephemeral runners for privileged work, prevent untrusted jobs from sharing them, and bind environment approvals and artifact provenance.

Batch jobs need identity for their execution window and cleanup when the job ends. Serverless functions use platform-provided identity and must not share an overbroad account across unrelated functions. CronJobs and controllers require stable logical principals even though pods change.

Identity for a build does not prove artifact integrity. Preserve build/workflow identity in provenance, verify artifacts at admission, and give runtime a separately attested identity.

### Secure the identity agents and brokers

Node agents often read runtime metadata, access local sockets, and cache many workload credentials. Compromise can impersonate workloads on that node or wider, depending on authorization and key architecture.

Run agents with the minimum host access required; protect their sockets and files; isolate control traffic; validate node attestation; rotate node credentials; constrain which registrations each node may receive; and monitor issuance by node, selector, and principal.

Federation brokers and security-token services concentrate trust. Separate administration, use hardware-backed or managed keys where appropriate, require dual control for root/provider changes, cap token exchange, rate-limit, and test key/provider compromise.

Do not assume sidecars or ambient mesh components are invisible implementation details. Document which component owns keys, authenticates local workload, terminates mTLS, supplies peer metadata, and enforces policy.

### Design lifecycle, revocation, and reconciliation

Lifecycle begins before first issuance. Registration should have an owner, approval, environment, source deployment, permitted selectors, role bindings, review date, and removal trigger.

On rollout, new and old revisions may overlap. Decide whether they share identity and permission. On rollback, ensure a vulnerable retired revision cannot regain credentials merely because an old registration remains.

On service deletion, remove admission/deployment, identity registration, cloud federation mapping, role bindings, certificates/tokens where actively revocable, trust-bundle relationships, dashboards, and exceptions. Periodic reconciliation discovers orphan principals and unused mappings.

On compromise, contain workload and node, revoke or remove registration/provider binding, rotate relevant issuer/key if necessary, expire sessions/connections, deny at policy points, hunt token use, and redeploy from trusted artifacts. Maximum residual access is governed by credential lifetime plus detection and propagation assumptions.

### Operate outage and recovery boundaries

Identity systems are runtime dependencies. If an agent cannot renew, workloads eventually lose credentials. If a verifier cannot refresh keys/bundles, new-key credentials may fail; accepting any unknown key is not recovery.

Define renewal SLOs, issuer capacity, cached credential and trust-bundle validity, clock monitoring, backoff/jitter, alert thresholds, and behavior before expiry. Maintain safe overlap during planned rotation.

Risk-tier degraded behavior: existing authenticated connections may drain; low-risk calls may continue only while valid credentials and cached policy permit; sensitive operations require fresh identity/policy and fail closed. Expired credentials never become valid because control plane is unavailable.

Backups must not restore retired roots, providers, mappings, or registrations. Recovery procedures reconcile restored configuration against a current revocation/retirement ledger and rotate exposed keys.

### Observe without leaking credentials

Record issuance and exchange decisions: principal, issuer/trust domain, attested selector summary, instance/node, credential kind, audience, TTL, mapping/policy revision, result, and reason. Record use at the resource server with authenticated caller, actor/delegation, tenant, resource, and policy outcome.

Never record raw JWTs, private keys, Authorization headers, projected-token contents, or full certificates when fingerprints/serials and redacted claims suffice. Scrub traces, crash dumps, support bundles, and proxy access logs.

Metrics include issuance/renewal success and latency, credentials near expiry, unknown issuer/key/audience, attestation rejection, orphan registration, wildcard binding, unused principal, abnormal exchange volume, unexpected node/region, and disable-to-denial latency.

Audit is useful only when identity is distinguishable. A single target cloud role shared by hundreds of workloads may make provider logs ambiguous; preserve source principal/session tags or broker records and correlation identifiers.

### Migrate from static secrets deliberately

Inventory every credential copy and consumer: manifests, secret stores, CI, images, local files, backups, scripts, vendor systems, and emergency procedures. Classify owner, permissions, use, rotation, and last-seen activity.

Introduce workload identity alongside the old path for a cohort. Instrument which path succeeds, validate exact permissions and failure behavior, and ensure SDK credential precedence does not silently keep using node or static credentials.

Reduce target role permissions, move traffic, disable old credential, observe, then revoke/delete all copies and scan for residue. Rotation of the old key is not complete migration if another valid copy or fallback remains.

Retire federation providers and trust roots with the same discipline: remove consumers and bindings, wait through maximum credential lifetime, remove trust, retain audit/tombstones, and prove restore cannot resurrect the path.

## Definitions and Notation

Let trust domains be $D$, logical workload identifiers be $W$, credential issuers be $I$, audiences be $A$, and resources be $R$. A workload principal is

$$
w=(d,id),\qquad d\in D,\ id\in W.
$$

For Kubernetes, define an attested source tuple

$$
q=(issuer,clusterUID,namespaceUID,serviceAccountUID,podUID,imageDigest).
$$

Names may be retained for operations, but security mapping $M(q)=w$ uses the issuer/provider boundary and immutable fields required by policy. $M$ is partial: unknown, ambiguous, stale, or conflicting evidence produces no principal.

A credential is

$$
C=(iss,sub,aud,t_i,t_e,k,a,j),
$$

where $k$ is a key identifier or confirmation claim, $a$ is attestation/context, and $j$ is a unique credential/token identifier when available. For receiver $r$ at time $t$,

$$
Valid_r(C,t)=Trust(iss)\land Sig(C)\land Map(iss,sub)=w\land r\in aud
\land t_i-\delta\le t<t_e+\delta\land KeyBound(C)\land Current(w,a),
$$

with bounded clock tolerance $\delta$. `KeyBound` is true by construction for an mTLS certificate proven during the handshake, an explicit sender constraint, or a bearer profile that knowingly lacks that protection. The distinction remains in policy.

Authorization is independent:

$$
Permit(w,h,a_c,r_c,x,\pi),
$$

where $h$ is a human or upstream actor if delegated, $a_c$ is concrete action, $r_c$ is concrete resource, $x$ is tenant/request context, and $\pi$ is current policy revision.

If compromise occurs at $t_c$, detection at $t_d$, and denial reaches every enforcement surface $s$ at $t_s$, a conservative exposure bound is

$$
E\le \max_s\left(\min(t_e,t_s)-t_c\right),
$$

under assumptions about credential theft time, verifier behavior, cached authorization, connection lifetime, and clock. Short TTL alone does not establish the bound unless those assumptions are tested.

## Mechanisms, Invariants, or Proof Structure

### Workload identity control loop

1. Define a stable workload principal, owner, environment/trust domain, tenant boundary, credential profiles, and allowed audiences.
2. Register the principal against authoritative, preferably immutable, node and workload selectors.
3. Attest the node or execution substrate before it may obtain registrations or issue local credentials.
4. Bind the local credential request to the calling process/pod/function/job and derive selectors from trusted runtime sources.
5. Match all required selectors to exactly one authorized registration; reject ambiguity or stale evidence.
6. Issue a short-lived X.509/JWT/projected/platform credential or exchange proof for a narrowly scoped target credential.
7. Deliver keys/tokens only through the intended workload boundary and rotate automatically before expiry.
8. Receiver validates exact issuer/trust domain, signature/chain, subject, audience/peer identity, time, key possession/profile, and current mapping.
9. Enforcement point separately authorizes caller, actor/delegation, tenant, action, and resource under current policy.
10. Telemetry records issuance, exchange, authentication, and authorization decisions without credential material.
11. Reconciliation removes orphan registrations, provider mappings, roles, and expired trust; compromise/deletion converges to denial.
12. Rotation, outage, migration, retirement, and restore exercises verify bounded behavior and prevent old trust resurrection.

### Principal invariant

Every accepted workload subject resolves under its exact issuer/trust domain to one current logical principal. Names or attributes that can be recreated cannot silently transfer the old principal.

### Issuance invariant

The issuer releases a credential only after authorized registration matches attested execution evidence. The workload cannot manufacture the evidence merely by choosing environment variables, labels, token claims, or a socket path.

### Credential invariant

Every credential is usable only for its declared profile, intended audience or peer trust, and bounded lifetime; proof-of-possession is required where the protocol supports it and replay risk demands it.

### Authorization invariant

Successful credential validation establishes the caller identity and context only. The request proceeds only after current resource and tenant authorization, including delegation constraints.

### Lifecycle invariant

Removing a workload, registration, mapping, or role converges to denial across issuance, token exchange, active credentials, cached decisions, long-lived connections, and every resource server within a stated and measured bound.

### Proof sketch: network location cannot establish workload identity

Suppose policy treats source IP `10.4.8.12` as the payment reconciler. At time $t_1$ a legitimate reconciler pod uses that address. It terminates; the scheduler assigns the same address to an unrelated or compromised pod at $t_2$. The observed source IP is identical while the executing workload, service account, image, owner, and authorization should differ.

Therefore IP equality cannot prove logical workload equality in a system that reuses addresses. Adding an IP allowlist can constrain routes but does not repair the missing identity proof. A valid design binds a credential to attested workload properties and authenticates possession; it then applies authorization. The conclusion is limited to identity: network controls remain useful defense in depth.

### Executable credential audit

This synthetic audit classifies nine credential observations by exact issuer, audience, subject mapping, expiration, and attestation freshness. It reproduces predicate ordering only; it does not parse or cryptographically verify production credentials.

<!-- bijux-verify: {"id":"workload-credential-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=4\nissuer=1\naudience=1\nsubject=1\nexpired=1\nattestation=1\n"}} -->
```python
credentials = [
    ("cluster-prod", "ledger", "payments/reconciler", True, True),
    ("cluster-prod", "ledger", "payments/reconciler", True, True),
    ("cluster-prod", "ledger", "payments/reconciler", True, True),
    ("cluster-prod", "ledger", "payments/reconciler", True, True),
    ("cluster-lab", "ledger", "payments/reconciler", True, True),
    ("cluster-prod", "secrets", "payments/reconciler", True, True),
    ("cluster-prod", "ledger", "unknown/default", True, True),
    ("cluster-prod", "ledger", "payments/reconciler", False, True),
    ("cluster-prod", "ledger", "payments/reconciler", True, False),
]

counts = {name: 0 for name in ("accepted", "issuer", "audience", "subject", "expired", "attestation")}
for issuer, audience, subject, unexpired, fresh_attestation in credentials:
    if issuer != "cluster-prod":
        counts["issuer"] += 1
    elif audience != "ledger":
        counts["audience"] += 1
    elif subject != "payments/reconciler":
        counts["subject"] += 1
    elif not unexpired:
        counts["expired"] += 1
    elif not fresh_attestation:
        counts["attestation"] += 1
    else:
        counts["accepted"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Test registrations and mappings with valid, missing, conflicting, mutable, cross-cluster, cross-tenant, deleted-and-recreated, and spoofed selectors. Prove that one observation cannot match several principals.

Exercise token/certificate validation with wrong issuer, subject, trust domain, audience, recipient, key, chain, algorithm, time, object binding, and sender. Test replay from a different pod/node and stolen bearer use.

Compromise node, agent socket, sidecar, CI runner, federation broker, signing key, and workload process independently. Observe blast radius, containment, and evidence.

Inject issuer, DNS, clock, kubelet, JWKS, trust-bundle, agent, token exchange, cloud IAM, and policy outages. Test renewal storms, rotation overlap, cached-key limits, expired credentials, long-lived connections, deletion, restore, and retirement.

## Alternatives and Trade-Offs

- **Static secret versus federated/attested identity.** Static secrets work with legacy systems but require distribution and independent rotation; attested identity removes leaf secret handling at control-plane complexity cost.
- **Node identity versus workload identity.** Node identity is simpler and may bootstrap agents; workload identity limits co-tenant blast radius and supports fine-grained policy.
- **Dedicated versus shared principal.** Dedicated principals improve least privilege and attribution; justified sharing reduces policy count but couples compromise and lifecycle.
- **Names versus immutable UIDs.** Names are readable and stable across some deployments; UIDs prevent delete/recreate inheritance. Store both and define continuity deliberately.
- **SPIFFE versus platform-specific identity.** SPIFFE supplies portable service identity and mTLS/JWT conventions; managed cloud identity integrates deeply with provider IAM. Hybrid designs can exchange between them.
- **X.509-SVID versus JWT-SVID.** X.509 supports mutual proof and connection authentication; JWT fits HTTP/token systems but bearer form increases replay risk and requires strict audience.
- **Direct mTLS versus proxy/mesh termination.** Direct integration preserves application control; proxies simplify adoption and rotation but become trusted deputies and enforcement points.
- **Online TokenReview versus offline OIDC verification.** TokenReview observes bound-object deletion; offline verification reduces control-plane dependency but accepts until expiry.
- **Direct cloud principal versus service-account/role impersonation.** Direct access preserves source identity; impersonation improves compatibility and central role management but can reduce attribution or add a hop.
- **Direct federation versus broker.** Direct relationships reduce concentrated trust; brokers normalize providers and audit but amplify compromise/outage blast radius.
- **One trust domain versus several.** One domain eases connectivity; separate domains isolate administration, environments, and incidents at federation cost.
- **Bearer versus sender-constrained token.** Bearer tokens are widely compatible; certificate or key binding resists replay but requires end-to-end protocol support.
- **Short versus longer TTL.** Short TTL bounds theft but increases issuer and outage sensitivity; longer TTL improves tolerance while enlarging residual access.
- **Identity in application versus sidecar/ambient layer.** Application integration can reason about peers directly; infrastructure mediation standardizes controls but requires secure local binding and metadata propagation.
- **Policy at mesh versus application.** Mesh policy handles uniform transport identity; application policy understands domain resource semantics. Layer them without ambiguous ownership.
- **Identity per revision versus per service.** Revision identity enables canary isolation and rapid denial; service identity keeps policies stable. Split only where permissions or trust differ.
- **Tenant-neutral versus tenant-specific identity.** Neutral control-plane identity reduces cardinality; tenant-specific identity narrows cross-tenant blast radius. Both still need explicit tenant authorization.
- **Fail closed versus bounded degraded mode.** Immediate denial protects freshness but may cause outage; valid cached credentials can bridge short failures if expiration and authorization remain enforced.
- **Big-bang versus cohort migration.** Big-bang removes static keys quickly but risks widespread failure; cohorts reveal SDK precedence, role gaps, and hidden consumers while dual paths last longer.

## Failure Modes and Misconceptions

- “An IP address is service identity” ignores reuse, proxies, NAT, and compromise.
- “DNS proves the calling process” confuses discovery with authentication.
- “A secret proves the current workload” proves possession only.
- “Secretless means there are no root keys” hides bootstrap trust.
- “The node role is good enough for all pods” gives co-tenants a shared blast radius.
- “Every pod needs the default service-account token” increases unnecessary exposure.
- “A Kubernetes service-account name is globally unique” ignores issuer, cluster, namespace, and recreation.
- “A projected token is safe for every API” ignores audience and verifier contract.
- “Offline JWT validation revokes on pod deletion” generally accepts until expiry.
- “A valid certificate authorizes the request” establishes identity, not resource permission.
- “mTLS is complete when the handshake succeeds” omits peer identity and policy checks.
- “Mesh identity eliminates network policy” discards containment.
- “JWT-SVID and X.509-SVID have identical replay properties” ignores bearer versus key possession.
- “The workload should tell the agent its selectors” makes attestation self-asserted.
- “Any pod in a trusted namespace can use the role” overtrusts namespace editors and unrelated services.
- “Granting all members of a federation pool is convenient” turns future identities into privilege.
- “Repository name is a permanent CI identity” ignores rename, transfer, and name reuse.
- “A broker removes upstream trust complexity” concentrates it.
- “A sidecar cannot be a confused deputy” ignores local caller binding.
- “Service identity can replace the human actor” destroys delegation accountability.
- “One shared cloud role still gives exact attribution” may collapse provider audit identity.
- “Rotation revokes stolen tokens immediately” confuses new issuance with old validity.
- “Long TTL solves issuer availability” enlarges compromise exposure.
- “Expired credentials may be accepted during outage” creates indefinite fail-open risk.
- “Deleting a deployment retires its identity” leaves registrations, mappings, roles, and trust.
- “Backup restore should reproduce all identity configuration” can resurrect retired trust.

## Worked Examples

### Example 1

Two clusters have namespace `payments` and service account `reconciler`. Production issuer `https://k8s.prod.example` maps to `spiffe://prod.example/payments/reconciler`; laboratory issuer is not trusted by the ledger federation provider.

Matching text does not collide because issuer/trust domain is part of identity. Recreating the production service account with a new UID requires reconciled registration before issuance.

### Example 2

A pod receives a projected token for audience `ledger-token-exchange` with a one-hour maximum. It presents the token to that exchange, which validates issuer, signature, time, subject, pod binding, and audience, then returns a ten-minute cloud credential for one append-only role.

The secrets service rejects the projected token and exchanged credential because neither targets its audience or policy.

### Example 3

A SPIRE agent binds a Workload API socket request to a process, retrieves Kubernetes metadata, and matches cluster, namespace/service-account UID, and image digest to one registration. It streams an X.509-SVID and trust bundle to the workload.

When the image changes without an approved registration, issuance fails. An environment variable claiming the old digest is irrelevant.

### Example 4

Ledger and reconciler establish mTLS. Ledger verifies the chain against the production bundle and matches URI SAN `spiffe://prod.example/payments/reconciler`. Its policy then permits only `append` for tenant carried in a verified request context.

A valid SVID for reporting service authenticates successfully but receives denial for `append`.

### Example 5

An EKS workload formerly read node-role credentials from instance metadata. The team creates a dedicated service account and IRSA or Pod Identity mapping for a narrower role, restricts metadata access, and observes credential provider use.

Only after telemetry shows the workload identity path does it remove the old node permission. Otherwise SDK precedence could hide continued dependence.

### Example 6

A GitHub Actions release workflow requests an OIDC token. Cloud trust requires exact issuer/audience, immutable organization and repository identifiers, protected production environment, and approved branch/workflow context.

A pull request from a fork can run tests but cannot match the production role condition. No cloud key is stored as a repository secret.

### Example 7

Portal calls deployer for human `usr-91`. Deployer authenticates portal’s workload SVID and accepts a five-minute delegated grant limited to environment `env-7`, action `deploy`, tenant `tn-a`, and artifact digest.

Audit preserves both `usr-91` and the portal/deployer workload chain. Deployer cannot reuse the grant to delete the environment.

### Example 8

The workload CA rotates. Trust bundles contain old and new roots during planned overlap; agents renew leaf certificates under the new chain; services reload bundles without restart; old root is removed after all old leaf validity and connection-drain bounds pass.

An unexpected unknown root is never fetched and trusted based only on the peer certificate.

### Example 9

Credential service fails for twenty minutes. Existing mTLS connections drain according to policy, valid cached certificates continue until expiry, and renewal retries use jitter. New sensitive operations requiring fresh token exchange fail closed.

Alerting fires well before mass expiry. Recovery restores issuance, not acceptance of expired certificates.

### Example 10

A retired batch service is deleted. Reconciliation finds its SPIFFE registration, Kubernetes service account, cloud provider mapping, IAM role binding, mesh policy, dashboard, and an old static fallback secret.

The team removes each dependency, waits through maximum credential lifetime, confirms no use, revokes the fallback, retains audit tombstones, and tests disaster restore does not recreate the provider mapping.

## Cross-Program Connections

- **API and Service Engineering:** resource servers validate issuer, audience, peer identity, scopes/delegation, and authorize each endpoint.
- **Security Engineering:** attestation, least privilege, credential theft, confused deputies, zero trust, incident containment, and threat modeling define guarantees.
- **Cryptography:** certificate chains, signatures, key possession, TLS, JWT, rotation, and validity windows make identity verifiable.
- **Operating Systems:** process identity, namespaces, sockets, kernel metadata, UID isolation, and node compromise bound local attestation.
- **Distributed Systems:** clocks, caches, renewal, partial failure, reconciliation, and revocation propagation determine exposure.
- **Cloud Engineering:** managed identities, instance metadata, security-token services, service accounts, IAM roles, and cross-account trust consume workload proofs.
- **DevOps and Delivery Engineering:** runner isolation, OIDC federation, protected environments, provenance, and deployment roles treat pipelines as workloads.
- **Software Supply Chain Security:** image digest/signature selectors and build identity connect approved artifacts to runtime identity without conflating them.
- **Reliability Engineering:** credential-plane SLOs, rotation overlap, retry jitter, expiry cliffs, degraded mode, and recovery prevent identity-caused outages.
- **Governance and Compliance:** principal ownership, access review, separation of duties, audit retention, disable-to-denial SLAs, and retirement make machine access accountable.

## References

1. SPIFFE. [SPIFFE Concepts](https://spiffe.io/docs/latest/spiffe/concepts/). Retrieved 2026-09-02.
2. SPIFFE. [SPIFFE Identity and Verifiable Identity Document](https://spiffe.io/docs/latest/spiffe-specs/spiffe-id/). Retrieved 2026-09-02.
3. SPIFFE. [SPIFFE Workload API](https://spiffe.io/docs/latest/spiffe-specs/spiffe_workload_api/). Retrieved 2026-09-02.
4. SPIFFE. [SPIRE Concepts](https://spiffe.io/docs/latest/spire-about/spire-concepts/). Retrieved 2026-09-02.
5. Kubernetes. [Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/). Retrieved 2026-09-02.
6. Kubernetes. [Managing Service Accounts](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/). Retrieved 2026-09-02.
7. Amazon Web Services. [IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html). Retrieved 2026-09-02.
8. Amazon Web Services. [Grant Kubernetes Workloads Access Using Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html). Retrieved 2026-09-02.
9. Google Cloud. [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation). Retrieved 2026-09-02.
10. Google Cloud. [Best Practices for Workload Identity Federation](https://cloud.google.com/iam/docs/best-practices-for-using-workload-identity-federation). Retrieved 2026-09-02.
11. Microsoft. [What Are Workload Identities?](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview). Retrieved 2026-09-02.
12. IETF. [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693). January 2020. Retrieved 2026-09-02.
13. IETF. [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705). February 2020. Retrieved 2026-09-02.
14. NIST. [SP 800-207A: A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments](https://csrc.nist.gov/pubs/sp/800/207/a/final). September 2023. Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define workload principals and trust domains for a platform running production and laboratory clusters in two clouds. Include identity granularity, immutable mapping fields, tenant context, and federation direction.

### Exercise 2

Design issuance for a Kubernetes payment reconciler using SPIFFE mTLS internally and cloud workload federation externally. Include registration, attestation, projected token, audiences, rotation, authorization, and telemetry.

### Exercise 3

Threat-model the node agent, service mesh proxy, federation broker, and CI runner. For each, identify impersonation blast radius, confused-deputy paths, containment, and evidence.

### Exercise 4

Define and calculate a defensible compromise exposure bound for a stolen bearer token and an X.509 workload credential. State assumptions about detection, policy propagation, expiration, connections, and clocks.

### Exercise 5

Plan migration of 240 workloads from static cloud keys and node-wide roles to workload identity. Include inventory, cohorts, hidden fallback detection, rollback, revocation, and retirement proof.

## Answers to the Exercises

### Answer 1

Create distinct trust domains/providers for production and laboratory environments; weaker laboratory controls must not issue production identities. Cloud location alone need not split a production logical principal if ownership and policy are identical, but use directional federation and separate roots/providers when administration or incident isolation differs.

Define principals by stable function and privilege, such as `payments/reconciler`, not replica or node. Split deployer, reporter, and reconciler; split tenant-specific data planes where shared identity would create unacceptable cross-tenant blast radius. Map exact issuer/provider plus cluster UID, namespace UID, service-account UID, and approved controller/image evidence to the principal. Retain names for readability, never as the only recreation-sensitive key.

Production domains accept only explicitly named foreign subjects and audiences; laboratory accepts no reciprocal production privilege by default. A shared control-plane principal carries explicit tenant context and current authorization. Registry records owner, selectors, credentials, target roles, review, and retirement.

### Answer 2

Register `spiffe://prod.example/payments/reconciler` against attested production cluster, namespace/service-account UID, controller, and approved image digest. Attest node before agent receives registrations. Agent binds Workload API socket caller to process/pod, derives selectors from kernel/runtime/kubelet, matches one entry, and streams short-lived X.509-SVID/private key and trust bundle.

Ledger verifies the production chain and exact SPIFFE ID during mTLS, then authorizes append for the request tenant/resource. For cloud access, kubelet projects and rotates a token for exact federation audience. Exchange validates cluster issuer/signature, subject/object binding, time, audience, and mapping, then issues a shorter target role credential. Kubernetes RBAC and cloud role permissions are independent.

Record issuance/exchange principal, node/instance, selector summary, audience, TTL, mapping revision, result, and fingerprint—not raw credentials. Test renewal, pod deletion, image change, same-name cluster collision, token replay, wrong audience, agent outage, and role removal.

### Answer 3

The node agent can impersonate authorized workloads on its node if compromised and may expose cached keys. Limit node-authorized registrations, socket mounts, host privileges, and control connectivity; rotate node credentials, quarantine node, revoke registrations, and use issuance/fingerprint logs.

The mesh proxy owns transport keys and may call peers for local applications. Bind local socket/listener to workload, isolate tenants, restrict destinations/actions, preserve peer and actor context, and prevent arbitrary identity selection. Proxy access/policy logs support investigation.

The federation broker can mint or exchange target credentials across many domains. Separate keys/providers, require dual control, constrain subject/audience/role, cap TTL/rate, and rehearse provider/key disable. Exchange logs must retain source and target principal correlation.

A persistent CI runner can steal tokens or inherit later privileged jobs. Use ephemeral isolated runners, segregate trusted workflows from pull requests, bind OIDC claims to immutable repository and protected environment, and destroy runner state. Workflow, approval, issuer, subject, artifact, and exchange logs establish evidence.

### Answer 4

For compromise at $t_c$, credential expiry $t_e$, detection $t_d$, and effective denial at each surface $t_s$, use $E\le\max_s(\min(t_e,t_s)-t_c)$. Add clock tolerance and long-lived connection/session behavior explicitly rather than assuming validation on every request.

A stolen bearer token remains usable by the thief until expiry or online denial reaches every verifier. If TTL is 15 minutes, worst-case theft occurs just after issuance, clock allowance is one minute, and no faster revocation exists, the credential component is about 16 minutes; cached authorization or established sessions may make the real bound larger.

An X.509 credential also lasts until expiry, but a copied certificate without its private key is unusable. If key is stolen, mTLS can be replayed until expiry or denial. Connection reauthentication frequency matters: a two-hour accepted connection violates a claimed ten-minute exposure despite a ten-minute leaf certificate unless the system drains it. Validate assumptions with timed compromise exercises.

### Answer 5

Inventory each key, node role, target account, permissions, owner, application, SDK/provider chain, storage copy, backup, last use, and emergency fallback. Create one least-privilege workload principal and mapping per security-distinct application; prepare projected/attested issuance, target federation roles, telemetry, and rollback that does not broaden privilege.

Migrate low-risk representatives by runtime and SDK, then higher-risk cohorts. Run dual path briefly, force/observe credential-source selection, compare authorized operations, inject federation outage, and scan logs for old key IDs or node role. Remove node metadata reachability and static-provider configuration so a successful call cannot mask fallback.

After each cohort, disable old key/permission, observe, then revoke and remove every copy from secrets, CI, images, machines, vendor systems, and backups under retention procedure. Reconcile unused roles and mappings. Completion evidence shows no old-key/node-role use through the observation window, all workloads renew/recover correctly, old permissions are gone, and disaster restore cannot recreate the credentials or bindings.
