---
module_id: API-044
program: API & Service Engineering
level: 1
module_number: 44
title: Applying OpenID Connect at API Boundaries
status: complete
last_verified: 2026-09-01
---

# Applying OpenID Connect at API Boundaries

## One-Page Review

### Governing question

How should a client and API use OpenID Connect authentication identity, OAuth access authority, claims, assurance, tenant context, and sessions without accepting the wrong token, linking the wrong account, or turning mutable profile data into authorization?

### Essential definitions

- **OpenID Connect (OIDC)** is an identity layer over OAuth 2.0 that lets a relying party verify an end-user authentication and obtain claims.
- An **OpenID Provider (OP)** is the authorization server performing OIDC; a **Relying Party (RP)** is the OAuth client using that authentication.
- An **ID token** is a signed JWT making authentication claims to the RP whose client identifier is its audience.
- An **access token** carries/references authority for a resource server; it is not an ID token.
- The **subject identifier** (`sub`) identifies the end user locally at an issuer; the durable principal key is the pair (`iss`, `sub`).
- A **claim** is an assertion about a subject or authentication event; its semantics, provenance, stability, and freshness determine safe use.
- `auth_time` records when end-user authentication occurred; `acr` identifies an authentication-context class; `amr` records methods used.
- `nonce` binds an OIDC authentication response/ID token to the initiating client transaction and helps prevent replay/substitution.

### Central model, mechanism, or theorem

Represent RP authentication context as

$$
C=(iss,sub,aud,azp,auth\_time,acr,amr,claims,session),
$$

constructed only after ID-token validation. For expected issuer $I$, client ID $c$, nonce $n$, and time $t$:

$$
V_{ID}=V_{sig}\land iss=I\land c\in aud\land V_{azp}\land t<exp\land V_{iat}\land nonce=n\land V_{policy}(auth\_time,acr,amr).
$$

At the API boundary, use a separate access-token validation profile $V_{AT}$ requiring the API audience and token purpose. Then authorize request $x$ with local state:

$$
\operatorname{allow}(x)=V_{AT}\land P(C_{AT},x,resource,state).
$$

The RP's valid ID token does not satisfy $V_{AT}$.

### Critical invariants

OIDC is requested with `openid` and processed as a complete profile, not inferred from generic OAuth. ID tokens are consumed by the RP and access tokens by the resource server. Token kinds have mutually exclusive validation rules and audiences. Issuer and key ownership are preconfigured or safely discovered and compared exactly. The durable external identity is (`iss`, `sub`), never email or username alone. `nonce`, state/PKCE, issuer checking, and redirect checks retain distinct purposes. Authentication time/assurance is evaluated for the requested action rather than inferred from token issue time or method labels. UserInfo `sub` matches the ID-token `sub`. Claims are minimized and classified by provenance/stability; mutable claims do not silently grant authority. Tenant membership and object permission come from authoritative policy. Logout/session termination and access-token revocation are described separately.

### Common failures

Sending an ID token to an API; accepting an access token as proof that a client logged in; keying users by email; auto-linking accounts from an unverified or recycled address; validating a JWT signature but not issuer/audience/nonce/time; following attacker-selected discovery/JWKS URLs; accepting any `acr` string or treating `amr` as assurance; using `iat` as authentication freshness; letting a body/header choose tenant over verified context; accepting UserInfo for a different subject; stuffing all profile data/groups into tokens indefinitely; logging tokens or sensitive claims; assuming OP logout revokes API tokens; and merging subjects from different issuers.

### Compact example

A web RP starts code+PKCE OIDC with expected issuer, nonce, and freshness requirement. It validates the returned ID token's configured algorithm/signature, exact issuer, client audience/`azp`, times, nonce, and approved `acr`, then maps (`https://id.example`, `248289761001`) to its local account. Its backend calls the orders API with a distinct access token whose audience is `orders-api`. The API validates that token and checks tenant/object permission. **Conclusion:** one authentication produces related artifacts for different recipients; neither recipient accepts the other's token.

### Connections

[OAuth Authorization Flows](043-oauth-authorization-flows.md) supplies the secure code transaction and [Credential and Token Handling](042-credential-and-token-handling.md) supplies token lifecycle rules. [Authentication Context Propagation](033-authentication-context-propagation.md) carries verified access-token context, while [Scope and Permission Design](../ROADMAP.md) and [Object-Level Authorization](../ROADMAP.md) turn that context into bounded decisions.

## Governing Question

Which component is the intended recipient of each OIDC/OAuth artifact, which exact validation and identity semantics apply, how are authentication assurance and freshness proven, and how does the API combine verified context with current local authorization?

## Why This Matters

OIDC solves a specific gap: OAuth defines delegated access but does not by itself provide an interoperable statement that a client can use to establish an end-user login. OIDC adds an ID token and claim semantics. That addition does not make every token interchangeable or centralize every authorization decision at the identity provider.

Many serious boundary failures come from collapsing distinctions. An API accepts an ID token because it is a signed JWT, even though its audience is the web client. A client treats an opaque access token as user identity. Two issuer accounts sharing an email are merged. A `groups` claim copied at login remains administrative authority after removal. An RP checks `iat` rather than `auth_time` and calls a refreshed token “fresh authentication.” An `amr` value like `pwd` is treated as organization-approved assurance without a policy mapping.

