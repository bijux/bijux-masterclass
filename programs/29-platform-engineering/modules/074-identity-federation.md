---
module_id: PLAT-074
program: Platform Engineering
level: 2
module_number: 74
title: Identity Federation
status: complete
last_verified: 2026-09-02
---

# Identity Federation

## One-Page Review

### Governing question

How should a platform trust external identity providers for human authentication while preserving issuer-scoped identity, tenant membership, local authorization, assurance, privacy, provisioning, session, key, incident, and decommissioning boundaries?

### Essential definitions

- **identity federation** lets a relying party establish a local authenticated session from a verifiable assertion issued by a trusted identity provider rather than directly verifying the user’s authenticator.
- An **identity provider (IdP)** authenticates a subscriber and issues assertions; a **relying party (RP)** validates them and provides the platform service.
- A **trust agreement/profile** defines permitted issuers, relying parties, protocols, keys, claims, assurance, attributes, privacy, operations, and lifecycle.
- A **federated identifier** is the issuer plus subject identifier, not an email address, display name, or mutable username.
- An **identity assertion** is a signed, audience- and time-bounded statement about an authentication event and subject; it is not a general API authorization token.
- An **ID token** is an OpenID Connect assertion intended for a client/RP; an **access token** authorizes access to a resource server under its audience/scope contract.
- **account resolution/linking** maps a verified federated identifier to a stable local account through an explicit, attack-resistant process.
- **provisioning** creates/updates/disables local accounts and group/attribute mappings, often through SCIM, batch sync, or governed just-in-time logic.
- **authentication assurance** describes confidence/properties of the authentication event; **federation assurance** covers protections of the assertion transaction.
- **step-up authentication** obtains a fresher or stronger authentication context before a sensitive action.
- A **session** is RP-local authenticated state with idle/absolute lifetime, revocation, reauthentication, and device/security context.
- **break-glass identity** is a separately protected, narrowly authorized recovery identity independent of the normal federation path.

### Central model, mechanism, or theorem

Let an assertion be

$$
A=(iss,sub,aud,t_i,t_e,jti,n,acr,amr,X),
$$

where issuer/subject establish external identity, audience identifies the intended RP, $t_i,t_e$ bound time, $jti$ and nonce $n$ resist replay/substitution under the protocol, $acr/amr$ describe authentication context, and $X$ is a minimal attribute set. The RP accepts only after validating protocol flow, trusted issuer and exact configuration, signature/algorithm/key, audience/client, time/skew, nonce/state/code binding where applicable, and transaction context. It maps $(iss,sub)$ to immutable local principal $p$, then independently resolves current tenant membership and authorization. No mutable claim or successful login alone grants platform privileges.

### Critical invariants

- Federated identity is keyed by issuer plus subject; email, username, group display name, and human name are attributes, never sole account keys.
- Issuer discovery/registration is allowlisted and bound to expected endpoints/keys; user input cannot select arbitrary metadata or token endpoints.
- Every assertion validates signature, allowed algorithm, issuer, audience/authorized party, time, nonce/state/code binding, and transaction context required by the chosen profile.
- ID tokens are consumed only by their intended client; access tokens only by the intended resource server/audience; neither is blindly forwarded.
- Authentication establishes identity/context, while every platform backend authorizes the concrete tenant, action, and resource from current policy.
- Account linking never relies only on matching mutable email; conflicts and reassignment enter verified recovery/review.
- Claims and group mappings have named authorities, transformations, freshness, size bounds, collision rules, and fail-closed behavior.
- Provisioning, suspension, termination, membership change, and token/session revocation form one reconciled lifecycle with bounded delay.
- Sensitive operations require adequate and fresh authentication context; an old session cannot silently satisfy new assurance requirements.
- Signing/encryption key rotation tolerates planned overlap but rejects unknown, stale-beyond-policy, weak, or ambiguous keys/algorithms.
- Federation outage has explicit degraded and break-glass behavior; cached claims never become indefinite authorization.
- Removing an IdP/RP drains users, sessions, provisioning, keys, metadata, callbacks, service trust, and retained identity obligations.

### Common failures

Email as primary key; automatic linking on verified email from any issuer; tenant chosen from untrusted domain; accepting any issuer discovered from user input; skipping exact issuer/audience; algorithm confusion; trusting token header key URL; missing state/nonce/PKCE; ID token used as API bearer; access token accepted by wrong service; long-lived group claims; authorization only in portal; huge group list in token; SCIM create without disable/delete; JIT provisioning with broad default role; stale session after termination; logout assumed globally reliable; clock skew made unlimited; signing-key rotation outage; federation proxy erasing upstream context; shared break-glass credential; and deleting IdP config before migrating identities.

### Compact example

User authenticates through issuer `https://id.example/` and subject `00u82`; the platform keys external identity as `(issuer,00u82)` and maps it to local principal `usr-91`. It validates authorization-code flow with PKCE, state, nonce, exact redirect, issuer, signature/algorithm/key, client audience, authorized party, and bounded times. Verified email is contact data only. Current directory/SCIM state maps `usr-91` into tenants `tn-a` and `tn-b`; user selects `tn-b`, which the backend revalidates. Deleting production requires step-up with required context and fresh authentication time. When SCIM disables the account, platform blocks new sessions, revokes local sessions, and reconciles outstanding tokens/privileges within a measured window.

### Connections

