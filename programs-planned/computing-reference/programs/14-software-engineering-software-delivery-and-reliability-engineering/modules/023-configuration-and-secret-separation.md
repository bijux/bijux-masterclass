---
module_id: SDRE-023
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 23
title: Configuration and Secret Separation
status: complete
last_verified: 2026-09-06
---

# Configuration and Secret Separation

## One-Page Review

### Governing question

How can a delivery system vary application behavior across deployments without hiding environment state, embedding credentials, or turning configuration changes into unaudited releases?

### Essential definitions

- **configuration** is declared input that selects behavior without changing artifact bytes;
- a **secret** is sensitive information whose disclosure enables an unauthorized action or reveals protected material;
- a **secret reference** identifies what a workload may request without containing the secret value;
- **effective configuration** is the normalized result after defaults, declarations, overlays, and policy are resolved;
- a **configuration schema** defines names, types, constraints, ownership, classification, defaults, and change semantics;
- **workload identity** is verifiable identity assigned to executing software rather than copied from a human account;
- a **dynamic credential** is created for a bounded subject, purpose, and lifetime;
- **secret zero** is the bootstrap credential or trust anchor used to obtain later secrets;
- **rotation** replaces a credential while preserving authorized service;
- **revocation** makes a credential unusable before or independently of ordinary expiry;
- **configuration drift** is divergence between approved, declared, and effective state;
- **capability** is authority to perform an operation, whether represented by a bearer token, key, role, or session.

### Central model, mechanism, or theorem

Let deployment subject $s=(a,c,r)$ contain artifact digest $a$, effective non-secret configuration digest $c$, and secret-reference set $r$. Let $V(a)$ be values embedded in the artifact and $V(c)$ values exposed by configuration. A valid deployment requires

$$
Valid(s,e)=Schema(c)\land Policy(c,e)\land Resolve(r,e)\land Values(r)\cap(V(a)\cup V(c))=\varnothing.
$$

The artifact and reviewable configuration contain references and policy, not secret values. At runtime, an authenticated workload resolves only authorized references in its own environment. Encryption protects storage or transport; identity, authorization, lifetime, audit, and revocation bound the capability.

### Critical invariants

- environment-specific secret values never enter source, artifact, image layer, configuration history, command line, URL, or review output;
- configuration has a schema, owner, classification, compatibility rule, and deterministic effective identity;
- secret names and references are not assumed harmless; they can reveal architecture and must be disclosed deliberately;
- workloads authenticate with narrow identity and receive only required secrets;
- development, test, and production secret namespaces are separate security boundaries;
- every credential has an owner, purpose, scope, creation event, expiry or review rule, rotation method, and revocation path;
- rotation supports a bounded overlap or an atomic handoff and proves old credentials become unusable;
- missing, malformed, stale, cross-environment, or unauthorized references fail according to explicit policy;
- redaction reduces accidental disclosure but is not a security boundary;
- disclosure response revokes the capability before attempting cosmetic removal from history.

### Common failures

Common failures include baking `.env` files into images, treating Base64 as protection, passing secrets in command arguments, sharing one production token across services, placing credentials in URLs, logging transformed secrets that evade masking, copying production secrets into tests, granting a broker wildcard read access, rotating only the stored value while clients cache the old one, deleting a leaked Git line without revocation, and changing configuration without binding it to a deployment record.

### Compact example

An invoice service artifact contains `PAYMENT_TOKEN_REF=prod/payments/invoice-writer`, not a token. Its workload identity may resolve exactly that reference in production for a ten-minute lease. The effective non-secret configuration is validated and hashed. Rotation stages a new credential, permits a measured overlap, reloads clients, verifies use of the new version, revokes the old version, and tests that the old value is rejected. A log masker is defense in depth; the service never intentionally emits either value.

### Connections

[SDRE-022](022-environment-promotion.md) binds configuration identity to promotion. [SDRE-024](../ROADMAP.md) applies compatibility and secret handling to database change delivery. Security Engineering owns credential threats and cryptographic controls; Platform Engineering owns broker and workload-identity mechanisms.

## Governing Question

An application binary is useful because the same bytes can run in more than one context. Yet a service must know its port, dependency endpoints, feature policy, quotas, and credentials. If all of those values are compiled into the binary, every operational change becomes a rebuild. If all of them are placed in an unrestricted text file, secrets spread through repositories, artifacts, logs, backups, and developer machines.

