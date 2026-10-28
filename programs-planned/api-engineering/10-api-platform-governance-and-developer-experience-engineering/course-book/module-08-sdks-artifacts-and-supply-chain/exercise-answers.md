# Worked Answers — Module 08: SDKs, CLIs, Artifacts, SBOMs, and Provenance

Use these solutions to audit your reasoning for **SDKs, CLIs, Artifacts, SBOMs, and Provenance**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is generated code not automatically a good SDK?

An SDK also needs stable naming, idiomatic errors, authentication boundaries, documentation, tests, versioning, support, and release traceability. A generator can emit types while producing a poor consumer experience.

The chapter’s decisive distinction is this: Generated clients reduce protocol work, but an SDK is more than generated methods. It defines authentication injection, retries, pagination helpers, errors, naming, documentation, and compatibility. A platform can standardize publication and evidence while language owners preserve idiomatic design.

## 2. What must link an SDK to an API release?

The API reference, contract version and digest, generator and configuration identity, source revision, tests, artifact digest, SBOM, and provenance evidence.

In the cumulative capstone, the rule becomes concrete: API 1.2 may have SDK 1.2.0, 1.2.1, or 2.0.0 depending on SDK semantics. A generator bug fix can change the SDK without changing the contract. Conversely, one SDK version may support several compatible API releases. Publication metadata must state the supported API range and exact generation baseline.

## 3. What does an SBOM describe?

The components present in an artifact and related metadata. It supports dependency, vulnerability, and license analysis but does not by itself prove how the artifact was built.

A useful way to reason about the boundary is: An SBOM helps answer which dependencies and components are present. Use it for vulnerability impact, license review, and dependency inventory. Verify that it matches the final package, not only source manifests. An SBOM generated before packaging can omit bundled or generated components.

## 4. What does provenance describe?

Where, when, and how an artifact was produced, including builder, inputs, parameters, and subjects. Provenance requires verification; a JSON file alone is not trust.

The implementation consequence is: Provenance links subjects to a build definition, builder, parameters, and resolved dependencies. Verification compares these claims with policy: expected repository, trusted builder, permitted parameters, and subject digest. SLSA levels describe increasing source and build guarantees; they are outcomes of a system and verification process, not labels added to a file.

## 5. Why does the course not claim a SLSA level?

The local course creates a provenance-shaped example but does not run on a verified hosted or hardened build platform. Claiming a level would exceed the evidence.

The important nuance is: CycloneDX 1.7 can describe application and library components. SLSA 1.2 provides current vocabulary and provenance formats for source and build integrity. The course creates a CycloneDX document and an in-toto statement with the SLSA provenance predicate. It labels the result as course evidence because the local builder is not a hardened hosted platform and the statement is not a production signature.

## 6. Why publish Python and TypeScript SDKs separately?

Each ecosystem has its own package names, version constraints, typing, errors, release channels, and consumers. Shared contract identity does not justify one artificial artifact model.

Under concurrency or failure, the distinction becomes: Python and npm differ in naming, dependency resolution, lockfiles, build artifacts, typing, and distribution. Publish ecosystem-native metadata. Avoid forcing one organization-wide package layout when the underlying tools disagree. Standardize the evidence and support contract instead.

**Evidence.** Render twice from validated inputs, compare exact outputs, compile/test generated artifacts, verify digests and SBOM/provenance profiles, and reject placeholders or secrets.

## 7. How should SDK versioning relate to API versioning?

The SDK should declare which API releases it supports, but its own version may change for generator fixes or ergonomics without an API change. The relationship must be explicit, not assumed identical.

The design remains honest only if: Pin the generator and templates. A new generator can change names, nullability, serialization, or runtime dependencies without an API change. Treat generator upgrades as SDK changes with consumer tests. Record both contract digest and generator identity in provenance.

## 8. What is a trusted publication gate?

A gate that verifies tests, contract digest, artifact digest, SBOM, provenance, package metadata, changelog, and owner before advancing a release channel.

The consumer-facing consequence is: A trustworthy artifact chain is: released contract digest → generation configuration and source → tests → package bytes → package digest → SBOM → provenance → registry publication. Each link answers a different question. The contract says what the API promises. The SBOM says what the package contains. Provenance says how it was built. Tests say which behavior was exercised.

## 9. Why are checksums not signatures?

A checksum detects changed bytes when the expected checksum is trusted. It does not authenticate who published the checksum. Signatures or trusted attestations bind identity.

The operational consequence is: A provenance file has no value if the consumer never checks subject digest, builder expectations, inputs, and signature or trusted channel. The course verifies that artifact digests match publication metadata and that the provenance subject refers to the publication record. An environment-backed route would also verify signed attestations against trusted builders.

## 10. Should the platform regenerate every SDK on demand for consumers?

Usually publish maintained, tested releases. Per-consumer regeneration can produce uncontrolled variants and move build risk to consumers. On-demand generation can be useful in a sandbox with clear non-production status.

The strongest engineering interpretation is: Do not publish every protocol as a conventional SDK. Event consumers may benefit more from message types and validation helpers. Protobuf already produces native stubs. GraphQL consumers may use persisted-operation types. The platform chooses artifacts based on consumer work, not a uniform “SDK generated” badge.

## 11. What is a CLI’s role beside an SDK?

A CLI provides operational and human workflows, often useful for onboarding and automation. It should use the same released contract and authentication boundaries rather than becoming a hidden alternative API.

The defect-oriented view is: An additive API change can still be an SDK breaking change if regenerated method signatures, names, or enum types change. Evaluate source compatibility, binary or package compatibility where relevant, and runtime behavior. Keep consumer-facing release notes. When an API version retires, identify SDK versions that target it and prevent new onboarding to those versions.

## 12. Why retain old SDK artifacts?

Consumers may need reproducible builds, rollback, and incident analysis. Retention follows lifecycle and vulnerability policy rather than deleting old packages immediately.

Across the Python and TypeScript tracks, the invariant is: Publish immutable package versions and move release channels such as stable or preview by reference. Never replace package bytes under the same version. Retain old artifacts according to lifecycle and security policy so builds and rollbacks remain reproducible. Vulnerable artifacts can be quarantined without rewriting history.
