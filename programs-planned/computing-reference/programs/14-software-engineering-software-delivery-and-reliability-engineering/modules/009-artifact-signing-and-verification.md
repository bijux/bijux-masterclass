---
module_id: SDRE-009
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 9
title: Artifact Signing and Verification
status: complete
last_verified: 2026-09-06
---

# Artifact Signing and Verification

## One-Page Review

### Governing question

How can a consumer verify that exact artifact or evidence bytes were authorized by an acceptable identity under a current trust policy, without mistaking a valid signature for trustworthy software?

### Essential definitions

- a **digital signature scheme** provides key generation, signing, and verification algorithms;
- a **private key** authorizes signature creation; a **public key** permits verification but does not itself explain who is trusted;
- the **signed payload** is the exact, unambiguous byte string covered by a signature;
- **domain separation** prevents a valid signature in one protocol or object type from being reinterpreted in another;
- a **certificate** binds a public key to names or attributes under an issuer and validity policy;
- a **trust anchor** is an independently configured starting point for validating keys or certificates;
- **authorization** decides whether an authenticated signer may sign this artifact namespace, predicate, release, or environment;
- **threshold policy** requires at least $t$ acceptable signatures from a defined set of $n$ authorities;
- **rotation** replaces signing or trust material while preserving a verifiable transition;
- **revocation** withdraws future or policy-defined reliance on a key or certificate;
- **transparency evidence** makes signing events publicly or organizationally auditable; inclusion is not correctness;
- a **verification bundle** retains signatures, certificates, timestamps, and log evidence needed for later or offline verification.

### Central model, mechanism, or theorem

Let $m$ be a domain-separated encoding of artifact digest, artifact type, release namespace, and claim type. A cryptographic verifier establishes

$$
Verify(pk,m,s)=true.
$$

Delivery acceptance is strictly stronger:

$$
Accept(a,e,\Pi)=DigestMatch(a,e)\land CryptoValid(e)\land IdentityValid(e)
\land Authorized(e,\Pi)\land TimeValid(e,\Pi)\land EvidenceValid(e,\Pi).
$$

A signature authenticates signed bytes under a key. Policy must separately bind the key to an identity, identity to authority, message to exact artifact, and evidence to an acceptable time and trust state.

### Critical invariants

- recompute the artifact digest from bytes presented for use;
- sign an unambiguous payload that binds digest, algorithm, type, and namespace;
- obtain trust anchors independently of the artifact being verified;
- use maintained cryptographic libraries and approved algorithms rather than handwritten primitives;
- validate certificate path, intended usage, names or claims, validity, and applicable revocation policy;
- authorize exact signer identities for exact artifact or evidence scopes;
- reject unknown payload types, algorithms, critical fields, and ambiguous encodings;
- keep signing authority outside untrusted build workloads when it asserts control-plane facts;
- enforce threshold, separation-of-duty, and delegation rules as policy requires;
- preserve rotation history and verification bundles for supported releases;
- verify transparency inclusion and consistency where policy depends on a log;
- treat signature validity as evidence of origin and integrity, never proof of quality, safety, or permission to deploy.

### Common failures

Common failures include signing a filename instead of bytes, trusting a key shipped beside the artifact, verifying cryptography but skipping subject claims, accepting any certificate from a broad issuer, ignoring identity case or namespace, letting one weak runner share a strong signing identity, exposing keys to tenant steps, trusting expired metadata forever, treating log presence as approval, omitting rollback protection, accepting one signature when policy requires two, losing old trust roots, and disabling claim checks because the signature still verifies.

### Compact example

Artifact bytes hash to `sha256:a1`. A signed statement covers payload type `release/v1`, subject digest `a1`, namespace `payments`, and provenance digest `p7`. The certificate authenticates workflow identity `release.yml@refs/tags/v*` under issuer `ci.example`; trusted policy authorizes that issuer/identity pair only for `payments`, requires log inclusion during certificate validity, and rejects unexpected fields. Reusing the signature for digest `a2`, namespace `admin`, or payload type `approval/v1` fails even though the original signature remains mathematically valid.