The engineering question is therefore not merely where to put settings. It is how to make behavior-changing state visible, typed, reviewable, reproducible, and reversible while keeping sensitive capabilities out of durable delivery surfaces. This chapter develops that boundary and the runtime mechanism that crosses it safely.

## Why This Matters

The Twelve-Factor App popularized strict separation of deploy-varying configuration from code and proposed environment variables as a language-neutral carrier [1]. Its open-source litmus test remains useful: publishing the codebase should not disclose credentials. The carrier, however, is not the security model. Environment variables can be inherited by child processes, captured by diagnostic tooling, exposed in crash material, or printed by careless debugging. A mature design separates configuration from code and secrets from ordinary configuration.

OWASP's current Secrets Management Cheat Sheet describes centralized management, fine-grained access, automation, auditing, and a lifecycle of creation, rotation, revocation, and expiration [2]. It also recommends dynamic secrets where possible and separation of production and development boundaries. These are mechanisms for reducing exposure and recovery time, not claims that a particular vault product makes secrets safe.

NIST SP 800-128 treats configuration management as a security practice across a system lifecycle [3]. A setting that disables certificate validation, expands an allowlist, changes an authorization mode, or redirects an endpoint is security-relevant even when it contains no credential. Configuration therefore needs governance proportionate to consequence.

## Prerequisites and Retrieval

Retrieve artifact, digest, provenance, deployment, environment, configuration, schema, default, overlay, identity, authentication, authorization, least privilege, credential, token, key, certificate, encryption, expiry, revocation, rotation, audit, drift, reconciliation, rollback, and incident response.

From SDRE-019 retrieve the distinction between trusted and untrusted execution. From SDRE-021 retrieve readiness versus deployment policy. From SDRE-022 retrieve the deployment subject $(a,c,m)$ and target-resolved secret references. Do not equate an application password with a cryptographic key: NIST SP 800-57's cryptoperiod guidance applies specifically to cryptographic key management, although its lifecycle discipline informs broader credential design [4].

## Learning Objectives

After completing this module, you should be able to:

1. distinguish code, non-secret configuration, secret values, references, and runtime state;
2. design a configuration schema with security and operational semantics;
3. bind effective configuration identity to a deployment without hashing secret values into public records;
4. explain why storage location, encoding, and redaction do not by themselves secure a secret;
5. design workload authentication and least-privilege secret resolution;
6. compare static, rotated, federated, and dynamically leased credentials;
7. plan rotation with bounded overlap, convergence evidence, and revocation;
8. calculate residual credential validity under expiry and revocation assumptions;
9. detect drift and respond safely to missing or malformed configuration;
10. design disclosure response, tests, and audit records without reproducing secret values.

## Core Exposition

**Classify state before choosing a carrier.** Code describes stable program behavior. A code default is appropriate when the value should remain the same across deployments and changing it deserves code review and a new artifact. Non-secret configuration selects behavior per deployment: port, replica target, timeout, feature policy, or dependency name. A secret value conveys sensitive knowledge or authority: a private key, password, bearer token, or signing material. A secret reference is metadata used to request such a value. Dynamic runtime state includes leases, caches, health, and discovered topology; it must not be mistaken for declared configuration.

Sensitivity and behavioral impact are independent dimensions. `TLS_VERIFY=false` is usually not confidential, but it is high-impact security configuration. A database password is confidential and high impact. A public color setting is neither. A broker path may reveal tenancy or system structure despite not granting access. Classify each field rather than declaring an entire file either “secret” or “safe.”

**Give configuration a contract.** For each setting, define a stable name, type, allowed domain, units, default, whether it is required, owner, sensitivity, environment scope, mutability, restart or reload semantics, compatibility range, deprecation rule, and safe failure behavior. Validate at the earliest trustworthy boundary and again before use. Reject unknown settings when silent typos would be dangerous.

Defaults trade convenience against ambiguity. A safe, durable default such as bounded batch size may reduce repetition. A production endpoint, tenant identity, or authorization mode should often be required explicitly. Never default a missing credential to a shared development credential. Include units in names or types: `request_timeout_ms=5` and `request_timeout_s=5` are different contracts.