This module supplies trusted human identity for tenant context in [PLAT-071](071-tenant-models.md), administration of boundaries in [PLAT-072](072-namespace-account-and-cluster-isolation.md), and quota changes in [PLAT-073](073-resource-quotas.md). It builds on portal/backend separation from [PLAT-070](070-integrating-platform-components-without-creating-a-portal-monolith.md) and policy enforcement from [PLAT-066](066-policy-decision-and-enforcement-points.md). PLAT-075 distinguishes workload identity; PLAT-076–079 use identity in policy, admission, supply-chain, and audit systems.

## Governing Question

How can a platform rely on organizational, partner, or customer identity systems without importing their mutable identifiers and availability assumptions directly into every authorization decision?

Federation separates authenticator verification from the relying platform. That improves single sign-on, central lifecycle, and phishing-resistant authentication adoption, but it creates a multi-party trust system. A compromised or misconfigured IdP can assert identities to many RPs; an RP can mishandle assertions or collect excessive attributes.

The platform therefore needs more than “OIDC works.” It needs a governed profile, stable account mapping, attribute authority, tenant resolution, session policy, provisioning/deprovisioning, key rotation, privacy, telemetry, incident response, and exit plan.

Federation is about human/subscriber authentication in this module. Machine and workload identity has different issuance, attestation, rotation, delegation, and lifecycle semantics, covered by PLAT-075.

## Why This Matters

Identity is the front door to privileged platform actions: code deployment, account vending, secrets, production access, policy exceptions, quota increases, and deletion. One identity mix-up crosses many downstream boundaries.

Mutable attributes create silent account takeover. Email addresses and usernames change or are reassigned. Two IdPs can issue the same subject string. Stable mapping must use issuer-scoped identifiers and verified linking procedures.

Lifecycle gaps are equally dangerous. Authentication may be central, while group sync, application sessions, API tokens, and cloud roles remain active after termination. The platform must measure and reconcile disable-to-denial time end to end.

Availability matters. If the only IdP or its key/discovery endpoint fails, users may be locked out during an incident. Indefinite cached authorization is not a safe fallback; protected recovery identities and explicit degraded modes are.

## Prerequisites and Retrieval

Retrieve authentication, authorization, identity proofing, authenticators/MFA, public-key cryptography, TLS, OAuth 2.0, OpenID Connect, SAML, JWT/JWS/JWK, PKCE, browser redirects/cookies/CSRF, SCIM, directory groups, sessions, token exchange, tenant models, policy decision/enforcement, audit, incident response, privacy, and high availability.

Distinguish federation from synchronization; IdP from directory/CSP; RP/client from resource server; authentication from authorization; ID token from access token; issuer/subject from email; account resolution from account linking; claim from locally governed attribute; group membership from role/permission; assertion lifetime from RP session lifetime; logout from revocation; disable from deletion; authentication assurance from federation assurance; human identity from workload identity; and federation proxy from transparent trust.

## Learning Objectives

After completing this module, you should be able to:

1. model IdP, CSP/directory, federation authority, RP/client, resource server, and local account responsibilities;
2. define a secure OIDC/SAML federation profile and validate assertions at exact boundaries;
3. map issuer-scoped subjects to local accounts and tenants without mutable-attribute takeover;
4. govern claims, groups, roles, entitlements, assurance, and step-up independently;
5. choose SCIM/pre-provisioning, just-in-time provisioning, or hybrid lifecycle;
6. design RP sessions, access tokens, revocation, logout, and termination response;
7. operate metadata, signing keys, secrets, clocks, discovery, and multi-IdP routing safely;
8. protect privacy and prevent token/claim leakage across portal and services;
9. test mix-up, replay, substitution, linking, lifecycle, key, outage, and recovery cases; and
10. migrate and retire IdPs/RPs without orphan identities or privilege.

## Core Exposition

### Model the federation roles and trust

The subscriber authenticates to an IdP; the IdP issues an assertion; the RP validates it and creates a local session. A credential service provider or directory may proof identity, maintain accounts, and supply attributes to the IdP. One product can perform several roles, but contracts remain distinct.

The federation authority establishes trust: approved parties, issuer/client identifiers, redirect/callback URIs, protocol/profile, keys, algorithms, attributes/purpose, assurance, incident contacts, logging, availability, and lifecycle.

Do not infer trust because an endpoint has valid TLS or publishes discovery metadata. Registration and issuer selection are administrative security decisions.

Inventory each IdP–RP relationship, owner, tenants/users, protocol, clients, keys/secrets, environments, assurance, sessions, provisioning path, and retirement dependencies.

### Choose a constrained protocol profile

OpenID Connect provides authentication on OAuth 2.0. For browser-based platform login, use authorization code flow with current security practices such as PKCE, exact redirect matching, state, nonce where required, and server-side token handling appropriate to architecture.

SAML can serve enterprise federation, but configure entity identifiers, audience, recipient/destination, request correlation, time, signature, binding, and metadata under an equally explicit profile. Avoid protocol auto-detection at runtime.

Disable implicit/legacy modes, weak algorithms, wildcard redirects, password grants, and unnecessary response types. RFC 9700 is the current OAuth security BCP and deprecates unsafe historical practices.

Use tested libraries and keep protocol parsing outside domain code. Configuration still needs security review; a correct library cannot choose the right issuer/audience or account-linking policy for you.

### Establish stable federated identity

OpenID Connect defines `sub` as locally unique and never reassigned within an issuer. The platform key is $(iss,sub)$. The same `sub` from another issuer is a different identity; the same person may have several federated identifiers linked to one local principal.

