# Module 8 — SBOMs, vulnerabilities, licenses, and VEX

A software bill of materials is an inventory claim. A vulnerability report is a correlation claim. VEX is a status assertion about whether a vulnerability affects a product under stated conditions. None of them is a complete security verdict.

This module teaches how to build, validate, compare, and use these records without allowing scanners to replace engineering judgment.

## Learning outcomes

By the end of the module you can:

- define the subject and scope of an SBOM;
- compare CycloneDX and SPDX roles without treating format choice as completeness;
- use package URLs, hashes, and supplier/version data to improve identity;
- distinguish source, build, image, and runtime inventories;
- interpret vulnerability matches, false positives, reachability, exploitability, and fix status;
- author bounded VEX statements with justification and expiry/review conditions;
- evaluate license obligations and unknown-license risk;
- reject incomplete or stale inventory evidence;
- attach inventory and VEX artifacts to exact OCI subjects.

## Inventory begins with the subject

An SBOM should say exactly what it describes:

```text
atlas-api image index digest
or
atlas-api linux/amd64 manifest digest
or
source repository release
```

These are not interchangeable. A source SBOM may list module dependencies. An image SBOM may list operating-system packages, copied libraries, certificates, and the application binary actually shipped. A runtime inventory may include injected agents or mounts absent from the image.

Atlas publishes a release-level CycloneDX SBOM bound to the image subject and records platform coverage. Where platform contents differ, the evidence identifies those differences rather than pretending one list is universal.

## Component identity is difficult

A component name and version can be ambiguous. Useful identifiers include:

- package URL (`purl`);
- cryptographic hashes;
- supplier/author;
- namespace/ecosystem;
- CPE where appropriate;
- license identifiers;
- dependency relationships;
- pedigree and evidence fields.

CPEs are common in vulnerability databases but can create broad or inaccurate matches. Package URLs often represent package-manager coordinates more precisely. File hashes help prove which bytes were observed.

The Atlas fixture uses purls and SHA-256 hashes for first-party binaries and declared dependencies.

## CycloneDX and SPDX

CycloneDX emphasizes BOM use cases across software, services, vulnerabilities, and related supply-chain data. SPDX provides a broad standard for software package, file, licensing, security, build, and AI data models. Both can represent useful inventories.

The course uses CycloneDX 1.7 as its executable SBOM profile and teaches SPDX 3.0.1 as a comparison model. Choosing a newer schema does not make an inventory complete. Tool support, component detection, relationships, subject binding, and validation matter more than version marketing.

## Completeness is a measured property

“SBOM generated” is not a completion criterion.

Check coverage against independent inventories:

```text
expected first-party executables
expected locked language dependencies
base/runtime packages
shared libraries and dynamic loader
certificates/data files where policy cares
licenses
component relationships
platform variants
```

An empty or suspiciously short SBOM can still validate against the schema. The course policy includes required Atlas component identities and rejects missing first-party binaries.

For a `scratch` image containing one static binary, a small SBOM may be correct. For a general Linux base, the same count is implausible. Completeness is contextual.

## Vulnerability matching is an evidence pipeline

A scanner generally:

1. identifies components;
2. maps them to vulnerability database records;
3. applies version-range logic;
4. reports severity, fix data, and metadata.

Failure can occur at every stage. The component may be misidentified, version parsing may be wrong, database data may be stale, a vulnerable source package may not be present, or the code path may be unreachable.

Do not reduce findings to “CVSS above 7 fails.” Consider:

- whether the component is truly present;
- whether the vulnerable code is included and reachable;
- whether the workload exposes the required attack precondition;
- whether compensating controls exist;
- whether a fix is available;
- exploit maturity and environment;
- business impact;
- evidence freshness.

Severity remains useful but is not the whole decision.

## Reachability and exploitability

Static reachability can show that a vulnerable function is not referenced by the built program. It cannot prove that reflection, dynamic loading, plugins, configuration, or future code paths will never reach it. Runtime reachability can miss unexercised paths.

The Atlas capstone includes a small reachability report as review evidence. Policy treats it as one input, not proof of non-affectability.

## VEX: status with responsibility

A VEX statement can express statuses such as:

- affected;
- not affected;
- fixed;
- under investigation.

A useful not-affected assertion includes:

- exact product subject;
- vulnerability identity;
- status;
- justification category;
- impact statement;
- supporting evidence;
- author/authority;
- time and review/expiry condition.

Bad VEX:

```text
CVE-XXXX: not affected — application does not use it
```

Better:

```text
Subject: atlas-api@sha256:...
Status: not affected
Justification: vulnerable code not present in compiled artifact
Evidence: binary symbol/reachability report + component hash
Review: invalidated by dependency or build-flag change
```

VEX must be regenerated or reevaluated when the subject digest changes. Copying a VEX record across versions without checking assumptions is evidence laundering.

## License evidence

License review asks:

- which licenses apply to shipped components and source modifications;
- whether notices/source offers are required;
- whether the intended distribution model is compatible;
- whether license data is declared or detected;
- what “NOASSERTION” or unknown means for release risk.

A scanner’s license guess is not legal advice. The course teaches evidence and policy mechanics, not jurisdiction-specific legal conclusions.

Atlas release policy blocks unknown licenses for components in the checked fixture unless an approved review record exists. The policy demonstrates explicit ownership; it is not universal license policy.

## SBOM storage and subject binding

The SBOM is stored as an OCI artifact whose manifest names the image subject. The release record stores the SBOM artifact digest. This gives:

```text
release digest
→ discover referrer
→ verify artifact manifest
→ verify subject
→ validate BOM schema/profile
→ evaluate completeness/freshness/policy
```

Embedding an SBOM inside the image can be useful for offline access but changes the image digest and can create circular build workflows. External subject-bound artifacts keep release bytes and evidence independently addressable.

## Worked case: the perfect empty SBOM

A scanner runs against a `scratch` final image and reports only the Atlas binary. The team concludes there are no dependencies.

The binary was dynamically linked and the image also contained copied shared libraries under a nonstandard path that the scanner did not recognize. The BOM schema was valid, but inventory coverage was false.

Correct review:

1. inspect ELF linkage;
2. inventory the rootfs independently;
3. compare locked source dependencies and copied files;
4. verify first-party binary hashes;
5. require expected component rules;
6. document scanner detection limits.

Schema validity and component count never substitute for coverage analysis.

## Atlas capstone increment

You will generate and validate a CycloneDX 1.7 BOM for the accepted Atlas subject, then evaluate a controlled vulnerability database and VEX record. The lab includes:

- a true affected result;
- a not-affected result supported by bounded evidence;
- an under-investigation result;
- a stale VEX subject;
- an incomplete SBOM missing Atlas itself;
- an unknown-license component.

Release policy must distinguish failure, review, and accepted outcomes.

## Inventory review questions

1. What exact subject and platform does this BOM describe?
2. Which inventory method produced each component?
3. What independent source checks completeness?
4. Are identities precise enough for vulnerability matching?
5. Which findings are affected, not affected, fixed, or unresolved?
6. Who owns each VEX assertion and when does it expire?
7. Which license fields are authoritative, detected, or unknown?
8. Is every evidence object bound to the candidate digest?


## An SBOM evaluation protocol

Validate an SBOM in layers.

### 1. Document validity

Check schema/profile version, unique serial number where required, timestamps, tools, component structures, and relationship syntax. Schema validity prevents malformed data but says nothing about completeness.

### 2. Subject binding

Identify the exact image index or platform manifest the inventory describes. Record repository only as context. An SBOM for `atlas-api:1.0.0` without a digest can drift as the tag moves. For a multi-platform index, decide whether the BOM inventories shared source, each platform image, or a composition of both.

### 3. First-party coverage

Verify Atlas executables, configuration/data assets, and generated artifacts expected from the image. Compare the final rootfs and build outputs independently. Missing first-party binaries are non-compensable.

### 4. Third-party coverage and identity

Check locked language modules, OS packages, shared libraries, copied tools, and base/runtime content. Package URLs, CPEs, hashes, suppliers, and versions have different matching strengths. Preserve evidence explaining how each identity was derived.

### 5. Relationships

