# OCI Distribution API map

A registry stores repository-scoped manifests and content-addressed blobs. The protocol separates mutable references from immutable content.

## Pull path

```text
GET /v2/
GET /v2/<name>/manifests/<reference>
GET /v2/<name>/blobs/<digest>
```

A client may use a tag for discovery, but it should resolve and retain the returned digest. Every blob and manifest must be verified by size/digest before use. Content negotiation matters because an index, image manifest, and older manifest format have different semantics.

## Push path

Typical blob upload:

```text
POST  /v2/<name>/blobs/uploads/
PATCH /v2/<name>/blobs/uploads/<uuid>
PUT   /v2/<name>/blobs/uploads/<uuid>?digest=sha256:...
```

Then publish manifests only after referenced blobs exist. Cross-repository mounts can avoid duplicate transfer but do not grant read/use authority automatically.

## Tags and digests

```text
repository:tag       mutable lookup
repository@digest    immutable content identity within repository context
```

Review and deployment use the digest. Tag mutation is audited and protected, but tag immutability is not the primary release control.

## Referrers

Evidence discovery can use a referrers endpoint or equivalent fallback. The client must still verify:

- returned artifact manifest digest;
- artifact type/media type;
- `subject` equality with the candidate;
- payload digest and signature;
- policy relevance.

A registry listing is not authorization.

## Retention and garbage collection

Reachability is necessary but not sufficient. A release system must retain:

- active deployment subjects;
- rollback subjects;
- evidence and signatures;
- incident/legal holds;
- referenced layers/configs;
- required platform children.

Deleting a tag does not prove blobs were erased. Garbage collection, replication, mirrors, backups, and caches each have their own timing and recovery behavior.

## Failure matrix

| Failure | Correct client behavior |
|---|---|
| Tag resolves to unexpected digest | stop; compare with approved release identity |
| Blob digest mismatch | reject bytes; do not retry as trusted content |
| Manifest references missing blob | reject incomplete graph |
| Referrer subject mismatch | ignore/reject evidence for this candidate |
| Partial upload interrupted | resume or abandon according to upload status; do not publish manifest early |
| Registry unavailable | use documented mirror/retained subject policy; do not rebuild silently |
