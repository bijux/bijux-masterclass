---
module_id: API-043
program: API & Service Engineering
level: 1
module_number: 43
title: OAuth Authorization Flows
status: complete
last_verified: 2026-09-01
---

# OAuth Authorization Flows

## One-Page Review

### Governing question

How should an API ecosystem choose and implement an OAuth authorization flow that matches the acting party, client capabilities, user interaction, redirect environment, and token exposure model without confusing delegation with authentication?

### Essential definitions

- The **resource owner** can grant access to a protected resource; the **client** requests that access; the **authorization server** issues tokens; the **resource server** hosts the API.
- An **authorization grant** is protocol evidence by which a client obtains access-token authority; it is not the access token itself.
- A **public client** cannot keep client credentials confidential; a **confidential client** can authenticate using protected credentials in its deployment.
- The **authorization endpoint** uses a user agent to obtain authorization; the **token endpoint** exchanges grants through a direct client-to-server request.
- An **authorization code** is a short-lived, single-use intermediary bound to client and redirect context.
- **PKCE** binds a code exchange to the client instance that initiated it using a verifier and derived challenge.
- A **redirect URI** is a registered client endpoint to which the authorization response returns; its matching and ownership are security-critical.
- The **client credentials grant** represents a client acting as itself, not a user delegation.

### Central model, mechanism, or theorem

Choose a flow from the authorization relationship and client environment:

$$
F=f(A,C,U,R,K,T),
$$

where $A$ is actor/authority, $C$ client confidentiality and deployment, $U$ user interaction, $R$ redirect capability, $K$ sender/key capability, and $T$ threat model. For a user-facing authorization-code transaction, safe completion requires correlated state:

$$
\operatorname{complete}\iff c_{issued}=c_{redeemed}\land r_{issued}=r_{redeemed}\land H(v)=h\land iss_{response}=iss_{expected}\land\text{single-use}\land\text{unexpired},
$$

where $c$ is client, $r$ redirect URI, $v$ PKCE verifier, $h$ challenge, and $iss$ authorization-server identity. Each predicate prevents a different substitution, interception, mix-up, or replay path.

### Critical invariants

OAuth delegates API access; OpenID Connect supplies interoperable authentication identity when required. The authorization server, client, resource server, and browser remain distinct security principals even under one owner. Public clients have no effective distributed secret. Redirect URIs are pre-registered and exactly matched under the applicable profile. Authorization codes are short-lived, one-time, and bound to client, redirect, issuer, and PKCE. Tokens do not enter the authorization response URL in modern browser/native flows. Native apps use an external user agent. Confidential clients authenticate at the token endpoint; PKCE protects code binding and is not a replacement for client authentication. Client credentials never invent a user. Refresh authority is minimized and protected. Deprecated implicit and resource-owner-password flows are not used for new systems.

### Common failures

Selecting a flow from framework defaults; calling OAuth “login” without OpenID Connect semantics; placing access tokens in front-channel URLs; embedding a secret in a SPA or mobile binary; accepting wildcard/prefix redirect URIs; omitting PKCE or permitting `plain` when `S256` is available; treating `state`, PKCE, issuer checking, and OIDC `nonce` as interchangeable; letting codes be reused; using an embedded webview for native authorization; using client credentials on behalf of users; giving a device user code excessive authority or life; issuing broad refresh tokens to weak clients; keeping implicit or password grants for convenience; and following attacker-controlled discovery/redirect endpoints.

### Compact example

A native orders app creates a high-entropy verifier, sends its `S256` challenge with a code request in the system browser, and uses an exactly registered app-link redirect. After return, it verifies correlation and expected issuer, then sends the one-time code, exact redirect URI, and verifier to the token endpoint. The server verifies every binding before issuing an orders-API token. The app never handles the user's authorization-server password. **Conclusion:** the code flow separates user interaction from token delivery, while PKCE binds the two legs to one client instance.

### Connections

[Credential and Token Handling](042-credential-and-token-handling.md) governs the resulting artifacts; [Authentication Context Propagation](033-authentication-context-propagation.md) consumes validated access-token context. [Applying OpenID Connect at API Boundaries](../ROADMAP.md) next separates authentication claims from OAuth authorization, while [Scope and Permission Design](../ROADMAP.md) narrows delegated capability.

## Governing Question

Which OAuth protocol path expresses the real actor and delegation, fits the client's ability to protect credentials and receive responses, prevents front-channel and code attacks, and yields tokens whose audience, privilege, lifetime, and holder match the API risk?

## Why This Matters

OAuth is a framework of roles, endpoints, grants, and extensions rather than a universal login exchange. Selecting the wrong flow can expose access tokens to browser history, ask a public client to keep an impossible secret, give a machine a fictional user identity, or hand a password to an unrelated client. A syntactically successful flow can still be unsafe if its redirect, issuer, PKCE, client, and code bindings are incomplete.

