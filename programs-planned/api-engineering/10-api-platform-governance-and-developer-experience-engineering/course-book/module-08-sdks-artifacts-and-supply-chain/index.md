# SDKs, CLIs, Artifacts, SBOMs, and Provenance

**Module 08 of 10**

> **Governing question:** How can developer artifacts remain convenient, idiomatic, reproducible, and traceable to the contracts that produced them?

## Place in the program

Module 07 helped consumers succeed manually. Module 08 turns released contracts into distributable developer artifacts while preserving identity and supply-chain evidence.

## Learning outcomes

- design SDKs as supported products rather than raw generated code
- link packages to exact contract releases
- distinguish SBOM, provenance, checksum, and signature evidence
- govern package versioning and retention
- reject untraceable or misleading publication claims

## Capstone result

Publish Python and TypeScript client artifacts with contract identity, SBOM, and bounded provenance evidence.

## SDK quality is a product concern

Generated clients reduce protocol work, but an SDK is more than generated methods. It defines authentication injection, retries, pagination helpers, errors, naming, documentation, and compatibility. A platform can standardize publication and evidence while language owners preserve idiomatic design.

The capstone includes minimal Python and TypeScript client artifacts to demonstrate explicit credentials and secure base URLs. It does not pretend that these small examples replace full generated clients from Course 1.

## Traceability chain

A trustworthy artifact chain is: released contract digest → generation configuration and source → tests → package bytes → package digest → SBOM → provenance → registry publication. Each link answers a different question. The contract says what the API promises. The SBOM says what the package contains. Provenance says how it was built. Tests say which behavior was exercised.

## SBOM and provenance are complementary

CycloneDX 1.7 can describe application and library components. SLSA 1.2 provides current vocabulary and provenance formats for source and build integrity. The course creates a CycloneDX document and an in-toto statement with the SLSA provenance predicate. It labels the result as course evidence because the local builder is not a hardened hosted platform and the statement is not a production signature.

## Verification, not file presence

A provenance file has no value if the consumer never checks subject digest, builder expectations, inputs, and signature or trusted channel. The course verifies that artifact digests match publication metadata and that the provenance subject refers to the publication record. An environment-backed route would also verify signed attestations against trusted builders.

## SDK and API version independence

API 1.2 may have SDK 1.2.0, 1.2.1, or 2.0.0 depending on SDK semantics. A generator bug fix can change the SDK without changing the contract. Conversely, one SDK version may support several compatible API releases. Publication metadata must state the supported API range and exact generation baseline.

## Registry and channels

Publish immutable package versions and move release channels such as `stable` or `preview` by reference. Never replace package bytes under the same version. Retain old artifacts according to lifecycle and security policy so builds and rollbacks remain reproducible. Vulnerable artifacts can be quarantined without rewriting history.

## Worked verification

The platform reads `publication.json`, hashes each SDK file, validates the CycloneDX profile, and checks the SLSA provenance predicate. A candidate missing provenance is rejected even if tests pass. The result says `verified` only for the local evidence chain; it does not claim external builder authenticity.

## Implementation review

The supply-chain core verifies artifact paths and digests, SBOM profile, and provenance predicate. The SDK clients require credentials explicitly and reject non-HTTPS remote base URLs. These mechanisms continue security lessons rather than sacrificing them for developer convenience.

## Standards anchors