### Connections

[SDRE-007](007-build-metadata-and-provenance.md) defines the production claim being authenticated. [SDRE-008](008-generating-and-verifying-software-bills-of-materials.md) defines composition evidence. [SDRE-010](../ROADMAP.md) next assembles these checks into an auditable build pipeline.

## Governing Question

Downloading bytes over an authenticated channel proves facts about that connection, not necessarily who authorized the artifact before it reached the server. A content digest detects a mismatch only if the expected digest arrived through a trusted path. A digital signature can bind a payload to control of a private key, but the verifier still needs to know why that key or identity is authorized.

Correct artifact verification is therefore a protocol and policy pipeline. It starts from independently trusted roots, parses bounded formats, verifies exact signed bytes, binds claims to the presented artifact, checks identity and delegated authority, evaluates time and revocation, and retains enough evidence to explain the decision later.

## Why This Matters

Artifact repositories, mirrors, caches, and deployment channels can be compromised. Signatures let integrity and authorization survive untrusted distribution, but only if verification does more than print “valid.” An attacker with an unrelated valid certificate, an old revoked key, a signature for another namespace, or control of a mutable tag should still fail.

FIPS 186-5 specifies digital signature techniques for detecting unauthorized modification and authenticating a signatory [1]. RFC 8032 specifies Ed25519 and Ed448 encodings, signing, verification, and test vectors [2]. Those cryptographic standards do not define organizational authorization. The Update Framework (TUF) adds signed roles, thresholds, delegation, expiry, versioning, and target hashes to defend software update workflows [3]. Sigstore offers an identity-based model using short-lived certificates and auditable transparency records [4]. Each model has assumptions that policy must name.

## Prerequisites and Retrieval

Retrieve byte string, hash function, digest, collision resistance, public/private key, signature, verification, identity, authentication, authorization, certificate, issuer, subject alternative name, trust anchor, chain, validity interval, revocation, timestamp, nonce, canonicalization, payload type, delegation, threshold, quorum, transparency log, Merkle tree, inclusion proof, consistency proof, rollback, freeze attack, and audit evidence.

From SDRE-005 retrieve immutable artifact coordinates. From SDRE-006 retrieve release namespaces. From SDRE-007 retrieve subject-bound provenance and builder identity. From SDRE-008 retrieve SBOM subject binding. Security Engineering owns cryptographic algorithm selection and deep key-management threat analysis; this chapter owns their safe use in delivery verification.

## Learning Objectives

After completing this module, you should be able to:

1. explain what digital signature verification establishes and what it does not;
2. define an unambiguous, domain-separated signed payload;
3. distinguish raw-key, certificate-based, identity-based, and delegated update trust;
4. bind signatures to exact artifact and evidence digests;
5. validate signer identity and artifact-scope authorization;
6. apply certificate validity, revocation, trusted-time, and transparency policy;
7. design threshold and separation-of-duty controls;
8. rotate and revoke keys without abandoning older supported releases;
9. retain verification bundles for reproducible and offline decisions;
10. diagnose substitution, replay, rollback, freeze, key-compromise, and policy-confusion failures.

## Core Exposition

**Separate cryptography from trust.** A signature scheme has algorithms $Gen$, $Sign$, and $Verify$. Correctness requires signatures made with a generated secret key to verify with its public key. Security additionally asks whether an adversary can forge a signature under a stated attack model. Neither property says the key belongs to the release team or may authorize package `payments`.

Trust begins with configuration: pinned public keys, certificate authorities, identity issuers, TUF root metadata, or another authenticated root. Never accept a public key merely because it accompanies the artifact. That proves only that some holder of the matching private key signed it.

**Define the message.** Signing raw artifact bytes can be sound, but large objects are commonly signed through a cryptographic digest. The payload must identify digest algorithm, byte boundary, artifact type, namespace, and claim semantics. Otherwise the same bytes or signature may be replayed as a different object.