OIDC also spans several lifecycles. Authentication session at the OP, local RP session, OAuth grant/refresh token, access token, user provisioning, tenant membership, and API domain state can expire or be revoked independently. A user clicking logout expects a simple outcome, but the system must state which of these states changed and when.

Applying OIDC at API boundaries therefore means more than validating an ID token. It means assigning each artifact to its recipient, creating a stable local identity safely, translating claims into a minimal authoritative context, evaluating freshness and assurance for the action, and retaining local authorization at the resource server.

## Prerequisites and Retrieval

Retrieve OAuth roles and authorization code with PKCE, JWT/JWS validation, issuer/audience/key distribution, access versus ID tokens, nonce/state, subject identifiers, public/pairwise subjects, authentication context and methods, sessions/cookies, UserInfo, discovery metadata, scopes/claims, tenant membership, account linking, step-up authentication, logout, token revocation, provisioning, privacy, and object authorization.

Before integration, retrieve trusted OP issuers and metadata bootstrap, RP client IDs/types/redirects, code-flow controls, accepted signing algorithms/keys, ID-token profile, access-token profile per API, subject type, local account mapping, multi-issuer/account-link policy, claim catalogue/provenance/stability, email-verification semantics, tenant source, required `acr` values and meaning, acceptable `amr` combinations if used, freshness/max-age rules, clock bounds, UserInfo need, session lifetimes, refresh/offline access, logout/revocation behavior, provisioning/deprovisioning source, privacy/retention, and incident/recovery ownership.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish OIDC authentication from OAuth delegation and API authorization;
2. assign ID tokens, access tokens, UserInfo, and sessions to their intended recipients;
3. validate ID tokens using issuer, key, audience/`azp`, time, nonce, and authentication policy;
4. use (`iss`, `sub`) for identity and design safe account linking and tenant binding;
5. interpret claims, `auth_time`, `acr`, and `amr` without overstating assurance or freshness;
6. design step-up, session, logout, revocation, and provisioning boundaries; and
7. test substitution, mix-up, linking, stale claims, tenant crossing, and lifecycle failures.

## Core Exposition

### Keep the protocols and roles distinct

OIDC is invoked by including the `openid` scope in an OAuth authorization request and following the OIDC profile. The OAuth authorization server becomes an OpenID Provider; the client becomes a Relying Party. The OP returns an ID token to the RP, commonly through the authorization code flow's token response.

Three questions remain separate:

1. **Authentication:** what evidence lets the RP conclude that a particular OP subject authenticated under stated context?
2. **Delegated access:** what API authority did the authorization server issue to the client as an access token?
3. **Authorization:** may the verified actor/client perform this action on this resource now under local policy?

The ID token answers the first for its RP. The access token participates in the second at its resource server. The resource server answers the third using verified token context plus current data/policy. The authorization server may issue permissions/scopes, but it usually cannot know every target object's state and relationship.

Do not use OIDC where no human authentication is involved. A client-credentials token represents a client/workload; inventing an ID token or `sub` that looks like a user obscures authority. Conversely, a user-facing application that needs login identity should not reverse-engineer it from an access token whose format and claims are resource-server concerns.

### Draw the artifact-recipient matrix

Before implementation, write an explicit matrix:

| Artifact | Issuer/presenter | Intended recipient | Purpose |
|---|---|---|---|
| authorization code | OP via browser, then RP | OP token endpoint | one-time bound grant intermediary |
| ID token | OP | RP client ID | authentication event and subject claims |
| access token | authorization server via client | named resource server/API | delegated/client API authority |
| refresh token | authorization server via client | authorization server token endpoint | renew bounded access |
| UserInfo request token | OP via RP | OP UserInfo endpoint | authorized claims retrieval |
| RP session cookie | RP via browser | RP | local application session |

This matrix catches token substitution early. An ID token audience normally contains the RP's client ID, not `orders-api`; the orders API rejects it. An API access token might be a JWT with identity-like claims, but the RP does not accept it as an ID token because its type, audience, nonce, and profile differ. A refresh token never reaches the API.

Use mutually exclusive validation profiles as RFC 8725 recommends: explicit token types where defined, different audience/required claims/keys where useful, and separate library entry points/configuration. Avoid a generic `validateJwt()` returning a trusted user for every JWT.

### Establish trusted issuer configuration

An RP begins with a trusted issuer identifier selected by product/tenant configuration, not an arbitrary login form URL. It can retrieve OIDC Discovery metadata from the issuer's well-known location, but it must compare the metadata `issuer` exactly with the issuer used to fetch/configure it and use only trusted endpoints/keys under SSRF and transport controls.

Pin the relationship among issuer, authorization endpoint, token endpoint, UserInfo endpoint, and `jwks_uri`. Bound metadata/key sizes, redirects, DNS/address ranges where needed, cache lifetime, and refresh. Token `kid`, `jku`, or claim URLs never cause arbitrary fetch. Key rotation accepts configured issuer keys through a controlled overlap, not any key that verifies a token.

Multi-issuer clients store the expected issuer with each authorization transaction and validate the response/code/token against it to prevent mix-up. Do not infer issuer from an unverified ID-token payload and then fetch its keys. Parse untrusted metadata only for bounded routing within a preapproved issuer set.