A flat component list cannot distinguish direct/indirect dependencies, containment, build-only tools, or generated artifacts. Relationships matter for license obligations, vulnerability reachability, and remediation ownership.

### 6. Licenses and policy

Separate declared license from detected file evidence. Normalize expressions but preserve original notices. Policy should distinguish prohibited, review-required, and allowed cases and account for distribution model, static linking, modification, and source-offer obligations.

### 7. Vulnerability context

Record scanner/tool version, database timestamp, matching basis, severity source, fixed version, and subject. Scan results age even when image bytes do not. Release systems need a rescanning/re-evaluation policy.

## Multi-platform inventory

The amd64 and arm64 Atlas binaries can differ while representing the same source release. Hashes are platform-specific. A top-level BOM can reference per-platform BOMs or include platform properties. Do not attach the amd64 component hash to the index and imply it describes arm64.

For dynamically linked images, OS package and library sets can also differ by platform. Vulnerability and license decisions may therefore be platform-specific.

## VEX decision quality

A VEX status needs:

```text
vulnerability identity
exact product subject
status
justification
impact statement
supporting evidence
issuer and authority
created/updated time
expiry or revalidation trigger
```

Examples:

- `not_affected`: vulnerable code absent from the built binary, proved by symbol/reachability evidence;
- `fixed`: subject contains a patched version, proved by component identity;
- `affected`: remediation or mitigation is required;
- `under_investigation`: temporary review state, not silent acceptance.

A VEX statement for one digest must not be copied to a rebuilt digest without checking whether source, compiler, link mode, features, or runtime exposure changed.

## Scanner disagreement

Two scanners can disagree because inventories, aliases, version parsing, databases, and severity sources differ. Resolve the underlying component and advisory evidence rather than choosing the greener report. Record the disposition and the reason one source is authoritative for the decision.

## Atlas evidence chain

The capstone generates a CycloneDX BOM bound to the API index, runs a deterministic vulnerability fixture, applies scoped VEX, and evaluates release policy. This demonstrates subject binding and decision mechanics. It does not claim complete discovery for arbitrary binaries or current global vulnerability intelligence. The native-tool lane is required to compare independent inventory/scanner outputs.

## Inventory quality is an epistemic claim

An SBOM is not “the output of an SBOM tool.” It is a statement about what the producer knows. Record:

- the subject digest;
- discovery methods;
- package and file coverage;
- dependency relationships;
- build-time versus runtime scope;
- generated or vendored code treatment;
- components not identifiable by package manager;
- completeness status and known blind spots.

Declaring a composition `complete` while omitting native files or statically linked dependencies is worse than honestly declaring incompleteness. It tells policy to trust a false boundary.

### Vulnerability data is time-dependent evidence

A scanner joins an inventory with a vulnerability database at a recorded time. Findings can change because the database changed, package identity was corrected, severity was re-scored, or reachability evidence improved. Preserve scanner/database identity and the subject SBOM rather than storing only a red/green result.

Version comparison is ecosystem-specific. String comparison is not enough. Distro backports can patch a vulnerability without adopting the upstream version. Static binaries can include vulnerable code without an installed package record. False positives and false negatives are expected; policy needs a review route.

### VEX narrows a finding; it does not erase history

A `not_affected` statement needs a reason such as component not present, vulnerable code not reachable, or vulnerable configuration not used. It should identify the product version/digest, vulnerability, author, time, and supporting evidence. When the product or evidence changes, reevaluate.

A VEX statement should coexist with the original finding. Auditors and incident responders need to know that the vulnerability was considered and why it was non-blocking. “Ignored” is not a status.

### Licenses are release inputs

License review needs detected licenses, declared licenses, notices, source-offer obligations where relevant, and policy decisions for unknown or conflicting results. A minimal scratch image can still contain licensed application code. Removing package-manager metadata may make license discovery harder, not remove obligations.

The Course 3 fixture is deliberately small. It teaches subject binding, component identity, completeness, VEX evidence, and release decisions. It is not a universal dependency discovery engine.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-07-runtime-hardening-resource-control-and-operational-contracts/index.md)
- [Next stage](../module-09-provenance-signatures-attestations-and-verification-policy/index.md)