Modern guidance changed the default landscape. The authorization code grant with PKCE replaces the historical reasons for implicit token delivery in browser/native clients. Resource owner password credentials bypass the authorization boundary and are prohibited by the current OAuth security BCP. Native apps authorize in an external browser rather than an embedded credential-capturing view. Browser applications must choose an explicit architecture based on whether tokens remain in a backend, pass through a token-mediating backend, or live in browser code.

Flow selection also determines operational ownership. Redirect registration, browser session security, token endpoint authentication, key management, refresh rotation, consent, resource indicators, and API audience validation span different components. Treating them as a single “OAuth middleware” setting hides the trust boundaries.

This module teaches selection and end-to-end flow invariants. It does not teach OpenID Connect identity semantics—that follows in API-044—and it does not make scopes sufficient object authorization. OAuth obtains bounded authority; the resource server still validates the token and applies local policy.

## Prerequisites and Retrieval

Retrieve HTTP redirects and TLS, user agents and origins, cross-site request forgery, secure random values and hashing, authorization codes, access/refresh tokens, issuer and audience, bearer and sender-constrained tokens, client registration, public/confidential clients, PKCE, redirect URI types, native deep links and loopback listeners, browser sessions/cookies, CORS/CSP, device authorization, client authentication, consent, scopes, discovery metadata, and threat modeling.

Before choosing a flow, retrieve the resource owner/actor, resource APIs and audiences, authorization server, client deployment, whether code is delivered to untrusted devices/browsers, ability to keep secrets/private keys, redirect ownership and platform binding, user-agent availability, input/display capability, cross-device needs, same-domain alternatives, user authentication requirement, requested permissions, refresh/offline need, sender constraint, client registration, exact endpoints/issuer metadata, logout/session expectations, account/tenant selection, phishing and mix-up threats, and incident/rotation ownership.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish OAuth roles, grants, endpoints, tokens, delegation, and authentication;
2. select authorization code with PKCE, client credentials, or device authorization from actor/client constraints;
3. explain redirect, issuer, state, PKCE, nonce, client authentication, and code binding without conflating them;
4. design secure flows for server web, browser-based, native, CLI/device, and machine clients;
5. reject implicit and password-based shortcuts under current guidance;
6. model refresh, consent, least privilege, errors, logout, and compromise honestly; and
7. verify complete transactions against injection, interception, mix-up, replay, phishing, and leakage.

## Core Exposition

### Start from roles and authority

OAuth 2.0 defines four logical roles:

- the **resource owner** controls access to a protected resource;
- the **client** requests access, often on behalf of that owner;
- the **authorization server** authenticates/authorizes according to policy and issues tokens; and
- the **resource server** accepts access tokens for a protected API.

One organization may operate all components, but they remain separate principals for validation. A client cannot mint its own resource-owner consent. A resource server cannot accept a token merely because it came from a sibling host. The authorization server does not make every object-level API decision.

State the actor in one sentence: “The invoicing web application accesses invoices on behalf of the signed-in employee,” or “The nightly reconciliation worker accesses its own integration queue.” The first needs user delegation; the second may use client credentials. “The backend calls the API” is insufficient because it omits whose authority is exercised.

OAuth is not intrinsically authentication. An access token tells a resource server about authorization under its validation profile. Using a generic OAuth authorization response to infer “who logged in” invites token substitution and missing identity semantics. When the client needs interoperable user authentication, use OpenID Connect and validate its ID-token/nonce/session rules separately.

### Classify the client by deployment reality

A confidential client can authenticate securely because its credential or private key is protected in a controlled server deployment. A public client—native app, browser-only JavaScript, distributed CLI—cannot keep a shared secret from the user or attacker controlling the package/runtime. Registering a string called `client_secret` does not make it confidential.

Classify each deployed instance, not the product name. A web frontend with a backend-for-frontend can have a confidential server-side OAuth client while the browser holds only a session cookie. The same vendor's standalone SPA is a public client. A native app can hold a device-generated private key with hardware support for proof mechanisms while still being unable to protect a globally embedded client secret.

Client identifiers are public routing identifiers. Client authentication at the token endpoint proves a confidential client's identity; it does not replace redirect checking, PKCE, user authorization, access-token validation, or object authorization. Prefer asymmetric client authentication where feasible so the authorization server need not store reusable client shared secrets.

### Use authorization code as the user-delegation baseline

The authorization code flow separates two channels:

1. **Front channel:** the client sends the user agent to the authorization endpoint with client ID, exact redirect URI, requested authorization details/scope, PKCE challenge, correlation/CSRF protection, and other profile fields.
2. **Back channel:** after authorization, the client sends the returned short-lived code, exact redirect URI, PKCE verifier, and confidential-client authentication where applicable directly to the token endpoint.

The authorization response carries no access token. A party observing the code cannot redeem it without the verifier, and the code is bound to the client/redirect and used once. Token delivery happens over authenticated TLS to the token endpoint.

The authorization server authenticates the resource owner as required, evaluates policy/consent, then records all bindings with the code. At redemption it atomically checks code existence, issuer/client, redirect URI, PKCE, expiry, single use, and client authentication. Mark the code consumed without a race. Do not perform a non-atomic “check then delete” that permits concurrent redemption.

