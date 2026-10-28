# Reference Answers — Module 07: Secrets, Cryptography, and Sensitive Data

Read after attempting all twelve Secrets, Cryptography, and Sensitive Data exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is an environment variable not a complete secret-management design?

**Answer.** It is one delivery channel but does not define access scope, versioning, rotation, audit, process exposure, backup behavior, or accidental rendering.

**Capstone check.** The secret-wrapper test must prevent accidental rendering through `str`, `repr`, structured events, and exception context.

## 2. Why separate keys by purpose?

**Answer.** Compromise and cryptanalytic assumptions remain bounded; one protocol cannot be used as an oracle or correlation key for another.

**Capstone check.** The production-configuration guard must reject fixture keys and document which operated secret provider remains outside local proof.

## 3. What must an algorithm profile name?

**Answer.** Primitive, key material, input framing/canonicalization, output encoding, version identifier, comparison, failure behavior, and rotation.

**Capstone check.** Use `capstone/shared/vectors/webhook.json` to distinguish digesting data from authenticating exact bytes with a secret key.

## 4. Why is `==` discouraged for authentication tags?

**Answer.** Many ordinary comparisons return early based on matching prefix, potentially leaking timing information; use a dedicated constant-time primitive.

**Capstone check.** Exercise overlapping active/retiring key IDs; old deliveries verify during the bounded overlap and fail after retirement.

## 5. Why validate lengths before timing-safe comparison?

**Answer.** Some primitives reject unequal lengths; shape validation avoids exceptions while not disclosing content.

**Capstone check.** The verification path must use constant-time comparison after length/encoding checks; a direct string equality mutant must be rejected.

## 6. What makes redaction structural?

**Answer.** It traverses parsed fields and nested containers under classification rules rather than replacing substrings in final text only.

**Capstone check.** Run every sensitive shape in `capstone/shared/vectors/redaction.json`, including nested mappings, arrays, headers, and embedded bearer tokens.

## 7. Why are pseudonyms still sensitive?

**Answer.** Stable values enable linking records and may be reversible through small-domain guessing or access to the key.

**Capstone check.** Use `capstone/shared/vectors/audit.json` to prove stable pseudonyms support correlation without exposing raw principal or tenant identifiers.

## 8. What should an audit record contain?

**Answer.** Actor/effective actor, action, target reference, decision, reason code, correlation, time, policy/security revision, and minimized context.

**Capstone check.** The audit-chain vector proves local tamper evidence only; the checkpoint must state that deletion, truncation, and external anchoring require operated controls.

## 9. What should it not contain?

**Answer.** Raw credentials, secrets, full payloads, unnecessary personal data, private keys, or reflected hostile bodies.

**Capstone check.** Verify retention and deletion decisions against migration 007 and the audit model; deletion must not silently destroy required incident evidence.

## 10. What does a local hash chain prove?

**Answer.** Given a trusted head/anchor and key, it can reveal certain deletions, insertions, or modifications; it does not independently prevent wholesale rewrite.

**Capstone check.** Scan source, generated reports, examples, archives, and the outgoing handoff; a fixture secret may exist only in explicitly bounded test material.

## 11. Trace purpose-bound secrets and sensitive-data handling in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/secrets.py` and `capstone/tracks/typescript-fastify/src/security/secrets.ts`. The required invariant is that secrets never render, keys are separated by purpose, redaction is recursive, and rotation has explicit overlap and retirement.

## 12. Compare purpose-bound secrets and sensitive-data handling across Python and TypeScript

Both tracks must preserve this invariant: secrets never render, keys are separated by purpose, redaction is recursive, and rotation has explicit overlap and retirement. The intentional difference is that wrapper types differ; logs, exceptions, fixtures, and handoffs must expose the same safe surface.