Availability matters: discovery/JWKS outage, stale caches, newly introduced keys, and emergency key compromise need policy. A cache may continue validating already known keys for a bounded period, but must not trust stale revoked authority forever or disable issuer/audience checks to recover service.

### Validate the OIDC authorization transaction

Use the secure authorization code with PKCE flow from API-043. The RP creates a one-time transaction containing expected issuer, client ID, exact redirect, PKCE verifier/challenge, `state`/CSRF property, OIDC `nonce`, requested claims/scopes, freshness/assurance request, post-login destination, and expiry.

The values are not interchangeable. PKCE binds code redemption; `state` can correlate/defend the authorization response; issuer validation prevents mix-up; `nonce` binds the ID token to the initiating authentication request. The exact redirect constrains delivery. Preserve each property unless an explicit profile proves another mechanism satisfies it.

At callback, verify the expected issuer/correlation and exchange the one-time code only at its bound token endpoint with exact redirect, verifier, and client authentication where applicable. Validate the token response before establishing a session. Do not create a partial logged-in session from unverified claims displayed in a browser parameter.

Use modern OAuth/OIDC security guidance rather than older implicit/hybrid examples merely because OIDC Core documents them. New browser/native designs use code+PKCE and keep tokens out of front-channel URLs unless a specialized current profile requires otherwise.

### Validate the ID token for this RP

ID-token validation follows the exact OIDC flow/profile and client registration. At minimum for a code-flow token:

1. bound size/encoding and use a maintained JOSE/OIDC library;
2. select a server-configured acceptable signing algorithm and key belonging to the exact trusted issuer;
3. validate the cryptographic signature (and decryption/nested processing when configured);
4. require exact `iss`;
5. require the RP client ID in `aud`;
6. if multiple audiences are present, validate `azp` according to OIDC rules and require this client where applicable;
7. require current time before `exp`, validate `iat` under policy, and use small documented clock skew;
8. compare the one-time `nonce` exactly when sent/required by the flow;
9. validate `auth_time`, `acr`, and other requested essential authentication properties under local policy; and
10. validate any flow-dependent token/hash claims required by the selected profile.

Do not read `sub`, email, groups, or tenant as trusted before signature/issuer/audience/time/transaction validation. The token header's algorithm and key identifiers are untrusted selectors constrained by configuration. Reject `none`, key-type confusion, missing required claims, duplicate/ambiguous JSON, wrong types, and unexpected token kinds.

An ID token says the OP authenticated its subject and issued these claims to this RP. It does not say the subject may access every RP feature or API object. It may also not prove the human identity level your action requires unless `acr`/policy evidence does.

### Use issuer and subject as the durable external key

The `sub` claim is locally unique and never reassigned within the issuer under OIDC's contract, but it is not globally meaningful without `iss`. Store the external principal key as the exact tuple (`iss`, `sub`). Treat strings as case-sensitive according to specification; do not lowercase, trim, parse, or combine them into an ambiguous delimiter string.

An issuer can use **public** subject identifiers consistent across clients or **pairwise** identifiers different per sector/client to reduce correlation. The same human can therefore have different `sub` values across RPs, and two issuers can use the same textual `sub` for different people. Do not attempt to reverse or correlate pairwise subjects.

Map (`iss`, `sub`) to an internal immutable principal ID. Internal records, audit, memberships, and ownership reference that local ID. Profile attributes can change without rewriting identity. If issuer migration changes identifiers, run an explicit verified account-migration process with proof from both trusted domains or administrative evidence—not fuzzy claim matching.

### Treat account linking as a privileged transition

Account linking joins two authentication paths to one local principal, so a mistake grants account takeover. Never auto-link solely because email strings match. Addresses can be unverified, recycled, reassigned, normalized differently, controlled through an attacker-added alias, or scoped differently across issuers. Even `email_verified=true` describes the OP's verification claim under its policy; it does not prove the address is a permanent global person identifier or that another account should merge.

Safe linking requires an explicit policy and proof of control of both existing local/authenticated accounts, or a trusted enterprise provisioning/admin assertion with audit and recovery. Show which issuers/accounts are linked, require recent/step-up authentication for changes, notify the user, prevent silent login-CSRF linking, and provide revocation/recovery.

For just-in-time provisioning, create a local account only for allowlisted issuers/tenants and policy-approved subjects. Do not let any discoverable issuer create production accounts. Decide how disabled/deprovisioned local accounts behave even when the OP still authenticates successfully.

### Classify claims by semantics and provenance

Build a claim catalogue with source, meaning, type, sensitivity, stability, freshness, verification, allowed consumers, conflict rule, and authorization use. Common standard claims include `name`, `preferred_username`, `email`, `email_verified`, locale, and picture. Most are profile/display information, not immutable identifiers.

- `email` may change and can be sensitive; pair it with issuer semantics and `email_verified`, but still avoid identity linking by email alone.
- `preferred_username` is human-friendly and mutable; never use it as a database/security key.
- `name` and picture are display data requiring output encoding/content/privacy controls.
- custom `groups`, `roles`, `tenant`, or entitlements are only meaningful under a documented issuer contract and freshness/lifecycle model.

