# Worked answers — Provenance and signatures

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. Distinguish signing an image digest from signing a provenance statement about that image.

A digest signature authorizes or authenticates exact artifact bytes. A provenance signature authenticates a structured claim about how one or more subjects were produced. The provenance must itself name the artifact digest. Both can be useful: artifact signature for direct authorization and signed provenance for origin/build-policy evaluation.

## 2. Why does DSSE include payload type in the signed pre-authentication encoding?

Including payload type prevents a valid signature over bytes in one semantic context from being reused as another statement type. The verifier signs/verifies a domain-separated encoding of type and payload, reducing cross-protocol interpretation attacks.

## 3. A provenance signature is valid but the statement subject differs by one hex digit. What is the decision?

Reject the candidate. Cryptographic validity proves only that the signer authenticated the statement bytes; the statement still describes a different subject. Near-match names, tags, or a one-character digest difference cannot be treated as clerical noise. The verifier must compare the candidate digest byte-for-byte with the declared provenance subject before evaluating builder or source policy.

## 4. Explain why a SLSA-shaped document does not establish a SLSA level.

A level includes properties of the build platform, process, isolation, provenance generation, source controls, and verification. Anyone can emit JSON with the right fields. Establishing a level requires evidence that the producer and process satisfy normative requirements, not schema resemblance.

## 5. Compare long-lived-key and keyless trust dependencies.

Long-lived keys depend on secure key generation/storage/use, distribution of public keys, rotation, and revocation. Keyless depends on identity provider, short-lived certificate authority, workflow identity, transparency log, clock, and verifier constraints. Keyless reduces long-lived secret handling but adds online identity infrastructure.

## 6. A valid organization key signs from a developer laptop. How can policy reject it?

Use distinct release-builder identity/key or keyless workflow claims, and require provenance builder ID, repository, workflow, protected ref, and issuer/subject constraints. If the same unconstrained key is shared, policy cannot reliably distinguish the laptop; fix the key architecture.

## 7. What does `materials complete: true` mean, and why might it be untrustworthy?

The producer claims all build materials influencing output are listed. Trust depends on whether the builder isolates/captures inputs and whether network or hidden state can influence output. A self-reported true value from an untrusted or non-hermetic builder is weak evidence.

## 8. Design a key-rotation overlap for Atlas.

Publish and independently verify the new public key, update verifier policy to accept old and new for a bounded window, sign new releases with the new key, verify consumers have updated, stop using the old private key, remove old acceptance after the cutoff, and retain historical verification metadata for older releases.

## 9. Registry referrers contain three signatures. What verification sequence is required?

Verify each OCI descriptor and subject, decode envelope/certificate, verify cryptographic signature, constrain signer identity and validity, check transparency where required, parse payload type, verify statement subject, evaluate predicate/source/builder/material policy, then choose the evidence that satisfies release policy. Count is irrelevant.

## 10. A compromised signing key signed a digest whose independent rebuild matches reviewed source. What decisions remain?

Determine signing time and compromise window, whether the digest was produced before/after compromise, whether independent provenance/source review is trustworthy, whether deployed policy accepts the key, and whether re-signing/rebuilding is required. Matching rebuild strengthens artifact-origin confidence but key revocation/admission and incident handling still need action.

## 11. Why can a reproducible malicious build still pass provenance checks?

Reproducibility shows consistent transformation from inputs to output. Provenance can truthfully describe malicious source and builder. Trust depends on source authorization/review, builder policy, and content/security gates. Determinism is not benevolence.

## 12. Write the non-compensable Atlas verification gates in order.

Verify immutable candidate identity and OCI graph integrity first; then platform executable truth, the effective runtime profile, SBOM subject and completeness, license evidence, vulnerability and VEX disposition, provenance subject/source/materials/builder, signer identity and signature validity, controlled-rebuild evidence class, revocation status, and finally environment-specific promotion authorization. The order prevents later evidence from laundering an earlier failure: a clean scan or valid signature cannot compensate for the wrong digest, a mislabelled platform, leaked secret, or unauthorized runtime authority.

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
