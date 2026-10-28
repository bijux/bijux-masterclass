# Worked Answers — Module 07: Secrets, Cryptography, and Sensitive Data

Use these solutions to audit your reasoning for **Secrets, Cryptography, and Sensitive Data**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is an environment variable not a complete secret-management design?

It is one delivery channel but does not define access scope, versioning, rotation, audit, process exposure, backup behavior, or accidental rendering.

**Capstone check.** The secret-wrapper test must prevent accidental rendering through `str`, `repr`, structured events, and exception context.

The chapter’s decisive distinction is this: A secret is not merely a string hidden from Git. It is created, distributed, held in memory, used for one purpose, rotated, revoked, audited, and eventually destroyed. Design that lifecycle before choosing whether the local adapter reads a file, environment variable, operating-system key store, or managed secret service.

## 2. Why separate keys by purpose?

Compromise and cryptanalytic assumptions remain bounded; one protocol cannot be used as an oracle or correlation key for another.

**Capstone check.** The production-configuration guard must reject fixture keys and document which operated secret provider remains outside local proof.

In the cumulative capstone, the rule becomes concrete: Separate keys by purpose and environment. JWT issuer keys, API-key peppers, webhook HMAC secrets, audit pseudonymization keys, data-encryption keys, and test fixtures have different compromise consequences and rotation schedules. Reusing one “master secret” couples all those domains and makes safe revocation impossible.

## 3. What must an algorithm profile name?

Primitive, key material, input framing/canonicalization, output encoding, version identifier, comparison, failure behavior, and rotation.

**Capstone check.** Use `capstone/shared/vectors/webhook.json` to distinguish digesting data from authenticating exact bytes with a secret key.

A useful way to reason about the boundary is: Cryptography is useful only when key ownership, purpose, encoding, comparison, rotation, and failure behavior are explicit. Sensitive data must be classified, minimized, non-rendering, redacted structurally, and retained only as long as justified.

## 4. Why is `==` discouraged for authentication tags?

Many ordinary comparisons return early based on matching prefix, potentially leaking timing information; use a dedicated constant-time primitive.

**Capstone check.** Exercise overlapping active/retiring key IDs; old deliveries verify during the bounded overlap and fail after retirement.

The implementation consequence is: Constant-time comparison protects secret-dependent equality checks from timing leakage within the implementation boundary. It does not compensate for a weak key, verbose error differences, network-level timing dominated by other work, or an authorization flaw.

## 5. Why validate lengths before timing-safe comparison?

Some primitives reject unequal lengths; shape validation avoids exceptions while not disclosing content.

**Capstone check.** The verification path must use constant-time comparison after length/encoding checks; a direct string equality mutant must be rejected.

The important nuance is: Use a password-hashing construction for human-memorable passwords, a keyed digest for high-entropy API-key verification, authenticated encryption when confidentiality and integrity are required, and HMAC or a suitable signature scheme for message authenticity. Hashing is not encryption; encoding is neither. Random identifiers need a cryptographically secure generator and enough entropy for their exposure and lifetime.

## 6. What makes redaction structural?

It traverses parsed fields and nested containers under classification rules rather than replacing substrings in final text only.

**Capstone check.** Run every sensitive shape in `capstone/shared/vectors/redaction.json`, including nested mappings, arrays, headers, and embedded bearer tokens.

Under concurrency or failure, the distinction becomes: Represent secrets as classes with private fields, toString() redaction, and no toJSON disclosure. Avoid structural typing that allows plain strings to masquerade as secrets; use branded types at boundaries. Recursively copy and redact objects without mutating application data. Use timingSafeEqual correctly.

## 7. Why are pseudonyms still sensitive?

Stable values enable linking records and may be reversible through small-domain guessing or access to the key.

**Capstone check.** Use `capstone/shared/vectors/audit.json` to prove stable pseudonyms support correlation without exposing raw principal or tenant identifiers.

The design remains honest only if: Add secret wrappers/providers, recursive redaction, keyed pseudonyms, and audit chaining. Run a canary-secret scan across logs, exceptions, reports, and handoff. Plant a secret-bearing dataclass/default object representation and prove the canary leaks before repair.

## 8. What should an audit record contain?

Actor/effective actor, action, target reference, decision, reason code, correlation, time, policy/security revision, and minimized context.

**Capstone check.** The audit-chain vector proves local tamper evidence only; the checkpoint must state that deletion, truncation, and external anchoring require operated controls.

The consumer-facing consequence is: Audit evidence has limits. A local hash chain can reveal accidental modification or a rewrite that does not also replace its trusted anchor. It does not make a host administrator unable to rewrite history. State the external anchoring or append-only storage required for a stronger claim.

## 9. What should it not contain?

Raw credentials, secrets, full payloads, unnecessary personal data, private keys, or reflected hostile bodies.

**Capstone check.** Verify retention and deletion decisions against migration 007 and the audit model; deletion must not silently destroy required incident evidence.

The operational consequence is: Data minimization is a security control. Do not collect request bodies, artifact contents, tokens, or full URLs merely because a telemetry library can. Define retention and deletion for security events and incident evidence, and ensure backup copies follow the same policy or document the delay explicitly.

## 10. What does a local hash chain prove?

Given a trusted head/anchor and key, it can reveal certain deletions, insertions, or modifications; it does not independently prevent wholesale rewrite.

**Capstone check.** Scan source, generated reports, examples, archives, and the outgoing handoff; a fixture secret may exist only in explicitly bounded test material.

The strongest engineering interpretation is: Use a SecretBytes wrapper with redacted representations and explicit reveal() at the crypto boundary. Define SecretProvider.get(name, version) and test that logging/config serialization cannot expose values. Redact recursively before logging; canonicalize audit records and hash-chain them with a separate keyed digest.

## 11. Trace purpose-bound secrets and sensitive-data handling in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/secrets.py` and `capstone/tracks/typescript-fastify/src/security/secrets.ts`. The required invariant is that secrets never render, keys are separated by purpose, redaction is recursive, and rotation has explicit overlap and retirement.

The defect-oriented view is: Rotation records need a key identifier, status, activation time, retirement condition, and verification overlap. The system must distinguish “may sign,” “may verify,” and “revoked.” Emergency compromise may require immediate denial and accepted delivery loss; routine rotation should preserve in-flight work.

## 12. Compare purpose-bound secrets and sensitive-data handling across Python and TypeScript

Both tracks must preserve this invariant: secrets never render, keys are separated by purpose, redaction is recursive, and rotation has explicit overlap and retirement. The intentional difference is that wrapper types differ; logs, exceptions, fixtures, and handoffs must expose the same safe surface.

Across the Python and TypeScript tracks, the invariant is: Separate keys by purpose and environment. JWT issuer keys, API-key peppers, webhook HMAC secrets, audit pseudonymization keys, data-encryption keys, and test fixtures have different compromise consequences and rotation schedules. Reusing one “master secret” couples all those domains and makes safe revocation impossible.