Normalize effective configuration before assigning identity. Resolve defaults and approved overlays, sort maps canonically, normalize units, and hash the non-secret result. Record the schema and policy versions. The digest makes a behavior-selecting subject auditable without exposing secret values. A secret reference identifier or version constraint may be bound separately when its disclosure is acceptable. Do not hash low-entropy secret values into a public record; attackers can test guesses offline.

**Keep values out of durable delivery surfaces.** A secret must not appear in source, commit history, build arguments retained in metadata, image layers, package archives, deployment plans, command-line arguments, URLs, filenames, telemetry labels, error messages, screenshots, review records, or test fixtures. Encrypting a repository file moves the key-management problem; it does not eliminate access, rotation, audit, or bootstrap design.

Base64 is encoding, not encryption. Redaction is a fallible output filter, not authorization. GitHub's current secure-use guidance explicitly warns that automatic redaction is not guaranteed because values can be transformed [5]. Prevent emission first, restrict which process can read the value, and use masking only as defense in depth.

Environment variables are portable and sometimes reasonable for low-risk settings. For secrets, evaluate the platform's process inspection, inheritance, crash collection, support tooling, and `/proc` behavior. A broker-provided memory file, protected volume, local agent, file descriptor, or direct API response can narrow exposure, but every carrier has lifecycle and cleanup requirements. There is no universally safe carrier independent of operating system and threat model.

**Resolve at runtime through identity.** A deployment declaration should contain a logical role or secret reference, not its value. At runtime the workload proves identity to a secret broker or identity provider. Policy maps that subject, environment, resource, and operation to the smallest authority. The broker returns a bounded credential or makes the requested operation without revealing key material.

The bootstrap produces a secret-zero problem: how does the workload authenticate to the broker? Prefer platform-attested workload identity, mutually authenticated credentials provisioned by the platform, or federation from a trusted identity provider. OpenID Connect Core defines signed identity assertions and validation including issuer and audience [6]. Federation removes a copied long-lived cloud key only when the relying service constrains issuer, audience, subject, and other relevant claims. A broad trust policy merely moves the vulnerability.

Use separate identities for build, deploy, runtime, rotation, and emergency recovery. Reading application data, writing deployments, rotating credentials, and changing policy are different capabilities. Human administrators should not automatically see all runtime values. Log broker decisions and metadata—subject, reference, version identifier, decision, and time—without logging the value.

**Prefer bounded credentials.** A static token remains useful until expiry or effective revocation. A short-lived dynamic credential reduces the maximum useful theft window and discourages reuse, but only if issuance is authenticated, scope is narrow, expiry is enforced by the relying service, and refresh cannot mint broader access. High issuance availability and clock behavior then become dependencies.

Let a stolen credential be issued at $t_i$, expire at $t_x$, be detected at $t_d$, and become effectively revoked at $t_r=t_d+\Delta_r$. Assuming the relying service enforces both expiry and revocation, the last useful time is

$$
t_{end}=\min(t_x,t_r),
$$

and exposure after detection is $\max(0,t_{end}-t_d)$. This is an upper bound under the stated controls, not a probability of misuse. Offline-decrypting keys, copied data, and sessions derived from the credential may outlive it and require separate containment.

**Rotate as a distributed protocol.** Replacing a value in storage is not rotation. Issuers, brokers, clients, caches, connection pools, and relying services must converge. A common protocol is: create new version; validate it without exposing it; allow old and new for a bounded overlap; signal or trigger client reload; observe authenticated use of the new version; stop issuing the old version; revoke it; verify rejection; then remove retained copies according to policy.

Overlap improves availability but temporarily doubles valid material. An atomic cutover reduces overlap but can cause outage when clients cannot update together. Choose from dependency behavior and risk. Define maximum overlap, lease duration, retry rules, client refresh jitter, telemetry, rollback, and authority to extend the window. Never let “temporary dual acceptance” become indefinite.

Cryptographic encryption keys require additional care. Changing a data-encryption key may require re-encryption or a key hierarchy that permits old ciphertext to remain readable. NIST SP 800-57 Part 1 Revision 5 distinguishes key states and cryptoperiod considerations [4]. Do not revoke a decryption key before proving retained data can be recovered, and do not confuse credential rotation with data transformation.