Email, login, employee number, name, and group are attributes with their own authority and lifecycle. Even a verified email does not prove that every issuer uses compatible proofing or reassignment policy.

Create immutable local principal IDs so application data survives issuer migration. Store external identity mapping, issuer, subject, creation/link evidence, status, last authentication, and provenance.

Never reuse local principal IDs. When an issuer recycles a username or email, a new subject must not inherit old platform resources.

### Resolve and link accounts safely

Account resolution maps a verified federated identifier to an existing local account. Direct mapping is safest when provisioned ahead through a trusted authoritative identifier.

Automatic email matching across issuers enables account takeover when proofing, domain ownership, or reassignment differs. Treat a new issuer/subject as a new identity unless a controlled linking ceremony proves possession/authority on both sides or an administrator applies verified migration mapping.

Linking is a privileged mutation with reauthentication, audit, notification, conflict detection, rollback/recovery, and prohibition for high-risk accounts where appropriate.

If two local accounts collide during migration, quarantine. Do not silently merge ownership, audit histories, tokens, or tenant memberships.

### Bind federation to tenant context

An external IdP tenant/organization/domain is not automatically the platform tenant. Maintain a governed mapping from issuer/subject/group/organization attributes to internal tenant memberships.

Users belonging to several tenants choose one context after login; backend verifies membership and resource scope on every request. A URL or email domain cannot grant membership.

For customer federation, route home-realm discovery from pre-registered tenant configuration, not arbitrary issuer URLs. Avoid disclosing tenant/employee existence through login errors.

Record mapping revision and source. Changes propagate to sessions and authorization within a defined freshness/revocation window.

### Validate OIDC assertions completely

Bind response to the initiating browser transaction using state, nonce, authorization code, PKCE verifier, exact redirect URI, secure cookies, and one-time transaction state as required by the flow.

Validate exact `iss`, cryptographic signature, allowlisted algorithm, trusted key for that issuer, `aud`, `azp` when applicable, expiration, not-before/issued-at policy, nonce, and any required authentication context. Bound clock skew.

Do not fetch a key or metadata URL supplied by an untrusted token header. Use issuer-bound discovery/configuration and validate key identifiers/sets with controlled caching and refresh.

Reject unsigned, weak, ambiguous, wrong-environment, wrong-client, stale, replayed, or unsolicited assertions according to the profile. Error safely without logging token contents.

### Keep ID tokens and access tokens separate

An ID token tells a client about an authentication event/subject. It is not a generic access token for every backend. A resource server validates access-token issuer, audience/resource, signature/introspection, time, scopes, client/subject, and other policy fields under its contract.

Do not forward the portal’s tokens to unrelated services. Use audience-bound access tokens or OAuth token exchange for constrained delegation, preserving actor and calling-service identities.

Opaque tokens can centralize introspection/revocation; self-contained tokens reduce lookup dependency but remain valid until expiry unless another revocation mechanism is enforced. Choose by risk and availability.

Never place tokens in URLs, analytics, traces, client logs, error reports, or browser storage without a reviewed model. Prefer secure, HttpOnly, SameSite cookies for web sessions where appropriate.

### Separate authentication claims from authorization

The IdP can assert subject, authentication context, and approved attributes. It does not decide whether the user may delete environment `env-82` unless the federation/authorization contract explicitly grants that authority.

Map coarse directory groups to locally governed roles or entitlements carefully. Resolve resource ownership, tenant, environment, separation of duties, approvals, and current policy at the backend enforcement point.

Avoid embedding thousands of groups/permissions in tokens. Size breaks headers/proxies, values stale, and group names collide. Use stable group IDs and server-side current lookup/sync where required.

Default access is minimal. A newly federated or JIT-provisioned user does not receive broad platform role merely because authentication succeeded.

### Govern attribute authority and transformation

For each attribute record authoritative source, semantics, format, uniqueness, mutability, verification, freshness, privacy class, consumers, and conflict resolution.

Normalize only for presentation/search. Security comparison follows issuer contract; unsafe case folding or whitespace/domain transformation can merge identities.

Map external groups/roles through explicit IDs and versioned rules. Display names are mutable. Deny or quarantine unknown/conflicting values rather than silently choose.

Minimize assertion claims. Request only attributes needed for declared purpose, restrict onward disclosure, expire caches, support correction/deletion, and avoid putting sensitive data into broad tokens.

### Choose provisioning and lifecycle strategy

Pre-provisioning/SCIM can create accounts and memberships before first login, deliver disable/change events, and support inventory. It depends on sync correctness and authentication/authorization of the provisioning client.

Just-in-time provisioning simplifies onboarding but learns termination/group changes only at login unless paired with sync or token/session checks. It must create minimal access and handle identity conflicts atomically.

A hybrid commonly pre-provisions high-risk roles/groups and permits minimal JIT accounts. Treat SCIM and login as concurrent writers with defined authority and version/conflict behavior.

Validate SCIM schemas, stable IDs, filters, pagination, bulk limits, PATCH semantics, idempotency, and tenant scope. Provisioning endpoints are high privilege and need independent credentials/audit.

### Reconcile deprovisioning end to end

Termination or suspension must block new authentication at IdP, disable local account/membership, revoke/expire RP sessions and refresh/access tokens, remove cloud/platform roles, cancel delegated approvals, and address active workflows.

Measure time from authoritative disable to effective denial at each system. Webhook/sync delivery can fail; periodic full reconciliation detects missed changes.