Confidential clients still use PKCE under modern profiles where supported/recommended: PKCE binds the authorization request/code to the initiating client instance; client authentication proves the configured client. They address different threats.

### Understand PKCE precisely

The client generates a high-entropy `code_verifier` for one authorization transaction. With the `S256` method it sends a base64url-encoded SHA-256 transformation as `code_challenge`. It retains the verifier in transaction state and sends it only to the token endpoint. The authorization server compares the derived value using exact octets.

PKCE prevents an intercepted or injected authorization code from being redeemed by a party lacking the initiating verifier. It does not authenticate the user, identify the correct issuer by itself, validate the redirect URI, protect a token after issuance, or authorize an API object.

Authorization servers require PKCE for public clients and support `S256`; clients must not silently downgrade because a response or attacker suggests PKCE is unavailable. Avoid reusing verifiers between transactions. Bind verifier, redirect correlation, issuer, and client state in a protected short-lived transaction record.

### Give each correlation control its own job

OAuth deployments commonly mishandle similar-looking values:

- **PKCE** binds authorization request/code redemption to a client instance and can contribute to CSRF/code-injection defenses under current profiles.
- **`state`** can bind the authorization response to the initiating browser/client transaction and carry or reference CSRF state; it must be unpredictable, one-time, and compared exactly when used for that purpose.
- **Authorization response `iss`** (RFC 9207), distinct redirect endpoints, or profile mechanisms identify the authorization server and prevent mix-up.
- **OIDC `nonce`** binds an ID token/authentication response to the client transaction; it is an OpenID Connect control, not a generic replacement word for every OAuth value.
- **Redirect URI** binds where the response may be delivered.

One value can sometimes satisfy more than one formally specified property, but only under an explicit profile and analysis. Do not remove `state` because “we have nonce” or skip issuer validation because “PKCE passed.” Store intended issuer and endpoint set with the transaction, especially when a client supports multiple authorization servers.

Do not put application return URLs or authorization data directly into unsigned `state` and redirect to them blindly. Store server-side transaction state or authenticate/encrypt a bounded value, allowlist post-login destinations, enforce expiry/single use, and prevent open redirects.

### Register and validate redirects exactly

Redirect control is part of credential delivery. Pre-register complete redirect URIs and use exact string matching under RFC 9700, except the specified native loopback-port allowance. Wildcards, prefix matching, arbitrary subdomains/paths, and attacker-selected continuations enable code/token theft.

At the authorization endpoint, validate the redirect URI before user authentication or consent and never redirect an error to an invalid URI. Bind the exact value into the authorization code and require the same value at redemption where the protocol requires it. Normalize only as the applicable specification says; independent parser normalization can make two components disagree.

Protect the redirect endpoint itself. It should consume one transaction, reject unsolicited/duplicate responses, remove code/parameters from browser-visible history where appropriate, avoid loading third-party resources before cleanup, set safe referrer policy, and never log codes. Redirect pages must not become open redirectors.

Multiple environments and clients get distinct registrations. Development loopback URIs and test hosts do not belong on a production web client. Ownership changes, DNS/subdomain takeover, mobile association files, and stale redirect routes are inventory concerns.

### Design server-side web clients

A traditional server web application or backend-for-frontend keeps OAuth tokens and client credentials in the server boundary. The browser carries a hardened application session cookie rather than API access tokens. The server starts authorization, stores transaction state and PKCE verifier in a protected session/store, receives the redirect, exchanges the code, and calls resource APIs.

Protect the session against fixation, theft, CSRF, cross-site leakage, and overly long life. Rotate the session identifier after authentication/authorization, set `Secure`, `HttpOnly`, appropriate `SameSite`, narrow domain/path, and enforce CSRF protection for state changes. The cookie is not magically safer than tokens; it changes the attacker surface and permits tokens to remain out of browser JavaScript.

The backend must not become an unconstrained proxy. It authorizes application routes, fixes API destinations, validates responses, bounds bodies and timeouts, prevents confused deputy behavior, and maps user/client context correctly. Its client credentials and refresh tokens use managed server storage and rotation.

For same-domain applications, RFC 10017 notes that OAuth between frontend and backend may be unnecessary: federated authentication can establish a server session, after which normal session controls protect the app. Choose OAuth when delegated access/resource-server separation actually requires it.

### Choose a browser-based architecture explicitly

RFC 10017 describes three patterns with decreasing token isolation:

1. **Backend-for-frontend (BFF):** the confidential backend performs OAuth, retains tokens, and proxies API calls. Browser compromise can issue actions through the BFF but cannot directly exfiltrate tokens if controls hold.
2. **Token-mediating backend:** a backend obtains/refreshes tokens but returns access tokens to browser code. This reduces refresh-token exposure but access tokens remain exfiltratable; evaluate whether a full BFF is feasible first.
3. **Browser-based OAuth client:** JavaScript is the public OAuth client and holds tokens. Malicious in-browser code can steal/use them; minimize lifetime/privilege, use authorization code with PKCE, exact redirects, robust script/CSP/supply-chain defenses, and applicable refresh protection.