CycloneDX lists version 1.7 as its current specification. SLSA 1.2 is the current approved SLSA specification and separates source and build tracks. Read [CycloneDX specification overview](https://cyclonedx.org/specification/overview/) and [SLSA 1.2](https://slsa.dev/spec/v1.2/).


## Generation pipeline

A robust SDK publication pipeline is:

```text
resolve immutable contract digest
→ verify compatibility and release approval
→ select pinned generator and configuration
→ generate in isolated workspace
→ apply maintained ergonomic layer
→ compile and test
→ build package
→ create SBOM
→ create provenance
→ sign or attest in trusted environment
→ publish immutable package
→ verify from consumer perspective
```

The ergonomic layer may add pagination iterators, domain-specific error types, or
retry helpers. Keep it generated or maintained deliberately; hand edits inside
generated files are lost and hard to review.

## Contract and generator compatibility

Pin the generator and templates. A new generator can change names, nullability,
serialization, or runtime dependencies without an API change. Treat generator
upgrades as SDK changes with consumer tests. Record both contract digest and
generator identity in provenance.

Run cross-version matrices where the SDK supports several server releases. A
client generated from HTTP API 1.2 might call 1.2 and a compatible 1.3, but the
support claim needs tests and policy. Do not infer it solely from semantic
versioning.

## Artifact metadata

Package publication should include:

- package ecosystem identity and version;
- supported API references and versions;
- artifact digest and size;
- source and build revisions;
- generator and configuration;
- test summary;
- SBOM location and digest;
- provenance and signature location;
- owner, support, license, and lifecycle;
- vulnerability and withdrawal status.

This metadata belongs in the platform catalog and artifact registry, not only in
release notes.

## SBOM use

An SBOM helps answer which dependencies and components are present. Use it for
vulnerability impact, license review, and dependency inventory. Verify that it
matches the final package, not only source manifests. An SBOM generated before
packaging can omit bundled or generated components.

CycloneDX supports more than software components, but the course uses a minimal
software BOM. Do not claim complete vulnerability or license assurance merely
because the JSON validates.

## Provenance use

Provenance links subjects to a build definition, builder, parameters, and
resolved dependencies. Verification compares these claims with policy: expected
repository, trusted builder, permitted parameters, and subject digest. SLSA
levels describe increasing source and build guarantees; they are outcomes of a
system and verification process, not labels added to a file.

## Signing and trust roots

A signature authenticates only relative to a trusted key or identity and
verification policy. Define key lifecycle, compromise response, transparency or
logging, and package-registry integration. A platform can publish unsigned local
course evidence while clearly separating the environment-backed signing route.

## Vulnerability response

When a dependency vulnerability affects an SDK:

1. determine affected versions from SBOMs;
2. assess exploitability in the SDK context;
3. build and test a fixed package;
4. publish advisory and replacement;
5. quarantine or deprecate vulnerable versions as policy requires;
6. notify active consumers;
7. preserve evidence and historical identity.

Do not overwrite the vulnerable package. Consumers need reproducible evidence of
what they used.

## Consumer verification

Document how consumers verify package source, digest, provenance, supported API,
and signature. Publication-side evidence without a consumer verification path is
incomplete. Automated package clients can enforce provenance expectations at
install or deployment time in a mature environment.


## SDK ergonomics review

Review the generated SDK as a consumer:

- Are credentials explicit and injectable?
- Do operations have stable, idiomatic names?
- Are nullable and optional values represented correctly?
- Are pagination and streaming helpers bounded?
- Are errors typed without hiding protocol evidence?
- Are retries opt-in and safe for operation semantics?
- Can timeouts and cancellation propagate?
- Is serialization compatible with the released contract?
- Does documentation state thread, async, and lifecycle behavior?

A package can pass compilation while failing these questions.

## Package ecosystem differences

Python and npm differ in naming, dependency resolution, lockfiles, build
artifacts, typing, and distribution. Publish ecosystem-native metadata. Avoid
forcing one organization-wide package layout when the underlying tools disagree.
Standardize the evidence and support contract instead.

For JavaScript numbers, preserve 64-bit identifiers as strings where required.
For Python async clients, do not hide blocking I/O. Lessons from Courses 5 and 7
remain part of SDK quality.

## Reproducible consumer example

A consumer record should be able to say:

```text
package: analysis-api-client 1.2.0
package digest: ...
contract: api:default/analysis-http 1.2.0
contract digest: ...
provenance: ...
sandbox example: submit-analysis-http-python
```

This evidence makes incident and upgrade questions answerable. “Installed latest
last month” does not.

## Artifact policy exceptions

An internal experimental client might not yet have signed provenance. It can
remain experimental under a scoped exception and non-production channel. It
should not be promoted to stable by changing a badge. Publication channels and
consumer environments enforce the distinction.

## Supply-chain incident drill

If the builder identity is compromised, identify all artifacts produced by it,
freeze channel promotion, verify source and subject digests, rebuild on a trusted
path, compare outputs, notify consumers, and update provenance expectations. An
SBOM alone cannot identify builder compromise; provenance and publication logs
are required.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## SDK publication pipeline

An SDK release should name the source contract release and generator or
implementation version, produce deterministic artifacts where feasible, run
language-level tests, create checksums, emit an SBOM, record provenance, publish
to an appropriate registry, and verify installation from that registry. The
package version and API version need not be identical, but their relationship
must be explicit.

Generated code is not automatically correct. Generators may approximate schema
semantics, omit unsupported features, or expose awkward language types. Maintain
conformance tests against the service and record known transformations. A
handwritten convenience layer must not hide headers, retries, idempotency, or
error details that consumers need for correct behavior.

## Compatibility of SDKs

An additive API change can still be an SDK breaking change if regenerated method
signatures, names, or enum types change. Evaluate source compatibility, binary or
package compatibility where relevant, and runtime behavior. Keep consumer-facing
release notes. When an API version retires, identify SDK versions that target it
and prevent new onboarding to those versions.

Do not publish every protocol as a conventional SDK. Event consumers may benefit
more from message types and validation helpers. Protobuf already produces native
stubs. GraphQL consumers may use persisted-operation types. The platform chooses
artifacts based on consumer work, not a uniform “SDK generated” badge.

## SBOM and provenance interpretation

A CycloneDX document records components and relationships in a standard format;
it does not prove those components are safe. Provenance records how an artifact
was produced; a locally authored example is not a trusted external attestation.
SLSA vocabulary helps state builder, inputs, and subjects, but assurance depends
on the build environment and verification policy.

The capstone labels its files as profiles and verifies internal consistency. It
checks that artifact digests match publication metadata, the SBOM uses the
expected profile, and provenance names the released subjects. It explicitly
does not claim a hardened build service, protected signing key, transparency
log, or independent registry verification.

## Revocation and incident response

Publication needs a response path for compromised artifacts. Preserve the
original evidence, mark affected versions, communicate with known consumers,
publish fixed artifacts, and update onboarding defaults. Deleting history can
make incident analysis harder. Package-manager behavior differs, so document
whether versions can be yanked, deprecated, or blocked and how existing installs
are detected.

## Implementation drill: publication completeness

Artifact existence is insufficient. Publication requires digest, SBOM, and
provenance evidence together.

```python
def publication_decision(
    *, has_digest: bool, has_sbom: bool, has_provenance: bool
) -> str:
    complete = has_digest and has_sbom and has_provenance
    return "publish" if complete else "incomplete-publication"
```

```typescript
function publicationDecision(
  hasDigest: boolean,
  hasSbom: boolean,
  hasProvenance: boolean,
): "publish" | "incomplete-publication" {
  return hasDigest && hasSbom && hasProvenance
    ? "publish"
    : "incomplete-publication";
}
```

The real verifier also recomputes every artifact digest and checks the declared
CycloneDX and SLSA profile identifiers. It still states that locally authored
metadata is not equivalent to a trusted external attestation.