Do not hard-delete identity immediately when audit, ownership transfer, legal hold, or recovery requires history. Disable access while preserving immutable principal references.

When membership rather than account ends, remove only that tenant/role and verify other legitimate memberships remain.

### Design RP sessions deliberately

The RP creates local session only after valid assertion and account resolution. Session ID is high entropy, rotated after authentication/privilege change, protected in transit/storage, and never accepted from URL.

Set idle and absolute lifetimes by risk. Track authentication time and context so sensitive actions can require reauthentication/step-up rather than treating session age as fresh assurance.

Session revocation supports account disable, role change, compromise, device loss, administrator action, and key/client incident. Maintain an inventory of active sessions or an equivalent bounded invalidation design.

Single logout across multiple RPs/IdPs is protocol- and implementation-dependent. Local logout always terminates local session; state what upstream/downstream sessions remain.

### Use assurance and step-up as policy inputs

Identity proofing, authenticator assurance, and federation protections are separate dimensions. NIST SP 800-63 defines IAL, AAL, and FAL concepts; choose the applicable organizational profile rather than copying labels without evidence.

Record authentication methods/context only when issuer semantics are contracted. `amr` strings or an MFA flag from different issuers may not be comparable.

High-risk actions may require phishing-resistant authentication, recent authentication, managed device, stronger federation protection, or approval. Initiate step-up with transaction binding and verify returned context/time.

Do not permanently elevate the whole session if only one operation required step-up. Bind authorization to operation/resource and bounded window.

### Operate multiple IdPs and federation brokers

A federation broker/proxy can normalize protocols and reduce RP integrations, but becomes a high-impact trust, privacy, availability, and account-linking authority. Preserve upstream issuer/subject and authentication context without collision.

Home-realm discovery uses trusted tenant mapping or user choice among configured issuers. Prevent mix-up where response from one issuer is accepted in another transaction.

Define precedence/conflict for attributes from HR, directory, partner IdP, and local systems. “Last writer wins” is unsafe for role or termination.

Isolate production/non-production issuers, clients, redirect URIs, keys, groups, and sessions. Test identical subjects and emails across issuers/environments.

### Manage keys, metadata, secrets, and clocks

Pin issuer identity and validate discovery metadata. Cache keys with bounded freshness, support planned overlapping rotation, refresh safely on unknown `kid`, and rate-limit refresh to prevent denial of service.

Allow only configured signature algorithms/key properties. Do not accept algorithm/key-type changes merely because metadata advertises them.

Protect client secrets/private keys in a secret authority, rotate, scope by environment/client, and avoid browser clients holding confidential secrets. Prefer asymmetric client authentication where the profile warrants it.

Synchronize clocks and monitor skew. Small bounded tolerance handles distribution; large tolerance enlarges replay/lifetime windows and masks operational defects.

### Engineer availability and degraded behavior

Authentication depends on IdP, DNS, network, browser flow, discovery/keys as cached, token endpoint, directory/provisioning, and RP session store. Define SLOs and dependencies.

Existing bounded local sessions may continue during IdP outage according to risk; new login and step-up may fail. Cached keys can validate already issued tokens until their lifetime/policy, but stale attributes do not become indefinite access.

Provide separate break-glass identities for incident response: phishing-resistant authenticators, narrow roles, offline/redundant protection, dual control where needed, alerts, short sessions, and regular drills.

Never share one recovery password. Federation outage is exactly when auditable recovery must work without relaxing ordinary authorization.

### Protect privacy and prevent correlation

Federation centralizes visibility into which RPs a person accesses and distributes attributes to RPs. Minimize disclosure and retention under the trust agreement and applicable privacy obligations.

Pairwise/pseudonymous subject identifiers can reduce cross-RP correlation where supported. If global subject is required for operations, constrain access and onward use.

Avoid placing email, group lists, HR attributes, device details, and authentication factors in logs/metrics/traces. Record stable local principal and bounded security event references, with protected lookup.

Explain consent/notice and administrative access. Support attribute correction, account export, deletion, and retention without breaking audit integrity.

### Observe and audit federation

Measure login start/success/failure by bounded reason, issuer/client, callback latency, token exchange, key refresh, clock error, account resolution/link conflicts, provisioning lag/errors, disable-to-denial, session revocation, and step-up.

Do not label metrics by subject, email, token ID, or raw tenant. Protect logs containing issuer-subject mappings and security events.

Audit issuer/client configuration, keys/secrets rotation, mappings, link/unlink, role/group transformations, provisioning actions, break-glass, session revocation, and IdP/RP retirement.

Authentication success rate alone misses incorrect account linkage and stale authorization. Reconcile directory, IdP, local accounts, tenant memberships, sessions, and external roles.

### Test federation adversarially

Test wrong issuer/audience/client/environment, altered signature, disallowed/none algorithm, unknown/duplicate key ID, stale/future token, excessive skew, nonce/state/code replay, redirect manipulation, and unsolicited responses.

Test issuer mix-up, discovery/key endpoint manipulation, SSRF, token substitution, ID/access-token confusion, group/claim overflow, malformed encodings, duplicate claims, and logout/session fixation.

Test same email/subject across issuers, email reassignment, linking conflict, SCIM/login race, missed disable, stale groups, multi-tenant membership, partner offboarding, and rehire.

Exercise IdP/key/token/directory/session outages, signing-key rotation, client-secret compromise, rollback, break-glass, and complete IdP migration/decommission.

### Migrate and retire federation safely