Architecture follows threat model, API topology, latency/streaming needs, deployment ownership, and browser code exposure. Do not call a SPA confidential because a build pipeline injected a secret. CORS is a browser read policy, not client authentication or bearer-token protection.

When browser code performs the flow, the authorization server supports appropriate CORS at the token endpoint only for intended origins/methods/headers; CORS does not relax redirect or PKCE validation. Prevent malicious scripts through dependency controls, CSP, Trusted Types where applicable, output encoding, minimal third-party code, and rapid incident response.

### Follow native-app best current practice

Native apps initiate authorization in the external system browser, not an embedded webview. The external browser prevents the app from directly reading authorization-server credentials/cookies and enables shared authentication and user-recognizable security context. An embedded user agent lets the hosting app capture passwords and manipulate content.

Use authorization code with PKCE. Receive responses through platform-appropriate claimed HTTPS links/universal/app links where the app can prove domain association, loopback redirects for desktop apps, or private-use schemes with reverse-domain ownership conventions where necessary. Threat-model app-claim collisions and interception. The authorization server records the client type and allowed redirect pattern.

Native apps are public clients even if a static secret is shipped in the binary. Protect tokens in OS secure storage and use device-bound/sender-constrained mechanisms when appropriate, but assume malware or a compromised device may act as the app. Never ask the user to enter authorization-server credentials directly into the native app for OAuth.

### Use device authorization for constrained input

The OAuth 2.0 Device Authorization Grant (RFC 8628) serves devices that lack a suitable browser or have constrained input. The device obtains a device code and user code, shows a verification URI/user code, and polls the token endpoint while the user authorizes on a separate capable device.

The device code is a secret credential for polling; the user code is optimized for manual entry and therefore needs bounded lifetime, rate limiting, and server-side binding. The verification page clearly shows which device/client and authority are being approved to resist phishing. Do not train users to enter codes received from strangers.

Honor polling interval and `slow_down`; expire atomically; issue no token before completed approval; and stop after denial/expiry/success. A device with a usable browser should normally use the native-app browser flow instead. Device flow does not turn a television into a confidential client or prove possession of the physical device without added controls.

### Use client credentials only for client authority

Client credentials fits a confidential client acting as itself or under prearranged organizational authority. The client authenticates to the token endpoint, requests its allowed resource/scope, and receives an access token whose subject/client semantics make machine authority clear.

Do not use it to impersonate whichever user ID appears in a request body. If a backend needs delegated user authority, propagate/exchange that authority through an appropriate reviewed design. If it runs a system job, authorize the workload/service principal directly and audit it as such.

Prefer asymmetric client authentication or workload federation where feasible, scope by audience and operation, use short-lived access tokens, rotate client keys, and prevent one service credential from spanning all tenants/environments. The authorization server rejects client-requested scopes/resources outside registration/policy.

### Reject obsolete and unsafe shortcuts

The **implicit grant** returns access tokens in the authorization response/front channel. Modern browsers support authorization code with PKCE and token endpoint CORS, removing its historical rationale. RFC 9700 says clients should not use implicit except under narrowly justified mitigations; new systems use code with PKCE.

The **resource owner password credentials grant** hands the user's password to the client, defeats federation/modern authentication, expands credential exposure, and cannot safely accommodate many authentication methods. RFC 9700 states it must not be used. Migrate rather than wrapping it in TLS and calling it legacy-safe.

Do not invent a “password exchange” or reuse API keys as authorization grants. Protocol extensions require reviewed specifications, metadata, threat analysis, and interoperability. Extension grants such as token exchange or JWT assertions express specialized relationships; they are not generic escape hatches.

### Minimize authorization and consent

Request the smallest resource audience and permissions needed at the time of use. Do not request every future scope at first login for implementation convenience. Incremental authorization can improve least privilege but must not surprise users or create unusable consent spam.

Consent is one input to authorization policy, not a liability waiver or security control. The authorization server must prevent a malicious client from choosing unauthorized scopes, resources, redirect URIs, or presentation text. Make client identity, publisher, requested capability, target resource, duration, and consequences understandable. High-risk actions may require step-up or transaction-specific authorization rather than a broad long-lived scope.

Multi-tenant flows explicitly bind account/organization selection. Prevent login/consent CSRF where an attacker connects their authorization context to a victim's client session. Preserve actor, client, tenant, and delegation chain for auditing.

### Handle tokens, refresh, and logout by architecture

Access tokens are audience-restricted and validated by resource servers as described in API-042. Refresh tokens go only to the authorization server and are issued only when offline/longer access is justified. Public-client refresh tokens use sender constraint or rotation/replay detection according to current policy; confidential clients also authenticate.

