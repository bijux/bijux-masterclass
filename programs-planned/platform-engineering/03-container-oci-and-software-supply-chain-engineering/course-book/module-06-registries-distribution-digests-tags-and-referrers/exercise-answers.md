# Worked answers — OCI distribution and registries

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. Distinguish repository name, tag, manifest digest, and blob digest.

The repository is a logical namespace and access boundary. A tag is a mutable name within it. A manifest/index digest identifies exact JSON bytes for a top-level object. A blob digest identifies exact config, layer, or artifact bytes. A release usually selects a repository plus top-level digest and follows verified descriptors to child blob digests.

## 2. Why should clients verify downloaded blobs even if the registry checked them on upload?

Storage corruption, compromised registry code, proxy/mirror faults, transport bugs, or incorrect server behavior can occur after upload. The digest is designed for consumers to verify exact bytes at the trust boundary. Server-side checking improves integrity but does not remove client responsibility.

## 3. Explain how content negotiation can change what a manifest request returns.

The client advertises accepted manifest media types. A registry may return an OCI index, a platform manifest, or a compatible Docker representation depending on reference and support. The selected bytes have different digests and semantics. Release evidence must record the actual subject and media type, not assume a tag always resolves identically.

## 4. A user can pull a blob digest but not list the repository. What authorization questions arise?

Determine whether possession of a digest grants fetch, whether cross-repository mounts leak existence, whether the blob contains sensitive data, and whether repository policy is enforced on blob requests. Physical deduplication must not erase logical tenant/repository boundaries.

## 5. Why is a referrer list not proof that an attached SBOM is trustworthy or complete?

The registry may omit, add, or reorder referrers. An artifact can have the wrong subject, malformed schema, untrusted signature, incomplete coverage, or stale content. Discovery gives candidates for verification; it is not an authorization decision.

## 6. Design a digest-based promotion record for Atlas.

Record top-level digest, repository, media type, platform child digests, evidence artifact digests, source/provenance decision, policy result, approver, time, target environment, and optional tag updates. Deployment consumes the exact digest. Post-promotion evidence confirms any tags point to it.

## 7. A registry has immutable tags. Why should deployment still retain the digest?

Immutability may be scoped, misconfigured, bypassable by administrators, or changed later. Digest identity is intrinsic to the object and portable across registries. Retaining it makes deployment and audit independent of tag-policy assumptions.

## 8. Explain why deleting a tag does not revoke an image.

Other tags, direct digest access, mirrors, caches, running nodes, and retained manifests can still expose or execute the content. Revocation is a policy/action across deployment, admission, registries, caches, and possibly key/evidence systems. Tag deletion is one reference change.

## 9. What can a compromised registry do despite cryptographic digests?

The attacker can move tags, delete or withhold content, publish new malicious digests, modify access control, hide referrers, serve malformed responses, and cause denial of service. They cannot substitute different bytes under a securely verified existing SHA-256 digest without a cryptographic break, but can target clients that skip verification.

## 10. Design a retention policy that supports rollback and incident investigation.

Retain current and previous approved digests, all subject-bound evidence, revoked releases for a forensic period, and blobs required to reconstruct them. Protect retention/GC authority, replicate critical content, document rollback windows, and delete unreferenced development content only after accounting for referrers and active deployments.

## 11. A mirror serves an old `latest` tag but correct digest pulls. Diagnose the difference.

A tag is a mutable lookup whose cached resolution can be stale. A digest names exact bytes; the mirror either has them or fails, and the client verifies them. The behavior demonstrates why mutable discovery names and immutable release identities serve different purposes.

## 12. State the missing properties that make the course mini-registry unsuitable for production.

It lacks production authentication/authorization, TLS hardening, scalable durable storage, replication, resumable robust uploads, quotas, audit, concurrent GC safety, HA, abuse resistance, comprehensive conformance, and operational recovery. It is protocol evidence, not a deployable registry product.

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