Inventory subjects, local mappings, tenants, privileged accounts, groups/roles, sessions, tokens, clients, redirects, SCIM, service integrations, keys/secrets, audit, and owners.

Pre-establish the new issuer trust and a verified old-to-new subject mapping from an authoritative source or controlled linking ceremony. Email alone is insufficient.

Run cohort migration with dual login where safe, explicit account resolution, step-up, conflict quarantine, session behavior, and rollback. Prevent two external identities from independently mutating one high-risk account without policy.

After all users and provisioning clients migrate, revoke old sessions/tokens, disable callbacks and SCIM, remove keys/secrets/trust/metadata, retain required mapping/audit tombstones, and test recovery does not re-enable the old path.

## Definitions and Notation

Let trusted issuers be $I$, relying parties/clients $R$, local principals $P$, and tenant memberships $M$.

An assertion is

$$
A=(iss,sub,aud,t_i,t_e,jti,n,acr,amr,X).
$$

External identity key is

$$
f=(iss,sub),
$$

and account resolution is a partial, versioned function $L:I\times Subject\rightarrow P$. It is partial because unknown/conflicting identities must not be forced into an account.

For RP $r$, acceptance predicate is

$$
V_r(A,\chi)=sig\land issuer\land audience\land time\land transaction\land profile,
$$

where $\chi$ is RP-initiated transaction context. Successful $V_r$ permits account resolution and session creation; it does not imply authorization $Permit(p,t,a,o)$ for tenant $t$, action $a$, and object $o$.

Let authoritative disable time be $t_d$ and effective denial across surface $s$ be $t_s$. Revocation exposure is

$$
E=\max_s(t_s-t_d),
$$

measured across login, local sessions, tokens, memberships, cloud roles, and active delegation under the platform contract.

## Mechanisms, Invariants, or Proof Structure

### Federation transaction mechanism

1. Register/allowlist issuer, RP client, exact callbacks, profile, algorithms, keys, attributes, assurance, provisioning, owners, and lifecycle.
2. User selects a configured home realm/tenant context without supplying arbitrary issuer endpoints.
3. RP creates one-time transaction state, state/nonce, PKCE verifier/challenge, and secure browser binding.
4. IdP authenticates user under requested context and returns authorization response bound to RP transaction.
5. RP exchanges code through configured endpoint and validates flow, redirect, PKCE, client authentication, and response.
6. RP validates assertion signature/algorithm/key, exact issuer, audience/authorized party, time/skew, nonce, and required context.
7. RP resolves $(iss,sub)$ to immutable local principal or applies controlled provisioning/linking.
8. RP resolves current tenant memberships/attributes and creates bounded local session.
9. Each backend validates its access token/delegation and authorizes concrete tenant/action/resource.
10. Provisioning and reconciliation propagate change/disable; session/token/role revocation closes stale access.
11. Telemetry/audit observes transactions without leaking assertions or mutable identifiers.
12. Key rotation, outage, incident, migration, and retirement follow rehearsed trust-lifecycle procedures.

### Identity invariant

Exactly one active local principal mapping is selected for a federated issuer-subject under a versioned resolution decision. Mutable attributes cannot create or merge that mapping by themselves.

### Assertion invariant

An assertion is accepted only by its configured RP, within its transaction/time/profile, from its expected issuer and trusted key. Successful validation grants no domain authorization by itself.

### Lifecycle invariant

Authoritative disable converges to denial across local sessions, tokens, memberships, external roles, and delegations within the published maximum exposure window, with reconciliation for missed events.

### Privacy invariant

The RP receives, retains, logs, and discloses only federation attributes needed for documented purpose, and protects issuer-subject linkage as sensitive security data.

### Proof sketch: email equality cannot prove identity equality

Suppose issuer $i_1$ assigns `alex@example.com` to subject $s_1$, while issuer $i_2$ independently assigns the same verified email to subject $s_2$, or $i_1$ later reassigns the email after $s_1$ leaves. Email equality holds, but the issuer-subject identities differ and may represent different people.

An RP that automatically links by email maps both to one local principal and can transfer the first account’s resources/privileges to the second. Therefore email equality—even with a verified flag—cannot prove federated identity equality without an additional trusted linking/migration authority and ceremony. This is a counterexample, not a claim that email is never useful as contact or discovery data.

### Executable assertion audit

This synthetic audit classifies nine assertion observations using issuer, audience, signature, time, nonce, and mapping checks. It tests local predicate ordering only; it does not perform cryptographic or protocol validation.