Bind refresh authority to client, subject, grant, resource/scope, and session/policy. On scope reduction, account disablement, client compromise, password/security event, or consent withdrawal, define which grants/tokens are revoked and within what latency. A refreshed access token must not silently recover removed authority from stale state.

OAuth authorization and application/authorization-server login sessions differ. Logging out of the client can clear its session/tokens but may not end the authorization-server SSO session or revoke access tokens. OIDC logout profiles, if used, add separate protocol semantics. State the user-visible result rather than promising universal logout.

### Make metadata and multi-issuer handling safe

Configure issuer identifiers and authorization/token endpoints through trusted registration or verified metadata (RFC 8414). Do not accept an attacker-supplied issuer URL and fetch arbitrary discovery/JWKS endpoints without allowlisting and SSRF controls. Validate the metadata issuer exactly and bind endpoints/keys to it.

When one client supports multiple authorization servers, store the chosen issuer with each transaction and validate the authorization response using RFC 9700/RFC 9207 or profile mechanisms. Send the code only to the token endpoint belonging to the expected issuer. Mix-up can otherwise send codes/credentials to an attacker-controlled server.

Metadata and key caches need bounded freshness, secure bootstrap, rotation, and outage behavior. A transient fetch failure must not cause fallback to an untrusted endpoint or disable issuer/audience checks.

### Specify failures without creating oracles

At the authorization endpoint, invalid redirect URI never receives a redirect; render a safe local error. For valid redirects, return protocol errors without credentials or sensitive policy detail. At the token endpoint, authenticate clients where applicable, rate-limit, use generic protocol errors, and avoid distinguishing whether a guessed code exists beyond the specification.

Consume or invalidate codes atomically according to policy so error retries do not create multiple token issues. Protect authorization and token endpoints from brute force, code/user-code guessing, parser abuse, and log flooding. Never log codes, verifiers, tokens, client secrets, or session cookies.

Clients treat denial, expiry, browser close, network loss, and server error as distinct user/retry outcomes. They do not loop authorization automatically or downgrade controls. Preserve correlation cleanup and bounded transaction lifetime on every exit.

The executable policy below illustrates flow selection for common actors and clients. It is a local design rule, not a complete OAuth implementation or protocol validator.