Minimize requested scopes/claims. The `openid` scope enables OIDC; `profile`, `email`, and other scopes request claim sets but do not guarantee every claim. Avoid putting full group directories, private profiles, or unnecessary personal data in every ID/access token. Tokens are visible to holders and copied into client memory/caches.

When multiple sources supply the same concept—ID token, UserInfo, enterprise directory, local account, access token—define precedence and staleness. Do not merge claims into a mutable dictionary where later untrusted input overwrites authoritative tenant/role data.

### Validate UserInfo as a separate protected call

The RP can call the OP's UserInfo endpoint with an access token intended for it to obtain authorized claims. Validate TLS/endpoint, token use, response type/signature when configured, schema/types, and privacy bounds. OIDC requires the UserInfo response `sub` to exactly match the ID token `sub`; reject the entire response on mismatch.

UserInfo may provide fresher profile claims than the ID token but is not automatically a real-time authorization directory. Its availability, caching, consent, scope, and update semantics need definition. Do not call it on every API request unless the architecture accepts latency/privacy/availability coupling.

Keep UserInfo access token and claims out of resource APIs unless explicitly needed. The API should receive its own audience-bound access token and minimal context, not the RP's ID token or whole UserInfo response forwarded in headers.

### Interpret authentication freshness and assurance correctly

`iat` says when the token was issued; it is not necessarily when the user last authenticated. A token can be newly minted from an old OP session. Use `auth_time` to evaluate authentication age when a high-risk action needs freshness, and request `max_age`/appropriate OIDC parameters so the OP is obligated to return/perform the needed authentication behavior.

`acr` identifies the Authentication Context Class Reference achieved. Its string is meaningful only through an issuer/client policy mapping: which authenticators, phishing resistance, identity proofing, device posture, and exception paths qualify? Require one of the explicitly approved values for a protected action. Do not compare unknown values lexicographically or assume a larger number is stronger.

`amr` lists Authentication Methods References used, such as password or OTP under the OP vocabulary. It is evidence, not a universal assurance scale. The combination `pwd` plus `otp` may or may not meet local phishing-resistant policy. Prefer `acr` contractual assurance with `amr` used for diagnostics/risk only under documented semantics.

For step-up, bind the initiating user/client/session/action/transaction, send an authentication request with required freshness/context, validate returned issuer/subject/nonce/`auth_time`/`acr`, and ensure it upgrades the same local principal. An attacker must not step up their own subject then attach the result to a victim's transaction.

### Build a minimal immutable context

After validation, map the ID token to an RP authentication result containing local principal ID, external (`iss`, `sub`), client ID, authentication time/context/methods, session identifier where applicable, and minimal approved display claims. Mark provenance and do not retain the raw token longer than needed.

For API calls, validate the distinct access token at the resource server and construct context containing issuer, subject/client, effective actor, tenant memberships/selection, token audience/scope/entitlements under issuer contract, sender binding, token/session safe identifiers, and relevant assurance/freshness evidence. The API trusts only fields produced by its validator/policy adapters.

If an access token's `sub` represents the same end user, map it according to the issuer/access-token profile—not merely because it textually matches the ID token. Client credentials may have no end-user subject. Token exchange/delegation can have actor and subject chains; preserve them explicitly.

Never copy `X-User`, `X-Tenant`, `X-Groups`, or an ID-token payload from an untrusted gateway request into context. Forwarded context requires authenticated service identity, integrity protection, audience, expiry, replay considerations, and stripping of public spoofed headers as covered in API-033.

### Keep tenant selection and authorization local

An external identity may belong to several local organizations. Tenant selection is a local application/API transition bound to verified memberships, not a free claim/body/header. Validate that (`iss`, `sub`) maps to a local principal with active membership, then bind the chosen tenant to session/access context. Recheck membership for sensitive/current actions according to revocation latency.

Issuer domain or email domain is not automatically tenant membership. A hosted-domain/custom claim may support policy only under a documented trusted issuer contract. Invitations, transfers, mergers, guests, and multi-tenant administrators create cases that string suffix checks cannot handle.

Scopes, groups, roles, and entitlements can be inputs to authorization, but local policy still evaluates action, target object, tenant, relationships, state, delegation, and risk. Avoid mapping every IdP group to a global application role. Use a governed mapping with owners, collision rules, maximum privilege, deprovisioning, evidence, and tests.

### Separate sessions, logout, revocation, and provisioning

Track at least these states:

- OP browser authentication/SSO session;
- RP local application session/cookie;
- OIDC/OAuth authorization grant and refresh token;
- issued access tokens at resource servers;
- local account status and tenant memberships; and
- external provisioning/directory state.

Ending one does not necessarily end the others. RP logout can clear the local session and tokens. RP-Initiated Logout can ask an OP to end its session under the selected specification, but other RPs/access tokens may remain. Revoking refresh authority stops renewal; self-contained access tokens may remain usable until expiry unless resource servers consult state. Disabling a local account must cause RP/API authorization denial even if the OP still authenticates it.

Document the user-visible logout guarantee and maximum revocation/deprovisioning latency. Back-channel/front-channel logout or session-management profiles, if adopted, add endpoint, delivery, replay, correlation, and availability considerations. Do not improvise logout by redirecting to an arbitrary OP URL with an ID token in logs.