**Fail according to consequence.** Validate configuration before accepting traffic. A malformed authorization policy should fail closed. A missing optional telemetry endpoint might degrade visibly under an approved policy. A secret broker outage may justify serving requests with an unexpired cached lease, but not silently extending an expired one. Specify each decision; “fail open” and “fail closed” are incomplete without the protected property and availability consequence.

Reload needs transactional semantics. Parse and validate a complete candidate snapshot, acquire required references, check cross-field invariants, then atomically publish the new snapshot. If validation fails, retain the last known valid state when policy allows and raise an alert. Updating fields one by one can expose impossible mixtures.

**Observe and reconcile.** Compare approved configuration identity with effective process state. Record which version each instance loaded, not just what the controller intended. Detect manual changes, stale replicas, unapproved broker paths, and inconsistent feature state. Reconciliation may restore declared state; incident response may instead freeze it to preserve evidence.

Configuration changes deserve a delivery record: actor, subject, review, policy, effective digest, secret references where safe, rollout, observations, and recovery. High-risk changes may require staged exposure even when artifact bytes do not change. Rollback means restoring a compatible configuration snapshot and resolving currently authorized secrets, never resurrecting a revoked credential from an old bundle.

**Respond to disclosure by invalidating capability.** Treat a secret found in code or logs as compromised. Identify its scope and derived credentials, revoke or constrain it, rotate dependents, audit use, preserve evidence, remove exposed copies from live surfaces and retention systems under governance, and test that the old value fails. Deleting a source line or rewriting Git history does not revoke authority and can destroy useful history or disrupt collaborators.

Preventive scanning should run before commit, during review, at build admission, and over governed repositories and artifacts. Detection patterns miss unknown and transformed values and produce false positives. Pair scanning with broker inventory, issuance audit, canary tokens where appropriate, egress controls, and practiced response. Tests use synthetic values with no production authority.

## Definitions and Notation

Let $A$ be artifact bytes, $C$ normalized non-secret configuration, $R$ a set of secret references, $E$ an environment, and $W$ a workload identity. Let $Values(R,E)$ be the secret values a broker could return for authorized references. The deployment subject is

$$
s=(H(A),H(C),R),
$$

where $H$ is a collision-resistant digest used for identity. References may be replaced by a digest when their names are sensitive, but policy must still bind their meaning.

Let $Authorize(W,r,E,o,t)$ decide whether workload $W$ may perform operation $o$ on reference $r$ in environment $E$ at time $t$. Resolution is safe only if authentication, authorization, channel protection, response handling, audit, expiry, and revocation assumptions all hold.

A **bearer credential** grants authority to whoever presents it. A **proof-of-possession credential** additionally requires possession of bound key material. The latter reduces some replay paths but does not repair excessive scope or compromised workloads.

## Mechanisms, Invariants, or Proof Structure

**Separation invariant.** If secret values are absent from $A$ and $C$, publishing artifact and configuration does not directly publish those values. This is a limited non-disclosure claim; reference names, endpoints, and policies can still reveal sensitive structure.

**Least-authority invariant.** For workload $W$, the granted set $G_W$ should be a subset of the required set $N_W$ only if requirements are wrong; operationally the target is $G_W=N_W$. Because incomplete authority breaks service and excess authority expands blast radius, derive $N_W$ from concrete operations and test both allowed and denied paths.

**Rotation invariant.** During a planned overlap, every healthy client can obtain the new version and the relying service may accept both declared versions. After the deadline, issuance and acceptance of the old version are denied. Observing new-version use is necessary but not sufficient; explicit old-version rejection proves retirement.

**Digest limitation.** A configuration digest proves equality to recorded bytes under hash assumptions. It does not prove the settings are safe, the running process loaded them, or secret references resolved correctly. Those are separate validation and observation claims.

**Executable policy model.** The following deterministic model validates non-secret configuration and runtime references. It models decisions, not a real broker or cryptographic system.