Ambiguous concatenation is dangerous: `ab || c` and `a || bc` produce the same unframed bytes. Use a specified serialization or length-delimited encoding. DSSE 1.0 defines a pre-authentication encoding containing a fixed domain string, payload-type length and bytes, and payload length and bytes [5]. This binds type without requiring JSON canonicalization. The envelope's `keyid` is only a hint; select trust through verified key material and policy.

**Bind the artifact claim.** Recompute $H(a)$ over the downloaded artifact. Parse the authenticated payload and compare its subject digest, algorithm, media type, and namespace. A valid signature on provenance for `a1` does not authorize artifact `a2`. A signature attached to an OCI tag must still bind the resolved manifest digest because the tag can move.

Sign release manifests when a release contains multiple target artifacts and evidence objects. The manifest transitively binds each digest; its signature does not automatically authenticate an unlisted SBOM or later replacement. Every edge in the evidence graph must be explicit.

**Authenticate identity.** With a pinned key, identity may be the key itself plus an out-of-band owner record. With PKI, validate the certificate path from a configured trust anchor, validity interval, critical extensions, intended usage, names or claims, algorithm policy, and applicable revocation information. RFC 5280 defines Internet X.509 path validation, but deployments must also apply current updates and local name and usage policy [6].

Identity-based signing maps short-lived keys to workload or human identity. Sigstore's Fulcio certificates bind an ephemeral key to an OIDC identity; Rekor records signing evidence for audit [4]. Verification must constrain issuer and exact identity or workflow claims. Trusting “any certificate issued by this public service” grants far too much authority.

**Authorize scope.** Authentication answers who controlled the signing credential; authorization answers what that identity may sign. Define rules over repository, package namespace, release line, workflow reference, builder mode, predicate type, environment, and required evidence. Prefer exact allowlists and structured claims. Reject unknown critical fields and unexpected identity patterns.

Keep producer and approver roles separate where risk warrants it. One build-platform identity might attest provenance, while two release authorities approve production. Threshold $t$-of-$n$ limits one-key compromise but adds coordination and recovery costs. Count distinct authorized principals, not repeated signatures from one key.

**Place signing after finalization.** Artifact bytes and their manifest must be finalized before subject digest and signature are created. Signing inside a tenant-controlled build step cannot support a claim against compromise of that step if the private key is accessible there. A trusted control plane can independently observe outputs, evaluate gates, and request signing using narrowly scoped authority.

Key custody depends on the model: offline keys, hardware-backed keys, managed signing services, or ephemeral identity credentials. Avoid exporting private keys. Record signer identity and mechanism without leaking secrets. Rate limits, audit events, and namespace constraints reduce misuse but do not substitute for verification.

**Handle time honestly.** Certificate `notBefore` and `notAfter` values require a trustworthy validation time. A local clock alone may be insufficient for later proof that a short-lived certificate was used while valid. Signed timestamps or transparency evidence can support historical verification, subject to their own trust roots and policies.

Expiration limits how long metadata or credentials are accepted; it does not delete past signatures. Revocation semantics vary. Decide whether a compromise invalidates all historical signatures, only signatures after a known time, or triggers artifact-specific review. Preserve the evidence needed to apply that decision.

**Use transparency precisely.** An append-only log can make signing events discoverable and provide inclusion and consistency evidence. RFC 9162 describes Merkle-tree transparency for certificates and explicitly depends on auditing [7]. Sigstore similarly requires monitoring to detect unexpected identity use and log inconsistency [4]. Inclusion proves that a recorded object was logged under the log protocol; it does not prove the signer was authorized or software benign.

Online lookup creates availability and equivocation dependencies. Verification bundles can retain the certificate, signature, inclusion proof, signed tree material or timestamp, and trust-root version for offline evaluation. A bundle is evidence, not a new root of trust; validate every contained binding.