Provisioning protocols/directories are separate from OIDC login. Just-in-time creation is easy but may not convey reliable removal, manager, license, or group lifecycle. For enterprise access, combine authentication with authoritative provisioning/deprovisioning and local policy rather than expecting login claims to be the entire identity lifecycle.

### Protect privacy and observability

Use pairwise subjects where appropriate and minimize claim release by client/purpose. Explain profile/tenant data use, retention, and sharing. Avoid cross-client correlation, global analytics identifiers, and copying raw tokens/claims into logs, traces, metrics, data warehouses, support tickets, or URLs.

Log safe issuer/client/outcome classes, local principal opaque ID under access policy, authentication age/assurance decision, and a correlation identifier. If token/session correlation is needed, use a keyed safe digest or issuer-provided non-secret identifier under privacy governance. Never log raw ID/access/refresh tokens, authorization codes, nonce, session cookies, or sensitive UserInfo.

Detect issuer/key/nonce/audience failures, account-link changes, unusual new issuer/subject pairs, assurance downgrades, stale/deprovisioned access, UserInfo subject mismatch, repeated step-up failure, logout/revocation failures, and cross-tenant denials. Avoid raw subjects/claims as unbounded metric labels.

### Handle errors and recovery without disclosure

Authentication errors at the RP distinguish internally among issuer, signature/key, audience, nonce, time, assurance, transaction, and account-state failures, but public responses remain generic enough not to reveal account existence, membership, or security policy. Preserve correlation for support.

Do not automatically retry with weaker `acr`, omit nonce, accept an old key forever, switch issuer, or create a new account on validation failure. Recovery starts a fresh transaction with explicit user intent. If the OP or key endpoint is unavailable, use a bounded cached trust policy or fail safely; never accept unverified identity to preserve availability.

Account recovery and issuer migration are high-authority workflows requiring recent proof, notification, audit, cooling-off/rollback where appropriate, and operator separation. A support agent should not edit (`iss`, `sub`) casually based on an email screenshot.

The executable model below illustrates claim-level ID-token policy after cryptographic verification. It does not perform JOSE, OAuth, discovery, or API access-token validation.

<!-- bijux-verify: {"id":"oidc-id-token-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=accept\nwrong_audience=reject:audience\nwrong_nonce=reject:nonce\nstale_auth=reject:freshness\nweak_context=reject:acr\nmulti_audience_wrong_azp=reject:azp\n","stderr":""}} -->
```python
POLICY = {
    "issuer": "https://id.example",
    "client_id": "orders-web",
    "nonce": "transaction-nonce-7",
    "accepted_acr": {"urn:example:acr:strong"},
    "max_auth_age": 300,
}

def validate_id_token(claims, now):
    if claims.get("iss") != POLICY["issuer"]:
        return "reject:issuer"
    audiences = claims.get("aud", [])
    if POLICY["client_id"] not in audiences:
        return "reject:audience"
    if len(audiences) > 1 and claims.get("azp") != POLICY["client_id"]:
        return "reject:azp"
    if not claims.get("iat", now + 1) <= now < claims.get("exp", 0):
        return "reject:time"
    if claims.get("nonce") != POLICY["nonce"]:
        return "reject:nonce"
    if now - claims.get("auth_time", 0) > POLICY["max_auth_age"]:
        return "reject:freshness"
    if claims.get("acr") not in POLICY["accepted_acr"]:
        return "reject:acr"
    return "accept"

base = {
    "iss": "https://id.example",
    "sub": "248289761001",
    "aud": ["orders-web"],
    "iat": 990,
    "exp": 1100,
    "nonce": "transaction-nonce-7",
    "auth_time": 900,
    "acr": "urn:example:acr:strong",
}

print("valid=" + validate_id_token(base, 1000))
print("wrong_audience=" + validate_id_token({**base, "aud": ["orders-api"]}, 1000))
print("wrong_nonce=" + validate_id_token({**base, "nonce": "other"}, 1000))
print("stale_auth=" + validate_id_token({**base, "auth_time": 600}, 1000))
print("weak_context=" + validate_id_token({**base, "acr": "urn:example:acr:basic"}, 1000))
print("multi_audience_wrong_azp=" + validate_id_token({**base, "aud": ["orders-web", "other"], "azp": "other"}, 1000))
```

Real validation must apply the exact OIDC specification/profile before claims become trusted. The model deliberately shows that the orders API audience is wrong for the orders web RP's ID token.

### Verify boundaries, claims, and lifecycle

Build independent suites for the OIDC transaction, ID-token RP validation, access-token resource-server validation, account mapping/linking, claims, assurance/step-up, tenant authorization, UserInfo, sessions/logout, provisioning, privacy, and operations.

Negative token tests cover wrong issuer/key/algorithm, wrong/multiple audiences and `azp`, missing/malformed subject/time/nonce, expired/future tokens, nonce replay, ID/access/refresh token substitution, hostile `kid`/URL, stale/new keys, discovery mismatch, and profile-specific claims. Transaction tests cover CSRF, mix-up, redirect, code injection/replay, and login CSRF.