<!-- bijux-verify: {"id":"configuration-secret-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_configuration=allowed\nembedded_secret=denied:secret-value-in-config\nmissing_reference=denied:unresolved-reference\ncross_environment=denied:wrong-environment\nrotation_overlap_accepts_old_and_new=True\npost_rotation_accepts_old=False\nartifact_contains_environment_secret=False\n","stderr":""}} -->
```python
schema = {"timeout_ms": int, "payment_secret_ref": str}
resolved = {("production", "production/payments/invoice-writer")}

def validate(config, environment):
    if set(config) != set(schema):
        return "denied:schema"
    if not isinstance(config["timeout_ms"], int) or not 1 <= config["timeout_ms"] <= 30_000:
        return "denied:bounds"
    reference = config["payment_secret_ref"]
    if config.get("payment_secret_value") or reference.startswith("value:"):
        return "denied:secret-value-in-config"
    if not reference.startswith(f"{environment}/"):
        return "denied:wrong-environment"
    if (environment, reference) not in resolved:
        return "denied:unresolved-reference"
    return "allowed"

valid = {"timeout_ms": 1500, "payment_secret_ref": "production/payments/invoice-writer"}
print(f"valid_configuration={validate(valid, 'production')}")
embedded = {"timeout_ms": 1500, "payment_secret_ref": "value:actual-token"}
print(f"embedded_secret={validate(embedded, 'production')}")
missing = {"timeout_ms": 1500, "payment_secret_ref": "production/payments/missing"}
print(f"missing_reference={validate(missing, 'production')}")
print(f"cross_environment={validate(valid, 'staging')}")
accepted_during_overlap = {"old-v4", "new-v5"}
print(f"rotation_overlap_accepts_old_and_new={accepted_during_overlap == {'old-v4', 'new-v5'}}")
accepted_after_deadline = {"new-v5"}
print(f"post_rotation_accepts_old={'old-v4' in accepted_after_deadline}")
artifact_files = {"service.py", "schema.json", "defaults.json"}
print(f"artifact_contains_environment_secret={'production-token' in artifact_files}")
```

The example intentionally uses a reference naming convention for clarity. A real system authenticates subjects, evaluates structured policy, protects transport, avoids revealing existence through error differences where that matters, and never handles values in this validator.

## Alternatives and Trade-Offs

**Environment variables versus mounted files versus broker calls.** Environment variables are portable but broadly inherited and often captured by diagnostics. Mounted files can use filesystem permissions and update atomically but may linger or be copied. Direct broker calls enable leases and detailed audit but add network, identity, caching, and availability concerns.

**Static versus dynamic credentials.** Static credentials work with legacy systems and disconnected operation but demand strong rotation and inventory. Dynamic credentials reduce lifetime and reuse but depend on reliable issuance and correct expiry enforcement.

**Reference latest versus pin a version.** Following the current version simplifies routine rotation. Pinning makes rollout reproducible. A useful design binds a permitted version range or role, records the resolved version securely, and controls convergence.

**Central broker versus platform-local broker.** Centralization standardizes policy and audit but can create a large failure domain. Local brokers improve latency and isolation but complicate consistent governance and replication.

**Automatic reload versus restart.** Reload avoids disruption but adds concurrency and partial-state hazards. Restart is simpler and exercises startup validation but consumes capacity and may prolong rollout.

**Overlap versus atomic rotation.** Overlap tolerates distributed clients at the cost of two valid credentials. Atomic cutover narrows coexistence but requires coordinated consumers or can cause outage.

**Encrypted configuration in Git versus external values.** Encrypted files provide reviewable declarations and offline workflows, but decryption keys, plaintext endpoints, rotation, and accidental output remain. External brokers minimize stored values in delivery systems but require identity and availability engineering.

## Failure Modes and Misconceptions

- **“Configuration is harmless because it is not code.”** settings can disable controls or redirect data.
- **“All configuration belongs in one environment file.”** fields have different sensitivity, ownership, and change semantics.
- **“Base64 protects the token.”** reversible encoding offers no confidentiality.
- **“Encrypted in Git means managed.”** access, bootstrap, rotation, revocation, audit, and plaintext handling remain.
- **“Environment variables are always secure.”** exposure depends on process and platform boundaries.
- **“A vault makes every reader trustworthy.”** wildcard policy and compromised workloads still disclose values.
- **“Secret names are public.”** names can reveal accounts, tenants, or architecture.
- **“Masking prevents leakage.”** transformed or segmented values can evade redaction.
- **“Rotation means writing a new value.”** consumers and relying services must converge and reject the old value.
- **“Short lived means low privilege.”** lifetime and scope are separate dimensions.
- **“Federation removes trust.”** it changes trust and requires constrained claim validation.
- **“Rollback can restore the old bundle.”** a revoked secret must stay revoked.
- **“Deleting the leaked line contains the incident.”** capability must be invalidated and use audited.
- **“Production credentials improve test realism.”** they turn test compromise into production compromise.
- **“A configuration hash proves safety.”** it proves identity, not correctness or effective loading.

