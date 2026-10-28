# Module 03 — Contract Registry and Multi-Protocol Publication

> **Program stage:** Course 10 of 10 — Operate APIs as an organizational platform.

> **Central question:** What makes an API contract a trustworthy published release across HTTP, events, RPC, and GraphQL?

## Where this module fits

Module 02 produced **Publish the Analysis Platform catalog and ownership graph**. This module extends that result by asking: **What makes an API contract a trustworthy published release across HTTP, events, RPC, and GraphQL?**

The new capstone increment is **Register the four inherited interface releases by digest and publication evidence**. It becomes the prerequisite for **Governance as Code, Evidence, Scorecards, and Exceptions**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish drafts, releases, channels, and promotions.
- Bind releases to exact bytes and owners.
- Preserve protocol-native contracts.
- Attach protocol-appropriate compatibility evidence.
- Reject mutable release identities.

## Capstone increment

Register the four inherited interface releases by digest and publication evidence.

## Publication is a state transition

A contract file in a repository is not automatically a published API release. Publication identifies an owner, protocol, version, exact bytes, lifecycle, compatibility evidence, and timestamp. The registry rejects reuse of a published version for changed bytes. This allows clients, SDKs, docs, and runtime routes to refer to one immutable subject.

Drafts can change. Releases cannot. Promotion from experimental to active should update metadata around the same digest rather than rebuilding the artifact, because a rebuild can create a different subject even when the source appears similar.

## Four protocols, four compatibility models

Analysis API Platform 1.0 registers an OpenAPI bundle, AsyncAPI document and schemas, Protobuf file, and GraphQL schema plus active operations. The platform normalizes release metadata, but compatibility remains protocol-specific.

For HTTP, request acceptance and response production have directional compatibility. For events, retained history and consumer replay matter. For Protobuf, field numbers and wire encodings dominate. For GraphQL, schema shape must be checked against active operations, nullability, and demand policy. A platform that says “all schemas passed JSON Schema” has misunderstood three of the four surfaces.

## Artifact identity

SHA-256 binds exact bytes. It does not prove the bytes are good, authored by the right owner, or built securely; it proves identity once trusted. The registry combines digest identity with owner authorization, compatibility evidence, and publication workflow. Later, SDK provenance links generated artifacts back to these contract digests.

## Immutability and idempotent publication

Publishing the same version and same bytes twice is an idempotent replay. Publishing the same version with different bytes is rejected. This rule prevents a consumer from regenerating an SDK today and receiving a different contract than yesterday under the same version. A correction becomes 1.2.1 or another explicit release, depending on protocol policy.

## Evidence attached to releases

A compatibility report names the baseline, candidate, change direction, tool or local profile, active consumer surface, and decision. The registry records its path. External tools such as Buf can independently detect Protobuf breaks, while OpenAPI, AsyncAPI, and GraphQL need their own validators. The platform may orchestrate these checks but must preserve their scope.

## Distribution channels

A registry can expose stable channels such as `experimental`, `active`, or `deprecated`, but a channel pointer is not an artifact identity. Consumer lockfiles and production deployments should resolve a channel to a version and digest. Mutable “latest” references are convenient for exploration and unsafe for reproducible release evidence.

## Worked conflict

An owner edits a description in Analysis Graph API 1.0 and attempts to republish. Although the change appears documentation-only, the exact release bytes differ. The registry rejects the overwrite. The owner may publish 1.0.1 after compatibility and active-operation checks. This preserves reproducibility and an auditable correction trail.

## Implementation review

The Python and TypeScript registries expose `publish`. They calculate a digest, check compatibility evidence, and compare an existing `(apiRef, version)` record. The small API demonstrates the immutable-release invariant without depending on a specific commercial registry.

## Standards anchors