**Protect update state.** Verifying one target signature does not prevent rollback to an older valid vulnerable target or freeze on stale metadata. TUF separates root, targets, snapshot, and timestamp roles, uses expiry and monotonic versions, and supports delegated target scopes and signature thresholds [3]. This demonstrates a general principle: freshness and consistent repository state require signed metadata beyond a standalone artifact signature.

**Design rotation and recovery.** Rotate before emergency: introduce new trust material through an authenticated transition, overlap verification windows where intended, update signers, then retire old authority. TUF root rotation requires new root metadata to satisfy thresholds under both the previous and new root, preserving a verified chain [3]. Keep offline recovery authority protected and tested.

After suspected compromise, stop signing, bound affected identities and time, preserve logs, revoke or remove authority, rotate trust, identify signed artifacts, and communicate disposition. Do not silently re-sign questionable bytes. A new valid signature cannot prove an old compromise irrelevant.

## Definitions and Notation

- $(sk,pk)\leftarrow Gen(1^\lambda)$: secret/public key pair at security parameter $\lambda$;
- $s\leftarrow Sign(sk,m)$: signature on message $m$;
- $Verify(pk,m,s)\in\{true,false\}$: cryptographic verification;
- $a$: artifact bytes and $H(a)$ their digest;
- $e$: signed evidence bundle;
- $Id(e)$: authenticated signer identity;
- $Scope(e)$: artifact namespace and claim type;
- $T(e)$: trusted-time evidence and validity interval;
- $\Pi$: verifier policy including trust roots, identity scopes, algorithms, thresholds, and time rules.

Signature correctness states

$$
\Pr[Verify(pk,m,Sign(sk,m))=true]=1
$$

for valid keys and messages, allowing any scheme-specific qualification. It does not imply

$$
Authorized(Id(e),Scope(e),\Pi)=true.
$$

That second judgment is policy, not a cryptographic theorem.

## Mechanisms, Invariants, or Proof Structure

**Substitution argument.** Suppose a signed payload contains digest $d$, the verifier recomputes $H(a)=d$, and the digest is collision-resistant for the specified boundary. Replacing $a$ with different bytes requires either a second preimage/collision relevant to the scheme or a newly acceptable signed payload. A filename comparison provides no comparable cryptographic binding.

**Threshold condition.** For authorized signer set $A$ and distinct verified signer identities $V$, a $t$-of-$n$ gate accepts only if $|A\cap V|\ge t$. Duplicate signatures from one identity do not increase the cardinality.

**Policy monotonicity warning.** Adding a new trusted root or broader identity pattern can only expand the set of cryptographically valid objects accepted by that rule, which may reduce security. Trust-store growth is a privileged policy change requiring review and rollback planning.

**Executable policy model.** This program evaluates already cryptographically verified facts. It intentionally performs no hashing, certificate validation, signature verification, or transparency proof.

<!-- bijux-verify: {"id":"evaluate-signature-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=True\nwrong_digest=False\nwrong_identity=False\nwrong_scope=False\ninsufficient_threshold=False\nstale_evidence=False\ncryptography_executed=False\n","stderr":""}} -->
```python
policy = {
    "digest": "sha256:a1",
    "scope": "payments/release",
    "identities": {"build.example/release", "approver.example/team-a"},
    "threshold": 2,
    "minimum_epoch": 42,
}

facts = {
    "digest": "sha256:a1",
    "scope": "payments/release",
    "verified_identities": {"build.example/release", "approver.example/team-a"},
    "evidence_epoch": 43,
}

def accepted(candidate):
    approved = policy["identities"] & candidate["verified_identities"]
    return (
        candidate["digest"] == policy["digest"]
        and candidate["scope"] == policy["scope"]
        and len(approved) >= policy["threshold"]
        and candidate["evidence_epoch"] >= policy["minimum_epoch"]
    )

def changed(name, value):
    return facts | {name: value}

print(f"accepted={accepted(facts)}")
print(f"wrong_digest={accepted(changed('digest', 'sha256:a2'))}")
print(f"wrong_identity={accepted(changed('verified_identities', {'other.example/user', 'approver.example/team-a'}))}")
print(f"wrong_scope={accepted(changed('scope', 'admin/release'))}")
print(f"insufficient_threshold={accepted(changed('verified_identities', {'build.example/release'}))}")
print(f"stale_evidence={accepted(changed('evidence_epoch', 41))}")
print("cryptography_executed=False")
```