## Worked Examples

### Example 1

**Classify five settings.**

**Situation.** A service has `PORT=8080`, `TLS_VERIFY=false`, a database password, `DB_PASSWORD_REF=prod/db/orders`, and a rolling error counter.

**Reasoning.** `PORT` and `TLS_VERIFY` are non-secret configuration, although the latter is security-critical. The password is a secret value. `DB_PASSWORD_REF` is a reference whose disclosure must be assessed but which does not itself authorize access. The counter is runtime state. Putting all five in a “secrets” file would hide the critical review difference; putting all five in ordinary config would expose the password.

**Conclusion.** Classify fields by behavioral impact, confidentiality, lifecycle, and ownership before selecting storage.

### Example 2

**Detect an image-layer leak.**

**Situation.** A container build copies `.env`, runs a command, and deletes `.env` in a later layer.

**Reasoning.** Layered images preserve earlier filesystem changes. Deletion in a later layer changes the merged view but does not necessarily remove bytes from previous layers or build caches. Anyone with image or cache access may recover the value. The build also cannot pass the open-publication litmus test.

**Conclusion.** Exclude values from build context and artifact creation; deletion after inclusion is not separation.

### Example 3

**Calculate a theft window.**

**Situation.** A credential is detected stolen at 10:00. It expires at 10:12. Revocation begins immediately but reaches the relying service after 18 minutes.

**Reasoning.** With enforced expiry and revocation, $t_{end}=\min(10{:}12,10{:}18)=10{:}12$. The residual validity after detection is at most 12 minutes. This does not bound damage from already copied data or sessions that the service fails to terminate.

**Conclusion.** Short expiry limits bearer use here, while downstream containment remains necessary.

### Example 4

**Design least privilege.**

**Situation.** A platform team proposes one credential that lets every service read all production secrets.

**Reasoning.** A compromise of any service then exposes the entire set and audit cannot reliably identify intended use. Derive each workload's needed operations: the invoice writer needs read access to one payment role, not rotation, policy administration, or unrelated databases. Separate namespaces and identities constrain both mistakes and attackers.

**Conclusion.** Grant per-workload, per-environment, per-purpose authority and test explicit denials.

### Example 5

**Reject a loose federation rule.**

**Situation.** A cloud trust policy accepts any signed assertion from the organization's CI identity provider.

**Reasoning.** Signature validation establishes issuer control, not that this repository, branch, workflow, environment, or audience should deploy. A malicious or compromised low-trust job may obtain a valid assertion. Constrain issuer, audience, subject, repository/environment claims where supported, permissions, and session lifetime.

**Conclusion.** Federation eliminates a stored cloud key only when claim-to-authority policy is narrow.

### Example 6

**Rotate without outage.**

**Situation.** Two hundred service instances cache a database credential for up to five minutes.

**Reasoning.** Create `v5`; let the database accept `v4` and `v5` for a bounded window longer than measured refresh plus margin; trigger jittered reload; observe successful `v5` authentication by every healthy cohort; stop issuing `v4`; revoke it; test a controlled `v4` rejection. If some instances remain stale, halt and remediate rather than extending overlap indefinitely.

**Conclusion.** Rotation is a measured convergence protocol ending in proven rejection.

### Example 7

**Handle an invalid reload.**

**Situation.** A live reload changes timeout from `1500ms` to `-5ms` and changes an endpoint simultaneously.

**Reasoning.** Field-by-field mutation could expose the new endpoint with an old timeout or an invalid negative timeout. Parse a complete candidate, validate types, bounds, cross-field rules, references, and policy, then publish atomically. On failure, retain the previous valid snapshot if policy permits and alert with sanitized diagnostics.

**Conclusion.** Configuration reload is a transaction, not a sequence of independent assignments.

### Example 8

**Diagnose a redaction failure.**