Identity tests create identical subjects under different issuers, changed/recycled/unverified email, pairwise subjects, Unicode/case boundaries, issuer migration, linking CSRF, both-account proof, disabled accounts, duplicate JIT creation races, and recovery. Claims tests cover missing/wrong types, stale groups, conflicting sources, excessive data, and UserInfo `sub` mismatch.

Assurance tests distinguish `iat` from `auth_time`, unknown/downgraded `acr`, misleading `amr`, step-up for the wrong subject/session/action, clock boundary, and OP exception paths. Lifecycle tests exercise RP logout, OP logout, refresh revocation, access-token residual life, directory deprovisioning, key/metadata outage, and incident recovery. Scan every artifact/telemetry destination for seeded sensitive tokens and claims.

## Definitions and Notation

Let authentication context $C=(iss,sub,aud,azp,auth\_time,acr,amr,claims,session)$. The durable external principal is ordered pair $p=(iss,sub)$; equality requires both exact strings. Let $V_{ID}$ be the RP's ID-token validation predicate and $V_{AT}$ the resource server's separate access-token predicate.

Let $P(C,x,r,s)$ be current local authorization policy over context, request/action $x$, resource $r$, and domain/policy state $s$. Token validation authenticates statements for the intended recipient; $P$ decides authority.

**Authentication freshness** is elapsed time since `auth_time`, under trusted OP semantics, not token issuance time. **Authentication assurance** is the locally interpreted guarantee of an approved `acr`/OP policy, not a raw `amr` count. **Pairwise subject** differs between sector/client contexts to reduce correlation. **Account linking** maps multiple authenticated external principals to one local principal and is therefore privilege-changing.

## Mechanisms, Invariants, or Proof Structure

1. Name OP/RP/resource-server roles and draw the artifact-recipient matrix.
2. Bootstrap exact trusted issuer metadata/endpoints/keys; bind issuer to each transaction.
3. Use secure code+PKCE OIDC with distinct state, nonce, issuer, redirect, and client bindings.
4. Validate ID-token cryptography, issuer, audience/`azp`, times, nonce, and requested authentication context before claims.
5. Map exact (`iss`, `sub`) to an immutable local principal; treat linking/provisioning as privileged lifecycle operations.
6. Classify/minimize claims and validate UserInfo subject/provenance rather than merging arbitrary data.
7. Evaluate `auth_time`, approved `acr`, and documented `amr` semantics for action-specific freshness/assurance.
8. Validate access tokens separately at each API and apply current tenant/object/action policy.
9. Define RP/OP sessions, grants, refresh/access tokens, logout, revocation, and provisioning as distinct states.
10. Test substitution, mix-up, linking, stale claims, assurance, cross-tenant access, failures, privacy, and response.

The security claim is bounded by OP trust, registration, OAuth flow, JOSE/OIDC libraries, discovery/key distribution, account lifecycle, local authorization, time, and operational evidence. The finite claim model assumes cryptographic verification and cannot prove these dependencies.

## Alternatives and Trade-Offs

ID-token claims avoid a UserInfo call and bind data to authentication issuance, but can be stale and increase token size/privacy exposure. UserInfo can return updated/consented claims but adds latency, availability, access-token handling, caching, and subject-consistency work. Request only what the client needs.

Public subjects simplify cross-client account correlation within an issuer but expand privacy linkability. Pairwise subjects reduce correlation but complicate legitimate account consolidation/support. Choose from privacy and product relationships, never attempt unofficial reversal.

JIT provisioning reduces administrative lead time but may miss deprovisioning and create duplicates/races. Directory-driven provisioning adds lifecycle accuracy but more integration/state. Enterprise systems often need both with clear authority/precedence.

Embedding roles/groups in tokens makes local decisions fast/offline but creates staleness, size, issuer coupling, and overexposure. Local policy lookup improves current control at latency/availability cost. Short token life, policy versions, and critical-action checks can combine approaches with explicit bounds.

Global logout is appealing but spans independent RP/OP sessions and tokens with unreliable browser channels. Local logout is predictable but narrower. Adopt formal logout profiles only with tested delivery/replay/session correlation and state the actual guarantee.

Strict online metadata/UserInfo/policy lookup improves freshness but couples login/API availability to dependencies. Bounded caches improve resilience but extend stale trust. Define freshness and compromise response per asset rather than “cache forever on failure.”

## Failure Modes and Misconceptions

- **“OIDC and OAuth are the same.”** OIDC profiles OAuth to add authentication; access and identity artifacts remain distinct.
- **“Any signed JWT authenticates a user.”** Recipient, type, issuer, audience, transaction, time, and profile determine meaning.
- **“The API should accept the ID token.”** Its intended recipient is the RP client; the API validates its access token.
- **“Email is the subject.”** Durable identity is exact (`iss`, `sub`).
- **“Verified email makes auto-linking safe.”** Verification does not guarantee global uniqueness, permanence, or merge intent.
- **“`iat` proves recent login.”** Use `auth_time` with requested freshness.
- **“Two factors means strong `acr`.”** Assurance depends on approved authenticator/context policy; `amr` is not a universal level.
- **“Groups in the token are current forever.”** State maximum staleness and deprovisioning behavior.
- **“The IdP tenant claim selects our tenant.”** Map through authoritative local membership/policy.
- **“UserInfo can belong to any authenticated user.”** Its `sub` must exactly match the ID token subject.
- **“Logout revokes all access.”** RP session, OP session, grant, refresh/access tokens, and local account differ.
- **“Discovery means trust any issuer URL.”** Bootstrap an approved issuer and validate metadata/endpoints safely.
- **“Client credentials can use OIDC user claims.”** Machine self-authority is not end-user authentication.
- **“More claims help authorization.”** Excess claims increase privacy, staleness, and confusion.

