# Worked answers — SDKs, CLIs, Artifacts, SBOMs, and Provenance

## 1. Why is generated code not automatically a good SDK?

An SDK also needs stable naming, idiomatic errors, authentication boundaries, documentation, tests, versioning, support, and release traceability. A generator can emit types while producing a poor consumer experience.

## 2. What must link an SDK to an API release?

The API reference, contract version and digest, generator and configuration identity, source revision, tests, artifact digest, SBOM, and provenance evidence.

## 3. What does an SBOM describe?

The components present in an artifact and related metadata. It supports dependency, vulnerability, and license analysis but does not by itself prove how the artifact was built.

## 4. What does provenance describe?

Where, when, and how an artifact was produced, including builder, inputs, parameters, and subjects. Provenance requires verification; a JSON file alone is not trust.

## 5. Why does the course not claim a SLSA level?

The local course creates a provenance-shaped example but does not run on a verified hosted or hardened build platform. Claiming a level would exceed the evidence.

## 6. Why publish Python and TypeScript SDKs separately?

Each ecosystem has its own package names, version constraints, typing, errors, release channels, and consumers. Shared contract identity does not justify one artificial artifact model.

## 7. How should SDK versioning relate to API versioning?

The SDK should declare which API releases it supports, but its own version may change for generator fixes or ergonomics without an API change. The relationship must be explicit, not assumed identical.

## 8. What is a trusted publication gate?

A gate that verifies tests, contract digest, artifact digest, SBOM, provenance, package metadata, changelog, and owner before advancing a release channel.

## 9. Why are checksums not signatures?

A checksum detects changed bytes when the expected checksum is trusted. It does not authenticate who published the checksum. Signatures or trusted attestations bind identity.

## 10. Should the platform regenerate every SDK on demand for consumers?

Usually publish maintained, tested releases. Per-consumer regeneration can produce uncontrolled variants and move build risk to consumers. On-demand generation can be useful in a sandbox with clear non-production status.

## 11. What is a CLI’s role beside an SDK?

A CLI provides operational and human workflows, often useful for onboarding and automation. It should use the same released contract and authentication boundaries rather than becoming a hidden alternative API.

## 12. Why retain old SDK artifacts?

Consumers may need reproducible builds, rollback, and incident analysis. Retention follows lifecycle and vulnerability policy rather than deleting old packages immediately.