**Situation.** A CI system masks the literal token, but a debugging step prints its characters separated by spaces.

**Reasoning.** Literal masking does not recognize every transformation. The sensitive job should not execute untrusted debug logic and should not possess credentials outside the exact step requiring them. Logs need access and retention controls, but containment begins by revoking the token and auditing use.

**Conclusion.** Redaction is defense in depth; trust separation and non-emission are primary.

### Example 9

**Recover from a broker outage.**

**Situation.** The secret broker is unavailable while instances hold leases valid for eight more minutes.

**Reasoning.** A declared policy may allow existing instances to use unexpired leases while refusing new privileged operations that require fresh credentials. The system alerts, stops risky rollout, preserves expiry, and recovers the broker. Extending lease validity locally would bypass issuer and relying-service policy.

**Conclusion.** Availability behavior must respect credential validity rather than inventing authority during failure.

### Example 10

**Respond to a committed token.**

**Situation.** A developer commits a production API token and removes it three minutes later.

**Reasoning.** Clones, mirrors, caches, notifications, and logs may retain the commit. First revoke the token, rotate dependent material, restrict affected paths, audit use from issuance through revocation, and check derived sessions. Then remove exposed copies according to repository and retention policy while preserving incident evidence. Test that the old token fails.

**Conclusion.** Removal improves hygiene; revocation and investigation contain capability.

## Cross-Program Connections

- **Security Engineering:** threat modeling, access control, credential compromise, cryptography, and incident response define the security properties.
- **Platform Engineering:** workload identity, secret brokers, admission policy, mounted projections, and reconciliation implement the boundary.
- **Cloud Engineering:** provider federation, managed identity, key services, and regional control planes change the mechanism and failure domains.
- **Systems Engineering:** process inheritance, memory, files, crash dumps, clocks, and signals determine carrier exposure and reload behavior.
- **Software Architecture:** configuration ownership and dependency boundaries determine which component may resolve which capability.
- **Database Engineering:** credentials, encryption keys, migrations, and connection pools impose rotation and compatibility constraints.
- **API Engineering:** tokens, audiences, scopes, proof of possession, and error behavior shape external secret use.
- **Testing and Quality Engineering:** synthetic credentials, denial tests, fault injection, and configuration combinatorics provide evidence without production authority.

## References