## Worked Examples

### Example 1

**Situation:** An orders API receives an ID token whose audience is `orders-web`. **Reasoning:** The JWT is valid for the RP, not the API. **Conclusion:** reject it and require an access token audience-bound to `orders-api`.

### Example 2

**Situation:** Issuers A and B both issue `sub="123"`. **Reasoning:** Subject identifiers are issuer-local. **Conclusion:** map (`iss-A`, `123`) and (`iss-B`, `123`) to distinct principals unless an explicit safe link occurs.

### Example 3

**Situation:** Two accounts share `alex@example.com`, one marked verified. **Reasoning:** Email equality does not prove same account owner or merge intent. **Conclusion:** require authenticated control of both accounts or governed enterprise provisioning.

### Example 4

**Situation:** A token was issued now from an OP session authenticated eight hours ago. **Reasoning:** `iat` is fresh but `auth_time` is stale for a wire transfer. **Conclusion:** request and validate step-up/fresh authentication with approved `acr`.

### Example 5

**Situation:** `amr=["pwd","otp"]` appears. **Reasoning:** Method labels do not prove the OTP is phishing-resistant or meets local assurance. **Conclusion:** require an approved OP `acr` contract and treat `amr` under documented semantics.

### Example 6

**Situation:** UserInfo returns a different `sub` than the validated ID token. **Reasoning:** Claims would attach another subject to the session. **Conclusion:** reject the response entirely and alert/investigate.

### Example 7

**Situation:** A guest belongs to tenants north and south and sends `X-Tenant: south`. **Reasoning:** Header input is not membership/selection authority. **Conclusion:** bind tenant through verified local membership/session/access context and scope every lookup.

### Example 8

**Situation:** An employee is disabled locally but still authenticates successfully at the OP. **Reasoning:** Authentication and application authorization/lifecycle differ. **Conclusion:** deny local/API access, preserve audit, and reconcile deprovisioning.

### Example 9

**Situation:** RP logout clears its cookie but the access token remains valid for five minutes. **Reasoning:** Local session termination did not revoke the resource token. **Conclusion:** document the window and add revocation/state checks where risk requires faster containment.

### Example 10

**Situation:** A token contains a `jku` pointing to an internal metadata address. **Reasoning:** Untrusted header URLs can cause SSRF and attacker-key trust. **Conclusion:** ignore/reject arbitrary locations and resolve keys only from configured issuer metadata.

## Cross-Program Connections

- **Identity and Access Management:** federation, subject identifiers, account linking, assurance, provisioning, and deprovisioning define principal lifecycle.
- **Security Engineering:** token substitution, mix-up, login CSRF, key confusion, SSRF, session fixation, and claim minimization shape trust.
- **Cryptography:** signatures, algorithm/key binding, nonce, key rotation, and JWT typing protect statements but not their local authorization meaning.
- **Web Engineering:** redirects, cookies, browser sessions, logout channels, same-origin protections, and BFF architecture govern RP exposure.
- **Database Engineering:** immutable principal IDs, uniqueness, linking transactions, membership state, and audit protect identity mappings.
- **Distributed Systems:** discovery/key caches, clock skew, revocation propagation, logout delivery, UserInfo availability, and stale claims need bounded semantics.
- **Privacy Engineering:** pairwise subjects, claim minimization, consent, retention, correlation, and telemetry govern identity-data exposure.

## References

