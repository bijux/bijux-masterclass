# Worked Answers — Module 03: Contract Registry and Multi-Protocol Publication

Use these solutions to audit your reasoning for **Contract Registry and Multi-Protocol Publication**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why store releases by digest as well as version?

A version is a human lifecycle label; a digest binds exact bytes. The same version with different bytes is an integrity failure even if the file name is unchanged.

The chapter’s decisive distinction is this: A registry release is the tuple (apiRef, version, digest, protocol, owner, source, publication time, compatibility evidence). The human version is useful for lifecycle and compatibility discussion; the digest identifies exact bytes. Publishing the same version with the same digest is idempotent. Publishing the same version with different bytes is rejected. “Fixing” a released document in place destroys reproducibility because consumers can no longer know which bytes the version meant.

## 2. Why can one registry not use one compatibility rule for every protocol?

OpenAPI request/response compatibility, event consumer compatibility, Protobuf wire/source compatibility, and GraphQL active-operation compatibility differ. The registry can normalize evidence and decisions, not erase protocol semantics.

In the cumulative capstone, the rule becomes concrete: For HTTP, request acceptance and response production have directional compatibility. For events, retained history and consumer replay matter. For Protobuf, field numbers and wire encodings dominate. For GraphQL, schema shape must be checked against active operations, nullability, and demand policy. A platform that says “all schemas passed JSON Schema” has misunderstood three of the four surfaces.

## 3. What does immutable publication mean?

After a version is published, replaying identical bytes is idempotent, but changed bytes require a new version. Corrections are new releases with explicit history.

A useful way to reason about the boundary is: A contract file in a repository is not automatically a published API release. Publication identifies an owner, protocol, version, exact bytes, lifecycle, compatibility evidence, and timestamp. The registry rejects reuse of a published version for changed bytes. This allows clients, SDKs, docs, and runtime routes to refer to one immutable subject.

## 4. Who may publish an API release?

The owning team or an authorized release workflow acting for it. The platform verifies authority and evidence but does not invent the release.

The implementation consequence is: Publication is a privileged action. Verify that the workflow acts for the API owner, the source revision is approved, and the candidate evidence belongs to the same digest. Protect against a confused deputy: a platform build token allowed to write one API must not publish another owner’s contract. Audit every release and channel movement.

## 5. What is the difference between a registry and a catalog?

The registry stores and verifies immutable contract releases. The catalog describes entities, ownership, relationships, and current lifecycle. Catalog entries reference registry releases.

The important nuance is: Consumers should resolve a declared version constraint to an exact version and digest, then record the result. Production deployments should not repeatedly resolve an unconstrained latest. SDK manifests, deployment records, and consumer catalog entries should point to the resolved subject. This makes incident and deprecation impact concrete.

## 6. Why preserve the original artifact format?

Protocol-native tools and semantics depend on the exact OpenAPI, AsyncAPI, Protobuf, or GraphQL artifact. Converting everything into a custom common model can lose meaning and evidence.

Under concurrency or failure, the distinction becomes: The registry should not flatten these contracts into a lowest-common-denominator schema. It records shared release metadata and links native evidence. A generic “schema valid” badge is insufficient: a valid GraphQL schema can invalidate all active persisted operations, and a valid .proto can reuse a field number that changes wire meaning.

## 7. What should happen when external validation tools are unavailable?

Run bounded local checks, label their scope, and mark independent validation as unexecuted. Do not declare standards conformance from a partial parser.

The design remains honest only if: A compatibility report names the baseline, candidate, change direction, tool or local profile, active consumer surface, and decision. The registry records its path. External tools such as Buf can independently detect Protobuf breaks, while OpenAPI, AsyncAPI, and GraphQL need their own validators. The platform may orchestrate these checks but must preserve their scope.

## 8. Why record compatibility evidence with the release?

A future reviewer needs to know what baseline, rules, active consumers, and tool versions justified the decision. A green result without context cannot be audited.

The consumer-facing consequence is: Require production consumers to record resolved contract or SDK subjects where feasible. Examples include package lockfiles, deployment metadata, broker schema IDs, or graph persisted-operation registry versions. The platform can then answer “which consumers are affected by this digest?” rather than approximate from page views.

## 9. Can a draft contract be mutable?

Yes before publication within a proposal workflow, provided it is not represented as an immutable released version. Draft identity and released identity must be distinct.

The operational consequence is: Store immutable artifacts separately from mutable projections. A search index, latest-version pointer, lifecycle label, or portal summary can be rebuilt. The released contract bytes and digest cannot. If registry metadata is lost while the content-addressed store survives, rebuild the projection from signed or otherwise trusted publication records. If bytes are lost but a portal still shows metadata, the release is not recoverable and must not be represented as verified.

## 10. What is a registry promotion?

Promotion changes lifecycle or channel references to an existing immutable artifact. It should not rebuild or rewrite the bytes merely to move from experimental to active.

The strongest engineering interpretation is: Drafts can change. Releases cannot. Promotion from experimental to active should update metadata around the same digest rather than rebuilding the artifact, because a rebuild can create a different subject even when the source appears similar.

**Evidence.** Reconcile catalog relations with source-owned metadata and verify immutable digest-addressed publication, authority, idempotent replay, and changed-byte rejection.

## 11. How should a registry handle a review-required change?

Store the candidate and evidence without advancing the active pointer until an accountable reviewer resolves the risk. Review is not equivalent to pass.

The defect-oriented view is: Not all changes are automatically safe or breaking. Adding a response enum value may be legal in a schema yet break exhaustive consumers. Adding an event field may be safe for tolerant readers but increase privacy classification. Changing a GraphQL description can alter generated docs without runtime behavior. The registry should preserve review and the reason, then attach the accountable decision.

## 12. What proves that Course 10 did not fabricate predecessor contracts?

The course copies actual release artifacts from Courses 2, 6, 7, and 9, records their SHA-256 digests, and verifies those bytes in the registry proof.

Across the Python and TypeScript tracks, the invariant is: SHA-256 binds exact bytes. It does not prove the bytes are good, authored by the right owner, or built securely; it proves identity once trusted. The registry combines digest identity with owner authorization, compatibility evidence, and publication workflow. Later, SDK provenance links generated artifacts back to these contract digests.