<!-- bijux-verify: {"id":"oauth-flow-selection-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"server_user=authorization-code-pkce\nnative_user=authorization-code-pkce\nbrowser_user=bff-authorization-code-pkce\ndevice_user=device-authorization\nservice_self=client-credentials\nspa_implicit=reject:implicit\npassword_exchange=reject:password-grant\nservice_as_user=reject:actor-mismatch\n","stderr":""}} -->
```python
def select(actor, client, browser=True, constrained=False, requested=None):
    if requested == "implicit":
        return "reject:implicit"
    if requested == "password":
        return "reject:password-grant"
    if actor == "service" and requested == "user":
        return "reject:actor-mismatch"
    if actor == "service":
        return "client-credentials"
    if constrained and not browser:
        return "device-authorization"
    if client == "browser":
        return "bff-authorization-code-pkce"
    if client in {"server", "native"} and browser:
        return "authorization-code-pkce"
    return "reject:unsupported-environment"

print("server_user=" + select("user", "server"))
print("native_user=" + select("user", "native"))
print("browser_user=" + select("user", "browser"))
print("device_user=" + select("user", "device", browser=False, constrained=True))
print("service_self=" + select("service", "server"))
print("spa_implicit=" + select("user", "browser", requested="implicit"))
print("password_exchange=" + select("user", "server", requested="password"))
print("service_as_user=" + select("service", "server", requested="user"))
```

The default browser decision prefers a BFF when feasible; RFC 10017 permits other patterns with explicitly different exposure. A real design records why its constraints justify the chosen pattern.

### Verify complete transactions and attacks

Use a client/flow matrix covering server web, BFF, browser public client if applicable, native platforms/redirect types, device clients, and machine clients. Verify registration, issuer metadata, endpoints, TLS, redirect exactness, client type/authentication, PKCE, transaction correlation, code lifetime/use, scopes/resources, token audiences, refresh, logout, and errors.

Attack tests cover authorization-code interception/injection, CSRF/login CSRF, mix-up, redirect wildcard/parser differences, open redirect, app-link/private-scheme interception, embedded webviews, malicious browser script, stolen client secret, verifier reuse/downgrade, concurrent code redemption, device-code phishing/guessing/poll flooding, excessive consent, refresh replay, cross-tenant account selection, and log/referrer leakage.

Fault tests stop the browser before return, lose the token response after code consumption, rotate client/signing keys, expire transaction/code, partition metadata/token endpoints, skew clocks, and partially deploy redirect changes. Evidence proves one-time grants, no control downgrade, safe cleanup, bounded retries, and no credentials in artifacts or telemetry.

## Definitions and Notation

Let $F=f(A,C,U,R,K,T)$ select a flow using authority/actor $A$, client deployment/confidentiality $C$, user interaction $U$, redirect capability $R$, sender/key capability $K$, and threat model $T$. Let authorization transaction $q$ bind expected issuer, client, exact redirect, PKCE challenge/method, requested resource/permissions, browser correlation, creation/expiry, and status.

Let $v$ be a PKCE verifier and $h$ its `S256` challenge; $c$ client identity; $r$ redirect URI; and $iss$ issuer. A code is redeemable once only when the stored and presented bindings match and the confidential client authenticates where required.

A **front channel** passes through the user's browser and is exposed to browser/navigation threats. A **back channel** is direct authenticated client-to-server communication. **Mix-up** confuses which authorization server a response/code belongs to. **Authorization code injection** causes a client to accept a code from an attacker's transaction. **Login CSRF** binds a victim's client session to the attacker's authorization context.

## Mechanisms, Invariants, or Proof Structure

1. State whether authority belongs to a user delegation or client itself.
2. Classify the deployed client as public/confidential and enumerate browser/redirect/storage threats.
3. Prefer authorization code with PKCE for interactive authorization; use device flow only for constrained input and client credentials only for self-authority.
4. Register exact issuer/endpoints/redirect URIs and keep environments/clients distinct.
5. Bind transaction, issuer, client, redirect, PKCE, requested authority, expiry, and correlation.
6. Authenticate/authorize the user at the authorization server and issue a one-time short code without front-channel tokens.
7. Atomically validate code bindings, PKCE, confidential-client authentication, time, and single use at the token endpoint.
8. Issue least-privilege audience-bound tokens and protect refresh according to client architecture.
9. Validate tokens and authorize resources independently; represent actor/client/delegation honestly.
10. Test interception, injection, mix-up, CSRF, replay, redirects, phishing, leakage, downgrade, rotation, and failure.

These invariants establish the intended protocol composition only when every participating implementation follows the selected RFC/profile and uses secure libraries/configuration. The finite selection example does not validate OAuth messages or prove a deployment secure.

## Alternatives and Trade-Offs

A BFF keeps tokens from browser JavaScript and enables confidential-client controls but adds server state, proxy latency/capacity, CSRF/session protection, and backend scaling. A browser public client is simpler for direct APIs/streams but exposes tokens to malicious script. A token-mediating backend lies between and still releases access tokens; choose explicitly.

Authorization code with PKCE adds a token exchange and transaction state but removes access tokens from front-channel responses and binds codes. Implicit can appear simpler but its historical browser advantages no longer justify front-channel tokens for new systems.

Client credentials is efficient for machine identity but cannot represent user consent/delegation. User code flow works on constrained devices but adds cross-device phishing, polling, and user-code risks. Native external-browser code flow is stronger when the device can launch/receive browser authorization.

Shared client secrets are familiar but cannot be confidential in distributed clients and create issuer storage/rotation exposure. Asymmetric authentication/workload identity reduces reusable secret sharing but adds key enrollment, signing, rotation, and platform dependencies.

Long refresh lifetimes improve offline usability but expand compromise duration and policy staleness. Short access tokens plus rotated/sender-constrained refresh authority improve containment but couple clients to renewal availability and state. Match the actual offline requirement.

One authorization server simplifies issuer/metadata handling; multi-issuer federation supports organizational needs but increases mix-up, account linking, policy, key, discovery, and incident complexity. Every transaction must retain expected issuer.

## Failure Modes and Misconceptions

- **“OAuth is authentication.”** Use OpenID Connect when the client needs standardized user identity/authentication.
- **“A client ID is secret.”** It is a public identifier.
- **“Our mobile secret is obfuscated.”** Distributed static credentials are recoverable; the client is public.
- **“PKCE authenticates the client.”** It binds the code exchange; confidential-client authentication is separate.
- **“State, nonce, issuer, and PKCE are the same.”** Each has distinct protocol properties.
- **“Any matching-domain redirect is safe.”** Register and exactly compare the complete allowed URI.
- **“CORS secures tokens.”** It is a browser response-read policy, not authorization or credential proof.
- **“Implicit is needed for SPAs.”** Modern code flow with PKCE and browser guidance replaces its historical rationale.
- **“Password grant is trusted first-party login.”** It exposes user credentials and is prohibited by current BCP.
- **“Client credentials can carry a user ID.”** Machine self-authority does not become delegation through a body claim.
- **“Consent means safe.”** Clients cannot request authority outside policy, and users need meaningful bounded choices.
- **“Device flow is easy login everywhere.”** Use it only for constrained devices and defend code phishing/polling.
- **“Logout revokes all tokens and SSO.”** Client session, refresh grant, access token, and authorization-server session differ.
- **“Same company means same trust principal.”** Client, authorization server, and resource server validate each other explicitly.

## Worked Examples

### Example 1

**Situation:** A server-rendered web app calls an orders API for a user. **Reasoning:** A confidential backend can protect tokens and session state. **Conclusion:** use authorization code with PKCE and client authentication, retain tokens server-side, and give the browser a hardened session.

### Example 2

**Situation:** A SPA injects its build-time `client_secret`. **Reasoning:** Every user can inspect it; it authenticates no client instance. **Conclusion:** register a public client or use a BFF; never rely on the embedded secret.

### Example 3

**Situation:** A native app opens an authorization page inside a webview. **Reasoning:** The app can observe credentials/cookies and users lose trusted browser context. **Conclusion:** use the external system browser, PKCE, and a platform-appropriate registered redirect.

### Example 4

**Situation:** A code is intercepted from a private-use URI redirect. **Reasoning:** The malicious app lacks the initiating verifier. **Conclusion:** PKCE prevents redemption, while claimed HTTPS links or platform binding further reduce interception.

### Example 5

**Situation:** A client supporting two issuers sends an attacker's code to the legitimate issuer's token endpoint. **Reasoning:** The transaction lost expected issuer identity. **Conclusion:** bind/validate response issuer and endpoint set, then redeem only at that issuer.

### Example 6

**Situation:** A television shows a device user code, and a caller asks the user to enter a different code. **Reasoning:** Device flow can be phished through cross-device social engineering. **Conclusion:** show client/device identity, short codes/life, confirmation context, rate limits, and user warnings.

### Example 7

**Situation:** A nightly reconciliation service needs its own queue access. **Reasoning:** No user delegation exists. **Conclusion:** use client credentials/workload identity for a narrow audience/scope and audit the service principal.

### Example 8

**Situation:** A backend uses client credentials, accepts `user_id`, and refunds as that user. **Reasoning:** Caller input invented delegation. **Conclusion:** reject the design; use a reviewed delegation/token-exchange pattern or authorize the service action directly with honest audit.

### Example 9

**Situation:** A redirect registration is `https://client.example/*`. **Reasoning:** An open redirect or attacker-controlled path can receive codes. **Conclusion:** register exact endpoint URIs and remove continuation redirects from the OAuth callback.

### Example 10

**Situation:** A user closes the browser after consent, while the token response is lost after code consumption. **Reasoning:** Reusing the code is forbidden, and blind flow loops can duplicate prompts. **Conclusion:** return a recoverable client state and restart a fresh bounded transaction without downgrading controls.

## Cross-Program Connections

- **Security Engineering:** CSRF, mix-up, credential phishing, interception, capability minimization, and sender constraint shape each flow.
- **Web Engineering:** origins, redirects, cookies, browser storage, CORS, CSP, referrer/history, and external user agents determine exposure.
- **Mobile and Operating Systems:** app links, scheme claiming, loopback listeners, secure storage, and system browsers determine native safety.
- **Distributed Systems:** one-time atomic code redemption, metadata/key caches, clock bounds, partial rollout, and lost responses create correctness edges.
- **Identity Engineering:** OAuth delegation, OpenID Connect authentication, client identity, user subject, tenant selection, and session/logout must remain distinct.
- **API Design:** resource audiences, permissions, error contracts, and local object authorization constrain the authority tokens actually exercise.
- **Platform Engineering:** workload identity, managed client keys, gateway trust, issuer availability, rate limits, and inventory operationalize flows.

## References

1. Hardt, D. [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749.html). IETF, October 2012. Checked 2026-09-01.
2. Lodderstedt, T., Bradley, J., Labunets, A., and Fett, D. [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html). IETF BCP 240, January 2025. Checked 2026-09-01.
3. Sakimura, N., Bradley, J., and Agarwal, N. [RFC 7636: Proof Key for Code Exchange by OAuth Public Clients](https://www.rfc-editor.org/rfc/rfc7636.html). IETF, September 2015. Checked 2026-09-01.
4. Denniss, W., and Bradley, J. [RFC 8252: OAuth 2.0 for Native Apps](https://www.rfc-editor.org/rfc/rfc8252.html). IETF BCP 212, October 2017. Checked 2026-09-01.
5. Parecki, A., and Waite, D. [RFC 10017: OAuth 2.0 for Browser-Based Applications](https://www.rfc-editor.org/rfc/rfc10017.html). IETF, 2026. Checked 2026-09-01.
6. Denniss, W., Bradley, J., Jones, M., and Andronache, H. [RFC 8628: OAuth 2.0 Device Authorization Grant](https://www.rfc-editor.org/rfc/rfc8628.html). IETF, August 2019. Checked 2026-09-01.
7. Meyer zu Selhausen, K., and Bradley, J. [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207.html). IETF, March 2022. Checked 2026-09-01.
8. Jones, M., Sakimura, N., and Bradley, J. [RFC 8414: OAuth 2.0 Authorization Server Metadata](https://www.rfc-editor.org/rfc/rfc8414.html). IETF, June 2018. Checked 2026-09-01.

## Exercises

### Exercise 1

Choose and specify flows for a server-rendered web app, SPA with optional backend, iOS/Android app, desktop CLI, television, nightly worker, and support tool acting for a user. Justify actor, client class, redirects, PKCE, client authentication, and token storage.

### Exercise 2

Write the complete state machine for one authorization-code transaction from initiation through redemption or failure. Include bindings, atomicity, expiry, concurrency, cleanup, and safe errors.

### Exercise 3

Threat-model a client supporting two authorization servers and five redirect URIs across production and staging. Cover mix-up, open redirects, wildcard/parser mismatch, DNS/app-link ownership, and deployment drift.

### Exercise 4

Compare BFF, token-mediating backend, and browser public-client architectures for an application using REST, WebSocket, and large direct uploads. State token exposure, proxy requirements, browser controls, and residual risk.

### Exercise 5

Plan migrations from implicit grant, resource-owner-password credentials, and a client-credentials “user impersonation” convention without breaking clients or preserving false security claims.

## Answers to the Exercises

### Answer 1

The server web app uses authorization code with PKCE plus confidential-client authentication, server token storage, exact HTTPS callback, and a hardened browser session. Prefer a BFF with the same flow for the SPA when feasible; if direct browser tokens are justified, register it public and use code+PKCE under RFC 10017 with minimal tokens and strong script defenses. Native mobile uses external browser, code+PKCE, claimed HTTPS/app links, OS storage, and optional sender binding; no embedded secret. Desktop CLI uses external browser with code+PKCE and loopback redirect when it can open one; a headless constrained CLI may use device authorization. Television uses device authorization with bounded user/device codes and polling. The nightly worker uses client credentials/asymmetric workload identity for self-authority. A support tool acting for a user needs explicit delegated/impersonation authority with actor/effective subject, approval, short life, and audit—not plain client credentials plus a user field.

### Answer 2

Initiation creates a random one-time transaction containing expected issuer/endpoints, client, exact redirect, PKCE `S256` challenge and protected verifier association, requested resource/permissions, browser correlation/CSRF property, creation/expiry, and return destination allowlist. The authorization server validates client/redirect before interaction, authenticates and authorizes the user, then atomically issues one short code bound to issuer/client/redirect/challenge/grant. The client accepts a response only for its pending transaction and expected issuer, then redeems at that issuer with exact redirect/verifier and client authentication if confidential. The token endpoint atomically checks all bindings, time, policy, and unused status, marks consumption, and issues one outcome. Denial, mismatch, expiry, duplicate/concurrent redemption, browser close, and network loss terminate/expire state without control downgrade or credential logging. A lost token response requires a fresh transaction unless a specified idempotent token protocol exists; never revive a consumed code.

### Answer 3

Register issuer metadata through trusted configuration and keep authorization/token/JWKS endpoint sets distinct. Store the selected issuer in each transaction; validate response `iss` or a profile equivalent and send its code only to its token endpoint. Give production and staging separate client IDs, secrets/keys, issuers/audiences, and exact redirect registrations. Remove wildcard/prefix rules and compare exact URIs with one standards-compliant interpretation; callbacks never accept arbitrary continuation URLs. Inventory DNS/subdomain ownership and prevent dangling records; verify mobile association files/app ownership and private-scheme collision risks; restrict loopback rules to native profiles. Test swapped issuer responses, malicious discovery, attacker endpoint/key URLs, encoded/path parser differences, open-redirect chains, stale routes, subdomain takeover, app interception, and partial deployment. Reconcile registration against gateways, DNS, apps, traffic, and release configuration.

### Answer 4

The BFF keeps all OAuth tokens server-side and proxies REST, WebSocket establishment/data path as designed, and uploads; it reduces exfiltration by script but adds proxy bandwidth/latency, session/CSRF security, destination allowlisting, scaling, and confused-deputy risk. Large uploads and long-lived sockets may make full proxying expensive, though direct presigned narrowly scoped operations or dedicated mediation can address this without general browser tokens. A token-mediating backend keeps refresh authority but releases access tokens for direct API/socket/upload use; script can steal those access tokens. A browser public client owns code+PKCE and all issued tokens; it minimizes backend proxying but malicious script can obtain current/renewed authority. All need exact redirects, correlation, least privilege, CSP/dependency controls, API validation/authorization, and safe refresh. Choose per data-flow threat model; use a BFF for ordinary calls and narrowly scoped single-purpose direct capabilities where justified rather than one broad token.

### Answer 5

Inventory clients, grants, redirect URIs, scopes/resources, token use, owners, and traffic first. For implicit clients, add code+PKCE and token-endpoint CORS/BFF support, run dual telemetry without silent downgrade, migrate SDKs, shorten old token authority, then reject implicit response types and remove URL-token handling/log copies. For password grant, move user interaction to authorization-server browser flows (code+PKCE or device authorization for constrained input), support modern/federated authentication, migrate refresh/session state, stop clients collecting passwords, revoke stored credentials, then disable the grant. For client-credentials impersonation, define whether actions are truly service-owned or delegated: authorize/audit service principals directly, or introduce an approved delegation/token-exchange/support-impersonation design preserving actor/effective subject and consent/approval. Version registrations/policies, publish deadlines, test fallbacks, monitor old use, revoke retired credentials, and never label a compatibility bridge as equivalent security.