1. Sakimura, N., Bradley, J., Jones, M., de Medeiros, B., and Mortimore, C. [OpenID Connect Core 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-core-1_0.html). OpenID Foundation, 15 December 2023. Checked 2026-09-01.
2. Sakimura, N., Bradley, J., Jones, M., and Jay, E. [OpenID Connect Discovery 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-discovery-1_0.html). OpenID Foundation, 15 December 2023. Checked 2026-09-01.
3. Sheffer, Y., Hardt, D., and Jones, M. [RFC 8725: JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725.html). IETF BCP 225, February 2020. Checked 2026-09-01.
4. Bertocci, V. [RFC 9068: JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens](https://www.rfc-editor.org/rfc/rfc9068.html). IETF, October 2021. Checked 2026-09-01.
5. Lodderstedt, T., Bradley, J., Labunets, A., and Fett, D. [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html). IETF BCP 240, January 2025. Checked 2026-09-01.
6. Jones, M., de Medeiros, B., Agarwal, N., Sakimura, N., and Bradley, J. [OpenID Connect RP-Initiated Logout 1.0](https://openid.net/specs/openid-connect-rpinitiated-1_0.html). OpenID Foundation. Checked 2026-09-01.

## Exercises

### Exercise 1

Create an artifact-recipient and validation matrix for an RP, BFF, orders API, UserInfo endpoint, and OP. Include type, issuer/presenter, recipient/audience, storage, validation, and authorization meaning.

### Exercise 2

Design the local principal/account-link schema and workflow for two enterprise issuers, one social issuer, pairwise subjects, email changes, issuer migration, and deprovisioning.

### Exercise 3

Specify a step-up authentication transaction for approving a high-value refund. Include action binding, subject/session, nonce, freshness, `acr`/`amr`, failure, replay, and API enforcement.

### Exercise 4

Diagnose a system that accepts either ID or access JWTs in one middleware, keys users by lowercase email, selects tenant from a header, and refreshes roles only at login. Provide a migration plan.

### Exercise 5

Design a lifecycle test matrix for OP/RP sessions, authorization grants, refresh/access tokens, local account state, tenant membership, UserInfo, provisioning, logout, and emergency key compromise.

## Answers to the Exercises

### Answer 1

The OP issues a code through the browser to the RP/BFF callback; the RP redeems it at the OP token endpoint with transaction bindings. The ID token is stored/validated only by the RP: exact trusted issuer/key/algorithm, RP client audience/`azp`, time, nonce, and assurance/freshness; it establishes (`iss`,`sub`) authentication for the local session. The UserInfo access token is held by the RP and accepted only by the OP UserInfo endpoint; its response `sub` must match. The orders access token is held/presented by the BFF to the orders API; the API validates its access-token type/profile, exact issuer/key, `orders-api` audience, time/sender/state, then applies tenant/object/action authorization. The browser holds a hardened RP session cookie under a BFF architecture, not raw OP/API tokens. Refresh tokens return only to the OP token endpoint. Every artifact has a distinct validator and no generic JWT-to-user path.

### Answer 2

Create an immutable local principal ID and unique external-principal table keyed by exact issuer and subject, with subject type/sector metadata, status, provenance, creation/link audit, and no email uniqueness as identity. Memberships, ownership, and audit reference the local ID. JIT creation is allowlisted per issuer/tenant; enterprise provisioning owns activation/deactivation and mapped memberships, while social login follows separate policy. Linking requires recent authentication to both existing principals or governed enterprise proof, step-up, CSRF/action binding, notification, and reversible audit; pairwise subjects are not correlated automatically. Email is versioned profile/contact data with issuer verification metadata and safe change handling. Issuer migration uses a signed/governed mapping and dual proof/reconciliation, preserves old identifiers/audit, prevents duplicate races, and expires the migration path. Deprovisioning disables local access immediately under its SLA even if OP authentication persists, removes memberships, revokes sessions/grants where supported, and retains audit per policy.

### Answer 3

The refund service creates a one-time step-up transaction bound to local principal, exact (`iss`,`sub`), RP session, client, tenant, refund ID/amount/currency/action, nonce, required approved `acr`, maximum `auth_time` age, creation/expiry, and return destination. It sends a fresh OIDC code+PKCE request with `nonce`, `max_age`/required context according to OP profile. On return it validates transaction, issuer, code flow, ID-token signature/audience/`azp`/time/nonce, same subject, `auth_time`, and exact approved `acr`; `amr` is checked only if documented supplementary policy requires it. It atomically marks the step-up result consumed/bound to that refund and issues a short local authorization fact. The API verifies access-token context and the step-up fact for the same principal/client/tenant/action/current refund state. Wrong subject/session/action, stale/unknown context, cancellation, duplicate callback/use, timeout, or downgrade fails safely and is audited without leaking details.

### Answer 4

Split middleware into mutually exclusive ID-token RP and access-token API validators with explicit types/audiences/claims/keys; inventory all callers before rejection. Stop sending ID tokens to APIs and issue audience-bound access tokens, first in observability/dual-validation rollout and then enforce. Introduce immutable local principal IDs and unique (`iss`,`sub`) mappings; reconcile current email-keyed collisions through verified user/admin workflows rather than automatic merge, then make email mutable profile data. Replace header tenant selection with membership-backed session/access context and scope repositories/caches/authorization. Move roles to a governed local/current policy source or bounded token/policy-version model with deprovisioning SLA and critical-action checks. Add negative substitution, multi-issuer, email recycling, cross-tenant, stale-role, revocation, and telemetry-leak tests; stage by client/tenant, monitor, retain rollback that does not restore insecure acceptance, and retire legacy tokens/keys/routes by deadline.

### Answer 5

Model each state and transition independently. Verify RP logout clears/invalidates the local cookie/session and tokens in its store; OP logout behavior under the adopted profile; refresh revocation/rotation and replay; access-token usability until exact expiry or resource-server revocation signal; local disablement denying even a cryptographically valid login/token; tenant removal affecting scoped authorization and caches; UserInfo outage/cache and subject mismatch; provisioning create/update/disable races; and session/token refresh not restoring removed authority. Exercise browser/back-channel logout loss, duplicate/reordered messages, clock skew, region partition, stale metadata/JWKS, and recovery. For signing-key compromise, publish clean replacement, reject compromised key according to containment policy, invalidate/re-authenticate affected sessions/tokens, test cached verifiers and partial rollout, assess access, notify, and prove old-key rejection. Reconcile audit cardinality and scan logs/traces/backups/support artifacts for raw tokens and sensitive claims.