<!-- bijux-verify: {"id":"federation-assertion-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=4\nissuer=1\naudience=1\nsignature=1\ntime=1\nnonce=1\n"}} -->
```python
assertions = [
    ("trusted", "portal", True, True, True),
    ("trusted", "portal", True, True, True),
    ("trusted", "portal", True, True, True),
    ("trusted", "portal", True, True, True),
    ("unknown", "portal", True, True, True),
    ("trusted", "api", True, True, True),
    ("trusted", "portal", False, True, True),
    ("trusted", "portal", True, False, True),
    ("trusted", "portal", True, True, False),
]

counts = {name: 0 for name in ("accepted", "issuer", "audience", "signature", "time", "nonce")}
for issuer, audience, signature, valid_time, nonce in assertions:
    if issuer != "trusted":
        counts["issuer"] += 1
    elif audience != "portal":
        counts["audience"] += 1
    elif not signature:
        counts["signature"] += 1
    elif not valid_time:
        counts["time"] += 1
    elif not nonce:
        counts["nonce"] += 1
    else:
        counts["accepted"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Use protocol conformance and negative fixtures for authorization flow, callbacks, metadata, keys, signatures, claims, clocks, transactions, tokens, and logout. Test every supported issuer/client/environment pair.

Fuzz parsers and exercise mix-up, substitution, replay, SSRF, redirect, algorithm, key rotation, duplicate claims, oversized groups, and token leakage.

Create colliding email/username/subject across issuers, reassignment, rehire, multi-tenant users, linking/unlinking, SCIM/JIT races, missed disable, and stale membership.

Inject IdP, DNS, discovery/key, token, SCIM/directory, session-store, and policy outages; test compromise/revocation, break-glass, migration, and restoration without re-enabling old trust.

## Alternatives and Trade-Offs

- **Federation versus local passwords.** Federation centralizes authenticator policy/lifecycle; local accounts reduce IdP dependency but multiply credential risk.
- **OIDC versus SAML.** OIDC fits modern OAuth/API ecosystems; SAML is common in enterprise SSO. Both require constrained profiles and correct validation.
- **Direct IdP trust versus federation broker.** Direct trust reduces intermediary impact; a broker normalizes integrations but concentrates identity and outage risk.
- **Pre-provisioning versus JIT.** Pre-provisioning supports lifecycle/inventory; JIT simplifies onboarding but needs separate timely deprovisioning.
- **SCIM versus batch/webhook sync.** SCIM standardizes resource operations; other feeds may match local authority but require equally explicit semantics.
- **Global versus pairwise subject.** Global IDs ease correlation/operations; pairwise IDs improve privacy and limit cross-RP correlation.
- **Self-contained versus opaque access tokens.** Self-contained tokens reduce lookup; opaque/introspected tokens enable current central status at availability cost.
- **Cookie session versus browser-held token.** Secure server sessions reduce token exposure; token-centric clients can scale independently but broaden browser threat handling.
- **Group claims versus directory lookup.** Claims reduce latency/dependency but stale/grow; lookup improves currency but adds runtime coupling.
- **IdP roles versus local authorization.** IdP roles centralize coarse entitlements; local policy understands tenant/resource context. Map rather than conflate.
- **Long sessions versus frequent reauthentication.** Long sessions improve usability/outage tolerance; shorter/fresh sessions reduce termination and compromise exposure.
- **Global logout versus local logout.** Global intent is convenient but protocol-dependent; local revocation is controllable and must always work.
- **Automatic linking versus explicit ceremony.** Automation reduces friction; ceremony prevents mutable-attribute takeover and preserves evidence.
- **Key caching versus live fetch.** Caching improves availability; bounded refresh is needed for rotation/revocation. Untrusted dynamic fetch is unsafe.
- **Fail open versus fail closed during outage.** Fail open preserves access but accepts stale/unknown authority; risk-tiered bounded sessions plus protected recovery is safer.
- **Big-bang versus cohort IdP migration.** Big-bang shortens dual trust but raises lockout/takeover risk; cohorts provide evidence while extending complexity.

## Failure Modes and Misconceptions

- “SSO is federation architecture” omits trust, mapping, lifecycle, and authorization.
- “A verified email is an identity key” ignores issuer and reassignment.
- “Subject is globally unique” ignores issuer scope.
- “Same person means same external ID” ignores pairwise IDs and issuer migration.
- “Discovery metadata is automatically trusted” permits malicious issuer/endpoints.
- “TLS proves the IdP is authorized” confuses channel identity with federation trust.
- “A valid signature is sufficient” omits issuer, audience, time, nonce, and transaction.
- “JWT header chooses the key source” enables untrusted key resolution.
- “ID token authorizes APIs” confuses authentication assertion with access token.
- “One access token can be forwarded everywhere” breaks audience and delegation.
- “Login success grants tenant access” skips membership and resource authorization.
- “IdP group name is a platform role” ignores collision, freshness, and local policy.
- “All groups fit in a token” ignores size and overage behavior.
- “JIT handles termination” learns only on another login.
- “SCIM delivery never misses” requires reconciliation and idempotency.
- “Disable and delete are interchangeable” can destroy audit/ownership history.
- “Logout revokes every token/session” overstates protocol behavior.
- “MFA claim is comparable across issuers” ignores assurance contracts.
- “Step-up permanently makes a user trusted” should bind stronger context narrowly.
- “Long clock skew improves reliability” enlarges replay window.
- “Unknown key means accept after arbitrary fetch” creates key/SSRF risk.
- “Cached claims can survive any outage” turns stale data into indefinite privilege.
- “Federation broker removes upstream identity” risks collision and lost assurance.
- “Break-glass is a shared admin password” defeats accountability and protection.
- “Non-production IdP can share production client” risks cross-environment tokens.
- “Removing login button retires an IdP” leaves mappings, sessions, SCIM, keys, and clients.

## Worked Examples

### Example 1

Two partner IdPs issue subject `123`. The platform stores `(issuer-a,123)` and `(issuer-b,123)` as different external identities. They map to different local principals even if display names match.

A deliberate linking ceremony could map both to one person, but only with reauthentication, authoritative evidence, audit, and conflict checks.

### Example 2

An employee leaves and email `sam@example.com` is reassigned. New user has a different subject. Email-keyed linking would inherit production ownership; issuer-subject mapping creates a new local principal and triggers ownership transfer workflow for the old account.

The old principal remains disabled/tombstoned for audit and is never recycled.

### Example 3

Portal receives an ID token for client `portal-web`; API accepts it because signature is valid. This violates audience/token-use boundary. API instead requires its own audience-bound access token and validates issuer, audience, time, scope, client/actor, and tenant authorization.

The portal backend uses constrained token exchange rather than forwarding an ambient token.

### Example 4

A login starts with trusted issuer A, but callback contains token from trusted issuer B with same client. Exact transaction-to-issuer binding rejects the mix-up, even though B is valid elsewhere.

Home-realm selection, state, nonce, PKCE, callback, and issuer configuration are stored in one-time transaction state.

### Example 5

SCIM disables user, but a missed webhook leaves an eight-hour portal session and cloud role. Periodic reconciliation compares authoritative directory, local accounts, sessions, tokens, and roles; it revokes stale access and measures disable-to-denial exposure.

High-risk roles use shorter tokens/current checks, reducing the window.

### Example 6

One user belongs to tenant A and B. Login authenticates the person; portal selection chooses B; every backend verifies current B membership and resource ownership. A URL parameter alone cannot switch tenant.

Audit records local principal, external identity reference, selected tenant, delegated service, policy, and action without logging raw assertion.

### Example 7

IdP rotates signing keys with overlap. RP accepts old/new allowlisted algorithm keys during the planned window, refreshes issuer-bound JWKS on unknown `kid` under rate limit, and removes old key after maximum token lifetime plus policy margin.

An arbitrary `jku` in a token is ignored. Rotation and rollback are tested before production.

### Example 8

Production deletion requires phishing-resistant step-up within five minutes. RP requests/validates the contracted authentication context and binds approval to one operation/resource. It does not convert the whole day-long session into permanent elevated privilege.

If IdP step-up is unavailable, deletion fails closed; break-glass follows separate incident procedure.

### Example 9

IdP outage prevents new login during incident. Existing low-risk sessions continue within absolute lifetime; high-risk operations requiring fresh context stop. Individually assigned recovery identities with hardware authenticators and narrow emergency roles restore only necessary control.

Every use alerts and is audited; recovery credentials are drilled and rotated.

### Example 10

Organization moves from issuer old to new. HR supplies verified subject mapping; cohorts authenticate to new issuer and resolve the same immutable local principals. Conflicts quarantine, not email-merge.

After migration, old sessions/tokens/SCIM/clients/callbacks/keys are revoked; audit/mapping tombstones remain; restore test confirms old trust cannot return.

## Cross-Program Connections

- **Security Engineering:** authentication protocols, phishing resistance, token validation, sessions, confused deputies, least privilege, and incident response define federation safety.
- **Cryptography:** signatures, algorithms, keys, TLS, nonce, entropy, rotation, and bounded validity protect assertions and clients.
- **API and Service Engineering:** OAuth audiences/scopes, token exchange, resource servers, redirects, error handling, and revocation connect identity to APIs.
- **Distributed Systems:** clocks, caches, replication, missed events, reconciliation, partial outage, and revocation latency shape lifecycle guarantees.
- **Data Engineering:** directory/SCIM synchronization, identity lineage, conflict resolution, change capture, and deletion govern replicated attributes.
- **Platform Engineering:** portals, tenants, policy enforcement, cloud roles, provisioning, and break-glass consume the federated principal.
- **Privacy Engineering:** minimization, pairwise identifiers, correlation, consent/notice, retention, and correction limit federation data exposure.
- **Reliability Engineering:** IdP/session dependencies, bounded degraded mode, SLOs, key rotation, failover, and recovery identities preserve access safely.
- **Governance and Compliance:** trust agreements, assurance profiles, separation of duties, audit, termination SLAs, and periodic access review make federation accountable.
- **Human Factors:** home-realm discovery, account linking, step-up friction, recovery, error disclosure, and logout expectations affect secure user behavior.

## References

1. OpenID Foundation. [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html). November 2014. Retrieved 2026-09-02.
2. OpenID Foundation. [OpenID Connect Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html). Retrieved 2026-09-02.
3. IETF. [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://datatracker.ietf.org/doc/html/rfc9700). January 2025. Retrieved 2026-09-02.
4. IETF. [RFC 7636: Proof Key for Code Exchange](https://datatracker.ietf.org/doc/html/rfc7636). September 2015. Retrieved 2026-09-02.
5. IETF. [RFC 8693: OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693). January 2020. Retrieved 2026-09-02.
6. IETF. [RFC 7519: JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519). May 2015. Retrieved 2026-09-02.
7. IETF. [RFC 8414: OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414). June 2018. Retrieved 2026-09-02.
8. IETF. [RFC 7643: SCIM Core Schema](https://datatracker.ietf.org/doc/html/rfc7643). September 2015. Retrieved 2026-09-02.
9. IETF. [RFC 7644: SCIM Protocol](https://datatracker.ietf.org/doc/html/rfc7644). September 2015. Retrieved 2026-09-02.
10. NIST. [SP 800-63-4: Digital Identity Guidelines](https://pages.nist.gov/800-63-4/sp800-63.html). July 2025. Retrieved 2026-09-02.
11. NIST. [SP 800-63C-4: Federation and Assertions](https://pages.nist.gov/800-63-4/sp800-63c.html). July 2025. Retrieved 2026-09-02.
12. OASIS. [SAML Version 2.0 Technical Overview](https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html). March 2008. Retrieved 2026-09-02.
13. OWASP. [OAuth 2.0 Protocol Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html). Retrieved 2026-09-02.
14. Kubernetes. [Authenticating](https://kubernetes.io/docs/reference/access-authn-authz/authentication/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define a federation trust profile for a platform portal and API using OIDC. Include registration, flow, callbacks, keys/algorithms, assertion validation, tokens, sessions, assurance, attributes, errors, and lifecycle.

### Exercise 2

Design account resolution for employees, contractors, partner IdPs, rehires, email changes, and users belonging to several tenants. Include collision, linking, unlinking, and recovery.

### Exercise 3

Design SCIM/JIT provisioning and end-to-end deprovisioning across portal, APIs, cloud roles, tenant memberships, sessions, tokens, approvals, and in-flight workflows.

### Exercise 4

Threat-model a federation broker supporting twelve IdPs and forty RPs. Cover mix-up, substitution, discovery, key rotation, attribute authority, privacy, outage, compromise, and break-glass.

### Exercise 5

Plan migration from one IdP to another for 50,000 users without using email as the identity key. Include mapping evidence, cohorts, conflicts, sessions, provisioning, rollback, and retirement.

## Answers to the Exercises

### Answer 1

Register exact issuer, discovery/authorization/token/JWKS endpoints, client ID, confidential-client authentication, exact HTTPS callbacks, authorization code flow, PKCE, state, nonce, allowed signed algorithms/keys, requested minimal claims, assurance, logout behavior, contacts, and rotation/retirement.

Store one-time browser transaction binding with issuer, state/nonce, PKCE verifier, callback, expiry. Validate response/code exchange, exact issuer, signature/algorithm/issuer-bound key, audience and authorized party, expiry/not-before/issued-at/skew, nonce, and required authentication context. Reject unsolicited/wrong environment/malformed response without logging it.

ID token creates client session only after issuer-subject account resolution. API accepts audience-bound access token and authorizes tenant/action/resource. Session has high-entropy rotated ID, secure cookie, idle/absolute lifetime, authentication time/context, revocation and step-up. Profile covers metadata/key/client-secret rotation, outage, privacy, audit, and decommission.

### Answer 2

Create immutable local principal and external mapping keyed by exact `(issuer,subject)`. HR/directory pre-provisions employee mapping using authoritative immutable employee relation; contractors have sponsor/expiry; each partner issuer has separate trust/mapping. Email/name/login are contact/display attributes only.

Rehire receives the same local principal only when authoritative HR policy proves continuity; otherwise new principal. Email change updates attribute, not key. Multi-tenant membership is separate, current, and selected/revalidated after login.

Linking a new external identity requires fresh authentication to existing account plus new IdP or administrator-authoritative migration, conflict check, notification, audit, and recovery. High-risk links may require dual approval. Collision quarantines; never merge audit/resources silently. Unlink prevents removing last recovery/auth path accidentally and revokes sessions tied to compromised mapping.

### Answer 3

SCIM authority pre-creates immutable principal, status, stable group IDs/memberships, sponsor/expiry, and tenant mappings. JIT may create only minimal account when mapping is unambiguous; privileged roles require pre-provision/approval. SCIM/login writes use versions and deterministic precedence.

Disable event blocks IdP login, marks local principal/membership disabled, revokes RP sessions/refresh tokens, shortens/introspects access tokens by risk, removes platform/cloud roles, cancels pending approval/delegation, and tells durable workflows whether to continue under service authority or stop. Preserve actor history.

Authenticate/authorize SCIM client per tenant, validate schema/filter/PATCH/bulk, use idempotency and audit. Periodic full reconciliation repairs missed events. Measure authoritative disable to denial across every surface and alert on breach. Hard deletion follows retention/ownership/legal policy separately.

### Answer 4

The broker is IdP to downstream RPs and RP to upstream IdPs. Preserve unique upstream `(issuer,subject)`, authentication time/context, assurance, and transaction provenance; issue new downstream issuer/subject/audience assertions under explicit mapping. Bind each login to selected upstream issuer and downstream RP to prevent mix-up/substitution.

Allowlist metadata/endpoints/algorithms/keys and callbacks; prevent SSRF/dynamic arbitrary issuer; isolate tenants/environments; rate-limit safe key refresh with overlap. Define authoritative attributes and conflicts, group bounds, pairwise IDs/minimal disclosure, logs/retention, and no cross-RP token reuse.

Model compromise of broker key/admin as all-RP blast radius; use HSM/segmented keys, dual control, short assertions, rapid revocation, monitoring, and drills. Redundant broker/IdP dependencies and bounded sessions handle outages. Separate narrow individually accountable break-glass identities bypass only needed federation functions, not domain authorization.

### Answer 5

Inventory old issuer-subject mappings, immutable local principals, tenants, privileged roles, groups, sessions/tokens, clients/callbacks, SCIM, service integrations, keys, and owners. Obtain authoritative old-subject-to-new-subject mapping from HR/directory or controlled dual-authentication ceremony; email is corroboration only.

Configure/test new issuer profile and provisioning. Pre-stage mappings with uniqueness/conflict validation. Migrate low-risk cohorts, then privileged/complex users, resolving to the same local principal and testing tenants, roles, step-up, sessions, token audiences, SCIM changes, and deprovisioning. Quarantine unmapped/duplicate/conflicting records.

Maintain explicit dual-trust window and rollback without allowing independent privilege changes through duplicate identities. Observe adoption and old use. Then revoke old sessions/tokens, stop old SCIM, disable clients/callbacks, rotate/remove secrets/keys/trust, notify owners, retain audit and mapping tombstones, and test restore cannot re-enable the old issuer.