## Alternatives and Trade-Offs

**Pinned keys versus certificates.** Pinned keys minimize PKI complexity but make distribution and rotation organizational work. Certificates bind names and validity through issuers but add path, usage, revocation, and identity-policy complexity.

**Long-lived versus ephemeral keys.** Long-lived keys support offline workflows and stable identity but accumulate theft risk. Ephemeral keys reduce stored-secret lifetime and use identity certificates and timestamp evidence, while depending on identity providers, CAs, logs, and monitoring.

**Single versus threshold authorization.** A single signer is fast and available. Threshold approval resists one-key compromise and supports separation of duty, but requires distinct principals, coordination, recovery, and precise failure semantics.

**Embedded versus detached signatures.** Embedded signatures travel with artifacts but change byte layout and may complicate reproducibility. Detached signatures preserve artifact bytes but require a reliable association and distribution convention.

**Online versus bundled verification.** Online services offer current information and discovery. Bundles support offline and historical verification but require freshness and trust-root update policy. High-assurance systems often support both.

**Transparency versus privacy.** Public logs improve auditability and identity monitoring but expose signing identities and timing. Private systems need equivalent append-only evidence, governance, and independent monitoring appropriate to their threat model.

## Failure Modes and Misconceptions

- **“The signature is valid, so the software is safe.”** Validity authenticates signed bytes under a key.
- **“The public key beside the binary is trusted.”** Trust must arrive independently.
- **“HTTPS makes artifact signing redundant.”** Channel and publisher authorization differ.
- **“A filename is the signed subject.”** Bind exact digest and type.
- **“Any certificate from the issuer is acceptable.”** Constrain exact identity and claims.
- **“Key ID proves key identity.”** It is commonly a lookup hint.
- **“A timestamp is trusted time.”** Authenticate its authority and binding.
- **“Log inclusion means approval.”** It means the entry is included under the log protocol.
- **“Transparency needs no monitoring.”** Undetected forks and misuse defeat its purpose.
- **“Expiration revokes history.”** Historical policy needs explicit semantics.
- **“Revocation repairs released artifacts.”** It changes trust decisions and triggers response.
- **“Two signatures mean two authorities.”** Count distinct authorized principals.
- **“Re-signing changes the artifact.”** Detached signing can preserve bytes; embedded signing may not.
- **“One signature prevents rollback.”** Freshness metadata and trusted state are also needed.
- **“Disabling claim checks is harmless.”** Cryptography may verify while subject binding fails.

## Worked Examples

### Example 1

**Untrusted adjacent key.** A mirror replaces binary, signature, and public key together. Raw verification succeeds under the attacker's key, but policy rejects it because the key is absent from independently trusted roots. **Conclusion:** self-supplied verification material cannot establish authority.

### Example 2

**Digest substitution.** A statement validly signs `sha256:a1`; the downloaded artifact hashes to `a2`. Verification stops at subject binding even though certificate and signature validate. **Conclusion:** always recompute and compare the presented bytes.

### Example 3

**Payload confusion.** A system signs untyped JSON and another subsystem interprets the same bytes as production approval rather than test evidence. Domain-separated payload types make the second interpretation fail. **Conclusion:** authenticate semantics as well as bytes.

### Example 4

**Overbroad issuer trust.** Policy accepts every certificate from a public CI issuer. An unrelated repository signs a malicious `payments` artifact. Exact repository, workflow, reference, and namespace constraints reject it. **Conclusion:** issuer validation is not artifact authorization.