1. Adam Wiggins, [“The Twelve-Factor App: Config”](https://www.12factor.net/config), last updated 2017; retrieved 2026-09-06. Used for code/config separation and the environment-variable pattern, not as a complete secret-security model.
2. OWASP Cheat Sheet Series, [“Secrets Management Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), current page retrieved 2026-09-06. Used for centralized management, least privilege, automation, lifecycle, rotation, revocation, expiry, audit, and environment separation.
3. NIST, [Special Publication 800-128: *Guide for Security-Focused Configuration Management of Information Systems*](https://csrc.nist.gov/pubs/sp/800/128/upd1/final), updated 2019; retrieved 2026-09-06.
4. NIST, [Special Publication 800-57 Part 1 Revision 5: *Recommendation for Key Management: Part 1 — General*](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final), May 2020; retrieved 2026-09-06. Applied to cryptographic keys, not generalized silently to all passwords or tokens.
5. GitHub Docs, [“Secure use reference”](https://docs.github.com/en/actions/reference/security/secure-use), current documentation retrieved 2026-09-06. Used for the limitation that automatic secret redaction is not guaranteed.
6. OpenID Foundation, [*OpenID Connect Core 1.0 incorporating errata set 2*](https://openid.net/specs/openid-connect-core-1_0.html), December 2023; retrieved 2026-09-06. Used for issuer, audience, signed assertion, and relying-party validation concepts.
7. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, Chapters 2 and 5. Used for configuration management and deployment-pipeline discipline.
8. NIST, [Special Publication 800-53 Revision 5: *Security and Privacy Controls for Information Systems and Organizations*](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), updated 2025; retrieved 2026-09-06. Used for least privilege, audit, configuration, and system-lifecycle control families.

## Exercises

### Exercise 1

**Precise understanding.**

Classify each item as code, non-secret configuration, secret value, secret reference, or runtime state: a compiled retry algorithm; `MAX_RETRIES=4`; a private signing key; `SIGNING_KEY_REF=prod/release/signer`; and the current retry count. Explain why confidentiality and behavioral impact are separate.

### Exercise 2

**Mechanism derivation.**

A token is detected at 14:00, expires at 14:40, and effective revocation completes 11 minutes after detection. Derive its maximum residual bearer-validity window under the chapter's assumptions. Name two effects the result does not bound.

### Exercise 3

**Implementation diagnosis.**

A service reads six settings independently during reload, prints the full candidate map on validation error, and falls back to `dev-password` when its production reference is missing. Diagnose the defects and propose a safe reload design.

### Exercise 4

**Design comparison.**

Compare a static credential mounted as a protected file with a five-minute dynamic credential fetched through workload federation. Evaluate exposure, bootstrap, availability, rotation, audit, and legacy compatibility. Choose one for a new payment service and state assumptions.

### Exercise 5

**Unfamiliar transfer.**

A fleet of intermittently connected field devices must verify signed update manifests for six months offline. Design configuration and key separation, rotation, compromise response, and recovery. Explain why ordinary short-lived online credentials are insufficient and distinguish signing from verification authority.

## Answers to the Exercises

### Answer 1

The retry algorithm is code because it defines stable behavior and changes with the artifact. `MAX_RETRIES=4` is non-secret configuration: it varies behavior but need not be confidential. The private signing key is a secret value and capability. `SIGNING_KEY_REF` is a secret reference; it identifies requested authority without being the key, although its name may reveal sensitive structure. The current retry count is runtime state. Confidentiality and behavioral impact are independent: a public `TLS_VERIFY=false` setting can be security-critical, while an opaque secret may be confidential even before its operational consequence is known.

### Answer 2

Let detection be $t_d=14{:}00$, expiry $t_x=14{:}40$, and effective revocation $t_r=14{:}11$. Then $t_{end}=\min(t_x,t_r)=14{:}11$, so maximum residual bearer validity after detection is 11 minutes. The bound assumes both controls are enforced and clocks and propagation behave as stated. It does not bound data already copied, actions already completed, sessions derived from the token, offline use of recovered key material, or damage from a broader compromise. Any two of these with explanation are acceptable.

### Answer 3

Independent reads allow a request to observe a mixed snapshot. Full-map logging exposes any secret or sensitive reference. The production fallback silently grants unintended shared authority and hides an outage or deployment defect. The service should parse a complete candidate, validate schema, bounds, cross-field rules, environment-scoped references, and policy, resolve required capabilities through workload identity, and atomically swap the snapshot. On failure it should retain the last valid snapshot only under explicit policy, sanitize diagnostics, alert, and refuse startup or affected operations when no safe prior state exists. It must never substitute a development credential in production.

### Answer 4

The protected file supports legacy consumers and broker outages but the static value persists on disk, requires coordinated rotation, and may be copied by diagnostics or privileged readers. Federation avoids a stored long-lived bootstrap key when platform identity is trustworthy; a five-minute lease narrows theft duration and provides issuance audit, but depends on identity-provider and broker availability, clock correctness, refresh logic, and relying-service expiry enforcement. For a new payment service, prefer narrowly scoped federation and dynamic credentials, cache only unexpired leases in protected memory, stop risky rollout on issuer failure, and test denial and expiry. A static file is acceptable only if the payment dependency cannot issue dynamic credentials and compensating controls, rapid rotation, and file lifecycle are demonstrated.

### Answer 5

Each artifact contains public verification keys or a compact trusted root set, never the release signing private key. Devices store non-secret update policy separately from mutable operational configuration and verify manifest signature, device class, version monotonicity, and validity rules offline. Because six-month disconnection prevents frequent online lease refresh, trust uses long-lived offline-capable verification material with planned overlapping public-key generations. The release system protects signing keys in a narrowly authorized signing service or hardware boundary. Before rotation, devices receive a manifest signed by an already trusted key that authorizes the next verification key and an activation interval. Compromise response revokes signing authority online, ships an emergency trust update through still-valid independent recovery keys, blocks vulnerable versions when devices reconnect, and audits signatures. Signing authority creates accepted updates and must remain secret; verification authority only checks signatures and can be distributed. A sound alternative may use threshold or multiple independent signatures, provided it defines offline recovery, anti-rollback, key expiry, and loss scenarios.
