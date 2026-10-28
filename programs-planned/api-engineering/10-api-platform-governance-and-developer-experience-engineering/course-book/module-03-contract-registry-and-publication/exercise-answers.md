# Worked answers — Contract Registry and Multi-Protocol Publication

## 1. Why store releases by digest as well as version?

A version is a human lifecycle label; a digest binds exact bytes. The same version with different bytes is an integrity failure even if the file name is unchanged.

## 2. Why can one registry not use one compatibility rule for every protocol?

OpenAPI request/response compatibility, event consumer compatibility, Protobuf wire/source compatibility, and GraphQL active-operation compatibility differ. The registry can normalize evidence and decisions, not erase protocol semantics.

## 3. What does immutable publication mean?

After a version is published, replaying identical bytes is idempotent, but changed bytes require a new version. Corrections are new releases with explicit history.

## 4. Who may publish an API release?

The owning team or an authorized release workflow acting for it. The platform verifies authority and evidence but does not invent the release.

## 5. What is the difference between a registry and a catalog?

The registry stores and verifies immutable contract releases. The catalog describes entities, ownership, relationships, and current lifecycle. Catalog entries reference registry releases.

## 6. Why preserve the original artifact format?

Protocol-native tools and semantics depend on the exact OpenAPI, AsyncAPI, Protobuf, or GraphQL artifact. Converting everything into a custom common model can lose meaning and evidence.

## 7. What should happen when external validation tools are unavailable?

Run bounded local checks, label their scope, and mark independent validation as unexecuted. Do not declare standards conformance from a partial parser.

## 8. Why record compatibility evidence with the release?

A future reviewer needs to know what baseline, rules, active consumers, and tool versions justified the decision. A green result without context cannot be audited.

## 9. Can a draft contract be mutable?

Yes before publication within a proposal workflow, provided it is not represented as an immutable released version. Draft identity and released identity must be distinct.

## 10. What is a registry promotion?

Promotion changes lifecycle or channel references to an existing immutable artifact. It should not rebuild or rewrite the bytes merely to move from experimental to active.

## 11. How should a registry handle a review-required change?

Store the candidate and evidence without advancing the active pointer until an accountable reviewer resolves the risk. Review is not equivalent to pass.

## 12. What proves that Course 10 did not fabricate predecessor contracts?

The course copies actual release artifacts from Courses 2, 6, 7, and 9, records their SHA-256 digests, and verifies those bytes in the registry proof.