### Example 5

**Threshold bypass attempt.** Policy requires two of three release authorities. One compromised key emits three signatures. Distinct verified identity cardinality remains one, so the gate fails. **Conclusion:** thresholds count independent authorized principals.

### Example 6

**Expired short-lived certificate.** A bundle proves the artifact was signed and logged while the certificate was valid. Historical policy accepts it after validating timestamp and log evidence; a bare signature with today's clock does not suffice. **Conclusion:** later verification needs trustworthy temporal evidence.

### Example 7

**Moved tag.** A signed OCI tag reference once resolved to digest `a1` and now resolves to `a2`. The signature payload binds `a1`, so deploying by tag without re-resolution checks is rejected. **Conclusion:** mutable selectors never replace signed content identity.

### Example 8

**Root rotation.** Clients trust root version 4. Version 5 introduces new root keys and is signed to satisfy both old and new thresholds. Clients verify the transition before accepting new target authority. **Conclusion:** rotation is an authenticated state transition, not a key-file replacement.

### Example 9

**Compromised signer.** A release key is suspected stolen at time $t$. The team freezes publication, removes authority, preserves evidence, enumerates artifacts signed by the key, and applies policy for before/after-$t$ review. **Conclusion:** revocation initiates investigation; it does not automatically classify every historical artifact.

### Example 10

**Valid old release rollback.** An attacker serves an older correctly signed but vulnerable release. Artifact signature passes; trusted timestamp/snapshot metadata shows a lower version than client state, so update verification fails. **Conclusion:** standalone signatures do not provide freshness or rollback resistance.

## Cross-Program Connections

- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns cryptographic primitives, PKI, key custody, and adversarial trust analysis.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns stable verification-result and policy APIs.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns signing services and workload identity as internal platform products.
- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) owns quorum, consistency, and replicated-log mechanisms.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns trust-boundary and delegation architecture.

## References