OpenAPI carries an HTTP contract through the lifecycle; AsyncAPI 3.1 describes message-driven interfaces; Buf documents protocol-aware Protobuf breaking checks. The platform uses their native artifacts rather than a lossy replacement. Consult [OpenAPI](https://www.openapis.org/what-is-openapi), [AsyncAPI 3.1](https://www.asyncapi.com/docs/reference/specification/latest), and [Buf breaking changes](https://buf.build/docs/breaking/).

## The release record

A complete registry record should contain at least:

```text
api reference
protocol
API version
native artifact media type
artifact digest
source repository and revision
owner
lifecycle channel
publication time
compatibility baseline and result
validation profile and tool versions
consumer-impact evidence
supersedes / replaced-by relationships
```

The source revision and artifact digest answer different questions. The revision
identifies intent in source control. The digest identifies the distributed
artifact. A build or bundle process can alter ordering, references, or generated
content, so both belong in provenance.

## Protocol-aware adapters

The registry may expose one publication API while delegating validation:

- **OpenAPI adapter:** parse, resolve references, lint, compare directional
  request and response compatibility, validate examples, and record tool
  capability.
- **AsyncAPI adapter:** validate channels, operations, messages, bindings, and
  event schema compatibility, with retained-history and consumer replay rules.
- **Protobuf adapter:** compile descriptors, apply wire/source/JSON breaking
  categories, reserve removed fields, and preserve package identity.
- **GraphQL adapter:** validate schema, active persisted operations, field
  ownership, nullability, demand budgets, and consumer usage.

A normalized result can say pass, review, or fail, but the detailed evidence
stays native. A consumer deciding whether to upgrade Protobuf needs field-number
information, not only a generic “compatible” label.

## Release channels and environments

Separate artifact identity from distribution intent:

- `candidate` may be under review;
- `experimental` is available to bounded consumers;
- `active` is the recommended supported release;
- `deprecated` remains available during migration;
- `retired` is historical and not routable.

A channel points to a version and digest. Promotion changes the pointer and
lifecycle evidence, not the bytes. Environment deployment is another axis:
staging can run the active artifact or a candidate. Do not encode environment
inside the API version.

## Registry authorization

Publication is a privileged action. Verify that the workflow acts for the API
owner, the source revision is approved, and the candidate evidence belongs to the
same digest. Protect against a confused deputy: a platform build token allowed to
write one API must not publish another owner’s contract. Audit every release and
channel movement.

## Replication and availability

A production registry may replicate artifacts and metadata. Immutability makes
replication simpler because content-addressed bytes can be verified at each
location. Define behavior when metadata is available but artifact storage is not,
or vice versa. A portal should not advertise a downloadable SDK whose contract
subject cannot be resolved.

## Correction and revocation

A bad release is not overwritten. Publish a corrected version, mark the bad
version withdrawn or quarantined, explain impact, and retain evidence. Consumers
with lockfiles still need a clear failure and migration path. A security
quarantine can prevent new downloads while preserving historical identity for
incident analysis.

## Consumer resolution

Consumers should resolve a declared version constraint to an exact version and
digest, then record the result. Production deployments should not repeatedly
resolve an unconstrained `latest`. SDK manifests, deployment records, and
consumer catalog entries should point to the resolved subject. This makes
incident and deprecation impact concrete.

## Registry trust review

Ask:

- Can an owner overwrite a release?
- Can a build publish evidence for different bytes?
- Are publication identities and channel changes audited?
- Are native artifacts retrievable after retirement?
- Can a consumer verify a downloaded artifact without trusting the portal page?
- Does the platform expose the exact compatibility profile used?

If any answer is unclear, the registry is a file store, not yet a trustworthy
publication system.

## Publication transaction

Publication should behave like a transaction across metadata:

1. validate owner authority;
2. calculate candidate digest;
3. verify native contract and examples;
4. compare with baseline using protocol policy;
5. evaluate active consumers and review triggers;
6. store immutable bytes;
7. store release metadata and evidence references;
8. move a channel only after all prior steps commit;
9. emit an auditable publication event.

If storage succeeds but metadata fails, the unreferenced content-addressed blob
can be garbage-collected later. If metadata points to missing bytes, the release
must not become active. A production implementation needs durable transaction or
reconciliation design; the course core isolates the semantic invariant.

## Cross-registry identity

Contracts may be mirrored to documentation storage, schema registries, package
registries, and gateways. Use the digest as the common subject and record each
location. Do not assume two systems’ version strings identify the same bytes.
During incident analysis, compare resolved digests rather than filenames.

## Review-required examples

Not all changes are automatically safe or breaking. Adding a response enum value
may be legal in a schema yet break exhaustive consumers. Adding an event field may
be safe for tolerant readers but increase privacy classification. Changing a
GraphQL description can alter generated docs without runtime behavior. The
registry should preserve `review` and the reason, then attach the accountable
decision.

## Registry disaster recovery

Back up immutable artifacts and mutable metadata separately. Rebuild indexes from
content and signed publication logs where possible. Test that a restored registry
preserves version-to-digest mapping and channel history. Losing mutable channel
state is inconvenient; losing proof that version 1.0 referred to specific bytes
undermines every downstream artifact.

## Consumer lock evidence

Require production consumers to record resolved contract or SDK subjects where
feasible. Examples include package lockfiles, deployment metadata, broker schema
IDs, or graph persisted-operation registry versions. The platform can then answer
“which consumers are affected by this digest?” rather than approximate from page
views.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Release identity and storage

A registry release is the tuple `(apiRef, version, digest, protocol, owner,
source, publication time, compatibility evidence)`. The human version is useful
for lifecycle and compatibility discussion; the digest identifies exact bytes.
Publishing the same version with the same digest is idempotent. Publishing the
same version with different bytes is rejected. “Fixing” a released document in
place destroys reproducibility because consumers can no longer know which bytes
the version meant.

Store immutable artifacts separately from mutable projections. A search index,
latest-version pointer, lifecycle label, or portal summary can be rebuilt. The
released contract bytes and digest cannot. If registry metadata is lost while
the content-addressed store survives, rebuild the projection from signed or
otherwise trusted publication records. If bytes are lost but a portal still
shows metadata, the release is not recoverable and must not be represented as
verified.

## Protocol-native publication

The platform uses one publication workflow but protocol-specific evidence:

- OpenAPI checks operation, parameter, request, response, and schema evolution.
- AsyncAPI checks channels, operations, messages, envelopes, and replay safety.
- Protobuf checks field numbers, presence, enum evolution, services, and wire
  compatibility.
- GraphQL checks schema shape, active operations, field ownership, demand policy,
  and client behavior.

The registry should not flatten these contracts into a lowest-common-denominator
schema. It records shared release metadata and links native evidence. A generic
“schema valid” badge is insufficient: a valid GraphQL schema can invalidate all
active persisted operations, and a valid `.proto` can reuse a field number that
changes wire meaning.

## Publication transaction

A robust publication flow stages bytes, computes the digest, verifies the owner,
runs protocol-specific checks, evaluates policy, records evidence, stores the
immutable artifact, and then creates the registry record. Define recovery for
each boundary. If the artifact is stored but the record write fails, a retry
should detect the same digest and complete. If the record exists but bytes are
missing, publication is corrupt and must fail closed. If documentation or SDK
publication fails after the contract release succeeds, record a partial product
release rather than rewriting the contract version.

Analysis API Platform dogfoods this rule. `platform-catalog@1.0.0` is an OpenAPI
release in the same registry as the business-facing and internal interfaces. It
has an owner, digest, compatibility statement, documentation, security and
reliability evidence, sandbox route, and support owner. A platform that exempts
its own API from its rules teaches users that governance is ceremonial.

## Disaster recovery exercise

Imagine the mutable registry database is lost. A recovery plan should enumerate
content-addressed artifacts, validate their hashes, read append-only publication
evidence, reconstruct API/version keys, and compare the result with owner source
repositories. Any ambiguous release remains unavailable rather than guessed.
The portal can operate in read-only mode from a verified snapshot, clearly
showing snapshot time. New publication remains closed until uniqueness and
immutability can be enforced again.

## Implementation drill: immutable publication

The decisive behavior is not file upload; it is idempotent replay and rejection
of changed bytes under an existing version.

```python
from hashlib import sha256

class Registry:
    def __init__(self) -> None:
        self.releases: dict[tuple[str, str], str] = {}

    def publish(self, api_ref: str, version: str, data: bytes) -> str:
        digest = sha256(data).hexdigest()
        key = (api_ref, version)
        previous = self.releases.get(key)
        if previous is not None and previous != digest:
            raise ValueError("immutable-release")
        if previous == digest:
            return "idempotent"
        self.releases[key] = digest
        return "published"
```

```typescript
class Registry {
  private readonly releases = new Map<string, string>();

  publish(apiRef: string, version: string, digest: string): string {
    const key = `${apiRef}@${version}`;
    const previous = this.releases.get(key);
    if (previous !== undefined && previous !== digest) {
      throw new Error("immutable-release");
    }
    if (previous === digest) return "idempotent";
    this.releases.set(key, digest);
    return "published";
  }
}
```

The TypeScript excerpt accepts a precomputed digest to keep the snippet
runtime-neutral; the complete track computes SHA-256. In either language, the
compatibility report and owner are also required before the real record is
created.

## Module synthesis

You are ready to leave this module when you can **distinguish drafts, releases, channels, and promotions, bind releases to exact bytes and owners, and preserve protocol-native contracts** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Then attempt: identical replay, changed bytes under the same version, a new version without compatibility evidence, and an experimental promotion that rebuilds rather than reuses bytes** and requiring the following oracle: **Identical replay is idempotent. Changed bytes under an existing version fail. A new version without evidence fails. Promotion references the existing digest.**

The cumulative platform now includes **Register the four inherited interface releases by digest and publication evidence**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Governance as Code, Evidence, Scorecards, and Exceptions](../module-04-governance-as-code/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