1. National Institute of Standards and Technology, *Digital Signature Standard (DSS)*, FIPS 186-5, February 3, 2023, with a May 12, 2025 planning note for future corrections. [Official publication](https://csrc.nist.gov/pubs/fips/186-5/final). Checked 2026-09-06.
2. Simon Josefsson and Ilari Liusvaara, “Edwards-Curve Digital Signature Algorithm (EdDSA),” RFC 8032, January 2017. [RFC Editor](https://www.rfc-editor.org/rfc/rfc8032.html).
3. The Update Framework Project, *TUF Specification 1.0.28*, roles, thresholds, expiry, delegated targets, target hashes, and root rotation. [Official specification](https://theupdateframework.github.io/specification/v1.0.28/). Checked 2026-09-06.
4. Sigstore Project, “Security Model,” identity certificates, signature transparency, monitoring, and stated non-guarantees. [Official documentation](https://docs.sigstore.dev/about/security/). Checked 2026-09-06.
5. Secure Systems Lab, *Dead Simple Signing Envelope Protocol 1.0*, pre-authentication encoding and envelope semantics. [Official protocol](https://github.com/secure-systems-lab/dsse/blob/v1.0.0/protocol.md). Checked 2026-09-06.
6. David Cooper et al., “Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List Profile,” RFC 5280, May 2008, as updated. [RFC Editor record](https://www.rfc-editor.org/info/rfc5280/). Checked 2026-09-06.
7. Ben Laurie, Emilia Messeri, and Rob Stradling, “Certificate Transparency Version 2.0,” RFC 9162, December 2021, Experimental. [RFC Editor](https://www.rfc-editor.org/rfc/rfc9162.html).

## Exercises

### Exercise 1

**State the guarantee.** For a valid signature over an artifact digest, list what is cryptographically established and every additional fact needed for a release-acceptance decision.

### Exercise 2

**Trace verification.** Trace verification of a bundle containing artifact digest, typed statement, short-lived certificate, signature, timestamp, and transparency inclusion proof. Identify inputs obtained independently.

### Exercise 3

**Diagnose a permissive gate.** A deployment accepts any signature chaining to a configured CA and ignores payload claims. Design containment, evidence collection, corrected policy, and retesting.

### Exercise 4

**Design signing governance.** Design signing, threshold approval, rotation, revocation, offline verification, and recovery for releases across three product namespaces.

### Exercise 5

**Transfer to disconnected devices.** Design artifact and metadata verification for devices offline for two years, including root updates, expiry, rollback resistance, emergency recovery, and audit evidence.

## Answers to the Exercises

### Answer 1

Cryptographic verification establishes that signature $s$ is valid for exact message $m$ under public key $pk$, subject to the scheme, implementation, algorithm, and key assumptions. If $m$ contains a digest and the verifier recomputes it, the message binds the presented bytes under the digest assumptions. Acceptance still needs independently trusted roots; key or certificate identity; certificate path, usage, validity, and revocation checks; exact signer authorization for namespace and claim type; safe parsing and domain separation; subject, algorithm, and media-type matching; threshold rules; trusted-time or transparency evidence; freshness and rollback state; and content policy. It never proves software correctness or safety.

### Answer 2

Begin with locally configured trust roots, allowed issuer/identity pairs, namespace policy, algorithms, log keys, and trusted state. Parse the bundle with resource limits. Validate certificate path and claims, then verify the signature over the specified domain-separated payload. Parse only the authenticated statement type. Recompute the artifact digest and match subject, type, and namespace. Verify the timestamp or signed log promise, inclusion proof, and any required consistency evidence against trusted log material; confirm signing occurred during certificate validity. Apply revocation, threshold, freshness, and authorization rules. The artifact, bundle, repository response, and claimed identity are untrusted inputs; roots and policy must not come solely from them.

### Answer 3

Stop automatic promotion through the gate, retain affected artifacts and bundles, inventory accepted signer identities and namespaces, and compare deployed digests with release records. The CA proves only certificate issuance, so unrelated identities may have been accepted. Correct policy to require exact issuer plus repository/workflow or human identity, allowed reference, artifact namespace, typed payload, subject digest, approved builder or release role, time evidence, and thresholds. Reject unknown claims and claim-check bypasses. Test known-good, wrong subject, wrong repository, wrong workflow, expired, revoked, stale, duplicate-signer, and malformed cases before reopening promotion. Review past acceptances under the new rules rather than assuming they were safe.

### Answer 4

Give each namespace distinct delegated authority. A control-plane build identity signs provenance after artifact finalization; two independent release approvers satisfy a two-of-three production threshold. The signed release manifest binds all artifact and evidence digests. Signing services enforce namespace, payload type, workflow, rate, and audit policy; private keys remain hardware-backed, managed, offline, or ephemeral according to role.

Root and delegation updates are versioned and authenticated. Rotate routinely with overlap and dual authorization; remove compromised keys, freeze affected scope, enumerate signatures, and publish disposition. Bundles retain certificates, signatures, timestamps, log proofs, root/version references, and policy identity for offline review. Offline recovery roots are separated and exercised. No namespace inherits another's signer unless an explicit reviewed delegation says so.

### Answer 5

Provision each device with a pinned initial root and monotonic trusted metadata version. Update bundles contain new root chain, timestamp/snapshot/targets metadata, target hash and length, artifact signature, expiry policy suitable for disconnected operation, and all verification material. Root updates are sequential and satisfy old and new thresholds. The device rejects target metadata older than trusted state and stores version state in rollback-resistant storage where hardware permits.

Two-year offline windows require metadata expiries and refresh logistics designed in advance; disabling expiry silently converts freeze attacks into accepted behavior. Emergency recovery uses a separately protected threshold authority, physical or authenticated service procedure, and auditable operator action. The device verifies root transition, thresholds, namespace, target digest, length, version monotonicity, and applicability before installation, then records decision evidence. Recovery authority is narrow and cannot authorize arbitrary product families.
